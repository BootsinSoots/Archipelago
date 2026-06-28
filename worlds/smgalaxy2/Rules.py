from typing import TYPE_CHECKING, Any

from BaseClasses import Entrance
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasFromList, Rule
from .Options import WorldShuffle, Goal, GreenStarBehavior
from .regions import connect_regions, region_list, all_galaxy_slots
from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname

if TYPE_CHECKING:
    from . import SMG2World

# main stage logic
def set_rules(world: "SMG2World", player: int): #TODO fix connections
    # World 1
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD1), "World 1 Map",
                                           rule=(True_()&
                                                 OptionFilter(WorldShuffle, WorldShuffle.option_Progressive)|(True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open))
                                                | (Has(itemname.GRAND1) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))))
    connect_regions(world, player, regname.WORLD1, regname.GOODEGG, "Dome 1 First Orbit Galaxy")
    connect_regions(world, player, regname.WORLD1, regname.SPINDIG, "Dome 1 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Second Orbit"], 4)))
    connect_regions(world, player, regname.WORLD1, regname.RIGHTDOWN, "Dome 1 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Third Orbit"], 5)))
    connect_regions(world, player, regname.WORLD1, regname.FLIPSWITCH, "Dome 1 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Fourth Orbit"], 6)))
    connect_regions(world, player, regname.WORLD1, regname.BOWJR1, "Dome 1 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,7))
    # World 2
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD2), "World 2 Map",
                                           rule=(Has(itemname.GRAND)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND2) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    connect_regions(world, player, regname.WORLD2, regname.FLUFFBLUFF, "Dome 2 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 8))
    connect_regions(world, player, regname.WORLD2, regname.WILDGLIDE, "Dome 2 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 9))
    connect_regions(world, player, regname.WORLD2, regname.PUZZPLAN, "Dome 2 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 10))
    connect_regions(world, player, regname.WORLD2, regname.HURRYSCUR, "Dome 2 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 11))
    connect_regions(world, player, regname.WORLD2, regname.BOWSER1, "Dome 2 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 12))
    # World 3
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD3), "World 3 Map",
                                           rule=(Has(itemname.GRAND, 2)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND3) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    connect_regions(world, player, regname.WORLD3, regname.HIGHTAIL, "Dome 3 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 13))
    connect_regions(world, player, regname.WORLD3, regname.ROLLMAST, "Dome 3 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 14))
    connect_regions(world, player, regname.WORLD3, regname.BOULBOWL, "Dome 3 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 15))
    connect_regions(world, player, regname.WORLD3, regname.HONEYHOP, "Dome 3 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 16))
    connect_regions(world, player, regname.WORLD3, regname.BOWJR2, "Dome 3 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 17))
    # World 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD4), "World 4 Map",
                                           rule=(Has(itemname.GRAND, 3)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND4) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    connect_regions(world, player, regname.WORLD4, regname.COSMICO, "Dome 4 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 18))
    connect_regions(world, player, regname.WORLD4, regname.TALLTRUNK, "Dome 4 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 19))
    connect_regions(world, player, regname.WORLD4, regname.CLOUCOUR, "Dome 4 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 20))
    connect_regions(world, player, regname.WORLD4, regname.UPDOWN, "Dome 4 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 21))
    connect_regions(world, player, regname.WORLD4, regname.BOWSER2, "Dome 4 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 22))
    # World 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD5), "World 5 Map",
                                           rule=(Has(itemname.GRAND, 4)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND5) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    connect_regions(world, player, regname.WORLD5, regname.HAUNHALL, "Dome 5 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 23))
    connect_regions(world, player, regname.WORLD5, regname.FREEFLAKE, "Dome 5 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 24))
    connect_regions(world, player, regname.WORLD5, regname.SUPMASS, "Dome 5 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 25))
    connect_regions(world, player, regname.WORLD5, regname.BONEFIN, "Dome 5 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 26))
    connect_regions(world, player, regname.WORLD5, regname.BOWJR3, "Dome 5 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 27))
    # World 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD6), "World 6 Map",
                                           rule=(Has(itemname.GRAND, 5)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND6) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    connect_regions(world, player, regname.WORLD6, regname.FLIPVILL, "Dome 6 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 28))
    connect_regions(world, player, regname.WORLD6, regname.STARBEACH, "Dome 6 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 29))
    connect_regions(world, player, regname.WORLD6, regname.MATTER, "Dome 6 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 30))
    connect_regions(world, player, regname.WORLD6, regname.CHOMWORK, "Dome 6 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 31))
    # World 7
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD7), "World S Map",
                                           rule=(Has(itemname.GRAND, 6)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND7) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    #Remaining Ship Connections
    connect_regions(world, player, regname.SHIP, regname.LIBRARY, "Library Entrance")
    connect_regions(world, player, regname.SHIP, regname.COTU, "Center Of the Universe Entry",
                    lambda state: state.has("Grand Star", player, 5) and state.has_group("Power Star", player, world.options.stars_to_finish.value))
    connect_regions(world, player, regname.COTU, regname.BOWSER3, "Galaxy's Center")
    connect_regions(world, player, regname.SHIP, regname.HONEYBLOOM, "Sweet Sweet Hungry Luma")
    connect_regions(world, player, regname.SHIP, regname.BEATBLOCK, "Sling Pod Hungry Luma",
                    lambda state: state.has("Grand Star", player))
    connect_regions(world, player, regname.SHIP, regname.SWEETMYS, "Drip Drop Hungry Luma",
                    lambda state: state.has("Grand Star", player, 2))
    connect_regions(world, player, regname.SHIP, regname.BIGMOUTH, "Bigmouth Hungry Luma",
                    lambda state: state.has("Grand Star", player, 3))
    connect_regions(world, player, regname.SHIP, regname.SANDSPIRAL, "Sand Spiral Hungry Luma",
                    lambda state: state.has("Grand Star", player, 4))
    connect_regions(world, player, regname.SHIP, regname.SNOWCAP, "Snow Cap Hungry Luma",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.FLIPSWAP, "Gateway Dome",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.BOOBONE, "Boo's Boneyard Hungry Luma",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.TRIALS, "Planet of Trials Launch Star",
                    lambda state: state.has("Green Star", player))
    connect_regions(world, player, regname.TRIALS, regname.ROLLINGGIZ, "Rolling Gizmo Launch Star")
    connect_regions(world, player, regname.TRIALS, regname.LOOPDEESWOOP, "Loopdeeswoop Launch Star")
    connect_regions(world, player, regname.TRIALS, regname.BUBBLEBLAST, "Bubble Blast Launch Star")
    # connect_regions(world, player, regname.SHIP, regname.FINALE, "Grand Finale Launch Star",
    #                 lambda state: state.has("Green Star", player) and state.has("Power Star", player, 120))
    world.set_completion_rule(Has("Peach"))

def rules_from_er_placements(world: "SMG2World"):
    available_locations = 1
    last_block_count = 0
    for world_num in list(world.star_block_counts.keys()): # For each world, apply rule to galaxy slot, based on last block count.
        block_dict: dict[str, int] = world.star_block_counts[world_num]
        for slot_num in range(1, 8): # Rotate through each galaxy slot to determine rule
            galaxy_entr: Entrance = world.get_entrance(f"World {world_num[6]} Slot {slot_num} Galaxy")
            galaxy_type: str = region_list[galaxy_entr.connected_region.name].type

            match (world_num, slot_num): # Match the correct pairing or world/slot to the correct block number to determine when to update the current count
                case (7, 2)|(1, 3)|(2, 7)|(3, 7)|(4, 7)|(5, 7)|(6, 4):
                    last_block_count = block_dict[f"Block 1"]
                case (7, 3)|(1, 7)|(6, 6):
                    last_block_count = block_dict[f"Block 2"]
                case (6, 7)|(7, 4):
                    last_block_count = block_dict[f"Block 3"]
                case (7, 5):
                    last_block_count = block_dict[f"Block 4"]
                case (7, 6):
                    last_block_count = block_dict[f"Block 5"]

            if last_block_count <= available_locations:
                world.set_rule(galaxy_entr, (HasFromList(itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                                         count=last_block_count)
                                             & OptionFilter(GreenStarBehavior, 1))
                               | (OptionFilter(GreenStarBehavior, 0) &
                                   HasFromList(itemname.POWER, itemname.GREEN, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                               count=last_block_count)))
            else:
                world.set_rule(galaxy_entr, (HasFromList(itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                                         count=available_locations)
                                             & OptionFilter(GreenStarBehavior, 1))
                               | (OptionFilter(GreenStarBehavior, 0) &
                                   HasFromList(itemname.POWER, itemname.GREEN, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                               count=available_locations)))
                world.star_block_counts[world_num][f"Block {slot_num}"] = available_locations
                last_block_count = available_locations
            if ((world.options.goal.value < 2 and (world_num, slot_num) == (6, 7))
                    or (world.options.goal.value > 1 and (world_num, slot_num) == (7, 7))): # TODO add in starbit requirements somehow
                world.set_rule(galaxy_entr,
                                (OptionFilter(Goal, Goal.option_Green_Star_Cutscene)
                                 & HasFromList(itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                               count=world.options.stars_to_finish.value) & Has(itemname.GREEN, 120)) |
                                (HasFromList(itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                             count=min(world.options.stars_to_finish.value, 120))
                                 & Has(itemname.GREEN, world.options.green_stars_to_finish.value)
                                 & OptionFilter(GreenStarBehavior, 1))
                                | (OptionFilter(GreenStarBehavior, 0) &
                                   HasFromList(itemname.POWER, itemname.GREEN, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7,
                                               count=world.options.stars_to_finish.value)))

            if world.options.enable_green_stars.value == 1 and world.options.green_star_behavior.value == 0:
                available_locations += 5 if galaxy_type == "Major" else 3
            else:
                available_locations += 2 if galaxy_type == "Major" else 1

    for galaxy_slot in all_galaxy_slots:
        world.shuffled_levels[world.get_entrance(galaxy_slot).name] = world.get_entrance(galaxy_slot).connected_region.name



# Common Rules
