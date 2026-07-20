import copy
import json
import os
from dataclasses import fields
from typing import ClassVar, Counter

import worlds.smgalaxy2.Options
from BaseClasses import Item, MultiWorld
from Utils import visualize_regions
from Options import OptionError
from entrance_rando import randomize_entrances
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from . import items, regions, Rules, web_world, Options, Connect
from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname
from .Constants.constants import AP_WORLD_VERSION_NAME, CLIENT_VERSION
from .Options import WorldShuffle
from .Rules import rules_from_er_placements
from .locations import LOCATION_NAME_TO_ID, get_location_names_per_category, SMG2Location, location_table
from .items import SMG2Item, ITEM_NAME_TO_ID, get_item_names_per_category, world_green_keys
from .regions import disconnect_from_option, region_list, SMG2RegionData
from .SMGSettings import SuperMarioGalaxy
from .Patch.Patch import SMGPlayerContainer

def runClient(*args):
    from .SMGClient import launch
    launch_subprocess(launch, name = "SMG2 Client", args = args)

components.append(Component("SMG2 Client", func=runClient, component_type=Type.CLIENT, file_identifier=SuffixIdentifier(".apsmg2")))

class SMG2World(World):
    """
    Super Mario Galaxy allows you to explore the cosmos with Rosalina in the Comet Observatory.
    Mario must collect Power Stars and Grand Stars to power the observatory so it can go to the
    center of the universe in order to save Princess Peach from Bowser's clutches.
    """

    game = "Super Mario Galaxy 2"
    topology_present = False
    
    web = web_world.SMG2WebWorld()
    
    #option definitions
    options_dataclass = Options.SMG2Options
    options: Options.SMG2Options
    settings: ClassVar[SuperMarioGalaxy]

    item_name_to_id: ClassVar[dict[str, int]] = ITEM_NAME_TO_ID
    location_name_to_id: ClassVar[dict[str, int]] = LOCATION_NAME_TO_ID

    item_name_groups = get_item_names_per_category()
    location_name_groups = get_location_names_per_category()
    required_client_version = (0, 6, 7)

    hint_blacklist = {"Peach"}

    def __init__(self, *args, **kwargs):
        super(SMG2World, self).__init__(*args, **kwargs)
        self.origin_region_name: str = regname.SHIP
        self.shuffled_levels: dict[str, str] = {} # Entrance Name (Galaxy Slot): Region name (Galaxy)
        self.starting_world: str = "World 1"
        self.star_block_counts: dict[str, dict[str, int]] = {}
        self.galaxy_key_items: list[SMG2Item] = []
        self.start_galaxy: str = regname.SKYOBS

    def generate_early(self) -> None:
        if "random" in self.options.starbit_luma_counts.value.keys():
            random_cap: int = self.options.starbit_luma_counts.value["random"]
            self.options.starbit_luma_counts.value = {
                "World 1 Starbit Luma": self.random.choice(range(random_cap)),
                "World 2 Starbit Luma": self.random.choice(range(random_cap)),
                "World 3 Starbit Luma": self.random.choice(range(random_cap)),
                "World 4 Starbit Luma": self.random.choice(range(random_cap)),
                "World 5 Starbit Luma": self.random.choice(range(random_cap)),
                "World 6 Starbit Luma": self.random.choice(range(random_cap)),
                "World 7 Starbit Luma": self.random.choice(range(random_cap))
            }
        if "random" in self.options.coin_luma_counts.value.keys():
            random_cap: int = self.options.coin_luma_counts.value["random"]
            self.options.coin_luma_counts.value = {
                "Fluffy Bluff Coin Luma": self.random.choice(range(random_cap)),
                "Puzzle Plank Coin Luma": self.random.choice(range(random_cap)),
                "Hightail Falls Coin Luma": self.random.choice(range(random_cap)),
                "Cosmic Cove Coin Luma": self.random.choice(range(random_cap)),
                "Cloudy Court Coin Luma": self.random.choice(range(random_cap)),
                "Clockwork Ruins Coin Luma": self.random.choice(range(random_cap)),
                "Battle Belt Coin Luma": self.random.choice(range(random_cap))
            }
        if self.options.goal.value > 2 and self.options.enable_green_stars.value == 2:
            raise OptionError(f"Green Star Locations cannot be locked behind a Galaxy Generator Goal. This error "
                              f"occurred in {self.player_name}'s Super Mario Galaxy 2 world. Their YAML must be fixed")
        self.star_block_counts = self.get_star_block_counts()

    def create_regions(self):
        regions.create_regions(self)

    def get_star_block_counts(self) -> dict[str, dict[str, int]]:
        """Gets all the required star block counts for each world """
        # Determine world order, whether left progressive or randomized
        star_block_copy = copy.copy(self.options.final_star_blocks.value)
        world_order: list[str] = ["World 1", "World 2", "World 3", "World 4", "World 5", "World 6", "World 7"]
        world_list_tuple: list[tuple[str, int]] = list(reversed(star_block_copy.most_common()))
        world_final_blocks: dict[str, int] = dict(world_list_tuple)
        if self.options.world_shuffle.value in [WorldShuffle.option_Keyed_Grand_Stars, WorldShuffle.option_Open]:
            world_order: list[str] = []
            self.starting_world = ("World " + list(world_final_blocks.keys())[0][17]) # Get world number from string in option
            if self.options.world_shuffle.value == WorldShuffle.option_Keyed_Grand_Stars:
                self.multiworld.push_precollected(self.create_item("Grand Star - " + self.starting_world))
            for i in range(7):
                world_order.append("World " + str(list(world_final_blocks.keys())[i][17])) # Get world number from string in option

        block_counts: dict[str, dict[str, int]] = {}

        # put out dict with str star block to int star count
        for world in world_order:
            dict_entry: dict[str, int] = {}
            match world:
                case "World 1":
                    dict_entry = {"Block 1": (max(world_final_blocks[world]-4, 0)),
                                  "Block 2": (max(world_final_blocks[world], 0))}
                case "World 6":
                    dict_entry = {"Block 1": (max(world_final_blocks[world] - 10, 0)),
                                  "Block 2": (max(world_final_blocks[world] - 5, 0)),
                                  "Block 3": (max(world_final_blocks[world], 0))}
                case "World 7":
                    dict_entry = {"Block 1": (max(world_final_blocks[world] - 35, 0)),
                                  "Block 2": (max(world_final_blocks[world] - 30, 0)),
                                  "Block 3": (max(world_final_blocks[world] - 20, 0)),
                                  "Block 4": (max(world_final_blocks[world] - 10, 0)),
                                  "blick 5": (max(world_final_blocks[world], 0))}
                case _:
                    dict_entry = {"Block 1": (max(world_final_blocks[world], 0)),}
            block_counts.update({world: dict_entry})

        return block_counts

    def set_rules(self):
        Connect.set_rules(self, self.player)
    
    def create_item(self, name: str) -> SMG2Item:
        item = items.SMG2Item(name, self.player, items.all_items_table[name])
        
        return item

    def get_filler_item_name(self) -> str:
        if self.options.powerup_consumables.value == 0:
            return self.random.choice(list(items.filler_items.keys()))
        elif self.options.powerup_consumables.value == 1:
            return self.random.choice(list(items.expanded_filler.keys()))
        elif self.options.powerup_consumables.value == 2:
            return self.random.choice(list(items.all_filler.keys()))
        else:
            return itemname.ONEUP
    
    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        local_pool: list[SMG2Item] = []
        copies: int = 1
        if self.options.enable_green_stars.value > 0 and self.options.green_star_behavior != 2:
            local_pool += self.create_items_from_list([itemname.GREEN], exclude)

        if self.options.enable_green_stars.value == self.options.enable_green_stars.option_Require_Green_Star_Comet:
            local_pool += self.create_items_from_list([itemname.GREENCOMETKEY], exclude)
        elif self.options.enable_green_stars.value == self.options.enable_green_stars.option_Require_World_Green_Key:
            local_pool += self.create_items_from_list(list(world_green_keys.keys()), exclude)

        if self.options.starbit_luma_locks.value == self.options.starbit_luma_locks.option_Global:
            local_pool += self.create_items_from_list([itemname.STARBITLUMAKEY], exclude)
        elif self.options.starbit_luma_locks.value == self.options.starbit_luma_locks.option_Individual:
            local_pool += self.create_items_from_list(list(items.starbit_world_keys.keys()), exclude)

        if self.options.coin_luma_locks.value == self.options.coin_luma_locks.option_Global:
            local_pool += self.create_items_from_list([itemname.COINLUMAKEY], exclude)
        elif self.options.coin_luma_locks.value == self.options.coin_luma_locks.option_Individual:
            local_pool += self.create_items_from_list(list(items.coin_world_keys.keys()), exclude)

        if self.options.world_shuffle.value == self.options.world_shuffle.option_Keyed_Grand_Stars:
            local_pool += self.create_items_from_list(list(items.keyed_grand_stars.keys()), exclude)
        else:
            local_pool += self.create_items_from_list([itemname.GRAND], exclude)

        if self.options.powerup_rando.value:
            local_pool += self.create_items_from_list(list(items.powerup_unlocks.keys()), exclude)

        if self.options.object_rando.value:
            local_pool += self.create_items_from_list(list(items.object_unlocks.keys()), exclude)

        if self.options.move_rando.value == 1:
            local_pool += self.create_items_from_list(list(items.move_rando_prog_jump.keys()), exclude)
        elif self.options.move_rando.value == 2:
            local_pool += self.create_items_from_list(list(items.move_rando_separate_jump.keys()), exclude)

        if self.options.comet_items.value == self.options.comet_items.option_Global:
            local_pool += self.create_items_from_list([itemname.ALLCOMETSKEY], exclude)
        elif self.options.comet_items.value == self.options.comet_items.option_Type:
            local_pool += self.create_items_from_list(list(items.comet_type_keys.keys()), exclude)

        if self.options.yoshi_rando.value:
            local_pool += self.create_items_from_list(list(items.yoshi_moves.keys()), exclude)

        if self.options.galaxy_lock.value:
            local_pool += self.create_items_from_list(list(items.galaxy_keys.keys()), exclude)
        
        # make sure we don't create more stars than locations, somehow
        local_pool += self.create_items_from_list([itemname.POWER], exclude)
        
        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        n_filler_items = n_locations - len(local_pool)

        # Create filler
        for _ in range(n_filler_items):
            local_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += local_pool

    def create_items_from_list(self, item_names: list[str], excluded_items: list[str]) -> list[SMG2Item]:
        created_items: list[SMG2Item] = []
        for item in item_names:
            copies = max(0, items.all_items_table[item].default_count - excluded_items.count(item))
            created_items += [self.create_item(item) for _ in range(copies)]
        return created_items

    def connect_entrances(self) -> None:
        if self.options.galaxy_shuffle:
            # Disconnect entrances based on options choice. Also ensures first available slot is a major galaxy
            disconnect_from_option(self)
            # Run randomize entrances, but do not get pairings - we create our own method for them
            randomize_entrances(self, True, {0: [0]})
        # Apply rules to newly formed entrances based on within-world access, regardless of randomization
        rules_from_er_placements(self)

    def pre_fill(self) -> None:
        visualize_regions(self.get_region(self.origin_region_name), "SMG2_region_graph.puml",show_entrance_names=True)

    def post_fill(self) -> None:
        if not self.options.galaxy_lock.value:
            return

        starting_galaxy_key_loc = self.multiworld.find_item_locations(f"{self.start_galaxy} Key", self.player)[0]
        if starting_galaxy_key_loc.player not in self.multiworld.groups:
            starting_galaxy_key_loc.item.location = None
            starting_galaxy_key_loc.item = self.create_item(self.get_filler_item_name())
            starting_galaxy_key_loc.item.location = starting_galaxy_key_loc

    # Output options, locations and doors for patcher TODO correct for SMG2
    def generate_output(self, output_directory: str):
        # Output seed name and slot number to seed RNG in randomizer client
        output_data: dict = {
            AP_WORLD_VERSION_NAME: CLIENT_VERSION,
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {
                "character_select": getattr(self.options, "character_select").value
            },
            "Locations": {},
            "Galaxies": self.shuffled_levels,
            "Galaxy Counts": self.star_block_counts,
            "Hints": {},
        }

        # Output relevant options to file
        for field in fields(self.options):
            if field.name == "plando_items":
                continue
            output_data["Options"][field.name] = getattr(self.options, field.name).value
            if isinstance(output_data["Options"][field.name], set):
                output_data["Options"][field.name] = list(output_data["Options"][field.name])
        output_data["Options"]["character_select"] = getattr(self.options, "character_select").value
        output_data["Options"]["mario_colors"] = getattr(self.options, "mario_colors").value

        # Output which item has been placed at each location
        for location in list(smgloc for smgloc in self.get_locations() if isinstance(smgloc, SMG2Location)):
            if location.address is None:
                continue
            if location.item.code is None:
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": self.game,
                    "classification": location.item.classification,
                    # "type": location.type,
                }
            elif location.item:
                loc_region: SMG2RegionData = region_list[location.parent_region.name]
                item_info = {
                    "player": location.item.player,
                    "name": location.item.name,
                    "game": location.item.game,
                    "classification": location.item.classification.name,
                    #"type": location.type,
                }
            else:
                item_info = {"name": "Nothing", "game": self.game, "classification": "filler"}
            output_data["Locations"][location.name] = item_info
        # # Outputs the plando details to our expected output file
        # # Create the output path based on the current player + expected patch file ending.
        # patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
        #                                             f"{SMGPlayerContainer.patch_file_ending}")
        # # Create a zip (container) that will contain all the necessary output files for us to use during patching.
        # smg_container = SMGPlayerContainer(output_data, patch_path, self.multiworld.player_name[self.player],
        #                                  self.player)
        # # Write the expected output zip container to the Generated Seed folder.
        # smg_container.write()

        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                    f"{SMGPlayerContainer.patch_file_ending}")
        
        player_container: SMGPlayerContainer = SMGPlayerContainer(output_data, patch_path, self.player_name, self.player)
        player_container.write()
        
