from typing import TYPE_CHECKING, Any

from BaseClasses import Entrance
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasFromList, Rule, HasGroup, CanReachLocation
from .Options import Goal, GreenStarBehavior, GreenStarstoFinish, GalaxyLock, \
    EnableGreenStars, PowerupRando, MoveRando, YoshiRando, StarbitLumaLocks, CoinLumaLocks, ObjectRando, CometMission, \
    CometItems, WorldShuffle, LogicDifficulty
from .locations import green_star_locations
from .regions import region_list, all_galaxy_slots
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname

if TYPE_CHECKING:
    from . import SMG2World

# main stage logic

def rules_from_er_placements(world: "SMG2World"):
    available_locations = 1
    last_block_count = 0
    for world_num in list(world.star_block_counts.keys()): # For each world, apply rule to galaxy slot, based on last block count.
        block_dict: dict[str, int] = world.star_block_counts[world_num]
        for gal_slot_num in range(1, 8): # Rotate through each galaxy slot to determine rule
            galaxy_entr: Entrance = world.get_entrance(f"World {world_num[6]} Slot {gal_slot_num} Galaxy")
            galaxy_type: str = region_list[galaxy_entr.connected_region.name].type

            match (world_num, gal_slot_num): # Match the correct pairing or world/slot to the correct block number to determine when to update the current count
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
            match (world_num, gal_slot_num):
                case (1,4)|(2,6)|(3,5)|(4,2)|(5,5)|(6,3)|(6,5)|(7,6)|(7,7):
                    starbit_count_grind = bool(world.options.starbit_luma_counts.value[f"World {world_num} Starbit Luma"]< 1000)
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
            world.set_rule(world.get_location(loc_name), data.default_access & Has(f"Green Star {world_map} Key"))
    elif world.options.enable_green_stars.value !=0 :
        for loc_name, data in green_star_locations.items():
            world.set_rule(world.get_location(loc_name), data.default_access & GreenStarRule)



# Common Rules
NoGreenList: list[str] = [itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7]
GreenSeparateGoal: Rule[Any] = ((Has(itemname.GREEN, FromOption(GreenStarstoFinish)) & OptionFilter(GreenStarBehavior, 1))
                     | OptionFilter(GreenStarBehavior, 2))

GreenStarRule: Rule[Any] = ((True_()&OptionFilter(EnableGreenStars,1))
                            | (OptionFilter(EnableGreenStars, 2)&CanReachLocation(locname.GALAXYGENSTAR1)
                               &((HasFromList(*NoGreenList, count=120)&OptionFilter(GreenStarBehavior, 0, operator="ne"))
                                 |(HasGroup("Power Stars", count=120)&OptionFilter(GreenStarBehavior, 0))))
                            | (OptionFilter(EnableGreenStars, 3)&Has(itemname.GREENCOMETKEY)))

CometMissionOff: Rule[Any] = True_()&OptionFilter(CometMission, 0) # CanReach previous star/CanReach Comet Medal/Both/Neither
CometItemsOff: Rule[Any] = True_()&OptionFilter(CometItems, 0)
Comet1ItemAccess: Rule[Any] = CometItemsOff|(Has(itemname.ALLCOMETSKEY)&OptionFilter(CometItems, 1))# Has All Comet Key and option or unlocked

OpenWorlds: Rule[Any] = True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)

PowerUpOff: Rule[Any] = True_()&OptionFilter(PowerupRando,0)
BeeFlight: Rule[Any] = PowerUpOff|(Has(itemname.BEEMARIO)&OptionFilter(PowerupRando,1))
SUPAPOWA: Rule[Any] = PowerUpOff|(Has(itemname.SUPASTAR)&OptionFilter(PowerupRando,1))
FireMario: Rule[Any] = PowerUpOff|(Has(itemname.FIREFLOWER)&OptionFilter(PowerupRando,1))
SPRONGIN: Rule[Any] = PowerUpOff|(Has(itemname.SPRING)&OptionFilter(PowerupRando,1))
BooMario: Rule[Any] = PowerUpOff|(Has(itemname.BOOMARIO)&OptionFilter(PowerupRando,1))
CloudMario: Rule[Any] = PowerUpOff|(Has(itemname.CLOUD)&OptionFilter(PowerupRando,1))
ROCKNROLLIN: Rule[Any] = PowerUpOff|(Has(itemname.ROCK)&OptionFilter(PowerupRando,1))
DRILLMASTER: Rule[Any] = PowerUpOff|(Has(itemname.SPINDRILL)&OptionFilter(PowerupRando,1))

