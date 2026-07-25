from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import True_, Has, CanReachLocation, CanReachEntrance
from .Rules import CanLongJump

if TYPE_CHECKING:
    from . import SMG2World
from .Constants.Names import region_names as regname, item_names as itemname, location_names as locname
from .Options import WorldShuffle, CoinLumaLocks, CometItems, CometMission
from . import Rules as RB


def set_rules(world: "SMG2World", player: int): #TODO add rules to entrances
    # World 1
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD1), "World 1 Map",
                                           rule=((True_()&
                                                 OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                 | RB.OpenWorlds
                                                | (Has(itemname.GRAND1) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))))
    # Sky Station
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SKYOBS), "World 1 Slot 1 Galaxy")
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS1STARTTOPSIDE), "Sky Station Star 1")
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1STARTBOTTOM),
                                                          rule=True_()|RB.CanLongJump|RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE),
                                                          rule=RB.JumpHeight5)
    world.get_region(regname.SKYOBS1STARTBOTTOM).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE))
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1GSTAR1),
                                                          rule=RB.JumpHeight3)
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GSTAR1),
                                                        rule=RB.JumpHeight1)
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GREENHILL),
                                                        "Sky Station 1: House Launch Star")
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1OCTOBONUS),
                                                       "Sky Station 1: Green Hill Teleporter",)
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1MINIPLANETS),
                                                       "Sky Station 1: Green Hill Launch Star",
                                                       RB.CanAirSpin)
    world.get_region(regname.SKYOBS1MINIPLANETS).connect(world.get_region(regname.SKYOBS1CYLINDER),
                                                       "Sky Station 1: Mini Planets Launch Star",
                                                         RB.CanAirSpin)
    world.get_region(regname.SKYOBS1CYLINDER).connect(world.get_region(regname.SKYOBS1BEFOREBOSS),
                                                       "Sky Station 1: Cylinder Launch Star")
    world.get_region(regname.SKYOBS1BEFOREBOSS).connect(world.get_region(regname.SKYOBS1BOSS),
                                                       "Sky Station 1: Two-Sided Launch Star")
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS2STARTTOPSIDE), "Sky Station Star 2")
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2STARTBOTTOM),
                                                          rule=True_()|RB.CanLongJump|RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2TOPOFHOUSE),
                                                          rule=RB.JumpHeight5)
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.SKYOBS2TOPOFHOUSE))
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.SKYOBS2SKYFLEET),
                                                        "Sky Station 2: House Launch Star")
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2OCTOBONUS),
                                                      "Sky Station 2: Sky Fleet Teleporter")
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2FLIPSWITCH),
                                                      "Sky Station 2: Sky Fleet Launch Star")
    world.get_region(regname.SKYOBS2FLIPSWITCH).connect(world.get_region(regname.SKYOBS2GRASSFLEET),
                                                        "Sky Station 2: Flipswitch Fleet Launch Star")
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS3STARTTOPSIDE), "Sky Station Comet Star",
                                             rule=((RB.Comet1ItemAccess|(OptionFilter(CometItems, 2)&Has(itemname.SPEEDYCOMET)))
                                                   &(RB.CometMissionOff
                                                     |(OptionFilter(CometMission, 1)&CanReachLocation(locname.SKYSTACM))
                                                     |(OptionFilter(CometMission, 2)&CanReachLocation(locname.SKYSTASTAR1))
                                                     |(OptionFilter(CometMission, 3)&CanReachLocation(locname.SKYSTACM)
                                                       &CanReachLocation(locname.SKYSTASTAR1)))))
    world.get_region(regname.SKYOBS3STARTTOPSIDE).connect(world.get_region(regname.SKYOBS3STARTBOTTOM),
                                                          rule=True_()|Has(itemname.MARIOLONG)|RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS3STARTTOPSIDE).connect(world.get_region(regname.SKYOBS3TOPOFHOUSE),
                                                          rule=RB.JumpHeight5)
    world.get_region(regname.SKYOBS3STARTBOTTOM).connect(world.get_region(regname.SKYOBS3TOPOFHOUSE))
    world.get_region(regname.SKYOBS3TOPOFHOUSE).connect(world.get_region(regname.SKYOBS3CYLINDER),
                                                        "Sky Station Comet: House Launch Star")
    world.get_region(regname.SKYOBS3CYLINDER).connect(world.get_region(regname.SKYOBS3BOSS),
                                                        "Sky Station Comet: Cylinder Launch Star",
                                                      RB.CanAirSpin)

    # Yoshi star
    world.get_region(regname.WORLD1).connect(world.get_region(regname.GOODEGG), "World 1 Slot 2 Galaxy")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG1LANDING), "Yoshi Star Star 1")
    world.get_region(regname.GOODEGG1LANDING).connect(world.get_region(regname.GOODEGG1MUDDY))
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGG1OCTOBONUS),
                                                      "Yoshi Star 1: Octogoomba Bonus Teleporter")
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGG1EARTH),
                                                      "Yoshi Star 1: Yoshi Planet Launch Star",
                                                    rule=RB.CanRideDino)
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGGGSTAR1))
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGGGSTAR2),
                                                    rule=(RB.CanRideDino|RB.CanLongSpin|RB.JumpHeight4))
    world.get_region(regname.GOODEGG1EARTH).connect(world.get_region(regname.GOODEGG1TOWER),
                                                      "Yoshi Star 1: Earthy Planet Launch Star")
    world.get_region(regname.GOODEGG1LANDING).connect(world.get_region(regname.GOODEGG1TOWER)) #Trick Entrance
    world.get_region(regname.GOODEGG1TOWER).connect(world.get_region(regname.GOODEGG1FOSSIL),
                                                      "Yoshi Star 1: Tower Launch Star",
                                                    rule=RB.CanDinoSwing)
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG2LANDING), "Yoshi Star Star 2")
    world.get_region(regname.GOODEGG2LANDING).connect(world.get_region(regname.GOODEGG2MUDDY))
    world.get_region(regname.GOODEGG2MUDDY).connect(world.get_region(regname.GOODEGG2SHOOTING),
                                              "Yoshi Star 2: Yoshi Planet Launch Star",
                                                    rule=RB.CanRideDino)
    world.get_region(regname.GOODEGG2SHOOTING).connect(world.get_region(regname.GOODEGG2ORBITS),
                                              "Yoshi Star 2: Mid-Travel Launch Star",
                                                       rule=RB.CanRideDino&RB.CanAirSpin)
    world.get_region(regname.GOODEGG2ORBITS).connect(world.get_region(regname.GOODEGG2MARBLE),
                                              "Yoshi Star 2: Planetoids Launch Star",
                                                     rule=RB.CanRideDino)
    world.get_region(regname.GOODEGG2SHOOTING).connect(world.get_region(regname.GOODEGG2MARBLE),
                                              "Yoshi Star 2: Shooting Gallery Launch Star",
                                                       rule=RB.CanRideDino)
    world.get_region(regname.GOODEGG2MARBLE).connect(world.get_region(regname.GOODEGG2BOSS),
                                              "Yoshi Star 2: Marble Block Launch Star")
    world.get_region(regname.GOODEGG2LANDING).connect(world.get_region(regname.GOODEGG2BOSS))  # Trick Entrance
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG3LANDING), "Yoshi Star Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.ROMPCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.YOSHSTARCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.YOSHSTARSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.YOSHSTARCM)
                                                          & CanReachLocation(locname.YOSHSTARSTAR1))))
                                              )
    world.get_region(regname.GOODEGG3LANDING).connect(world.get_region(regname.GOODEGG3MUDDY))
    # Spin-Dig
    world.get_region(regname.WORLD1).connect(world.get_region(regname.SPINDIG), "World 1 Slot 3 Galaxy")
    world.get_region(regname.SPINDIG).connect(world.get_region(regname.SPINDIG1TETRA), "Spin-Dig Star 1")
    world.get_region(regname.SPINDIG1TETRA).connect(world.get_region(regname.SPINDIG1DRILL),
                                                    "Spin-Dig 1: Dig Dirt Launch Star",
                                                    rule=RB.DRILLMASTER)
    world.get_region(regname.SPINDIG1DRILL).connect(world.get_region(regname.SPINDIG1STEEL),
                                                    "Spin-Dig 1: Drill Zone Launch Star",
                                                    rule=RB.DRILLMASTER)
    world.get_region(regname.SPINDIG1STEEL).connect(world.get_region(regname.SPINDIG1BONUS),
                                                    "Spin-Dig 1: Twirlips Bonus Teleporter")
    world.get_region(regname.SPINDIG1STEEL).connect(world.get_region(regname.SPINDIG1DIRTT),
                                                    "Spin-Dig 1: Steel Ring Launch Star")
    world.get_region(regname.SPINDIG1DIRTT).connect(world.get_region(regname.SPINDIG1TOADS),
                                                    "Spin-Dig 1: Dirt Tower Launch Star",
                                                    rule=RB.DRILLMASTER&RB.CanAirSpin)
    world.get_region(regname.SPINDIG1TOADS).connect(world.get_region(regname.SPINDIG1BOSS),
                                                    "Spin-Dig 1: Red Toadship Launch Star",
                                                    rule=RB.CanAirSpin)
    world.get_region(regname.SPINDIG).connect(world.get_region(regname.SPINDIG2TETRA), "Spin-Dig Star 2")
    world.get_region(regname.SPINDIG2TETRA).connect(world.get_region(regname.SPINDIG2DARKT),
                                                    "Spin-Dig 2: Dig Dirt Sling to Vine")
    world.get_region(regname.SPINDIG2DARKT).connect(world.get_region(regname.SPINDIG2DARKIN1),
                                                    "Spin-Dig 2: Dark Canister 1st Green Pipe")
    world.get_region(regname.SPINDIG2DARKIN1).connect(world.get_region(regname.SPINDIG2DARKIN2),
                                                    "Spin-Dig 2: Dark Canister 2nd Green Pipe",
                                                      rule=RB.DRILLMASTER)
    world.get_region(regname.SPINDIG2DARKIN2).connect(world.get_region(regname.SPINDIG2DARKB),
                                                    "Spin-Dig 2: Dark Canister Orange Pipe",
                                                      rule=RB.DRILLMASTER)
    world.get_region(regname.SPINDIG2DARKB).connect(world.get_region(regname.SPINDIG2BTOAD),
                                                    "Spin-Dig 2: Dark Canister Launch Star")
    world.get_region(regname.SPINDIG2BTOAD).connect(world.get_region(regname.SPINDIG2SQUARE),
                                                    "Spin-Dig 2: Blue Toadship Launch Star",
                                                    rule=RB.CanAirSpin)
    world.get_region(regname.SPINDIG).connect(world.get_region(regname.SPINDIG3BOSS), "Spin-Dig Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.SPINDIGCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.SPINDIGSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.SPINDIGCM)
                                                          & CanReachLocation(locname.SPINDIGSTAR1))))
                                              )
    # FlipSwap
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLIPSWAP), "World 1 Slot 4 Galaxy")
    world.get_region(regname.FLIPSWAP).connect(world.get_region(regname.FLIPSWAP1), "Flip-Swap Star")
    world.get_region(regname.FLIPSWAP).connect(world.get_region(regname.FLIPSWAP2), "Flip-Swap Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.FLIPSWAPCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.FLIPSWAPSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.FLIPSWAPCM)
                                                           & CanReachLocation(locname.FLIPSWAPSTAR1))))
                                               )
    # Fluffl Bluff
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLUFFBLUFF), "World 1 Slot 5 Galaxy")
    world.get_region(regname.FLUFFBLUFF).connect(world.get_region(regname.FLUFFBLUFF1LANDING), "Fluffy Bluff Star")
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FLUFFBLUFF1COINROOM),
                                                         "Fluffy Bluff: Landing Green Pipe")
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FLUFFBLUFF1BUILDING),
                                                         rule=RB.JumpHeight3|RB.CanMakeCloud)
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FLUFFBLUFF1BIGTREE),
                                                         rule=RB.CanMakeCloud|RB.JumpHeight6)
    world.get_region(regname.FLUFFBLUFF1BUILDING).connect(world.get_region(regname.FLUFFBLUFF1CLIFF1),
                                                          rule=RB.CanMakeCloud|(RB.CloudMario&(RB.JumpHeight3|(RB.CanWallSpin))))
    world.get_region(regname.FLUFFBLUFF1CLIFF1).connect(world.get_region(regname.FLUFFBLUFF1BIGTREE),
                                                        rule=RB.CanMakeCloud|RB.JumpHeight5)
    world.get_region(regname.FLUFFBLUFF1BIGTREE).connect(world.get_region(regname.FLUFFBLUFF1BIGCLOUD),
                                                         "Fluffy Bluff: Landing Big Tree Sling Star")
    world.get_region(regname.FLUFFBLUFF1BIGCLOUD).connect(world.get_region(regname.FLUFFBLUFF3TOWER),
                                                         "Fluffy Bluff: Hungry Luma",                                                     rule=((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL1)))
                                                     &(True_() if world.options.coin_luma_counts.value["Fluffy Bluff Coin Luma"]<100
                                                       else Has("Can Farm Coins")))),
    world.get_region(regname.FLUFFBLUFF1BIGCLOUD).connect(world.get_region(regname.FLUFFBLUFF1CLIFF1))
    world.get_region(regname.FLUFFBLUFF1CLIFF1).connect(world.get_region(regname.FLUFFBLUFF1CLIFF2),
                                                        rule=(RB.CloudMario&RB.CanLongJump)|RB.CanMakeCloud)
    world.get_region(regname.FLUFFBLUFF1CLIFF2).connect(world.get_region(regname.FLUFFBLUFF1WATER),
                                                         "Fluffy Bluff: Wall Jump Launch Star",
                                                        rule=RB.CanWallJump|(RB.CanLongJump&RB.CanMakeCloud))
    world.get_region(regname.FLUFFBLUFF1WATER).connect(world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB),
                                                         "Fluffy Bluff: Water Sphere Launch Star",
                                                       rule=RB.CanCollectStarChips)
    world.get_region(regname.FLUFFBLUFF1BIGCLOUD).connect(
    world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB))  # Trick Entrance
    world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB).connect(world.get_region(regname.FLUFFBLUFF1TREECLIMB),
                                                         "Fluffy Bluff: Vine Swing",
                                                            rule=RB.CanMakeCloud)
    world.get_region(regname.FLUFFBLUFF).connect(world.get_region(regname.FLUFFBLUFF2LANDING), "Fluffy Bluff Chimp Star")
    world.get_region(regname.FLUFFBLUFF2LANDING).connect(world.get_region(regname.FLUFFBLUFF2BUILDING),
                                                         rule=RB.JumpHeight3|True_()) # Replace True_() with Launch star rule when implemented
    world.get_region(regname.FLUFFBLUFF2LANDING).connect(world.get_region(regname.FLUFFBLUFF2TREE),
                                                         rule=RB.JumpHeight6)
    world.get_region(regname.FLUFFBLUFF2BUILDING).connect(world.get_region(regname.FLUFFBLUFF2CLIFF),
                                                          "Fluffy Bluff Chimp: Buildings Sling Star")
    world.get_region(regname.FLUFFBLUFF2CLIFF).connect(world.get_region(regname.FLUFFBLUFF2TREE),
                                                       rule=RB.CanLongJump)
    # Righside Down
    world.get_region(regname.WORLD1).connect(world.get_region(regname.RIGHTDOWN), "World 1 Slot 6 Galaxy")
    world.get_region(regname.RIGHTDOWN).connect(world.get_region(regname.RIGHTDOWNLANDING), "Rightside Down Star")
    world.get_region(regname.RIGHTDOWNLANDING).connect(world.get_region(regname.RIGHTDOWNCORRIDOR),
                                                "Rightside Down: Flower Fling")
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNCOINROOM),
                                                "Rightside Down: Green Pipe")
    world.get_region(regname.RIGHTDOWNCOINROOM).connect(world.get_region(regname.RIGHTDOWNBREAKER),
                                                "Rightside Down: Orange Pipe")
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNBONUS),
                                                "Rightside Down: Paragoomba Bonus Teleporter")
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNTOPVIEW),
                                                "Rightside Down: Flower Fling")
    # Fiery Fleet
    world.get_region(regname.WORLD1).connect(world.get_region(regname.BOWJR1), "World 1 Slot 7 Galaxy")
    world.get_region(regname.BOWJR1).connect(world.get_region(regname.FIREFLOT1LANDING), "Fiery Flotilla Grand Star")
    world.get_region(regname.FIREFLOT1LANDING).connect(world.get_region(regname.FIREFLOT1LAVA),
                                                       "Fiery Flotilla: Fort Sling Star")
    world.get_region(regname.FIREFLOT1LAVA).connect(world.get_region(regname.FIREFLOT1BOSS),
                                                       "Fiery Flotilla: Lava Planet Launch Star",
                                                    rule=RB.CanAirSpin)
    world.get_region(regname.FIREFLOT1LANDING).connect(world.get_region(regname.FIREFLOT1BOSS))  # Trick Entrance
    world.get_region(regname.BOWJR1).connect(world.get_region(regname.FIREFLOT2BOSS), "Fiery Flotilla Comet Star",
                                             rule=((RB.Comet1ItemAccess | (
                                                         OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                   & (RB.CometMissionOff
                                                      | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                 locname.FIREFLOTCM))
                                                      | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                 locname.FIREFLOTSTAR1))
                                                      | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                 locname.FIREFLOTCM)
                                                         & CanReachLocation(locname.FIREFLOTSTAR1))))
                                             )
    # World 2
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD2), "World 2 Map",
                                           rule=(Has(itemname.GRAND)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND2) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Puzzle Plank
    world.get_region(regname.WORLD2).connect(world.get_region(regname.PUZZPLAN), "World 2 Slot 1 Galaxy")
    world.get_region(regname.PUZZPLAN).connect(world.get_region(regname.PUZZPLAN1BLOCK), "Puzzle Plank Star")
    world.get_region(regname.PUZZPLAN1BLOCK).connect(world.get_region(regname.PUZZPLAN1GROUND),
                                                     rule=RB.CanPound)
    world.get_region(regname.PUZZPLAN1GROUND).connect(world.get_region(regname.PUZZPLAN1GRUZZY),
                                                      "Puzzle Plank: Wiggler Platform Launch Star",
                                                      rule=RB.CanPound)
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN1COINRO),
                                                      "Puzzle Plank: Grassy Buzzsaw Green Pipe")
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN3BUGABO),
                                                      "Puzzle Plank: Hungry Luma",
                                                      rule=((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL2)))
                                                     &(True_() if world.options.coin_luma_counts.value["Puzzle Plank Coin Luma"]<100
                                                       else Has("Can Farm Coins"))))
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN1SAWBLA),
                                                      "Puzzle Plank: Grassy Buzzsaw Launch Star",
                                                      rule=RB.CanPound|RB.JumpHeight6)
    world.get_region(regname.PUZZPLAN1SAWBLA).connect(world.get_region(regname.PUZZPLAN1CHECKP),
                                                      "Puzzle Plank: Saws & Planks Sling Star",
                                                      rule=RB.CanWallJump&RB.CanPound)
    world.get_region(regname.PUZZPLAN1CHECKP).connect(world.get_region(regname.PUZZPLAN1MANDIB),
                                                      "Puzzle Plank: Checkpoint Launch Star",
                                                      rule=RB.CanAirSpin)
    world.get_region(regname.PUZZPLAN).connect(world.get_region(regname.PUZZPLAN2GRUZZY), "Puzzle Plank Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.PUZZPLANKCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.PUZZPLANKSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.PUZZPLANKCM)
                                                           & CanReachLocation(locname.PUZZPLANKSTAR1))))
                                               )
    world.get_region(regname.PUZZPLAN2GRUZZY).connect(world.get_region(regname.PUZZPLAN2COINRO),
                                                      "Puzzle Plank Comet: Green Pipe")
    # Boulder Bowl
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOULBOWL), "World 2 Slot 2 Galaxy")
    world.get_region(regname.BOULBOWL).connect(world.get_region(regname.BOULBOWL1CRYSTAL), "Boulder Bowl Star")
    world.get_region(regname.BOULBOWL1CRYSTAL).connect(world.get_region(regname.BOULBOWL1FALLING),
                                                       rule=RB.ROCKNROLLIN)
    world.get_region(regname.BOULBOWL1FALLING).connect(world.get_region(regname.BOULBOWL1BOULDER),
                                                       "Boulder Bowl: Falling Rocks Launch Star")
    world.get_region(regname.BOULBOWL1CRYSTAL).connect(world.get_region(regname.BOULBOWL1BOULDER)) #Trick Entrance
    world.get_region(regname.BOULBOWL1BOULDER).connect(world.get_region(regname.BOULBOWL1DODECAH),
                                                       "Boulder Bowl: Boulder Sling Star",
                                                       rule=RB.ROCKNROLLIN)
    world.get_region(regname.BOULBOWL1BOULDER).connect(world.get_region(regname.BOULBOWL1DICEROOM),
                                                       "Boulder Bowl: Boulder Green Pipe")
    world.get_region(regname.BOULBOWL1DODECAH).connect(world.get_region(regname.BOULBOWL1BOSS),
                                                       "Boulder Bowl: Dodecahedron Launch Star",
                                                       rule=RB.CanAirSpin)
    world.get_region(regname.BOULBOWL).connect(world.get_region(regname.BOULBOWL2ASTEROI), "Boulder Bowl Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.ROMPCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.ROCKBOWLCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.ROCKBOWLSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.ROCKBOWLCM)
                                                           & CanReachLocation(locname.ROCKBOWLSTAR1))))
                                               )
    world.get_region(regname.BOULBOWL2ASTEROI).connect(world.get_region(regname.BOULBOWL2CAGEPLA),
                                                       "Boulder Bowl: Asteroid Launch Star")
    # Hightail Falls
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HIGHTAIL), "World 2 Slot 3 Galaxy")
    world.get_region(regname.HIGHTAIL).connect(world.get_region(regname.HIGHTAIL1LANDING), "Hightail Falls Star")
    world.get_region(regname.HIGHTAIL1LANDING).connect(world.get_region(regname.HIGHTAIL1GIANTRA),
                                                       "Hightail Falls: Hot Pepper Landing Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1GIANTRA).connect(world.get_region(regname.HIGHTAILGSTAR1),
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1GIANTRA).connect(world.get_region(regname.HIGHTAIL1PLATDAS),
                                                       "Hightail Falls: Hot Pepper Climb Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1PLATDAS).connect(world.get_region(regname.HIGHTAIL1BONUS),
                                                       "Hightail Falls: Paragoomba Bonus Teleporter",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1PLATDAS).connect(world.get_region(regname.HIGHTAIL1DASHWAL1),
                                                       "Hightail Falls: Hot Pepper Dash Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAIL1DASHWAL2),
                                                        rule=RB.CanDinoRun&RB.CanDinoSwing)
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAIL3SILVERS),
                                                        "Hightail Falls: Hungry Luma",
                                                        rule=((RB.CoinLumaBase |
                                                               (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL3)))
                                                              & (True_() if world.options.coin_luma_counts.value[
                                                                                "Hightail Falls Coin Luma"] < 100
                                                                 else Has("Can Farm Coins"))))
    world.get_region(regname.HIGHTAIL1DASHWAL2).connect(world.get_region(regname.HIGHTAILGSTAR3))
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAILGSTAR2),
                                                        rule=RB.CanDinoRun&CanLongJump)
    world.get_region(regname.HIGHTAIL).connect(world.get_region(regname.HIGHTAIL2LANDING), "Hightail Falls Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.HIGHFALLCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.HIGHFALLSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.HIGHFALLCM)
                                                           & CanReachLocation(locname.HIGHFALLSTAR1))))
                                               )
    world.get_region(regname.HIGHTAIL2LANDING).connect(world.get_region(regname.HIGHTAIL2GIANTRA),
                                                       "Hightail Falls Comet: Hot Pepper Landing Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL2GIANTRA).connect(world.get_region(regname.HIGHTAILGSTAR1),
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL2GIANTRA).connect(world.get_region(regname.HIGHTAIL2PLATDAS),
                                                       "Hightail Falls Comet: Hot Pepper Climb Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL2PLATDAS).connect(world.get_region(regname.HIGHTAIL2DASHWAL1),
                                                       "Hightail Falls Comet: Hot Pepper Dash Launch Star",
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL2DASHWAL1).connect(world.get_region(regname.HIGHTAIL2DASHWAL2),
                                                        rule=RB.CanDinoRun&RB.CanDinoSwing)
    world.get_region(regname.HIGHTAIL2DASHWAL2).connect(world.get_region(regname.HIGHTAILGSTAR3))
    world.get_region(regname.HIGHTAIL2DASHWAL1).connect(world.get_region(regname.HIGHTAILGSTAR2),
                                                        rule=RB.CanDinoRun&RB.CanLongJump)
    # Wild Glide
    world.get_region(regname.WORLD2).connect(world.get_region(regname.WILDGLIDE), "World 2 Slot 4 Galaxy")
    world.get_region(regname.WILDGLIDE).connect(world.get_region(regname.WILDGLIDESTART), "Wild Glide Star")
    world.get_region(regname.WILDGLIDESTART).connect(world.get_region(regname.WILDGLIDECOURSE),
                                                     rule=RB.CanRideBird)
    # Cosmic Cove
    world.get_region(regname.WORLD2).connect(world.get_region(regname.COSMICO), "World 2 Slot 5 Galaxy")
    world.get_region(regname.COSMICO).connect(world.get_region(regname.COSMIC1LANDING), "Cosmic Cove Star 1")
    world.get_region(regname.COSMIC1LANDING).connect(world.get_region(regname.COSMIC1POOL),
                                                     rule=RB.CanSwim)
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC1DICEROOM),
                                                  "Cosmic Cove 1: Green Pipe")
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC3WATER),
                                                  "Cosmic Cove: Hungry Luma",
                                                  rule=((RB.CoinLumaBase |
                                                         (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL4)))
                                                        & (True_() if world.options.coin_luma_counts.value[
                                                                          "Cosmic Cove Coin Luma"] < 100
                                                           else Has("Can Farm Coins")))   )
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC1WATERFA),
                                                  "Cosmic Cove 1: Icy Waterfall",
                                                  rule=RB.CanPound)
    world.get_region(regname.COSMICO).connect(world.get_region(regname.COSMIC2LANDING), "Cosmic Cove Star 2")
    world.get_region(regname.COSMIC2LANDING).connect(world.get_region(regname.COSMIC2INPIPE),
                                                  "Cosmic Cove 2: Green Pipe to Cave")
    world.get_region(regname.COSMIC2INPIPE).connect(world.get_region(regname.COSMIC2WATERPA),
                                                  "Cosmic Cove 2: Green Pipe in Cave",
                                                    rule=RB.CanSwim)
    world.get_region(regname.COSMIC2WATERPA).connect(world.get_region(regname.COSMIC2LANDING),
                                                  "Cosmic Cove 2: Return Green Pipe",
                                                     rule=RB.CanSwim)
    world.get_region(regname.COSMIC2LANDING).connect(world.get_region(regname.COSMIC2TOADSHI),
                                                  "Cosmic Cove 2: Landing Launch Star",
                                                     rule=CanReachEntrance("Cosmic Cove 2: Return Green Pipe"))
    world.get_region(regname.COSMIC2TOADSHI).connect(world.get_region(regname.COSMIC2WATERPL1),
                                                  "Cosmic Cove 2: Toadship Launch Star")
    world.get_region(regname.COSMIC2WATERPL1).connect(world.get_region(regname.COSMIC2WATERPL2),
                                                      rule=RB.CanSwim&RB.DRILLMASTER)
    # Honeybloom
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HONEYBLOOM), "World 2 Slot 6 Galaxy")
    world.get_region(regname.HONEYBLOOM).connect(world.get_region(regname.HONEYBLOOM1LANDING), "Honeybloom Star")
    world.get_region(regname.HONEYBLOOM1LANDING).connect(world.get_region(regname.HONEYBLOOM1SECRET),
                                                         rule=RB.CanSwing&RB.CanWallJump)
    world.get_region(regname.HONEYBLOOM1LANDING).connect(world.get_region(regname.HONEYBLOOM1WALL2),
                                                         rule=(RB.CanSwing&RB.CanWallJump)&
                                                              (RB.BeeFlight|RB.JumpHeight3))
    world.get_region(regname.HONEYBLOOM1WALL2).connect(world.get_region(regname.HONEYBLOOM1WALL3),
                                                       rule=RB.BeeFlight)
    world.get_region(regname.HONEYBLOOM1WALL3).connect(world.get_region(regname.HONEYBLOOM1HONELOG),
                                                       rule=RB.CanSwing&RB.BeeFlight)
    # Lava Lair
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOWSER1), "World 2 Slot 7 Galaxy")
    world.get_region(regname.BOWSER1).connect(world.get_region(regname.LAVALAIR1LANDING), "Lava Lair Grand Star")
    world.get_region(regname.LAVALAIR1LANDING).connect(world.get_region(regname.LAVALAIR1LAVACYL1),
                                                       "Lava Lair: Pull Star to Lava")
    world.get_region(regname.LAVALAIR1LAVACYL1).connect(world.get_region(regname.LAVALAIR1LAVACYL2),
                                                        rule=RB.CanPound)
    world.get_region(regname.LAVALAIR1LAVACYL2).connect(world.get_region(regname.LAVALAIR1LAVAPLA1B),
                                                       "Lava Lair: Lava Cylinder Launch Star")
    world.get_region(regname.LAVALAIR1LAVAPLA1B).connect(world.get_region(regname.LAVALAIR1LAVAPLA1W),
                                                       "Lava Lair: Lava Sling Star")
    world.get_region(regname.LAVALAIR1LAVAPLA1W).connect(world.get_region(regname.LAVALAIR1LAVAPLA2C),
                                                       "Lava Lair: Purple Bowser Door",
                                                         rule=RB.CanPound)
    world.get_region(regname.LAVALAIR1LAVAPLA2C).connect(world.get_region(regname.LAVALAIR1LAVAPLA2S))
    world.get_region(regname.LAVALAIR1LAVAPLA2S).connect(world.get_region(regname.LAVALAIR1BOSSPLA),
                                                       "Lava Lair: Red Bowser Door")
    world.get_region(regname.BOWSER1).connect(world.get_region(regname.LAVALAIR2LANDING), "Lava Lair Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.LAVALAIRCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.LAVALAIRSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.LAVALAIRCM)
                                                          & CanReachLocation(locname.LAVALAIRSTAR1))))
                                              )
    world.get_region(regname.LAVALAIR2LANDING).connect(world.get_region(regname.LAVALAIR2LAVACYL1),
                                                       "Lava Lair Comet: Pull Star to Lava")
    world.get_region(regname.LAVALAIR2LAVACYL1).connect(world.get_region(regname.LAVALAIR2LAVACYL2),
                                                        rule=RB.CanPound)
    world.get_region(regname.LAVALAIR2LAVACYL2).connect(world.get_region(regname.LAVALAIR2LAVAPLA1B),
                                                       "Lava Lair Comet: Lava Cylinder Launch Star")
    world.get_region(regname.LAVALAIR2LAVAPLA1B).connect(world.get_region(regname.LAVALAIR2LAVAPLA1W),
                                                       "Lava Lair Comet: Lava Sling Star")
    world.get_region(regname.LAVALAIR2LAVAPLA1W).connect(world.get_region(regname.LAVALAIR2LAVAPLA2C),
                                                       "Lava Lair Comet: Purple Bowser Door",
                                                         rule=RB.CanPound)
    world.get_region(regname.LAVALAIR2LAVAPLA2C).connect(world.get_region(regname.LAVALAIR2LAVAPLA2S))
    # World 3
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD3), "World 3 Map",
                                           rule=(Has(itemname.GRAND, 2)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND3) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Tall Trunk
    world.get_region(regname.WORLD3).connect(world.get_region(regname.TALLTRUNK), "World 3 Slot 1 Galaxy")
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK1BIGTREE), "Tall Trunk Star 1")
    world.get_region(regname.TALLTRUNK1BIGTREE).connect(world.get_region(regname.TALLTRUNK1LOG),
                                                        "Tall Trunk 1: Big Tree Launch Star",
                                                        rule=RB.CanDinoBlimp)
    world.get_region(regname.TALLTRUNK1BIGTREE).connect(world.get_region(regname.TALLTRUNK1PIRANHABONUS),
                                                        "Tall Trunk 1: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1WOODCIRClE),
                                                        "Tall Trunk 1: Carved Log Launch Star",
                                                    rule=RB.CanDinoBlimp&RB.CanCollectStarChips)
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1DICEPIPE),
                                                        "Tall Trunk 1: Carved Log Green pipe")
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK2BIGTREE), "Tall Trunk Star 2")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2PIRANHABONUS),
                                                        "Tall Trunk 2: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2SLIDE),
                                                        "Tall Trunk 2: Big Tree Launch Star",
                                                        rule=RB.CanDinoBlimp)
    world.get_region(regname.TALLTRUNK2SLIDE).connect(world.get_region(regname.TALLTRUNK2SLIDEND),
                                                      rule=RB.CanSlide)
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK3PCOINSLIDE), "Tall Trunk Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.TALLTREECM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.TALLTREESTAR2))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.TALLTREECM)
                                                            & CanReachLocation(locname.TALLTREESTAR2))))
                                                )
    world.get_region(regname.TALLTRUNK3PCOINSLIDE).connect(world.get_region(regname.TALLTRUNK3PCOINEND))
    # Cloudy Court
    world.get_region(regname.WORLD3).connect(world.get_region(regname.CLOUCOUR), "World 3 Slot 2 Galaxy")
    world.get_region(regname.CLOUCOUR).connect(world.get_region(regname.CLOUCOUR1LANDING), "Cloudy Court Star")
    world.get_region(regname.CLOUCOUR1LANDING).connect(world.get_region(regname.CLOUCOUR1CYMBAL),
                                                       rule=RB.CanMakeCloud)
    world.get_region(regname.CLOUCOUR1CYMBAL).connect(world.get_region(regname.CLOUCOUR1TOWERS),
                                                      "Cloudy Court: Cymbal Launch Star")
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR3PCOINS),
                                                      "Cloudy Court: Hungry Luma",
                                                      rule=((RB.CoinLumaBase |
                                                             (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL5)))
                                                            & (True_() if world.options.coin_luma_counts.value[
                                                                              "Cloudy Court Coin Luma"] < 100
                                                               else Has("Can Farm Coins"))))
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1PARAGOOMBONUS),
                                                      "Cloudy Court: Paragoomba Bonus Teleporter",
                                                      rule=RB.CanMakeCloud)
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1CASTLE),
                                                      "Cloudy Court: Tower Launch Star",
                                                      rule=RB.CanMakeCloud&RB.CanPound)
    world.get_region(regname.CLOUCOUR).connect(world.get_region(regname.CLOUCOUR2LANDING), "Cloudy Court Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.COSMICCLONE)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.CLOUDCOURTCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.CLOUDCOURTSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.CLOUDCOURTCM)
                                                           & CanReachLocation(locname.CLOUDCOURTSTAR1))))
                                               )
    world.get_region(regname.CLOUCOUR2LANDING).connect(world.get_region(regname.CLOUCOUR2CASTLE1),
                                                       "Cloudy Court Comet: Launch Star",
                                                       rule=RB.CanCollectStarChips)
    world.get_region(regname.CLOUCOUR2CASTLE1).connect(world.get_region(regname.CLOUCOUR2CASTLE2),
                                                       "Cloudy Court Comet: Wall Jump Sling Star",
                                                       rule=RB.CanWallSpin)
    world.get_region(regname.CLOUCOUR2CASTLE2).connect(world.get_region(regname.CLOUCOUR2FINAL),
                                                       "Cloudy Court Comet: Final Sling Star")
    # Haunty halls
    world.get_region(regname.WORLD3).connect(world.get_region(regname.HAUNHALL), "World 3 Slot 3 Galaxy")
    world.get_region(regname.HAUNHALL).connect(world.get_region(regname.HAUNHALL1HALLWAY), "Haunty Halls Star 1")
    world.get_region(regname.HAUNHALL1HALLWAY).connect(world.get_region(regname.HAUNHALL1JACKBON),
                                               "Haunty Halls 1: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.HAUNHALL1HALLWAY).connect(world.get_region(regname.HAUNHALL1DISAPPE),
                                               "Haunty Halls 1: Hallway Launch Star")
    world.get_region(regname.HAUNHALL1DISAPPE).connect(world.get_region(regname.HAUNHALL1BULBBER),
                                               "Haunty Halls 1: Green Pipe")
    world.get_region(regname.HAUNHALL).connect(world.get_region(regname.HAUNHALL2HALLWAY), "Haunty Halls Star 2")
    world.get_region(regname.HAUNHALL2HALLWAY).connect(world.get_region(regname.HAUNHALL2JACKBON),
                                               "Haunty Halls 2: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.HAUNHALL2HALLWAY).connect(world.get_region(regname.HAUNHALL2CREEPYC),
                                               "Haunty Halls 2: Hallway Launch Star",
                                                       rule=RB.CanAirSpin)
    world.get_region(regname.HAUNHALL2CREEPYC).connect(world.get_region(regname.HAUNHALL2CREEPYH),
                                               "Haunty Halls 2: Creepy Platforms Sling Star")
    world.get_region(regname.HAUNHALL).connect(world.get_region(regname.HAUNHALL3CREEPYH), "Haunty Halls Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.COSMICCLONE)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.HAUNTHALLCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.HAUNTHALLSTAR2))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.HAUNTHALLCM)
                                                           & CanReachLocation(locname.HAUNTHALLSTAR2))))
                                               )
    # Freezy Flake
    world.get_region(regname.WORLD3).connect(world.get_region(regname.FREEFLAKE), "World 3 Slot 4 Galaxy")
    world.get_region(regname.FREEFLAKE).connect(world.get_region(regname.FREEFLAK1LOGCABI), "Freezy Flake 1")
    world.get_region(regname.FREEFLAK1LOGCABI).connect(world.get_region(regname.FREEFLAK1SNOWBYH),
                                                       "Freezy Flake 1: Log Cabin Launch Star",
                                                       rule=RB.FireMario)
    world.get_region(regname.FREEFLAK1SNOWBYH).connect(world.get_region(regname.FREEFLAK3CHIMP),
                                                       "Freezy Flake 1: Snowy Hill 1 Green Pipe")
    world.get_region(regname.FREEFLAK1SNOWBYH).connect(world.get_region(regname.FREEFLAK1SLIDELA),
                                                       "Freezy Flake 1: Snow Slide",
                                                       rule=RB.CanSlide&RB.FireMario)
    world.get_region(regname.FREEFLAK1SLIDELA).connect(world.get_region(regname.FREEFLAK1LAVASNO),
                                                       "Freezy Flake 1: Slide Landing Green Pipe",
                                                       rule=RB.FireMario)
    world.get_region(regname.FREEFLAKE).connect(world.get_region(regname.FREEFLAK2LOGCABI), "Freezy Flake 2")
    world.get_region(regname.FREEFLAK2LOGCABI).connect(world.get_region(regname.FREEFLAK2SNOWBYH),
                                                       "Freezy Flake 2: Log Cabin Launch Star",
                                                       rule=RB.FireMario)
    world.get_region(regname.FREEFLAK2SNOWBYH).connect(world.get_region(regname.FREEFLAK3CHIMP),
                                                       "Freezy Flake 2: Snowy Hill 2 Green Pipe")
    world.get_region(regname.FREEFLAK2SNOWBYH).connect(world.get_region(regname.FREEFLAK2WHITOUT),
                                                       "Freezy Flake 2: Snowy Hill Launch Star")
    world.get_region(regname.FREEFLAK2WHITOUT).connect(world.get_region(regname.FREEFLAK2DICEROOM),
                                                       "Freezy Flake 2: Whiteout Green Pipe")
    world.get_region(regname.FREEFLAK2WHITOUT).connect(world.get_region(regname.FREEFLAK2SORBHEA),
                                                       "Freezy Flake 2: Whiteout Launch Star")
    world.get_region(regname.FREEFLAK2SORBHEA).connect(world.get_region(regname.FREEFLAK2SORBETT),
                                                       "Freezy Flake 2: Sorbetti's Head Sling Star",
                                                       rule=RB.CanAirSpin)
    # Beat Block
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BEATBLOCK), "World 3 Slot 5 Galaxy")
    world.get_region(regname.BEATBLOCK).connect(world.get_region(regname.BEATBLOK1), "Beat Block Star")
    world.get_region(regname.BEATBLOCK).connect(world.get_region(regname.BEATBLOK2), "Beat Block Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.DOUBLETIME)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.BEATBLOCKCM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.BEATBLOCKSTAR1))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.BEATBLOCKCM)
                                                            & CanReachLocation(locname.BEATBLOCKSTAR1))))
                                                )
    #Rolling masterpiece
    world.get_region(regname.WORLD3).connect(world.get_region(regname.ROLLMAST), "World 3 Slot 6 Galaxy")
    world.get_region(regname.ROLLMAST).connect(world.get_region(regname.ROLLMAST1LANDING), "Rolling Masterpiece Star")
    world.get_region(regname.ROLLMAST1LANDING).connect(world.get_region(regname.ROLLMAST1PAINTBR),
                                                       "Rolling Masterpiece: Landing Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST1PAINTBR).connect(world.get_region(regname.ROLLMAST1ELEVATO),
                                                       "Rolling Masterpiece: Paintbrush Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST1ELEVATO).connect(world.get_region(regname.ROLLMAST1SAWBLAD),
                                                       "Rolling Masterpiece: Elevator Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST1SAWBLAD).connect(world.get_region(regname.ROLLMAST1SILVERC))
    world.get_region(regname.ROLLMAST).connect(world.get_region(regname.ROLLMAST2LANDING), "Rolling Masterpiece Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.ROLLMASTERCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.ROLLMASTERSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.ROLLMASTERCM)
                                                           & CanReachLocation(locname.ROLLMASTERSTAR1))))
                                               )
    world.get_region(regname.ROLLMAST2LANDING).connect(world.get_region(regname.ROLLMAST2PAINTBR),
                                                       "Rolling Masterpiece Comet: Landing Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST2PAINTBR).connect(world.get_region(regname.ROLLMAST2ELEVATO),
                                                       "Rolling Masterpiece Comet: Paintbrush Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST2ELEVATO).connect(world.get_region(regname.ROLLMAST2BOMBOMB),
                                                       "Rolling Masterpiece Comet: Elevator Ball Launcher",
                                                       rule=RB.CanBalance)
    world.get_region(regname.ROLLMAST2BOMBOMB).connect(world.get_region(regname.ROLLMAST2SILVERC),
                                                       "Rolling Masterpiece Comet: Bob-omb Ball Launcher",
                                                       rule=RB.CanBalance)
    # Fearsome Fleet
    world.get_region(regname.WORLD3).connect(world.get_region(regname.BOWJR2), "World 3 Slot 7 Galaxy")
    world.get_region(regname.BOWJR2).connect(world.get_region(regname.FEARFLET1LANDING), "Fearsome Fleet Grand Star")
    world.get_region(regname.FEARFLET1LANDING).connect(world.get_region(regname.FEARFLET1UNDERGR),
                                                       "Fearsome Fleet: First Electric Cage",
                                                       rule=RB.CanRideDino)
    world.get_region(regname.FEARFLET1UNDERGR).connect(world.get_region(regname.FEARFLET1BULLETB),
                                                       "Fearsome Fleet: Firing Line Sling Star",
                                                       rule=RB.CanRideDino)
    world.get_region(regname.FEARFLET1BULLETB).connect(world.get_region(regname.FEARFLET1AIRSHIP),
                                                       rule=RB.CanDinoSwing)
    world.get_region(regname.FEARFLET1AIRSHIP).connect(world.get_region(regname.FEARFLET1MEGAHAM),
                                                       "Fearsome Fleet: Airship Launch Star")
    world.get_region(regname.BOWJR2).connect(world.get_region(regname.FEARFLET2MEGAHAM), "Fearsome Fleet Comet Star",
                                             rule=((RB.Comet1ItemAccess | (
                                                         OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                   & (RB.CometMissionOff
                                                      | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                 locname.FEARFLEETCM))
                                                      | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                 locname.FEARFLETSTAR1))
                                                      | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                 locname.FEARFLEETCM)
                                                         & CanReachLocation(locname.FEARFLETSTAR1))))
                                             )
    # World 4
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD4), "World 4 Map",
                                           rule=(Has(itemname.GRAND, 3)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND4) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Supermassive
    world.get_region(regname.WORLD4).connect(world.get_region(regname.SUPMASS), "World 4 Slot 1 Galaxy")
    world.get_region(regname.SUPMASS).connect(world.get_region(regname.SUPMASS1START), "Supermassive Star")
    world.get_region(regname.SUPMASS1START).connect(world.get_region(regname.SUPMASS1PIPES),
                                                    rule=RB.CanWallJump)
    world.get_region(regname.SUPMASS1PIPES).connect(world.get_region(regname.SUPMASS1THWOMPS))
    world.get_region(regname.SUPMASS1PIPES).connect(world.get_region(regname.SUPMASS1GSTAR2),
                                                    rule=RB.CanLongSpin)
    world.get_region(regname.SUPMASS1THWOMPS).connect(world.get_region(regname.SUPMASS1GSTAR2),
                                                      rule=RB.CanAirSpin)
    world.get_region(regname.SUPMASS1THWOMPS).connect(world.get_region(regname.SUPMASS1KOOPAS),
                                                      "Supermassive 1: Thwomps Launch Star",
                                                      rule=(RB.CanWallJump|RB.JumpHeight4)&RB.CanAirSpin)
    world.get_region(regname.SUPMASS1KOOPAS).connect(world.get_region(regname.SUPMASS1STARCHIPS),
                                                     "Supermassive 1: Koopa Launch Star",
                                                     rule=RB.CanAirSpin)
    world.get_region(regname.SUPMASS1STARCHIPS).connect(world.get_region(regname.SUPMASS1GARDEN),
                                                        "Supermassive 1: ? Block Launch Star")
    world.get_region(regname.SUPMASS1STARCHIPS).connect(world.get_region(regname.SUPMASS1WIGGLERS)) # Trick Entrance
    world.get_region(regname.SUPMASS1GARDEN).connect(world.get_region(regname.SUPMASS1WIGGLERS),
                                                     "Supermassive 1: Garden Planet Launch Star")
    world.get_region(regname.SUPMASS).connect(world.get_region(regname.SUPMASS1START), "Supermassive Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.SUPERMASSCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.SUPERMASSSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.SUPERMASSCM)
                                                          & CanReachLocation(locname.SUPERMASSSTAR1))))
                                              )
    world.get_region(regname.SUPMASS2START).connect(world.get_region(regname.SUPMASS2PIPES),
                                                    rule=RB.CanWallJump)
    world.get_region(regname.SUPMASS2PIPES).connect(world.get_region(regname.SUPMASS2THWOMPS))
    world.get_region(regname.SUPMASS2THWOMPS).connect(world.get_region(regname.SUPMASS2KOOPAS),
                                                      "Supermassive Comet: Thwomps Launch Star",
                                                      rule=(RB.CanWallJump|RB.JumpHeight4)&RB.CanAirSpin)
    world.get_region(regname.SUPMASS2KOOPAS).connect(world.get_region(regname.SUPMASS2STARCHIPS),
                                                     "Supermassive Comet: Koopa Launch Star",
                                                     rule=RB.CanAirSpin)
    world.get_region(regname.SUPMASS2STARCHIPS).connect(world.get_region(regname.SUPMASS2GARDEN),
                                                        "Supermassive Comet: ? Block Launch Star")
    world.get_region(regname.SUPMASS2STARCHIPS).connect(world.get_region(regname.SUPMASS2WIGGLERS)) # Trick Entrance
    world.get_region(regname.SUPMASS2GARDEN).connect(world.get_region(regname.SUPMASS2WIGGLERS),
                                                     "Supermassive Comet: Garden Planet Launch Star")
    # Sweet Mystery
    world.get_region(regname.WORLD4).connect(world.get_region(regname.SWEETMYS), "World 4 Slot 2 Galaxy")
    world.get_region(regname.SWEETMYS).connect(world.get_region(regname.SWEETMYS1START), "Sweet Mystery Star")
    world.get_region(regname.SWEETMYS1START).connect(world.get_region(regname.SWEETMYS1COOKIE),
                                                     rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS1COOKIE).connect(world.get_region(regname.SWEETMYS1CHOCO),
                                                      rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS1CHOCO).connect(world.get_region(regname.SWEETMYS1BISCUIT),
                                                     rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS1BISCUIT).connect(world.get_region(regname.SWEETMYS1SWITCHES),
                                                       rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS1SWITCHES).connect(world.get_region(regname.SWEETMYS1CAKE),
                                                        "Sweet Mystery: Flipswitch Launch Star",
                                                        RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS).connect(world.get_region(regname.SWEETMYS2START), "Sweet Mystery Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.SWEETMYSTCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.SWEETMYSTSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.SWEETMYSTCM)
                                                           & CanReachLocation(locname.SWEETMYSTSTAR1))))
                                               )
    world.get_region(regname.SWEETMYS2START).connect(world.get_region(regname.SWEETMYS2COOKIE),
                                                     rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS2COOKIE).connect(world.get_region(regname.SWEETMYS2CHOCO),
                                                      rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS2CHOCO).connect(world.get_region(regname.SWEETMYS2BISCUIT),
                                                     rule=RB.CanDinoGlow)
    world.get_region(regname.SWEETMYS2BISCUIT).connect(world.get_region(regname.SWEETMYS2END),
                                                       rule=RB.CanDinoGlow)
    # Flipsville
    world.get_region(regname.WORLD4).connect(world.get_region(regname.FLIPVILL), "World 4 Slot 3 Galaxy")
    world.get_region(regname.FLIPVILL).connect(world.get_region(regname.FLIPVILL1MAZESTART), "Flipsville Star 1")
    world.get_region(regname.FLIPVILL1MAZESTART).connect(world.get_region(regname.FLIPVILL1MAZEBOTTOM))
    world.get_region(regname.FLIPVILL1MAZESTART).connect(world.get_region(regname.FLIPVILL1MAZEBACK))
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1MAZEBACK))
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1MAZETOP))
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1MAZETOP)) # Trick Entrance
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1COMETMEDAL))
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1COMETMEDAL))
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1TWIRLIP),
                                                        "Flipsville 1: Twirlip Bonus Teleporter")
    world.get_region(regname.FLIPVILL1MAZETOP).connect(world.get_region(regname.FLIPVILL1WANWANSTART),
                                                       "Flipsville 1: Dollhouse Launch Star")
    world.get_region(regname.FLIPVILL1WANWANSTART).connect(world.get_region(regname.FLIPVILL1WANWANALLEY))
    world.get_region(regname.FLIPVILL1WANWANSTART).connect(world.get_region(regname.FLIPVILL1WANWANLANE)) #Advanced Logic
    world.get_region(regname.FLIPVILL1WANWANALLEY).connect(world.get_region(regname.FLIPVILL1WANWANLANE))
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1WANWANLANE)) # Trick Entrance
    world.get_region(regname.FLIPVILL1WANWANLANE).connect(world.get_region(regname.FLIPVILL1WANWANBACK))
    world.get_region(regname.FLIPVILL1WANWANBACK).connect(world.get_region(regname.FLIPVILL1LIFTSTART),
                                                          "Flipsville 1: Chomps Launch Star")
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1LIFTSTART)) # Trick Entrance
    world.get_region(regname.FLIPVILL1LIFTSTART).connect(world.get_region(regname.FLIPVILL1LIFTBELOW))
    world.get_region(regname.FLIPVILL1LIFTSTART).connect(world.get_region(regname.FLIPVILL1LIFTTOP))
    world.get_region(regname.FLIPVILL1LIFTBELOW).connect(world.get_region(regname.FLIPVILL1LIFTTOP))
    world.get_region(regname.FLIPVILL1LIFTTOP).connect(world.get_region(regname.FLIPVILL1STARSHROOM),
                                                       "Flipsville 1: Lifts Launch Star")
    world.get_region(regname.FLIPVILL1WANWANLANE).connect(world.get_region(regname.FLIPVILL1STARSHROOM)) # Trick Entrance
    world.get_region(regname.FLIPVILL1STARSHROOM).connect(world.get_region(regname.FLIPVILL1GLAM),
                                                          "Flipsville 1: Starshroom Launch Star")
    world.get_region(regname.FLIPVILL1WANWANLANE).connect(world.get_region(regname.FLIPVILL1GLAM)) # Trick Entrance
    world.get_region(regname.FLIPVILL1GLAM).connect(world.get_region(regname.FLIPVILL1STAR))
    world.get_region(regname.FLIPVILL).connect(world.get_region(regname.FLIPVILL2MAZESTART), "Flipsville Star 2")
    world.get_region(regname.FLIPVILL2MAZESTART).connect(world.get_region(regname.FLIPVILL2MAZEBOTTOM))
    world.get_region(regname.FLIPVILL2MAZESTART).connect(world.get_region(regname.FLIPVILL2MAZEBACK))
    world.get_region(regname.FLIPVILL2MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL2MAZEBACK))
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2TWIRLIP),
                                                        "Flipsville 2: Twirlip Bonus Teleporter")
    world.get_region(regname.FLIPVILL2MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL2MAZETOP))
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2MAZETOP))
    world.get_region(regname.FLIPVILL2MAZETOP).connect(world.get_region(regname.FLIPVILL2MAZELAUNCH))
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2MAZELAUNCH))
    world.get_region(regname.FLIPVILL2MAZELAUNCH).connect(world.get_region(regname.FLIPVILL2TOWERSTART),
                                                          "Flipsville 2: Dollhouse Planet Launch Star")
    world.get_region(regname.FLIPVILL2TOWERSTART).connect(world.get_region(regname.FLIPVILL2TOWERBELOW))
    world.get_region(regname.FLIPVILL2TOWERSTART).connect(world.get_region(regname.FLIPVILL2PIPE))
    world.get_region(regname.FLIPVILL2TOWERBELOW).connect(world.get_region(regname.FLIPVILL2PIPE))
    world.get_region(regname.FLIPVILL2PIPE).connect(world.get_region(regname.FLIPVILL2GRAVITYSTART),
                                                    "Flipsville 2: Spin-Drill Tower Pipe")
    world.get_region(regname.FLIPVILL2GRAVITYSTART).connect(world.get_region(regname.FLIPVILL2GRAVITYMAIN))
    world.get_region(regname.FLIPVILL).connect(world.get_region(regname.FLIPVILL3TOWER), "Flipsville Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.FLIPVILLECM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.FLIPVILLESTAR2))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.FLIPVILLECM)
                                                           & CanReachLocation(locname.FLIPVILLESTAR2))))
                                               )
    world.get_region(regname.FLIPVILL3TOWER).connect(world.get_region(regname.FLIPVILL3GRAVITY),
                                                     "Flipsville 3: Spin-Drill Tower Pipe")
    # Honeyhop
    world.get_region(regname.WORLD4).connect(world.get_region(regname.HONEYHOP), "World 4 Slot 4 Galaxy")
    world.get_region(regname.HONEYHOP).connect(world.get_region(regname.HONEYHOP1START), "Honeyhop Star 1")
    world.get_region(regname.HONEYHOP1START).connect(world.get_region(regname.HONEYHOP1POND),
                                                     rule=RB.BeeFlight&RB.CanSwing)
    world.get_region(regname.HONEYHOP1POND).connect(world.get_region(regname.HONEYHOP1CLOUDS))
    world.get_region(regname.HONEYHOP1POND).connect(world.get_region(regname.HONEYHOP1DICEROOM),
                                                    "Honeyhop: Pond Green Pipe")
    world.get_region(regname.HONEYHOP1CLOUDS).connect(world.get_region(regname.HONEYHOP1QBBASE),
                                                      rule=RB.BeeFlight&RB.CanSwing)
    world.get_region(regname.HONEYHOP1QBBASE).connect(world.get_region(regname.HONEYHOP1QBBUBBLE),
                                                      rule=RB.BeeFlight|(RB.CanWallJump&(RB.CanLongJump|RB.JumpHeight3)))
    world.get_region(regname.HONEYHOP1QBBUBBLE).connect(world.get_region(regname.HONEYHOP1QBTOP),
                                                        rule=(RB.BeeFlight|RB.CanWallJump)&RB.CanSwing)
    world.get_region(regname.HONEYHOP).connect(world.get_region(regname.HONEYHOP2QBBASE), "Honeyhop Chimp Star")
    world.get_region(regname.HONEYHOP2QBBASE).connect(world.get_region(regname.HONEYHOP2QBBUBBLE),
                                                      rule=True_()|RB.CanWallJump) # Replace True_() with sling star rule in the future
    world.get_region(regname.HONEYHOP2QBBUBBLE).connect(world.get_region(regname.HONEYHOP2QBTOP),
                                                        rule=RB.CanSwing)
    # Starshine Beach
    world.get_region(regname.WORLD4).connect(world.get_region(regname.STARBEACH), "World 4 Slot 5 Galaxy")
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH1WATER), "Starshine Star 1")
    world.get_region(regname.STARBEACH1WATER).connect(world.get_region(regname.STARBEACH1MAIN),
                                                      "Starshine Star 1: Waterdrop Launch Star",
                                                      rule=RB.CanSwim)
    world.get_region(regname.STARBEACH1MAIN).connect(world.get_region(regname.STARBEACH1BONUS),
                                                      "Starshine Star 1: Crabber Bonus Teleporter")
    world.get_region(regname.STARBEACH1MAIN).connect(world.get_region(regname.STARBEACH1COINR),
                                                      "Starshine Star 1: Tropical Beach Green Pipe")
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH2WATER), "Starshine Star 2")
    world.get_region(regname.STARBEACH2WATER).connect(world.get_region(regname.STARBEACH2MAIN),
                                                      "Starshine Star 2: Waterdrop Launch Star",
                                                      rule=RB.CanSwim)
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2DEEPW),
                                                     rule=RB.CanSwim)
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2BONUS),
                                                      "Starshine Star 2: Crabber Bonus Teleporter")
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2COINR),
                                                      "Starshine Star 2: Tropical Beach Green Pipe")
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH3MAIN), "Starshine Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.STARBEACHCM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.STARBEACHSTAR2))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.STARBEACHCM)
                                                            & CanReachLocation(locname.STARBEACHSTAR2))))
                                                )
    # Chompworks
    world.get_region(regname.WORLD4).connect(world.get_region(regname.CHOMWORK), "World 4 Slot 6 Galaxy")
    world.get_region(regname.CHOMWORK).connect(world.get_region(regname.CHOMWORK1START), "Chompworks Star 1")
    world.get_region(regname.CHOMWORK1START).connect(world.get_region(regname.CHOMWORK1ROLLING),
                                                     "Chompworks 1: Start Launch Star",
                                                     rule=RB.JumpHeight3)
    world.get_region(regname.CHOMWORK1ROLLING).connect(world.get_region(regname.CHOMWORK1BONUS),
                                                       "Chompworks 1: Bonus Room Pipe")
    world.get_region(regname.CHOMWORK1ROLLING).connect(world.get_region(regname.CHOMWORK1FLIPSWAP),
                                                       "Chompworks 1: Rolling Chomps Launch Star")
    world.get_region(regname.CHOMWORK1FLIPSWAP).connect(world.get_region(regname.CHOMWORK1LAVA),
                                                        "Chompworks 1: Flipping Platforms Launch Star")
    world.get_region(regname.CHOMWORK).connect(world.get_region(regname.CHOMWORK2START), "Chompworks Star 2")
    world.get_region(regname.CHOMWORK2START).connect(world.get_region(regname.CHOMWORK2ROLLING),
                                                     "Chompworks 2: Start Launch Star",
                                                     rule=RB.JumpHeight5|RB.SPRONGIN)
    world.get_region(regname.CHOMWORK2ROLLING).connect(world.get_region(regname.CHOMWORK2TOWER),
                                                       "Chompworks 2: Rolling Chomps Launch Star",
                                                       rule=RB.JumpHeight5|RB.SPRONGIN)
    world.get_region(regname.CHOMWORK).connect(world.get_region(regname.CHOMWORK3LAVA), "Chompworks Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.COSMICCLONE)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.CHOMPWORKCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.CHOMPWORKSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.CHOMPWORKCM)
                                                           & CanReachLocation(locname.CHOMPWORKSTAR1))))
                                               )
    # Gravity Gauntlet
    world.get_region(regname.WORLD4).connect(world.get_region(regname.BOWSER2), "World 4 Slot 7 Galaxy")
    world.get_region(regname.BOWSER2).connect(world.get_region(regname.GRAVGAUN1LANDING), "Gravity Gauntlet Grand Star")
    world.get_region(regname.GRAVGAUN1LANDING).connect(world.get_region(regname.GRAVGAUN1WATERCO),
                                                       rule=RB.CanSwim)
    world.get_region(regname.GRAVGAUN1LANDING).connect(world.get_region(regname.GRAVGAUNGSTAR1),
                                                       rule=RB.JumpHeight3)
    world.get_region(regname.GRAVGAUN1WATERCO).connect(world.get_region(regname.GRAVGAUN1WHOMPWA))
    world.get_region(regname.GRAVGAUN1WHOMPWA).connect(world.get_region(regname.GRAVGAUNGSTAR2),
                                                       rule=RB.JumpHeight6|(RB.CanWallSpin&RB.JumpHeight4))
    world.get_region(regname.GRAVGAUN1WHOMPWA).connect(world.get_region(regname.GRAVGAUN1DOORTOD),
                                                       "Gravity Gauntlet: Fire Wheel Launch Star",
                                                       rule=RB.CanAirSpin)
    world.get_region(regname.GRAVGAUN1DOORTOD).connect(world.get_region(regname.GRAVGAUN1BOSSARE))
    world.get_region(regname.BOWSER2).connect(world.get_region(regname.GRAVGAUN2LANDING), "Gravity Gauntlet Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.GRAVGAUNTCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.GRAVGAUNSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.GRAVGAUNTCM)
                                                          & CanReachLocation(locname.GRAVGAUNSTAR1))))
                                              )
    world.get_region(regname.GRAVGAUN2LANDING).connect(world.get_region(regname.GRAVGAUN2WATERCO),
                                                       rule=RB.CanSwim)
    world.get_region(regname.GRAVGAUN2LANDING).connect(world.get_region(regname.GRAVGAUNGSTAR1),
                                                       rule=RB.JumpHeight3)
    world.get_region(regname.GRAVGAUN2WATERCO).connect(world.get_region(regname.GRAVGAUN2WHOMPWA))
    world.get_region(regname.GRAVGAUN2WHOMPWA).connect(world.get_region(regname.GRAVGAUNGSTAR2),
                                                       rule=RB.JumpHeight6|(RB.CanWallSpin&RB.JumpHeight4))
    # World 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD5), "World 5 Map",
                                           rule=(Has(itemname.GRAND, 4)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND5) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Space Storm
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SPACSTOR), "World 5 Slot 1 Galaxy")
    world.get_region(regname.SPACSTOR).connect(world.get_region(regname.SPACSTOR1PULL), "Space Storm Star 1")
    world.get_region(regname.SPACSTOR1PULL).connect(world.get_region(regname.SPACSTOR1SATELLITE),
                                                    "Space Storm 1: Pull to Launch Star")
    world.get_region(regname.SPACSTOR1SATELLITE).connect(world.get_region(regname.SPACSTOR1REDCANOUT),
                                                    "Space Storm 1: Satellite Launch Star",
                                                         rule=RB.CanLongJump|RB.JumpHeight3)
    world.get_region(regname.SPACSTOR1REDCANOUT).connect(world.get_region(regname.SPACSTOR1REDCANIN))
    world.get_region(regname.SPACSTOR1REDCANIN).connect(world.get_region(regname.SPACSTOR1TOPMAN),
                                                    "Space Storm 1: Canister Launch Star")
    world.get_region(regname.SPACSTOR1TOPMAN).connect(world.get_region(regname.SPACSTOR1PULLPATH),
                                                    "Space Storm 1: Pull Star Path")
    world.get_region(regname.SPACSTOR).connect(world.get_region(regname.SPACSTOR2PULL), "Space Storm Star 2")
    world.get_region(regname.SPACSTOR2PULL).connect(world.get_region(regname.SPACSTOR2TOPTOWERBASE),
                                                    "Space Storm 2: Pull to Launch Star")
    world.get_region(regname.SPACSTOR2TOPTOWERBASE).connect(world.get_region(regname.SPACSTOR2TOPTOWER),
                                                    "Space Storm 2: Tower Base Sling Star")
    world.get_region(regname.SPACSTOR2TOPTOWERBASE).connect(world.get_region(regname.SPACSTOR2GSTAR2),
                                                            rule=RB.JumpHeight6|(RB.CanWallSpin))
    world.get_region(regname.SPACSTOR2TOPTOWER).connect(world.get_region(regname.SPACSTOR2COINROOM),
                                                    "Space Storm 2: Tower Green Pipe")
    world.get_region(regname.SPACSTOR2TOPTOWER).connect(world.get_region(regname.SPACSTOR2GSTAR2))
    # Boo Moon
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOOMOON), "World 5 Slot 2 Galaxy")
    world.get_region(regname.BOOMOON).connect(world.get_region(regname.BOOMOON1DARK), "Boo Moon Star 1")
    world.get_region(regname.BOOMOON1DARK).connect(world.get_region(regname.BOOMOON1GOOMBONUS),
                                                   "Boo Moon 1: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.BOOMOON1DARK).connect(world.get_region(regname.BOOMOON1POISON),
                                                   "Boo Moon 1: Dark Planet Launch Star")
    world.get_region(regname.BOOMOON1POISON).connect(world.get_region(regname.BOOMOON1MOON),
                                                   "Boo Moon 1: Poison Swamp Launch Star")
    world.get_region(regname.BOOMOON1MOON).connect(world.get_region(regname.BOOMOON1POPUP),
                                                   "Boo Moon 1: Moon Launch Star",
                                                   rule=RB.CanCollectStarChips&RB.JumpHeight3)
    world.get_region(regname.BOOMOON).connect(world.get_region(regname.BOOMOON2DARK), "Boo Moon Star 2")
    world.get_region(regname.BOOMOON2DARK).connect(world.get_region(regname.BOOMOON2GOOMBONUS),
                                                   "Boo Moon 2: Jack O'Gomba Bonus Teleporter")
    world.get_region(regname.BOOMOON2DARK).connect(world.get_region(regname.BOOMOON2TOWER),
                                                   "Boo Moon 2: Dark Planet Launch Star")
    # Upside Dizzy
    world.get_region(regname.WORLD5).connect(world.get_region(regname.UPDOWN), "World 5 Slot 3 Galaxy")
    world.get_region(regname.UPDOWN).connect(world.get_region(regname.UPDOWNCASTLE), "Upside Dizzy Castle")
    world.get_region(regname.UPDOWNCASTLE).connect(world.get_region(regname.UPDOWNINSIDE),
                                                   "Upside Dizzy: Castle Pipe")
    world.get_region(regname.UPDOWNINSIDE).connect(world.get_region(regname.UPDOWNFIRE),
                                                   "Upside Dizzy: 1st Green Pipe")
    world.get_region(regname.UPDOWNFIRE).connect(world.get_region(regname.UPDOWNBREAKER),
                                                   "Upside Dizzy: Fiery Orange Pipe")
    world.get_region(regname.UPDOWNINSIDE).connect(world.get_region(regname.UPDOWNGRAV),
                                                   "Upside Dizzy: Final Green Pipe")
    # Slipsand
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SLIPSAND), "World 5 Slot 4 Galaxy")
    world.get_region(regname.SLIPSAND).connect(world.get_region(regname.SLIPSAND1LONG), "Slipsand Star 1")
    world.get_region(regname.SLIPSAND1LONG).connect(world.get_region(regname.SLIPSAND1COINROOM),
                                                    "Slipsand 1: Green Pipe")
    world.get_region(regname.SLIPSAND1LONG).connect(world.get_region(regname.SLIPSAND1CUBE),
                                                    "Slipsand 1: Long Launch Star")
    world.get_region(regname.SLIPSAND1CUBE).connect(world.get_region(regname.SLIPSAND1SLIDE),
                                                    "Slipsand 1: Cube Launch Star")
    world.get_region(regname.SLIPSAND1SLIDE).connect(world.get_region(regname.SLIPSAND1BOSS),
                                                    "Slipsand 1: Slide Launch Star",
                                                     rule=RB.CanSlide)
    world.get_region(regname.SLIPSAND).connect(world.get_region(regname.SLIPSAND2LONG1), "Slipsand Star 2")
    world.get_region(regname.SLIPSAND2LONG1).connect(world.get_region(regname.SLIPSAND2GRAV),
                                                    "Slipsand 2: Green Pipe",
                                                     rule=RB.JumpHeight3)
    world.get_region(regname.SLIPSAND2LONG1).connect(world.get_region(regname.SLIPSAND2LONG2))
    world.get_region(regname.SLIPSAND2GRAV).connect(world.get_region(regname.SLIPSAND2LONG2),
                                                    "Slipsand 2: Orange Pipe")
    world.get_region(regname.SLIPSAND2LONG2).connect(world.get_region(regname.SLIPSAND2LONG3))
    world.get_region(regname.SLIPSAND2LONG2).connect(world.get_region(regname.SLIPSAND2BIRD),
                                                    "Slipsand 2: Long Launch Star")
    world.get_region(regname.SLIPSAND).connect(world.get_region(regname.SLIPSAND3BOSS), "Slipsand Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.SLIPSANDCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.SLIPSANDSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.SLIPSANDCM)
                                                           & CanReachLocation(locname.SLIPSANDSTAR1))))
                                               )
    # Fleet Glide
    world.get_region(regname.WORLD5).connect(world.get_region(regname.FLEETGLIDE), "World 5 Slot 5 Galaxy")
    world.get_region(regname.FLEETGLIDE).connect(world.get_region(regname.FLEETGLIDESTART))
    world.get_region(regname.FLEETGLIDESTART).connect(world.get_region(regname.FLEETGLIDECOURSE),
                                                      rule=RB.CanRideBird)
    #Shiverburn
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SHIVBURN), "World 5 Slot 6 Galaxy")
    world.get_region(regname.SHIVBURN).connect(world.get_region(regname.SHIVBURN1VOLCANO), "Shiverburn Star")
    world.get_region(regname.SHIVBURN1VOLCANO).connect(world.get_region(regname.SHIVBURN3CHIMP),
                                                       "Shiverburn: Green Pipe",
                                                       rule=RB.CanMakeCloud&RB.CanPound)
    world.get_region(regname.SHIVBURN1VOLCANO).connect(world.get_region(regname.SHIVBURN1LAVA),
                                                       "Shiverburn: Volcano Launch Star",
                                                       rule=RB.CanMakeCloud&RB.CanPound)
    world.get_region(regname.SHIVBURN1LAVA).connect(world.get_region(regname.SHIVBURN1FIREICE),
                                                       "Shiverburn: Lava Ball Launch Star")
    world.get_region(regname.SHIVBURN1FIREICE).connect(world.get_region(regname.SHIVBURN1TOAD),
                                                       "Shiverburn: Lava Ice Launch Star")
    world.get_region(regname.SHIVBURN1TOAD).connect(world.get_region(regname.SHIVBURN1BOSS),
                                                       "Shiverburn: Green Toadship Launch Star")
    world.get_region(regname.SHIVBURN).connect(world.get_region(regname.SHIVBURN2TOAD), "Shiverburn Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.ROMPCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.COLDFIRECM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.COLDFIRESTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.COLDFIRECM)
                                                           & CanReachLocation(locname.COLDFIRESTAR1))))
                                               )
    world.get_region(regname.SHIVBURN2TOAD).connect(world.get_region(regname.SHIVBURN2ROMP),
                                                       "Shiverburn Comet: Green Toadship Launch Star")
    # Boom bunker
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOWJR3), "World 5 Slot 7 Galaxy")
    world.get_region(regname.BOWJR3).connect(world.get_region(regname.BOOMBUNK1HAMMER), "Boom Bunker Grand Star")
    world.get_region(regname.BOOMBUNK1HAMMER).connect(world.get_region(regname.BOOMBUNK1BOOMER),
                                                      "Boom Bunker: Hammer Hilt Cannon",
                                                      rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK1BOOMER).connect(world.get_region(regname.BOOMBUNK1CHECK),
                                                      "Boom Bunker: Fort Launch Star")
    world.get_region(regname.BOOMBUNK1CHECK).connect(world.get_region(regname.BOOMBUNK1PLAT),
                                                      "Boom Bunker: Checkpoint Cannon",
                                                     rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK1PLAT).connect(world.get_region(regname.BOOMBUNK1BOSS),
                                                      "Boom Bunker: Platform Launch Star",
                                                    rule=RB.CanPound)
    world.get_region(regname.BOWJR3).connect(world.get_region(regname.BOOMBUNK2HAMMER), "Boom Bunker Comet Star",
                                             rule=((RB.Comet1ItemAccess | (
                                                         OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                   & (RB.CometMissionOff
                                                      | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                 locname.BOOMBUNKCM))
                                                      | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                 locname.BOOMBUNKSTAR1))
                                                      | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                 locname.BOOMBUNKCM)
                                                         & CanReachLocation(locname.BOOMBUNKSTAR1))))
                                             )
    world.get_region(regname.BOOMBUNK2HAMMER).connect(world.get_region(regname.BOOMBUNK2BOOMER),
                                                      "Boom Bunker Comet: Hammer Hilt Cannon",
                                                      rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK2BOOMER).connect(world.get_region(regname.BOOMBUNK2CHECK),
                                                      "Boom Bunker Comet: Fort Launch Star")
    world.get_region(regname.BOOMBUNK2CHECK).connect(world.get_region(regname.BOOMBUNK2DARK),
                                                      "Boom Bunker Comet: Checkpoint Cannon")
    world.get_region(regname.BOOMBUNK2DARK).connect(world.get_region(regname.BOOMBUNK2BOSS),
                                                      "Boom Bunker Comet: Dark Matter Launch Star",
                                                    rule=RB.CanMakeCloud)
    # World 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD6), "World 6 Map",
                                           rule=(Has(itemname.GRAND, 5)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND6) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Melty Monster
    world.get_region(regname.WORLD6).connect(world.get_region(regname.MELTY), "World 6 Slot 1 Galaxy")
    world.get_region(regname.MELTY).connect(world.get_region(regname.MELTY1LANDING), "Melty Monster Star 1")
    world.get_region(regname.MELTY1LANDING).connect(world.get_region(regname.MELTY3CHIMP),
                                                    "Melty Monster 1: Green Pipe")
    world.get_region(regname.MELTY1LANDING).connect(world.get_region(regname.MELTY1MAGMAARG),
                                                    "Melty Monster 1: Pull Star Path")
    world.get_region(regname.MELTY1MAGMAARG).connect(world.get_region(regname.MELTY1LAVAWAVE1),
                                                    "Melty Monster 1: Magmaargh Launch Star")
    world.get_region(regname.MELTY1LAVAWAVE1).connect(world.get_region(regname.MELTY1LAVAWAVE2),
                                                      rule=(RB.CanClimbPole | RB.MediumLogic))
    world.get_region(regname.MELTY1LAVAWAVE2).connect(world.get_region(regname.MELTY1LAVAWAVE3))
    world.get_region(regname.MELTY1LAVAWAVE3).connect(world.get_region(regname.MELTY1MAGMAW),
                                                      "Melty Monster 1: Lava Wave Launch Star",
                                                      rule=RB.CanSwing)
    world.get_region(regname.MELTY).connect(world.get_region(regname.MELTY2LANDING), "Melty Monster Star 2")
    world.get_region(regname.MELTY2LANDING).connect(world.get_region(regname.MELTY3CHIMP),
                                                    "Melty Monster 2: Green Pipe")
    world.get_region(regname.MELTY2LANDING).connect(world.get_region(regname.MELTY2BOWLING),
                                                    "Melty Monster 2: Roll to Launch Star",
                                                    rule=RB.ROCKNROLLIN)
    # Clockwork Ruins
    world.get_region(regname.WORLD6).connect(world.get_region(regname.CLOCKWORK), "World 6 Slot 2 Galaxy")
    world.get_region(regname.CLOCKWORK).connect(world.get_region(regname.CLOCKWORK1COGS), "Clockwork Ruins Star")
    world.get_region(regname.CLOCKWORK1COGS).connect(world.get_region(regname.CLOCKWORK1PUSH),
                                                     "Clockwork Ruins: Cog Wall Launch Star")
    world.get_region(regname.CLOCKWORK1PUSH).connect(world.get_region(regname.CLOCKWORK1WHEELSB),
                                                     "Clockwork Ruins: Push Block Launch Star",
                                                     rule=RB.CanPound)
    world.get_region(regname.CLOCKWORK1WHEELSB).connect(world.get_region(regname.CLOCKWORK1WHEELST),
                                                        rule=(RB.CanWallJump))
    world.get_region(regname.CLOCKWORK1WHEELST).connect(world.get_region(regname.CLOCKWORK1COINROOM),
                                                     "Clockwork Ruins: Wheel Planet Green Pipe")
    world.get_region(regname.CLOCKWORK1COGS).connect(world.get_region(regname.CLOCKWORK3HAMMER),
                                                     "Clockwork Ruins: Hungry Luma",
                                                     rule=((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL6)))
                                                     &(True_() if world.options.coin_luma_counts.value["Clockwork Ruins Coin Luma"]<100
                                                       else Has("Can Farm Coins"))))
    world.get_region(regname.CLOCKWORK3HAMMER).connect(world.get_region(regname.CLOCKWORK3HAMMERTOP),
                                                     "Clockwork Ruins Hungry Luma: Hammer Zone Green Pipe")
    world.get_region(regname.CLOCKWORK).connect(world.get_region(regname.CLOCKWORK2COGS), "Clockwork Ruins Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.CLOCKRUINSCM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.CLOCKRUINSTAR1))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.CLOCKRUINSCM)
                                                            & CanReachLocation(locname.CLOCKRUINSTAR1))))
                                                )
    # Flash Black
    world.get_region(regname.WORLD6).connect(world.get_region(regname.FLASHBLACK), "World 6 Slot 3 Galaxy")
    world.get_region(regname.FLASHBLACK).connect(world.get_region(regname.FLASHBLACK1TOWER), "Flash Black Star")
    world.get_region(regname.FLASHBLACK1TOWER).connect(world.get_region(regname.FLASHBLACK1PATH),
                                                       "Flash Black: Tower Launch Star",
                                                       rule=RB.CanDinoBlimp)
    world.get_region(regname.FLASHBLACK).connect(world.get_region(regname.FLASHBLACK2PATH), "Flash Black Comet Star",
                                                 rule=((RB.Comet1ItemAccess | (
                                                             OptionFilter(CometItems, 2) & Has(itemname.ROMPCOMET)))
                                                       & (RB.CometMissionOff
                                                          | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                     locname.FLASHBLACKCM))
                                                          | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                     locname.FLASHBLACKSTAR1))
                                                          | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                     locname.FLASHBLACKCM)
                                                             & CanReachLocation(locname.FLASHBLACKSTAR1))))
                                                 )
    # Throwback
    world.get_region(regname.WORLD6).connect(world.get_region(regname.WHOMPFORT), "World 6 Slot 4 Galaxy")
    world.get_region(regname.WHOMPFORT).connect(world.get_region(regname.WHOMP1FORT), "Throwback Star 1")
    world.get_region(regname.WHOMP1FORT).connect(world.get_region(regname.WHOMP1BONUS),
                                                 "Throwback 1: Piranha Bonus Teleporter")
    world.get_region(regname.WHOMP1FORT).connect(world.get_region(regname.WHOMP1UNDER),
                                                 rule=RB.CanPound)
    world.get_region(regname.WHOMPFORT).connect(world.get_region(regname.WHOMP2FORT), "Throwback Star 2")
    world.get_region(regname.WHOMP2FORT).connect(world.get_region(regname.WHOMP2BONUS),
                                                 "Throwback 2: Piranha Bonus Teleporter")
    world.get_region(regname.WHOMPFORT).connect(world.get_region(regname.WHOMP3FORT), "Throwback Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.THROWBACKCM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.THROWBACKSTAR2))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.THROWBACKCM)
                                                            & CanReachLocation(locname.THROWBACKSTAR2))))
                                                )
    # Slimy Spring
    world.get_region(regname.WORLD6).connect(world.get_region(regname.SLIMSPRI), "World 6 Slot 5 Galaxy")
    world.get_region(regname.SLIMSPRI).connect(world.get_region(regname.SLIMSPRI1MOUTH1), "Slimy Spring Star")
    world.get_region(regname.SLIMSPRI1MOUTH1).connect(world.get_region(regname.SLIMSPRI1CAVE1),
                                                      rule=RB.CanSwim&RB.CanSlide)
    world.get_region(regname.SLIMSPRI1MOUTH1).connect(world.get_region(regname.SLIMSPRI1CHESTROOM),
                                                      "Slimy Spring: Green Pipe")
    world.get_region(regname.SLIMSPRI1CAVE1).connect(world.get_region(regname.SLIMSPRI1MOUTH2),
                                                     "Slimy Spring: First Cave Launch Star",
                                                     rule=(RB.CanSwim & (RB.CanShell | RB.HardLogic)))
    world.get_region(regname.SLIMSPRI1MOUTH2).connect(world.get_region(regname.SLIMSPRI1CAVE2),
                                                      rule=RB.CanSwim)
    world.get_region(regname.SLIMSPRI).connect(world.get_region(regname.SLIMSPRI2MOUTH1), "Slimy Spring Chimp Star")
    world.get_region(regname.SLIMSPRI2MOUTH1).connect(world.get_region(regname.SLIMSPRI2CAVE1),
                                                      rule=RB.CanSwim&RB.CanSlide)
    world.get_region(regname.SLIMSPRI2CAVE1).connect(world.get_region(regname.SLIMSPRI2MOUTH2),
                                                     "Slimy Spring Chimp: First Cave Launch Star",
                                                     rule=(RB.CanSwim & (RB.CanShell | RB.HardLogic)))
    world.get_region(regname.SLIMSPRI2MOUTH2).connect(world.get_region(regname.SLIMSPRI2CAVE2),
                                                      rule=RB.CanSwim)
    # Battle Belt
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BATTLEBELT), "World 6 Slot 6 Galaxy")
    world.get_region(regname.BATTLEBELT).connect(world.get_region(regname.BATTBELT1GOOM), "Battle Belt Star")
    world.get_region(regname.BATTBELT1GOOM).connect(world.get_region(regname.BATTBELT1LAVA),
                                                    "Battle Belt: Goomba Sling Star")
    world.get_region(regname.BATTBELT1LAVA).connect(world.get_region(regname.BATTBELT1URCH),
                                                    "Battle Belt: Li'l Cinders Sling Star")
    world.get_region(regname.BATTBELT1URCH).connect(world.get_region(regname.BATTBELT1CRAB),
                                                    "Battle Belt: Urchin Sling Star",
                                                    rule=(RB.FireMario | (RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.BATTBELT1CRAB).connect(world.get_region(regname.BATTBELT1PTOA),
                                                    "Battle Belt: Crabber Sling Star")
    world.get_region(regname.BATTBELT1PTOA).connect(world.get_region(regname.BATTBELT1PUMP),
                                                    "Battle Belt: Pink Toadship Sling Star")
    world.get_region(regname.BATTBELT1PUMP).connect(world.get_region(regname.BATTBELT1PUMI),
                                                    "Battle Belt: Jack O'Goomba Green Pipe")
    world.get_region(regname.BATTBELT1PUMP).connect(world.get_region(regname.BATTBELT1RTOA),
                                                    "Battle Belt: Jack O'Goomba Sling Star",
                                                    rule=(RB.CanShell & RB.CanSwim))
    world.get_region(regname.BATTBELT1RTOA).connect(world.get_region(regname.BATTBELT1ICEP),
                                                    "Battle Belt: Red Toadship Sling Star")
    world.get_region(regname.BATTBELT1ICEP).connect(world.get_region(regname.BATTBELT3BOSS),
                                                    "Battle Belt: Hungry Luma",
                                                    rule=((RB.CoinLumaBase |
                                                           (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL7)))
                                                          & (True_() if world.options.coin_luma_counts.value[
                                                                            "Battle Belt Coin Luma"] < 100
                                                             else Has("Can Farm Coins"))))
    world.get_region(regname.BATTBELT1ICEP).connect(world.get_region(regname.BATTBELT1MOLE),
                                                    "Battle Belt: Li'l Brr Sling Star")
    world.get_region(regname.BATTBELT1MOLE).connect(world.get_region(regname.BATTBELT1MOLI),
                                                    "Battle Belt: Swapphopper Green Pipe",
                                                    rule=RB.CanPound)
    world.get_region(regname.BATTBELT1MOLE).connect(world.get_region(regname.BATTBELT1CHOM),
                                                    "Battle Belt: Swaphopper Sling Star",
                                                    rule=RB.CanPound)
    world.get_region(regname.BATTLEBELT).connect(world.get_region(regname.BATTBELT2GOOM), "Battle Belt Comet Star",
                                                 rule=((RB.Comet1ItemAccess | (
                                                             OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                       & (RB.CometMissionOff
                                                          | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                     locname.BATTBELTCM))
                                                          | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                     locname.BATTBELTSTAR1))
                                                          | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                     locname.BATTBELTCM)
                                                             & CanReachLocation(locname.BATTBELTSTAR1))))
                                                 )
    world.get_region(regname.BATTBELT2GOOM).connect(world.get_region(regname.BATTBELT2LAVA),
                                                    "Battle Belt Comet: Goomba Sling Star")
    world.get_region(regname.BATTBELT2LAVA).connect(world.get_region(regname.BATTBELT2URCH),
                                                    "Battle Belt Comet: Li'l Cinders Sling Star")
    world.get_region(regname.BATTBELT2URCH).connect(world.get_region(regname.BATTBELT2CRAB),
                                                    "Battle Belt Comet: Urchin Sling Star",
                                                    rule=(RB.FireMario | (RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.BATTBELT2CRAB).connect(world.get_region(regname.BATTBELT2PTOA),
                                                    "Battle Belt Comet: Crab Sling Star")
    world.get_region(regname.BATTBELT2PTOA).connect(world.get_region(regname.BATTBELT2PUMP),
                                                    "Battle Belt Comet: Yellow Toadship Sling Star")
    world.get_region(regname.BATTBELT2PUMP).connect(world.get_region(regname.BATTBELT2PUMI),
                                                    "Battle Belt Comet: Jack O'Goomba Green Pipe")
    world.get_region(regname.BATTBELT2PUMP).connect(world.get_region(regname.BATTBELT2RTOA),
                                                    "Battle Belt Comet: Jack O'Goomba Sling Star",
                                                    rule=(RB.CanShell & RB.CanSwim))
    world.get_region(regname.BATTBELT2RTOA).connect(world.get_region(regname.BATTBELT2ICEP),
                                                    "Battle Belt Comet: Red Toadship Sling Star")
    world.get_region(regname.BATTBELT2ICEP).connect(world.get_region(regname.BATTBELT2MOLE),
                                                    "Battle Belt Comet: Li'l Brr Sling Star")
    world.get_region(regname.BATTBELT2MOLE).connect(world.get_region(regname.BATTBELT2MOLI),
                                                    "Battle Belt Comet: Swaphopper Green Pipe",
                                                    rule=RB.CanPound)
    world.get_region(regname.BATTBELT2MOLE).connect(world.get_region(regname.BATTBELT2CHOM),
                                                    "Battle Belt Comet: Swaphopper Sling Star",
                                                    rule=RB.CanPound)
    # Galaxy Generator
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BOWSER3), "World 6 Slot 7 Galaxy")
    world.get_region(regname.BOWSER3).connect(world.get_region(regname.GALGEN1LANDING), "Galaxy Generator Grand Star")
    world.get_region(regname.GALGEN1LANDING).connect(world.get_region(regname.GALGEN1HAMMER),
                                                     "Galaxy Generator: Landing Launch Star")
    world.get_region(regname.GALGEN1HAMMER).connect(world.get_region(regname.GALGEN1VOLCANO))
    world.get_region(regname.GALGEN1VOLCANO).connect(world.get_region(regname.GALGEN1LAVACYL))
    world.get_region(regname.GALGEN1LAVACYL).connect(world.get_region(regname.GALGEN1TOWER),
                                                     "Galaxy Generator: Lava Cylinder Launch Star",
                                                     rule=RB.DRILLMASTER)
    world.get_region(regname.GALGEN1TOWER).connect(world.get_region(regname.GALGEN1YOSHI),
                                                     "Galaxy Generator: Tower Launch Star",
                                                   rule=(RB.CanMakeCloud | RB.CanWallSpin | RB.CanLongSpin
                                                         | (RB.CanAirSpin & RB.MediumLogic)))
    world.get_region(regname.GALGEN1YOSHI).connect(world.get_region(regname.GALGEN1DASHCAS),
                                                   rule=(RB.CanDinoSwing
                                                         | (RB.CanMakeCloud & CanLongJump & RB.CanWallJump & RB.HardLogic)))
    world.get_region(regname.GALGEN1DASHCAS).connect(world.get_region(regname.GALGEN1LAVASNA),
                                                     "Galaxy Generator: Dash Castle Sling Star",
                                                     rule=(RB.CanDinoRun
                                                           | (RB.CanMakeCloud & RB.CanLongJump & RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.GALGEN1LAVASNA).connect(world.get_region(regname.GALGEN1STATUE))
    world.get_region(regname.GALGEN1STATUE).connect(world.get_region(regname.GALGEN1THEDOOR),
                                                    rule=RB.CanClimbPole)
    world.get_region(regname.GALGEN1YOSHI).connect(world.get_region(regname.GALGEN1THEDOOR),
                                                   rule=RB.CanInfiniteFlutter&RB.CanAirSpin&RB.CanSideflip) #Trick Entrance
    world.get_region(regname.GALGEN1THEDOOR).connect(world.get_region(regname.GALGEN1BOSS),
                                                     "Galaxy Generator: The Door")
    world.get_region(regname.BOWSER3).connect(world.get_region(regname.GALGEN2LANDING), "Galaxy Generator Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.GLXYGENCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.GALAXYGENSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.GLXYGENCM)
                                                          & CanReachLocation(locname.GALAXYGENSTAR1))))
                                              )
    world.get_region(regname.GALGEN2LANDING).connect(world.get_region(regname.GALGEN2BOOMER),
                                                     "Galaxy Generator Comet: Landing Sling Star")
    world.get_region(regname.GALGEN2BOOMER).connect(world.get_region(regname.GALGEN2VOLCANO))
    world.get_region(regname.GALGEN2VOLCANO).connect(world.get_region(regname.GALGEN2LAVACYL))
    world.get_region(regname.GALGEN2LAVACYL).connect(world.get_region(regname.GALGEN2TOWER),
                                                     "Galaxy Generator Comet: Lava Cylinder Launch Star",
                                                     rule=RB.DRILLMASTER)
    world.get_region(regname.GALGEN2TOWER).connect(world.get_region(regname.GALGEN2YOSHI),
                                                   "Galaxy Generator Comet: Tower Launch Star",
                                                   rule=(RB.CanMakeCloud | RB.CanWallSpin | RB.CanLongSpin
                                                         | (RB.CanAirSpin & RB.MediumLogic)))
    world.get_region(regname.GALGEN2YOSHI).connect(world.get_region(regname.GALGEN2DASHCAS),
                                                   rule=(RB.CanDinoSwing
                                                         | (RB.CanMakeCloud & CanLongJump & RB.CanWallJump & RB.HellLogic))
                                                   )
    world.get_region(regname.GALGEN2DASHCAS).connect(world.get_region(regname.GALGEN2LAVASNA),
                                                     "Galaxy Generator Comet: Dash Castle Sling Star",
                                                     rule=(RB.CanDinoRun
                                                           | (RB.CanMakeCloud & RB.CanLongJump & RB.JumpHeight6 & RB.HellLogic))
                                                     )
    world.get_region(regname.GALGEN2LAVASNA).connect(world.get_region(regname.GALGEN2STATUE))
    # World 7
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD7), "World S Map",
                                           rule=(Has(itemname.GRAND, 6)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND7) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Mario Squared
    world.get_region(regname.WORLD7).connect(world.get_region(regname.MARIO), "World 7 Slot 1 Galaxy")
    world.get_region(regname.MARIO).connect(world.get_region(regname.MARIOSQ1RIGHT), "Mario Squared Star")
    world.get_region(regname.MARIOSQ1RIGHT).connect(world.get_region(regname.MARIOSQ1MAIN))
    world.get_region(regname.MARIOSQ1MAIN).connect(world.get_region(regname.MARIOSQ1LEFT))
    world.get_region(regname.MARIO).connect(world.get_region(regname.MARIOSQ2LEFT), "Mario Squared Comet Star",
                                            rule=((RB.Comet1ItemAccess | (
                                                        OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                  & (RB.CometMissionOff
                                                     | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                locname.MARIOSQRCM))
                                                     | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                locname.MARIOSQRSTAR1))
                                                     | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                locname.MARIOSQRCM)
                                                        & CanReachLocation(locname.MARIOSQRSTAR1))))
                                            )
    world.get_region(regname.MARIOSQ2LEFT).connect(world.get_region(regname.MARIOSQ2MAIN))
    world.get_region(regname.MARIOSQ2MAIN).connect(world.get_region(regname.MARIOSQ2RIGHT))
    # Rolling Coaster
    world.get_region(regname.WORLD7).connect(world.get_region(regname.ROLLCOAST), "World 7 Slot 2 Galaxy")
    world.get_region(regname.ROLLCOAST).connect(world.get_region(regname.ROLLCOAST1), "Rolling Coaster Star")
    world.get_region(regname.ROLLCOAST).connect(world.get_region(regname.ROLLCOAST2), "Rolling Coaster Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.PURPLECOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.ROLLSLIDECM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.ROLLSLIDESTAR1))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.ROLLSLIDECM)
                                                            & CanReachLocation(locname.ROLLSLIDESTAR1))))
                                                )
    # Twisty Trials
    world.get_region(regname.WORLD7).connect(world.get_region(regname.TWISTTRI), "World 7 Slot 3 Galaxy")
    world.get_region(regname.TWISTTRI).connect(world.get_region(regname.TWISTY1PLAT1), "Twisty Trials Star")
    world.get_region(regname.TWISTY1PLAT1).connect(world.get_region(regname.TWISTY1PLAT2),
                                                   rule=(RB.CanLongJump | RB.CanAirSpin | RB.MediumLogic ))
    world.get_region(regname.TWISTY1PLAT2).connect(world.get_region(regname.TWISTY1PLAT3),
                                                   rule=((RB.CanAirSpin & RB.CanRideDino)
                                                         | RB.MediumLogic)
                                                   )
    world.get_region(regname.TWISTY1PLAT3).connect(world.get_region(regname.TWISTY1PLAT4))
    world.get_region(regname.TWISTTRI).connect(world.get_region(regname.TWISTY2PLAT1), "Twisty Trials Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.DOUBLETIME)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.TWISTTRIALCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.TWISTTRIALSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.TWISTTRIALCM)
                                                           & CanReachLocation(locname.TWISTTRIALSTAR1))))
                                               )
    world.get_region(regname.TWISTY2PLAT1).connect(world.get_region(regname.TWISTY2PLAT2),
                                                   rule=(RB.CanLongJump | RB.CanAirSpin | RB.MediumLogic))
    world.get_region(regname.TWISTY2PLAT2).connect(world.get_region(regname.TWISTY2PLAT3),
                                                   rule=((RB.CanAirSpin&RB.CanRideDino)
                                                         | RB.MediumLogic))
    world.get_region(regname.TWISTY2PLAT3).connect(world.get_region(regname.TWISTY2PLAT4))
    # Stone Cyclone
    world.get_region(regname.WORLD7).connect(world.get_region(regname.STONECYC), "World 7 Slot 4 Galaxy")
    world.get_region(regname.STONECYC).connect(world.get_region(regname.STONECYC1), "Stone Cyclone Star")
    world.get_region(regname.STONECYC).connect(world.get_region(regname.STONECYC2), "Stone Cyclone Comet Star",
                                               rule=((RB.Comet1ItemAccess | (
                                                           OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                     & (RB.CometMissionOff
                                                        | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                   locname.STONECYCLOCM))
                                                        | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                   locname.STONECYCLOSTAR1))
                                                        | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                   locname.STONECYCLOCM)
                                                           & CanReachLocation(locname.STONECYCLOSTAR1))))
                                               )
    # Boss Blitz
    world.get_region(regname.WORLD7).connect(world.get_region(regname.BOSSBLITZ), "World 7 Slot 5 Galaxy")
    world.get_region(regname.BOSSBLITZ).connect(world.get_region(regname.BOSSBLITZ1DINOPIR), "Boss Blitz Star")
    world.get_region(regname.BOSSBLITZ1DINOPIR).connect(world.get_region(regname.BOSSBLITZ1KINGKAL),
                                                        "Boss Blitz: Dino Piranha Launch Star")
    world.get_region(regname.BOSSBLITZ1KINGKAL).connect(world.get_region(regname.BOSSBLITZ1MAJORBU),
                                                        "Boss Blitz: King Kaliente Launch Star")
    world.get_region(regname.BOSSBLITZ1MAJORBU).connect(world.get_region(regname.BOSSBLITZ1BOULDER),
                                                        "Boss Blitz: Major Burrows Launch Star",
                                                        rule=RB.CanPound)
    world.get_region(regname.BOSSBLITZ1BOULDER).connect(world.get_region(regname.BOSSBLITZ1TINYMET),
                                                        "Boss Blitz: Bouldergeist Launch Star")
    world.get_region(regname.BOSSBLITZ1TINYMET).connect(world.get_region(regname.BOSSBLITZ1FIREDIN),
                                                        "Boss Blitz: Tiny Meteor Launch Star")
    world.get_region(regname.BOSSBLITZ).connect(world.get_region(regname.BOSSBLITZ2DINOPIR), "Boss Blitz Comet Star",
                                                rule=((RB.Comet1ItemAccess | (
                                                            OptionFilter(CometItems, 2) & Has(itemname.SPEEDYCOMET)))
                                                      & (RB.CometMissionOff
                                                         | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                    locname.BOSSBLITCM))
                                                         | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                    locname.BOSSBLITSTAR1))
                                                         | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                    locname.BOSSBLITCM)
                                                            & CanReachLocation(locname.BOSSBLITSTAR1))))
                                                )
    world.get_region(regname.BOSSBLITZ2DINOPIR).connect(world.get_region(regname.BOSSBLITZ2KINGKAL),
                                                        "Boss Blitz Comet: Dino Piranha Launch Star")
    world.get_region(regname.BOSSBLITZ2KINGKAL).connect(world.get_region(regname.BOSSBLITZ2MAJORBU),
                                                        "Boss Blitz Comet: King Kaliente Launch Star")
    world.get_region(regname.BOSSBLITZ2MAJORBU).connect(world.get_region(regname.BOSSBLITZ2BOULDER),
                                                        "Boss Blitz Comet: Major Burrows Launch Star",
                                                        rule=RB.CanPound)
    world.get_region(regname.BOSSBLITZ2BOULDER).connect(world.get_region(regname.BOSSBLITZ2TINYMET),
                                                        "Boss Blitz Comet: Bouldergeist Launch Star")
    world.get_region(regname.BOSSBLITZ2TINYMET).connect(world.get_region(regname.BOSSBLITZ2FIREDIN),
                                                        "Boss Blitz Comet: Tiny Meteor Launch Star")
    # Flipout
    world.get_region(regname.WORLD7).connect(world.get_region(regname.FLIPOUT), "World 7 Slot 6 Galaxy")
    world.get_region(regname.FLIPOUT).connect(world.get_region(regname.FLIPOUT1LANDING), "Flip-Out Star")
    world.get_region(regname.FLIPOUT1LANDING).connect(world.get_region(regname.FLIPOUT1CLIMB), "Flip-Out: Green Pipe")
    world.get_region(regname.FLIPOUT).connect(world.get_region(regname.FLIPOUT2LANDING), "Flip-Out Comet Star",
                                              rule=((RB.Comet1ItemAccess | (
                                                          OptionFilter(CometItems, 2) & Has(itemname.COSMICCLONE)))
                                                    & (RB.CometMissionOff
                                                       | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                  locname.FLIPOUTCM))
                                                       | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                  locname.FLIPOUTSTAR1))
                                                       | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                  locname.FLIPOUTCM)
                                                          & CanReachLocation(locname.FLIPOUTSTAR1))))
                                              )
    world.get_region(regname.FLIPOUT2LANDING).connect(world.get_region(regname.FLIPOUT2CLIMB), "Flip-Out Comet: Green Pipe")
    # Grandmaster
    world.get_region(regname.WORLD7).connect(world.get_region(regname.GRANDMASTER), "World 7 Slot 7 Galaxy")
    world.get_region(regname.GRANDMASTER).connect(world.get_region(regname.GRANDMASTER1YOSHI), "Grandmaster Star")
    world.get_region(regname.GRANDMASTER1YOSHI).connect(world.get_region(regname.GRANDMASTER1SWITCH),
                                                        "Grandmaster: Yoshi Flower Launch Star",
                                                        rule=RB.CanDinoSwing)
    world.get_region(regname.GRANDMASTER1SWITCH).connect(world.get_region(regname.GRANDMASTER1CLOUD),
                                                        "Grandmaster: Flipswitch Launch Star"),
    world.get_region(regname.GRANDMASTER1CLOUD).connect(world.get_region(regname.GRANDMASTER1SWAP),
                                                        "Grandmaster: Electric Clouds Launch Star",
                                                        rule=RB.CanMakeCloud)
    world.get_region(regname.GRANDMASTER1SWAP).connect(world.get_region(regname.GRANDMASTER1PULL),
                                                        "Grandmaster: Flip-Swap Launch Star",
                                                       rule=(RB.JumpHeight4 | RB.MediumLogic))
    world.get_region(regname.GRANDMASTER1PULL).connect(world.get_region(regname.GRANDMASTER1BROS1),
                                                        "Grandmaster: Pull Star Launch Star")
    world.get_region(regname.GRANDMASTER1BROS1).connect(world.get_region(regname.GRANDMASTER1BROS2),
                                                        "Grandmaster: Bros Landing Sling Star")
    world.get_region(regname.GRANDMASTER).connect(world.get_region(regname.GRANDMASTER2YOSHI), "Grandmaster Star Comet",
                                                  rule=((RB.Comet1ItemAccess | (
                                                              OptionFilter(CometItems, 2) & Has(itemname.DAREDEVILCOMET)))
                                                        & (RB.CometMissionOff
                                                           | (OptionFilter(CometMission, 1) & CanReachLocation(
                                                                      locname.GRANDMASTRCM))
                                                           | (OptionFilter(CometMission, 2) & CanReachLocation(
                                                                      locname.GRANDMASTSTAR1))
                                                           | (OptionFilter(CometMission, 3) & CanReachLocation(
                                                                      locname.GRANDMASTRCM)
                                                              & CanReachLocation(locname.GRANDMASTSTAR1))))
                                                  )
    world.get_region(regname.GRANDMASTER2YOSHI).connect(world.get_region(regname.GRANDMASTER2SWITCH),
                                                        "Grandmaster Comet: Yoshi Flower Launch Star",
                                                        rule=RB.CanDinoSwing)
    world.get_region(regname.GRANDMASTER2SWITCH).connect(world.get_region(regname.GRANDMASTER2CLOUD),
                                                        "Grandmaster Comet: Flipswitch Launch Star")
    world.get_region(regname.GRANDMASTER2CLOUD).connect(world.get_region(regname.GRANDMASTER2SWAP),
                                                        "Grandmaster Comet: Electric Clouds Launch Star",
                                                         rule=RB.CanMakeCloud)
    world.get_region(regname.GRANDMASTER2SWAP).connect(world.get_region(regname.GRANDMASTER2PULL),
                                                        "Grandmaster Comet: Flip-Swap Launch Star",
                                                       rule=(RB.JumpHeight4 | RB.MediumLogic))
    world.get_region(regname.GRANDMASTER2PULL).connect(world.get_region(regname.GRANDMASTER2BROS1),
                                                        "Grandmaster Comet: Pull Star Launch Star")
    world.get_region(regname.GRANDMASTER2BROS1).connect(world.get_region(regname.GRANDMASTER2BROS2),
                                                        "Grandmaster Comet: Bros Landing Sling Star")
    world.get_region(regname.GRANDMASTER2BROS2).connect(world.get_region(regname.GRANDMASTER2ROSA),
                                                        "Grandmaster Comet: Jumping Bros Launch Star")


    world.get_region(regname.SHIP).connect(world.get_region(regname.SHIP2)),
    world.get_region(regname.SHIP2).connect(world.get_region(regname.SHIPINSIDE)),
    world.set_completion_rule(Has("Peach"))
