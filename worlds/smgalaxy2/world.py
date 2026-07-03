import copy
import json
import os
from dataclasses import fields
from typing import ClassVar, Counter

import worlds.smgalaxy2.Options
from BaseClasses import Item, MultiWorld
from Utils import visualize_regions
from entrance_rando import randomize_entrances
from worlds.AutoWorld import World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from . import items, regions, Rules, web_world, Options
from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname
from .Constants.constants import AP_WORLD_VERSION_NAME, CLIENT_VERSION
from .Options import WorldShuffle
from .Rules import rules_from_er_placements
from .locations import LOCATION_NAME_TO_ID, get_location_names_per_category, SMG2Location, location_table
from .items import SMG2Item, ITEM_NAME_TO_ID, get_item_names_per_category
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
        self.star_block_counts = self.get_star_block_counts()

    def create_regions(self):
        regions.create_regions(self)

    def get_star_block_counts(self) -> dict[str, dict[str, int]]:
        """Gets all the required star block counts for each world """
        # Determine world order, whether left progressive or randomized
        star_block_copy = copy.deepcopy(self.options.final_star_blocks.value)
        world_order: list[str] = ["World 1", "World 2", "World 3", "World 4", "World 5", "World 6", "World 7"]
        world_list_tuple: list[tuple[str, int]] = star_block_copy.most_common().reverse()
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
        Rules.set_rules(self, self.player)
    
    def create_item(self, name: str) -> SMG2Item:
        item = items.SMG2Item(name, self.player, items.all_items_table[name])
        
        return item

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(items.filler_items.keys()))
    
    def create_items(self):
        exclude = [item.name for item in self.multiworld.precollected_items[self.player]]
        local_pool: list[SMG2Item] = []
        copies: int = 1
        if self.options.enable_green_stars.value == 1 and self.options.green_star_behavior != 2:
            copies = max(0, items.all_items_table["Green Star"].default_count - exclude.count("Green Star"))
            local_pool += [self.create_item("Green Star") for i in range(copies)]
        if self.options.world_shuffle.value == 1:
            for item in items.keyed_grand_stars.keys():
                copies = max(0, items.all_items_table[item].default_count - exclude.count(item))
                local_pool += [self.create_item(item) for _ in range(copies)]
        else:
            copies = max(0, items.all_items_table[itemname.GRAND].default_count - exclude.count(itemname.GRAND))
            local_pool += [self.create_item(itemname.GRAND) for i in range(copies)]

        if self.options.galaxy_lock.value:
            for item in items.galaxy_keys.keys():
                copies = max(0, items.all_items_table[itemname.GRAND].default_count - exclude.count(itemname.GRAND))
                local_pool += [self.create_item(itemname.GRAND) for i in range(copies)]
        
        # make sure we don't create more stars than locations, somehow
        copies = max(0, items.all_items_table[itemname.POWER].default_count - exclude.count(itemname.POWER))
        local_pool += [self.create_item(itemname.POWER) for i in range(copies)]
        
        # Calculate the number of additional filler items to create to fill all locations
        n_locations = len(self.multiworld.get_unfilled_locations(self.player))
        leftover_locations = min([109, (len(list(self.multiworld.get_unfilled_locations(self.player))) - len(local_pool))])
        n_filler_items = n_locations - len(local_pool)

        # Create filler
        for _ in range(n_filler_items):
            local_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += local_pool

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
        
