from typing import Any

from typing import TYPE_CHECKING

from BaseClasses import Entrance
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, True_, Has, HasFromList, HasGroup
from .Constants.Names import item_names as itemname
from .Options import StarbitLumaLocks, GreenStarBehavior, GalaxyLock, Goal
from .Rules import NoGreenList, GreenSeparateGoal, GreenStarLocationRule
from .locations import green_star_locations
from .regions import region_list, all_galaxy_slots

if TYPE_CHECKING:
    from . import SMG2World

def rules_from_er_placements(world: "SMG2World"):
    available_locations = 1
    last_block_count = 0
    for world_num in list(world.star_block_counts.keys()): # For each world, apply rule to galaxy slot, based on last block count.
        block_dict: dict[str, int] = world.star_block_counts[world_num]
        for gal_slot_num in range(1, 8): # Rotate through each galaxy slot to determine rule
            galaxy_entr: Entrance = world.get_entrance(f"World {world_num[6]} Slot {gal_slot_num} Galaxy")
            galaxy_type: str = region_list[galaxy_entr.connected_region.name].type

            match (int(world_num[6]), gal_slot_num): # Match the correct pairing or world/slot to the correct block number to determine when to update the current count
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

            req_star_count = min(last_block_count, available_locations)
            lumarule: Rule[Any] = True_()
            match (int(world_num[6]), gal_slot_num):
                case (1,4)|(2,6)|(3,5)|(4,2)|(5,5)|(6,3)|(6,5)|(7,6)|(7,7):
                    starbit_count_grind = bool(world.options.starbit_luma_counts.value[f"{world_num} Starbit Luma"]< 1000)
                    dontneedgrind = True_() if starbit_count_grind else Has("Can Farm Starbits")
                    lumarule: Rule[Any] = ((True_()&OptionFilter(StarbitLumaLocks, 0))|
                                           (Has(itemname.STARBITLUMAKEY)&OptionFilter(StarbitLumaLocks, 1))
                                          |(Has(f"Starbit Luma World {world_num}")&OptionFilter(StarbitLumaLocks,2))) & dontneedgrind
                case _:
                    lumarule: Rule[Any] = True_()
            world.set_rule(galaxy_entr, ((HasFromList(*NoGreenList, count=req_star_count)
                                         & OptionFilter(GreenStarBehavior, 0, operator="gt"))
                                         | (OptionFilter(GreenStarBehavior, 0) &
                                             HasGroup("Power Stars", count=req_star_count))
                           & ((OptionFilter(GalaxyLock, 1) & Has(f"{galaxy_entr.connected_region.name} Key"))
                              | (OptionFilter(GalaxyLock, 0)&True_()))&lumarule))
            world.star_block_counts[world_num][f"Block {gal_slot_num}"] = req_star_count
            last_block_count = req_star_count
            if ((world.options.goal.value < 2 and (world_num, gal_slot_num) == (6, 7))
                    or (4 > world.options.goal.value > 1 and (world_num, gal_slot_num) == (7, 7))):
                world.set_rule(galaxy_entr,
                               (((OptionFilter(Goal, Goal.option_Green_Star_Cutscene)
                                 & ((HasGroup("Power Stars", count=max(world.options.stars_to_finish.value, 120))
                                 & OptionFilter(GreenStarBehavior, 0))
                               |(HasFromList(*NoGreenList, count=120)
                                 & GreenSeparateGoal)))
                               |(OptionFilter(GreenStarBehavior, 0) &
                                   HasGroup("Power Stars", count=world.options.stars_to_finish.value)
                                   & OptionFilter(Goal, Goal.option_Green_Star_Cutscene, operator="ne"))
                                |(GreenSeparateGoal &
                                   HasFromList(*NoGreenList, count=min(world.options.stars_to_finish.value, 120))
                                   & OptionFilter(Goal, Goal.option_Green_Star_Cutscene, operator="ne")))
                               & ((OptionFilter(GalaxyLock, 1) & Has(f"{galaxy_entr.connected_region.name} Key"))
                              | (OptionFilter(GalaxyLock, 0)&True_())))&lumarule)

            if world.options.enable_green_stars.value == 1 and world.options.green_star_behavior.value == 0:
                available_locations += 5 if galaxy_type == "Major" else 3
            else:
                available_locations += 2 if galaxy_type == "Major" else 1

    #first world, get slot 1 galaxy
    world.start_galaxy = world.get_entrance(f"{list(world.star_block_counts.keys())[0]} Slot 1 Galaxy").connected_region.name
    if world.options.galaxy_lock.value:
        world.multiworld.push_precollected(world.create_item(f"{world.start_galaxy} Key"))
    for galaxy_slot in all_galaxy_slots:
        world.shuffled_levels[world.get_entrance(galaxy_slot).name] = world.get_entrance(galaxy_slot).connected_region.name
    # apply rule to green star locations to include correct world key if th
    if world.options.enable_green_stars.value == 4:
        for loc_name, data in green_star_locations.items():
            world_map: str = world.get_region(data.galaxy).entrances[0].parent_region.name
            world.set_rule(world.get_location(loc_name),
                           ((data.default_access if data.default_access is not None else True_()) & Has(f"Green Star {world_map} Key")))
    elif world.options.enable_green_stars.value !=0 :
        for loc_name, data in green_star_locations.items():
            world.set_rule(world.get_location(loc_name),
                           (data.default_access if data.default_access is not None else True_()) & GreenStarLocationRule)
