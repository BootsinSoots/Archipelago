from typing import TYPE_CHECKING, Any

from BaseClasses import Entrance
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasFromList, Rule, HasGroup
from .Options import WorldShuffle, Goal, GreenStarBehavior, StarstoFinish, GreenStarstoFinish
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
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SKYOBS), "World 1 Slot 1 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.GOODEGG), "World 1 Slot 2 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SPINDIG), "World 1 Slot 3 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLIPSWAP), "World 1 Slot 4 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLUFFBLUFF), "World 1 Slot 5 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.RIGHTDOWN), "World 1 Slot 6 Galaxy")
    world.get_region(regname.WORLD1).connect(world.get_region(regname.BOWJR1), "World 1 Slot 7 Galaxy")
    # World 2
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD2), "World 2 Map",
                                           rule=(Has(itemname.GRAND)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND2) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    world.get_region(regname.WORLD2).connect(world.get_region(regname.FLUFFBLUFF), "World 2 Slot 1 Galaxy")
    world.get_region(regname.WORLD2).connect(world.get_region(regname.WILDGLIDE), "World 2 Slot 2 Galaxy")
    world.get_region(regname.WORLD2).connect(world.get_region(regname.PUZZPLAN), "World 2 Slot 3 Galaxy")
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HURRYSCUR), "World 2 Slot 4 Galaxy")
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOWSER1), "World 2 Slot 5 Galaxy")
    # World 3
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD3), "World 3 Map",
                                           rule=(Has(itemname.GRAND, 2)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND3) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    world.get_region(regname.WORLD3).connect(world.get_region(regname.HIGHTAIL), "World 3 Slot 1 Galaxy")
    world.get_region(regname.WORLD3).connect(world.get_region(regname.ROLLMAST), "World 3 Slot 2 Galaxy")
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BOULBOWL), "World 3 Slot 3 Galaxy")
    world.get_region(regname.WORLD3).connect(world.get_region(regname.HONEYHOP), "World 3 Slot 4 Galaxy")
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BOWJR2), "World 3 Slot 5 Galaxy")
    # World 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD4), "World 4 Map",
                                           rule=(Has(itemname.GRAND, 3)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND4) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    world.get_region(regname.WORLD4).connect(world.get_region(regname.COSMICO), "World 4 Slot 1 Galaxy")
    world.get_region(regname.WORLD4).connect(world.get_region(regname.TALLTRUNK), "World 4 Slot 2 Galaxy")
    world.get_region(regname.WORLD4).connect(world.get_region(regname.CLOUCOUR), "World 4 Slot 3 Galaxy")
    world.get_region(regname.WORLD4).connect(world.get_region(regname.UPDOWN), "World 4 Slot 4 Galaxy")
    world.get_region(regname.WORLD4).connect(world.get_region(regname.BOWSER2), "World 4 Slot 5 Galaxy")
    # World 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD5), "World 5 Map",
                                           rule=(Has(itemname.GRAND, 4)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND5) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    world.get_region(regname.WORLD5).connect(world.get_region(regname.HAUNHALL), "World 5 Slot 1 Galaxy")
    world.get_region(regname.WORLD5).connect(world.get_region(regname.FREEFLAKE), "World 5 Slot 2 Galaxy")
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SUPMASS), "World 5 Slot 3 Galaxy")
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BONEFIN), "World 5 Slot 4 Galaxy")
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOWJR3), "World 5 Slot 5 Galaxy")
    # World 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD6), "World 6 Map",
                                           rule=(Has(itemname.GRAND, 5)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND6) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    world.get_region(regname.WORLD6).connect(world.get_region(regname.FLIPVILL), "World 6 Slot 1 Galaxy")
    world.get_region(regname.WORLD6).connect(world.get_region(regname.STARBEACH), "World 6 Slot 2 Galaxy")
    world.get_region(regname.WORLD6).connect(world.get_region(regname.MATTER), "World 6 Slot 3 Galaxy")
    world.get_region(regname.WORLD6).connect(world.get_region(regname.CHOMWORK), "World 6 Slot 4 Galaxy")
    # World 7
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD7), "World S Map",
                                           rule=(Has(itemname.GRAND, 6)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND7) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
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
                world.set_rule(galaxy_entr, (HasFromList(*NoGreenList, count=last_block_count)
                                             & OptionFilter(GreenStarBehavior, 0, operator= "gt"))
                                             | (OptionFilter(GreenStarBehavior, 0) &
                                                 HasGroup("Power Star", count=last_block_count)))
            else:
                world.set_rule(galaxy_entr, (HasFromList(*NoGreenList, count=available_locations)
                                             & OptionFilter(GreenStarBehavior, 0, operator="gt"))
                                             | (OptionFilter(GreenStarBehavior, 0) &
                                                 HasGroup("Power Star", count=available_locations)))
                world.star_block_counts[world_num][f"Block {slot_num}"] = available_locations
                last_block_count = available_locations
            if ((world.options.goal.value < 2 and (world_num, slot_num) == (6, 7))
                    or (4 > world.options.goal.value > 1 and (world_num, slot_num) == (7, 7))): # TODO add in starbit requirements somehow
                world.set_rule(galaxy_entr,
                                (OptionFilter(Goal, Goal.option_Green_Star_Cutscene)
                                 & ((HasGroup("Power Star", count=max(world.options.stars_to_finish.value, 120))
                                 & OptionFilter(GreenStarBehavior, 0))
                               |(HasFromList(*NoGreenList, count=120)
                                 & GreenSeparateGoal)))
                               |(OptionFilter(GreenStarBehavior, 0) &
                                   HasGroup("Power Star", count=world.options.stars_to_finish.value)
                                   & OptionFilter(Goal, Goal.option_Green_Star_Cutscene, operator="ne"))
                                |(GreenSeparateGoal &
                                   HasFromList(*NoGreenList, count=min(world.options.stars_to_finish.value, 120))
                                   & OptionFilter(Goal, Goal.option_Green_Star_Cutscene, operator="ne")))

            if world.options.enable_green_stars.value == 1 and world.options.green_star_behavior.value == 0:
                available_locations += 5 if galaxy_type == "Major" else 3
            else:
                available_locations += 2 if galaxy_type == "Major" else 1

    for galaxy_slot in all_galaxy_slots:
        world.shuffled_levels[world.get_entrance(galaxy_slot).name] = world.get_entrance(galaxy_slot).connected_region.name



# Common Rules
NoGreenList: list[str] = [itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7]
GreenSeparateGoal = ((Has(itemname.GREEN, FromOption(GreenStarstoFinish)) & OptionFilter(GreenStarBehavior, 1))
                     | OptionFilter(GreenStarBehavior, 2))