YoshiRandoOff: Rule[Any] = True_()&OptionFilter(YoshiRando, 0)
CanRideDino: Rule[Any] = YoshiRandoOff|(Has(itemname.YOSHI)&OptionFilter(YoshiRando, 1))
CanDinoBlimp: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIBLIMP)&OptionFilter(YoshiRando, 1))
CanDinoRun: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIPEPPER)&OptionFilter(YoshiRando, 1))
CanDinoGlow: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIBULB)&OptionFilter(YoshiRando, 1))
CanDinoSwing: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIFLOWER)&OptionFilter(YoshiRando, 1))

MoveRandoOff: Rule[Any] = True_()&OptionFilter(MoveRando,0)
CanStarbitShoot: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSTARBIT)&OptionFilter(MoveRando, 0, operator="gt"))
CanBackflip: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOBACK)&OptionFilter(MoveRando, 0, operator="gt"))
CanSideflip: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSIDE)&OptionFilter(MoveRando, 0, operator="gt"))
CanAirSpin: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOAIRSPIN)&OptionFilter(MoveRando, 0, operator="gt"))
CanLongJump: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOLONG)&OptionFilter(MoveRando, 0, operator="gt"))
CanSwim: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSWIM)&OptionFilter(MoveRando, 0, operator="gt"))
CanWallJump: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOWALL)&OptionFilter(MoveRando, 0, operator="gt"))
CanPound: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOPOUND)&OptionFilter(MoveRando, 0, operator="gt"))
CanClimbPole: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOCLIMB)&OptionFilter(MoveRando, 0, operator="gt"))
CanSlide: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSLIDE)&OptionFilter(MoveRando, 0, operator="gt"))
CanGrabLedge: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOLEDGE)&OptionFilter(MoveRando, 0, operator="gt"))
CanBalance: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSTARBALL)&OptionFilter(MoveRando, 0, operator="gt"))
CanRideBird: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOFLUZZ)&OptionFilter(MoveRando, 0, operator="gt"))
CanTriple: Rule[Any] = (MoveRandoOff
                        |(Has(itemname.MARIOPROGJUMP, 2)&OptionFilter(MoveRando, 1))
                        |(Has(itemname.MARIOTRIPLE)&OptionFilter(MoveRando,2)))
CanDouble: Rule[Any] = (MoveRandoOff
                        |(Has(itemname.MARIOPROGJUMP)&OptionFilter(MoveRando, 1))
                        |(Has(itemname.MARIODOUBLE)&OptionFilter(MoveRando,2))
                        |CanTriple)
JumpHeight6: Rule[Any] = (CanTriple&CanAirSpin)
JumpHeight5: Rule[Any] = (CanTriple|(CanSideflip&CanAirSpin)|(CanBackflip&CanAirSpin))
JumpHeight4: Rule[Any] = (CanDouble&CanAirSpin|JumpHeight5)
JumpHeight3: Rule[Any] = (CanAirSpin|CanSideflip|CanBackflip|JumpHeight4)
JumpHeight2: Rule[Any] = (CanDouble|JumpHeight3)
JumpHeight1: Rule[Any] = True_()

CanMakeCloud: Rule[Any] = CloudMario&CanAirSpin
CanWallSpin: Rule[Any] = CanWallJump&CanAirSpin
CanLongSpin: Rule[Any] = CanLongJump&CanAirSpin

ObjectRandoOff: Rule[Any] = True_()&OptionFilter(ObjectRando, 1)
CanSwing: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSWING)&OptionFilter(ObjectRando,1))
CanCannon: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOCANNON)&OptionFilter(ObjectRando,1))
CanShell: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSHELL)&OptionFilter(ObjectRando,1))
CanCollectStarChips: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSTARCHIPS)&OptionFilter(ObjectRando,1))

CoinLumaBase: Rule[Any] = ((True_()&OptionFilter(CoinLumaLocks, 0))
                           |(Has(itemname.COINLUMAKEY)&OptionFilter(CoinLumaLocks,1)))

HellLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 3)
HardLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 2)
MediumLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 1)
EasyLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 0)
CanInfiniteFlutter: Rule[Any] = HellLogic&CanRideDino