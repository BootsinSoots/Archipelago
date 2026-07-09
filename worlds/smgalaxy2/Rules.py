from typing import TYPE_CHECKING, Any

from BaseClasses import Entrance, Location
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasFromList, Rule, HasGroup, CanReachLocation
from .Options import WorldShuffle, Goal, GreenStarBehavior, StarstoFinish, GreenStarstoFinish, GalaxyLock, \
    EnableGreenStars
from .locations import green_star_locations, SMG2Location
from .regions import region_list, all_galaxy_slots
from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname

if TYPE_CHECKING:
    from . import SMG2World

# main stage logic
def set_rules(world: "SMG2World", player: int): #TODO fix connections
    # World 1
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD1), "World 1 Map",
                                           rule=(True_()&
                                                 OptionFilter(WorldShuffle, WorldShuffle.option_Progressive)|(True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open))
                                                | (Has(itemname.GRAND1) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))))
    # Sky Station
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SKYOBS), "World 1 Slot 1 Galaxy")
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS1STARTTOPSIDE), "Sky Station Star 1")
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1STARTBOTTOM))
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE))
    world.get_region(regname.SKYOBS1STARTBOTTOM).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE))
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1GSTAR1)) #Needs move rando rules
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GSTAR1))
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GREENHILL),
                                                        "Sky Station 1: Launch Star 1")
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1OCTOBONUS),
                                                       "Sky Station 1: Green Hill Teleporter")
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1MINIPLANETS),
                                                       "Sky Station 1: Green Hill Launch Star")
    world.get_region(regname.SKYOBS1MINIPLANETS).connect(world.get_region(regname.SKYOBS1CYLINDER),
                                                       "Sky Station 1: Mini Planets Launch Star")
    world.get_region(regname.SKYOBS1CYLINDER).connect(world.get_region(regname.SKYOBS1BEFOREBOSS),
                                                       "Sky Station 1: Cylinder Launch Star")
    world.get_region(regname.SKYOBS1BEFOREBOSS).connect(world.get_region(regname.SKYOBS1BOSS),
                                                       "Sky Station 1: Two-Sided Launch Star")
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS2STARTTOPSIDE), "Sky Station Star 2")
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2STARTBOTTOM))
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2TOPOFHOUSE))
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.SKYOBS2TOPOFHOUSE))
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.SKYOBS2SKYFLEET),
                                                        "Sky Station 2: Launch Star 1")
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2OCTOBONUS),
                                                      "Sky Station 2: Sky Fleet Teleporter")
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2FLIPSWITCH),
                                                      "Sky Station 2: Sky Fleet Launch Star")
    world.get_region(regname.SKYOBS2FLIPSWITCH).connect(world.get_region(regname.SKYOBS2GRASSFLEET),
                                                        "Sky Station 2: Flipswitch Fleet Launch Star")
    # Yoshi star
    world.get_region(regname.WORLD1).connect(world.get_region(regname.GOODEGG), "World 1 Slot 2 Galaxy")
    # Spin-Dig
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SPINDIG), "World 1 Slot 3 Galaxy")
    # FlipSwap
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLIPSWAP), "World 1 Slot 4 Galaxy")
    # Fluffl Bluff
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLUFFBLUFF), "World 1 Slot 5 Galaxy")
    # Righside Down
    world.get_region(regname.WORLD1).connect(world.get_region(regname.RIGHTDOWN), "World 1 Slot 6 Galaxy")
    # Fiery Fleet
    world.get_region(regname.WORLD1).connect(world.get_region(regname.BOWJR1), "World 1 Slot 7 Galaxy")
    # World 2
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD2), "World 2 Map",
                                           rule=(Has(itemname.GRAND)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND2) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Puzzle Plank
    world.get_region(regname.WORLD2).connect(world.get_region(regname.PUZZPLAN), "World 2 Slot 1 Galaxy")
    # Boulder Bowl
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOULBOWL), "World 2 Slot 2 Galaxy")
    # Hightail Falls
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HIGHTAIL), "World 2 Slot 3 Galaxy")
    # Wild Glide
    world.get_region(regname.WORLD2).connect(world.get_region(regname.WILDGLIDE), "World 2 Slot 4 Galaxy")
    # Cosmic Cove
    world.get_region(regname.WORLD2).connect(world.get_region(regname.COSMICO), "World 2 Slot 5 Galaxy")
    # Honeybloom
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HONEYBLOOM), "World 2 Slot 6 Galaxy")
    # Lava Lair
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOWSER1), "World 2 Slot 7 Galaxy")
    # World 3
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD3), "World 3 Map",
                                           rule=(Has(itemname.GRAND, 2)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND3) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Tall Trunk
    world.get_region(regname.WORLD3).connect(world.get_region(regname.TALLTRUNK), "World 3 Slot 1 Galaxy")
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK1BIGTREE), "Tall Trunk Star 1")
    world.get_region(regname.TALLTRUNK1BIGTREE).connect(world.get_region(regname.TALLTRUNK1LOG),
                                                        "Tall Trunk 1: Big Tree Launch Star")
    world.get_region(regname.TALLTRUNK1BIGTREE).connect(world.get_region(regname.TALLTRUNK1PIRANHABONUS),
                                                        "Tall Trunk 1: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1WOODCIRClE),
                                                        "Tall Trunk 1: Carved Log Launch Star")
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1DICEPIPE),
                                                        "Tall Trunk 1: Carved Log Green pipe")
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK2BIGTREE), "Tall Trunk Star 2")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2PIRANHABONUS),
                                                        "Tall Trunk 2: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2SLIDE),
                                                        "Tall Trunk 2: Big Tree Launch Star")
    world.get_region(regname.TALLTRUNK2SLIDE).connect(world.get_region(regname.TALLTRUNK2SLIDEND))
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK3PCOINSLIDE), "Tall Trunk Star 3")
    world.get_region(regname.TALLTRUNK3PCOINSLIDE).connect(world.get_region(regname.TALLTRUNK3PCOINEND))
    # Cloudy Court
    world.get_region(regname.WORLD3).connect(world.get_region(regname.CLOUCOUR), "World 3 Slot 2 Galaxy")
    world.get_region(regname.CLOUCOUR).connect(world.get_region(regname.CLOUCOUR1LANDING), "Cloudy Court Star 1")
    world.get_region(regname.CLOUCOUR1LANDING).connect(world.get_region(regname.CLOUCOUR1CYMBAL))
    world.get_region(regname.CLOUCOUR1CYMBAL).connect(world.get_region(regname.CLOUCOUR1TOWERS),
                                                      "Cloudy Court 1: Cymbal Launch Star")
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR3PCOINS),
                                                      "Cloudy Court 3: Hungry Luma")
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1PARAGOOMBONUS),
                                                      "Cloudy Court 1: Paragoomba Bonus Teleporter")
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1CASTLE),
                                                      "Cloudy Court 1: Tower Launch Star")
    world.get_region(regname.CLOUCOUR).connect(world.get_region(regname.CLOUCOUR2LANDING), "Cloudy Court Star 2")
    world.get_region(regname.CLOUCOUR2LANDING).connect(world.get_region(regname.CLOUCOUR2CASTLE1),
                                                       "Cloudy Court 2: Launch Star")
    world.get_region(regname.CLOUCOUR2CASTLE1).connect(world.get_region(regname.CLOUCOUR2CASTLE2),
                                                       "Cloudy Court 2: Wall Jump Sling Star")
    world.get_region(regname.CLOUCOUR2CASTLE2).connect(world.get_region(regname.CLOUCOUR2FINAL),
                                                       "Cloudy Court 2: Final Sling Star")
    # Haunty halls
    world.get_region(regname.WORLD3).connect(world.get_region(regname.HAUNHALL), "World 3 Slot 3 Galaxy")
    # Freezy Flake
    world.get_region(regname.WORLD3).connect(world.get_region(regname.FREEFLAKE), "World 3 Slot 4 Galaxy")
    # Beat Block
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BEATBLOCK), "World 3 Slot 5 Galaxy")
    #Rolling masterpiece
    world.get_region(regname.WORLD3).connect(world.get_region(regname.ROLLMAST), "World 3 Slot 6 Galaxy")
    # Fearsome Fleet
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BOWJR2), "World 3 Slot 7 Galaxy")
    # World 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD4), "World 4 Map",
                                           rule=(Has(itemname.GRAND, 3)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND4) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Supermassive
    world.get_region(regname.WORLD4).connect(world.get_region(regname.SUPMASS), "World 4 Slot 1 Galaxy")
    # Sweet Mystery
    world.get_region(regname.WORLD4).connect(world.get_region(regname.SWEETMYS), "World 4 Slot 2 Galaxy")
    # Flipville
    world.get_region(regname.WORLD4).connect(world.get_region(regname.FLIPVILL), "World 4 Slot 3 Galaxy")
    # Honeyhop
    world.get_region(regname.WORLD4).connect(world.get_region(regname.HONEYHOP), "World 4 Slot 4 Galaxy")
    # Starshine beach
    world.get_region(regname.WORLD4).connect(world.get_region(regname.STARBEACH), "World 4 Slot 5 Galaxy")
    # Chompworks
    world.get_region(regname.WORLD4).connect(world.get_region(regname.CHOMWORK), "World 4 Slot 6 Galaxy")
    # Gravity Gauntlet
    world.get_region(regname.WORLD4).connect(world.get_region(regname.BOWSER2), "World 4 Slot 7 Galaxy")
    # World 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD5), "World 5 Map",
                                           rule=(Has(itemname.GRAND, 4)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND5) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Space Storm
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SPACSTOR), "World 5 Slot 1 Galaxy")
    # Boo Moon
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOOMOON), "World 5 Slot 2 Galaxy")
    # Upside Dizzy
    world.get_region(regname.WORLD5).connect(world.get_region(regname.UPDOWN), "World 5 Slot 3 Galaxy")
    # Slipsand
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SLIPSAND), "World 5 Slot 4 Galaxy")
    # Fleet Glide
    world.get_region(regname.WORLD5).connect(world.get_region(regname.FLEETGLIDE), "World 5 Slot 5 Galaxy")
    #Shiverburn
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SHIVBURN), "World 5 Slot 6 Galaxy")
    # Boom bunker
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOWJR3), "World 5 Slot 7 Galaxy")
    # World 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD6), "World 6 Map",
                                           rule=(Has(itemname.GRAND, 5)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND6) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Melty Monster
    world.get_region(regname.WORLD6).connect(world.get_region(regname.MELTY), "World 6 Slot 1 Galaxy")
    # Clockwork Ruins
    world.get_region(regname.WORLD6).connect(world.get_region(regname.CLOCKWORK), "World 6 Slot 2 Galaxy")
    # Flash Black
    world.get_region(regname.WORLD6).connect(world.get_region(regname.FLASHBLACK), "World 6 Slot 3 Galaxy")
    # Throwback
    world.get_region(regname.WORLD6).connect(world.get_region(regname.WHOMPFORT), "World 6 Slot 4 Galaxy")
    # Slimy Spring
    world.get_region(regname.WORLD6).connect(world.get_region(regname.SLIMSPRI), "World 6 Slot 5 Galaxy")
    # Battle Belt
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BATTLEBELT), "World 6 Slot 6 Galaxy")
    # Galaxy Generator
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BOWSER3), "World 6 Slot 7 Galaxy")
    # World 7
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD7), "World S Map",
                                           rule=(Has(itemname.GRAND, 6)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND7) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | (True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)))
    # Mario Squared
    world.get_region(regname.WORLD7).connect(world.get_region(regname.MARIO), "World 7 Slot 1 Galaxy")
    # Rolling Coaster
    world.get_region(regname.WORLD7).connect(world.get_region(regname.ROLLCOAST), "World 7 Slot 2 Galaxy")
    # Twisty Trials
    world.get_region(regname.WORLD7).connect(world.get_region(regname.TWISTTRI), "World 7 Slot 3 Galaxy")
    # Stone Cyclone
    world.get_region(regname.WORLD7).connect(world.get_region(regname.STONECYC), "World 7 Slot 4 Galaxy")
    # Boss Blitz
    world.get_region(regname.WORLD7).connect(world.get_region(regname.BOSSBLITZ), "World 7 Slot 5 Galaxy")
    # Flipout
    world.get_region(regname.WORLD7).connect(world.get_region(regname.FLIPOUT), "World 7 Slot 6 Galaxy")
    # Grandmaster
    world.get_region(regname.WORLD7).connect(world.get_region(regname.GRANDMASTER), "World 7 Slot 7 Galaxy")


    world.get_region(regname.SHIP).connect(world.get_region(regname.SHIPINSIDE)), "Inside Starship Mario"
    world.set_completion_rule(Has("Peach"))

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
            world.set_rule(galaxy_entr, (HasFromList(*NoGreenList, count=req_star_count)
                                         & OptionFilter(GreenStarBehavior, 0, operator="gt"))
                                         | (OptionFilter(GreenStarBehavior, 0) &
                                             HasGroup("Power Star", count=req_star_count))
                           & ((OptionFilter(GalaxyLock, 1) & Has(f"{galaxy_entr.connected_region.name} Key"))
                              | (OptionFilter(GalaxyLock, 0)&True_())))
            world.star_block_counts[world_num][f"Block {gal_slot_num}"] = req_star_count
            last_block_count = req_star_count
            if ((world.options.goal.value < 2 and (world_num, gal_slot_num) == (6, 7))
                    or (4 > world.options.goal.value > 1 and (world_num, gal_slot_num) == (7, 7))): # TODO add in starbit requirements somehow
                world.set_rule(galaxy_entr,
                               ((OptionFilter(Goal, Goal.option_Green_Star_Cutscene)
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
                               & ((OptionFilter(GalaxyLock, 1) & Has(f"{galaxy_entr.connected_region.name} Key"))
                              | (OptionFilter(GalaxyLock, 0)&True_())))

            if world.options.enable_green_stars.value == 1 and world.options.green_star_behavior.value == 0:
                available_locations += 5 if galaxy_type == "Major" else 3
            else:
                available_locations += 2 if galaxy_type == "Major" else 1

    #firs world, get slot 1 galaxy
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
GreenSeparateGoal: Rule[Any] = ((HasGroup(itemname.GREEN, FromOption(GreenStarstoFinish)) & OptionFilter(GreenStarBehavior, 1))
                     | OptionFilter(GreenStarBehavior, 2))

GreenStarRule: Rule[Any] = ((True_()&OptionFilter(EnableGreenStars,1))
                            | (OptionFilter(EnableGreenStars, 2)&CanReachLocation(locname.GALAXYGENSTAR1)
                               &((HasFromList(*NoGreenList, count=120)&OptionFilter(GreenStarBehavior, 0, operator="ne"))
                                 |(HasGroup("Power Star", count=120)&OptionFilter(GreenStarBehavior, 0))))
                            | (OptionFilter(EnableGreenStars, 3)&Has(itemname.GREENCOMETKEY)))

CometAccessBase: Rule[Any] = # CanReach previous star/CanReach Comet Medal/Both/Neither

Comet1ItemAccess: Rule[Any] = # Has All Comet Key and option or unlocked