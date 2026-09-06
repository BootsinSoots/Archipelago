from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import True_, Has, CanReachLocation, CanReachEntrance
from .Rules import CanLongJump, ROCKNROLLIN, CanSwim

if TYPE_CHECKING:
    from . import SMG2World
from .Constants.Names import region_names as regname, item_names as itemname, location_names as locname
from .SMG2Options import WorldShuffle, CoinLumaLocks, CometItems, CometMission, PowerupRando
from . import Rules as RB


def set_rules(world: "SMG2World", player: int):
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
                                                          "Sky Station 1: House Green Pipe",
                                                          rule=RB.CanPipe | RB.CanLongJump | RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE),
                                                          rule=(RB.JumpHeight6 | RB.CanWallSpin
                                                                | (RB.CanGrabLedge & RB.CanAirSpin & RB.CanBackOrSideflip)
                                                                | (RB.CanTriple & RB.CanWallJump & RB.HardLogic)))
    world.get_region(regname.SKYOBS1STARTBOTTOM).connect(world.get_region(regname.SKYOBS1TOPOFHOUSE))
    world.get_region(regname.SKYOBS1STARTTOPSIDE).connect(world.get_region(regname.SKYOBS1GSTAR1),
                                                          rule=((RB.JumpHeight3 & RB.CanWallJump) | RB.JumpHeight4))
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GSTAR1))
    world.get_region(regname.SKYOBS1TOPOFHOUSE).connect(world.get_region(regname.SKYOBS1GREENHILL),
                                                        "Sky Station 1: House Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1OCTOBONUS),
                                                       "Sky Station 1: Green Hill Teleporter",)
    world.get_region(regname.SKYOBS1GREENHILL).connect(world.get_region(regname.SKYOBS1MINIPLANETS),
                                                       "Sky Station 1: Green Hill Launch Star",
                                                       rule=RB.CanLaunchStar | (RB.CanHomingPound & RB.HellLogic))
    world.get_region(regname.SKYOBS1MINIPLANETS).connect(world.get_region(regname.SKYOBS1CYLINDER),
                                                       "Sky Station 1: Mini Planets Launch Star",
                                                         rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS1CYLINDER).connect(world.get_region(regname.SKYOBS1BEFOREBOSS),
                                                       "Sky Station 1: Cylinder Launch Star",
                                                      rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS1BEFOREBOSS).connect(world.get_region(regname.SKYOBS1BOSS),
                                                       "Sky Station 1: Two-Sided Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS2STARTTOPSIDE), "Sky Station Star 2")
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2STARTBOTTOM),
                                                          "Sky Station 2: House Green Pipe",
                                                          rule=RB.CanPipe | RB.CanLongJump | RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS2STARTTOPSIDE).connect(world.get_region(regname.SKYOBS2TOPOFHOUSE),
                                                          rule=(RB.JumpHeight6 | RB.CanWallSpin
                                                                | (RB.CanGrabLedge & RB.CanAirSpin & RB.CanBackOrSideflip)
                                                                | (RB.CanTriple & RB.CanWallJump & RB.MediumLogic)))
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.SKYOBS2SKYFLEET),
                                                        "Sky Station 2: House Launch Star",
                                                         rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2OCTOBONUS),
                                                      "Sky Station 2: Sky Fleet Teleporter")
    world.get_region(regname.SKYOBS2SKYFLEET).connect(world.get_region(regname.SKYOBS2FLIPSWITCH),
                                                      "Sky Station 2: Sky Fleet Launch Star",
                                                      rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS2FLIPSWITCH).connect(world.get_region(regname.SKYOBS2GRASSFLEET),
                                                        "Sky Station 2: Flipswitch Fleet Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS).connect(world.get_region(regname.SKYOBS3STARTTOPSIDE), "Sky Station Comet Star",
                                             rule=((RB.Comet1ItemAccess|(OptionFilter(CometItems, 2)&Has(itemname.SPEEDYCOMET)))
                                                   &(RB.CometMissionOff
                                                     |(OptionFilter(CometMission, 1)&CanReachLocation(locname.SKYSTACM))
                                                     |(OptionFilter(CometMission, 2)&CanReachLocation(locname.SKYSTASTAR1))
                                                     |(OptionFilter(CometMission, 3)&CanReachLocation(locname.SKYSTACM)
                                                       &CanReachLocation(locname.SKYSTASTAR1)))))
    world.get_region(regname.SKYOBS3STARTTOPSIDE).connect(world.get_region(regname.SKYOBS3STARTBOTTOM),
                                                          "Sky Station Comet: House Green Pipe",
                                                          rule=RB.CanPipe | RB.CanLongJump | RB.JumpHeight3) # replace the True_() with a pipe once pipes are in
    world.get_region(regname.SKYOBS3STARTTOPSIDE).connect(world.get_region(regname.SKYOBS3TOPOFHOUSE),
                                                          rule=(RB.JumpHeight6 | RB.CanWallSpin
                                                                | (RB.CanGrabLedge & RB.CanAirSpin & RB.CanBackOrSideflip)
                                                                | (RB.CanTriple & RB.CanWallJump & RB.HardLogic)))
    world.get_region(regname.SKYOBS3STARTBOTTOM).connect(world.get_region(regname.SKYOBS3TOPOFHOUSE))
    world.get_region(regname.SKYOBS3TOPOFHOUSE).connect(world.get_region(regname.SKYOBS3CYLINDER),
                                                        "Sky Station Comet: House Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.SKYOBS3CYLINDER).connect(world.get_region(regname.SKYOBS3BOSS),
                                                        "Sky Station Comet: Cylinder Launch Star",
                                                      rule=RB.CanLaunchStar)

    # Yoshi star
    world.get_region(regname.WORLD1).connect(world.get_region(regname.GOODEGG), "World 1 Slot 2 Galaxy")
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG1LANDING), "Yoshi Star Star 1")
    world.get_region(regname.GOODEGG1LANDING).connect(world.get_region(regname.GOODEGG1MUDDY))
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGG1OCTOBONUS),
                                                      "Yoshi Star 1: Octogoomba Bonus Teleporter",
                                                    rule=(RB.CanRideDino | RB.CanLongSpin))
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGG1EARTH),
                                                      "Yoshi Star 1: Yoshi Planet Launch Star",
                                                    rule=RB.CanLaunchStar & RB.CanRideDino)
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGGGSTAR1),
                                                    rule=(RB.CanRideDino | (RB.CanBackOrSideflip & RB.CanAirSpin))),
    world.get_region(regname.GOODEGG1MUDDY).connect(world.get_region(regname.GOODEGGGSTAR2),
                                                    rule=(RB.CanRideDino | RB.CanLongSpin))
    world.get_region(regname.GOODEGG1EARTH).connect(world.get_region(regname.GOODEGG1TOWER),
                                                      "Yoshi Star 1: Earthy Planet Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.GOODEGG1LANDING),world.get_region(regname.GOODEGG1TOWER), # Trick Entrance
                          (RB.CanInfiniteFlutter & RB.CanAirSpin))
    world.get_region(regname.GOODEGG1TOWER).connect(world.get_region(regname.GOODEGG1FOSSIL),
                                                      "Yoshi Star 1: Tower Launch Star",
                                                    rule=RB.CanLaunchStar & (RB.CanDinoSwing | RB.CanInfiniteFlutter
                                                                             | (RB.MediumLogic & RB.CanRideDino)))
    world.get_region(regname.GOODEGG).connect(world.get_region(regname.GOODEGG2LANDING), "Yoshi Star Star 2")
    world.get_region(regname.GOODEGG2LANDING).connect(world.get_region(regname.GOODEGG2MUDDY))
    world.get_region(regname.GOODEGG2MUDDY).connect(world.get_region(regname.GOODEGG2BONUS),
                                                      "Yoshi Star 2: Octogoomba Bonus Teleporter")
    world.get_region(regname.GOODEGG2MUDDY).connect(world.get_region(regname.GOODEGG2SHOOTING),
                                              "Yoshi Star 2: Yoshi Planet Launch Star",
                                                    rule=RB.CanRideDino & RB.CanLaunchStar)
    world.get_region(regname.GOODEGG2SHOOTING).connect(world.get_region(regname.GOODEGG2ORBITS),
                                              "Yoshi Star 2: Mid-Travel Launch Star",
                                                       rule=RB.CanRideDino & RB.CanLaunchStar)
    world.get_region(regname.GOODEGG2ORBITS).connect(world.get_region(regname.GOODEGG2MARBLE),
                                              "Yoshi Star 2: Planetoids Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.GOODEGG2SHOOTING).connect(world.get_region(regname.GOODEGG2MARBLE),
                                              "Yoshi Star 2: Shooting Gallery Launch Star",
                                                       rule=RB.CanLaunchStar & RB.CanRideDino)
    world.get_region(regname.GOODEGG2MARBLE).connect(world.get_region(regname.GOODEGG2BOSS),
                                              "Yoshi Star 2: Marble Block Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.GOODEGG2LANDING),world.get_region(regname.GOODEGG2BOSS), # Trick Entrance
                          (RB.CanInfiniteFlutter & RB.CanAirSpin))
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
                                                    rule=RB.CanLaunchStar
                                                         & (RB.DRILLMASTER | RB.JumpHeight6
                                                            | (RB.MediumLogic & RB.CanWallSpin & (RB.CanDouble | RB.CanBackflip))
                                                            | (RB.HardLogic & RB.CanLongSpin & RB.CanWallJump)))
    world.get_region(regname.SPINDIG1DRILL).connect(world.get_region(regname.SPINDIG1STEEL),
                                                    "Spin-Dig 1: Drill Zone Launch Star",
                                                    rule=RB.CanLaunchStar & RB.DRILLMASTER)
    world.get_region(regname.SPINDIG1STEEL).connect(world.get_region(regname.SPINDIG1BONUS),
                                                    "Spin-Dig 1: Twirlips Bonus Teleporter")
    world.get_region(regname.SPINDIG1STEEL).connect(world.get_region(regname.SPINDIG1DIRTT),
                                                    "Spin-Dig 1: Steel Ring Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SPINDIG1DIRTT).connect(world.get_region(regname.SPINDIG1TOADS),
                                                    "Spin-Dig 1: Dirt Tower Launch Star",
                                                    rule=RB.CanLaunchStar & RB.DRILLMASTER)
    world.get_region(regname.SPINDIG1TOADS).connect(world.get_region(regname.SPINDIG1BOSS),
                                                    "Spin-Dig 1: Red Toadship Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SPINDIG).connect(world.get_region(regname.SPINDIG2TETRA), "Spin-Dig Star 2")
    world.get_region(regname.SPINDIG2TETRA).connect(world.get_region(regname.SPINDIG2DARKT),
                                                    "Spin-Dig 2: Dig Dirt Sling to Vine",
                                                    rule=(RB.CanLaunchStar | RB.JumpHeight3 | (RB.CanDouble & RB.MediumLogic)))
    world.get_region(regname.SPINDIG2DARKT).connect(world.get_region(regname.SPINDIG2DARKIN1),
                                                    "Spin-Dig 2: Dark Canister 1st Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.SPINDIG2DARKT).connect(world.get_region(regname.SPINDIG2BONUS),
                                                    "Spin-Dig 2: Twirlips Bonus Teleporter")
    world.get_region(regname.SPINDIG2DARKIN1).connect(world.get_region(regname.SPINDIG2DARKIN2),
                                                    "Spin-Dig 2: Dark Canister 2nd Green Pipe",
                                                      rule=RB.DRILLMASTER & RB.CanPipe)
    world.get_region(regname.SPINDIG2DARKIN2).connect(world.get_region(regname.SPINDIG2DARKB),
                                                    "Spin-Dig 2: Dark Canister Orange Pipe",
                                                      rule=RB.DRILLMASTER)
    world.get_region(regname.SPINDIG2DARKB).connect(world.get_region(regname.SPINDIG2BTOAD),
                                                    "Spin-Dig 2: Dark Canister Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SPINDIG2BTOAD).connect(world.get_region(regname.SPINDIG2SQUARE),
                                                    "Spin-Dig 2: Blue Toadship Launch Star",
                                                    rule=RB.CanLaunchStar)
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
    # Flip-Swap
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
    # Fluffy Bluff
    world.get_region(regname.WORLD1).connect(world.get_region(regname.FLUFFBLUFF), "World 1 Slot 5 Galaxy")
    world.get_region(regname.FLUFFBLUFF).connect(world.get_region(regname.FLUFFBLUFF1LANDING), "Fluffy Bluff Star")
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FLUFFBLUFF1COINROOM),
                                                         "Fluffy Bluff: Landing Green Pipe",
                                                         rule=RB.CanPipe)
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FLUFFBLUFF1BUILDING),
                                                         rule=RB.JumpHeight3 | RB.CloudMario)
    world.get_region(regname.FLUFFBLUFF1BUILDING).connect(world.get_region(regname.FLUFFBLUFF1BIGTREE),
                                                         rule=(RB.CanMakeCloud | (RB.CloudMario & (RB.CanLongJump | RB.MediumLogic))))
    world.get_region(regname.FLUFFBLUFF1BUILDING).connect(world.get_region(regname.FLUFFBLUFF1CLIFF1),
                                                          rule=RB.CanMakeCloud
                                                               | (RB.CloudMario & (RB.JumpHeight3 | RB.CanWallSpin | RB.CanGrabLedge))
                                                               | (RB.JumpHeight6 & RB.CanWallSpin & RB.MediumLogic))
    world.get_region(regname.FLUFFBLUFF1CLIFF1).connect(world.get_region(regname.FLUFFBLUFF1BIGTREE),
                                                        rule=RB.CloudMario | RB.CanLongJump | RB.JumpHeight6
                                                             | (RB.CanAirSpin & RB.CanBackflip))
    world.get_region(regname.FLUFFBLUFF1BIGTREE).connect(world.get_region(regname.FLUFFBLUFF1BIGCLOUD),
                                                         "Fluffy Bluff: Landing Big Tree Sling Star",
                                                         rule=RB.CanLaunchStar & RB.CloudMario)
    world.get_region(regname.FLUFFBLUFF1BIGCLOUD).connect(world.get_region(regname.FLUFFBLUFF3TOWER),
                                                         "Fluffy Bluff: Hungry Luma",
                                                          rule=RB.CanLaunchStar & ((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL1)))
                                                     & RB.CoinLumaRule(world.options.coin_luma_counts.value["Fluffy Bluff Coin Luma"]))),
    world.get_region(regname.FLUFFBLUFF1BIGCLOUD).connect(world.get_region(regname.FLUFFBLUFF1CLIFF1))
    world.get_region(regname.FLUFFBLUFF1CLIFF1).connect(world.get_region(regname.FLUFFBLUFF1CLIFF2),
                                                        rule=RB.CloudMario | (RB.HellLogic & RB.CanWallSpin & RB.CanSideflip))
    world.get_region(regname.FLUFFBLUFF1CLIFF2).connect(world.get_region(regname.FLUFFBLUFF1WATER),
                                                         "Fluffy Bluff: Wall Jump Launch Star",
                                                        rule=RB.CanLaunchStar
                                                             & (RB.CanWallJump
                                                                | (RB.CanMakeCloud & RB.MediumLogic)
                                                                | (RB.CloudMario & RB.CanLongJump & RB.HardLogic)))
    world.get_region(regname.FLUFFBLUFF1WATER).connect(world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB),
                                                         "Fluffy Bluff: Water Sphere Launch Star",
                                                       rule=RB.CanLaunchStar & RB.CanCollectStarChips)
    world.create_entrance(world.get_region(regname.FLUFFBLUFF1BIGCLOUD),world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB), # Trick Entrance
                          RB.CanLongJump & RB.CanMakeCloud & RB.HardLogic)
    world.get_region(regname.FLUFFBLUFF1CLOUDCLIMB).connect(world.get_region(regname.FLUFFBLUFF1TREECLIMB),
                                                         "Fluffy Bluff: Vine Swing",
                                                            rule=RB.CanMakeCloud
                                                                 | (RB.CanWallSpin & RB.JumpHeight4 & RB.MediumLogic & RB.CanSwing)
                                                                 | (RB.CloudMario & RB.CanSwing
                                                                    & (RB.CanGrabLedge | RB.MediumLogic | RB.JumpHeight3)))
    world.get_region(regname.FLUFFBLUFF).connect(world.get_region(regname.FLUFFBLUFF2LANDING), "Fluffy Bluff Chimp Star")
    world.get_region(regname.FLUFFBLUFF2LANDING).connect(world.get_region(regname.FLUFFBLUFF2BUILDING),
                                                         rule=RB.JumpHeight3 | True_()) # Replace True_() with Launch star rule when implemented
    world.get_region(regname.FLUFFBLUFF2BUILDING).connect(world.get_region(regname.FLUFFBLUFF2CLIFF),
                                                          "Fluffy Bluff Chimp: Buildings Sling Star",
                                                          rule=RB.CanLaunchStar| (RB.CanTriple & RB.CanWallSpin))
    world.get_region(regname.FLUFFBLUFF2CLIFF).connect(world.get_region(regname.FLUFFBLUFF2TREE),
                                                       rule=RB.CanLongJump | RB.JumpHeight6 | (RB.CanAirSpin & RB.CanBackflip))
    # Rightside Down
    world.get_region(regname.WORLD1).connect(world.get_region(regname.RIGHTDOWN), "World 1 Slot 6 Galaxy")
    world.get_region(regname.RIGHTDOWN).connect(world.get_region(regname.RIGHTDOWNLANDING), "Rightside Down Star")
    world.get_region(regname.RIGHTDOWNLANDING).connect(world.get_region(regname.RIGHTDOWNCORRIDOR),
                                                "Rightside Down: Entrance Pipe",
                                                       rule=RB.CanPipe)
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNCOINROOM),
                                                "Rightside Down: Green Pipe",
                                                        rule=RB.CanPipe)
    world.get_region(regname.RIGHTDOWNCOINROOM).connect(world.get_region(regname.RIGHTDOWNBREAKER),
                                                "Rightside Down: Orange Pipe",
                                                        rule=RB.CanPipe & RB.FireMario)
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNBONUS),
                                                "Rightside Down: Paragoomba Bonus Teleporter")
    world.get_region(regname.RIGHTDOWNCORRIDOR).connect(world.get_region(regname.RIGHTDOWNTOPVIEW),
                                                        rule=RB.FireMario & (RB.CanWallJump | (RB.CanTriple & RB.MediumLogic)))
    # Fiery Flotilla
    world.get_region(regname.WORLD1).connect(world.get_region(regname.BOWJR1), "World 1 Slot 7 Galaxy")
    world.get_region(regname.BOWJR1).connect(world.get_region(regname.FIREFLOT1LANDING), "Fiery Flotilla Grand Star")
    world.get_region(regname.FIREFLOT1LANDING).connect(world.get_region(regname.FIREFLOT1LAVA),
                                                       "Fiery Flotilla: Fort Sling Star",
                                                       rule= (RB.CanLaunchStar | (RB.HardLogic & (RB.CanLongJump | RB.CanAirSpin))))
    world.get_region(regname.FIREFLOT1LAVA).connect(world.get_region(regname.FIREFLOT1BOSS),
                                                       "Fiery Flotilla: Lava Planet Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.FIREFLOT1LANDING),world.get_region(regname.FIREFLOT1BOSS), # Trick Entrance
                          (RB.MediumLogic & (RB.JumpHeight3 | RB.CanLongJump)))
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
                                                      rule=RB.CanPound & RB.CanLaunchStar)
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN1COINRO),
                                                      "Puzzle Plank: Grassy Buzzsaw Green Pipe",
                                                      rule=RB.CanPipe)
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN3BUGABO),
                                                      "Puzzle Plank: Hungry Luma",
                                                      rule=RB.CanLaunchStar & ((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL2)))
                                                     & RB.CoinLumaRule(world.options.coin_luma_counts.value["Puzzle Plank Coin Luma"])))
    world.get_region(regname.PUZZPLAN1GRUZZY).connect(world.get_region(regname.PUZZPLAN1SAWBLA),
                                                      "Puzzle Plank: Grassy Buzzsaw Launch Star",
                                                      rule=RB.CanLaunchStar & (RB.CanPound | (RB.JumpHeight5 & RB.CanAirSpin)))
    world.get_region(regname.PUZZPLAN1SAWBLA).connect(world.get_region(regname.PUZZPLAN1CHECKP),
                                                      "Puzzle Plank: Saws & Planks Sling Star",
                                                      rule=RB.CanLaunchStar & RB.CanPound & (RB.CanWallJump | (RB.HellLogic & RB.JumpHeight6)))
    world.get_region(regname.PUZZPLAN1CHECKP).connect(world.get_region(regname.PUZZPLAN1MANDIB),
                                                      "Puzzle Plank: Checkpoint Launch Star",
                                                      rule=RB.CanLaunchStar)
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
                                                      "Puzzle Plank Comet: Green Pipe",
                                                      rule=RB.CanPipe)
    # Boulder Bowl
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOULBOWL), "World 2 Slot 2 Galaxy")
    world.get_region(regname.BOULBOWL).connect(world.get_region(regname.BOULBOWL1CRYSTAL), "Boulder Bowl Star")
    world.get_region(regname.BOULBOWL1CRYSTAL).connect(world.get_region(regname.BOULBOWL1FALLING),
                                                       rule=RB.ROCKNROLLIN)
    world.get_region(regname.BOULBOWL1FALLING).connect(world.get_region(regname.BOULBOWL1BOULDER),
                                                       "Boulder Bowl: Falling Rocks Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.BOULBOWL1CRYSTAL),world.get_region(regname.BOULBOWL1BOULDER), # Trick Entrance
                          (RB.HardLogic & ROCKNROLLIN) | (RB.MediumLogic & RB.CanLongSpin))
    world.get_region(regname.BOULBOWL1BOULDER).connect(world.get_region(regname.BOULBOWL1DODECAH),
                                                       "Boulder Bowl: Boulder Sling Star",
                                                       rule=RB.ROCKNROLLIN & RB.CanLaunchStar)
    world.get_region(regname.BOULBOWL1BOULDER).connect(world.get_region(regname.BOULBOWL1DICEROOM),
                                                       "Boulder Bowl: Boulder Green Pipe",
                                                       rule=RB.CanPipe & RB.ROCKNROLLIN)
    world.get_region(regname.BOULBOWL1DODECAH).connect(world.get_region(regname.BOULBOWL1BOSS),
                                                       "Boulder Bowl: Dodecahedron Launch Star",
                                                       rule=RB.CanLaunchStar)
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
                                                       "Boulder Bowl Comet: Asteroid Launch Star",
                                                       rule=RB.CanLaunchStar)
    # Hightail Falls
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HIGHTAIL), "World 2 Slot 3 Galaxy")
    world.get_region(regname.HIGHTAIL).connect(world.get_region(regname.HIGHTAIL1LANDING), "Hightail Falls Star")
    world.get_region(regname.HIGHTAIL1LANDING).connect(world.get_region(regname.HIGHTAIL1GIANTRA),
                                                       "Hightail Falls: Hot Pepper Landing Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.CanDinoRun | (RB.MediumLogic & RB.CanRideDino)))
    world.get_region(regname.HIGHTAIL1GIANTRA).connect(world.get_region(regname.HIGHTAILGSTAR1),
                                                       rule=RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1GIANTRA).connect(world.get_region(regname.HIGHTAIL1PLATDAS),
                                                       "Hightail Falls: Hot Pepper Climb Launch Star",
                                                       rule=RB.CanLaunchStar & RB.CanDinoRun)
    world.get_region(regname.HIGHTAIL1PLATDAS).connect(world.get_region(regname.HIGHTAIL1BONUS),
                                                       "Hightail Falls: Paragoomba Bonus Teleporter",
                                                       rule=RB.CanRideDino | RB.CanLongJump)
    world.get_region(regname.HIGHTAIL1PLATDAS).connect(world.get_region(regname.HIGHTAIL1DASHWAL1),
                                                       "Hightail Falls: Hot Pepper Dash Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.CanRideDino | RB.CanLongJump))
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAIL1DASHWAL2),
                                                        rule=RB.CanDinoRun & (RB.CanDinoSwing | RB.CanInfiniteFlutter))
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAIL3SILVERS),
                                                        "Hightail Falls: Hungry Luma",
                                                        rule=((RB.CoinLumaBase |
                                                               (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL3)))
                                                              & RB.CoinLumaRule(world.options.coin_luma_counts.value[
                                                                                "Hightail Falls Coin Luma"])))
    world.get_region(regname.HIGHTAIL1DASHWAL2).connect(world.get_region(regname.HIGHTAILGSTAR3))
    world.get_region(regname.HIGHTAIL1DASHWAL1).connect(world.get_region(regname.HIGHTAILGSTAR2),
                                                        rule=RB.CanDinoRun)
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
                                                       rule=RB.CanLaunchStar & (RB.CanDinoRun | (RB.CanRideDino & RB.MediumLogic)))
    world.get_region(regname.HIGHTAIL2GIANTRA).connect(world.get_region(regname.HIGHTAIL2PLATDAS),
                                                       "Hightail Falls Comet: Hot Pepper Climb Launch Star",
                                                       rule=RB.CanDinoRun & RB.CanLaunchStar)
    world.get_region(regname.HIGHTAIL2PLATDAS).connect(world.get_region(regname.HIGHTAIL2DASHWAL1),
                                                       "Hightail Falls Comet: Hot Pepper Dash Launch Star",
                                                       rule=RB.CanDinoRun & RB.CanLaunchStar)
    world.get_region(regname.HIGHTAIL2DASHWAL1).connect(world.get_region(regname.HIGHTAIL2DASHWAL2),
                                                        rule=RB.CanDinoRun&RB.CanDinoSwing)
    # Wild Glide
    world.get_region(regname.WORLD2).connect(world.get_region(regname.WILDGLIDE), "World 2 Slot 4 Galaxy")
    world.get_region(regname.WILDGLIDE).connect(world.get_region(regname.WILDGLIDE1START), "Wild Glide Star 1")
    world.get_region(regname.WILDGLIDE1START).connect(world.get_region(regname.WILDGLIDE1COURSE),
                                                     rule=RB.CanRideBird)
    world.get_region(regname.WILDGLIDE).connect(world.get_region(regname.WILDGLIDE2START), "Wild Glide Star 2",
                                                rule=True_()) #Add Letter if needed
    world.get_region(regname.WILDGLIDE2START).connect(world.get_region(regname.WILDGLIDE2COURSE),
                                                      rule=RB.CanRideBird)
    # Cosmic Cove
    world.get_region(regname.WORLD2).connect(world.get_region(regname.COSMICO), "World 2 Slot 5 Galaxy")
    world.get_region(regname.COSMICO).connect(world.get_region(regname.COSMIC1LANDING), "Cosmic Cove Star 1")
    world.get_region(regname.COSMIC1LANDING).connect(world.get_region(regname.COSMIC1POOL),
                                                     rule=RB.CanSwim)
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC1DICEROOM),
                                                  "Cosmic Cove 1: Green Pipe",
                                                  rule=RB.CanPipe)
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC3WATER),
                                                  "Cosmic Cove: Hungry Luma",
                                                  rule=((RB.CoinLumaBase |
                                                         (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL4)))
                                                        & RB.CoinLumaRule(world.options.coin_luma_counts.value[
                                                                          "Cosmic Cove Coin Luma"])))
    world.get_region(regname.COSMIC1POOL).connect(world.get_region(regname.COSMIC1WATERFA),
                                                  "Cosmic Cove 1: Icy Waterfall",
                                                  rule=RB.CanPound & RB.CanWallJump)
    world.get_region(regname.COSMICO).connect(world.get_region(regname.COSMIC2LANDING), "Cosmic Cove Star 2")
    world.get_region(regname.COSMIC2LANDING).connect(world.get_region(regname.COSMIC2INPIPE),
                                                  "Cosmic Cove 2: Green Pipe to Cave",
                                                     rule=RB.CanPipe)
    world.get_region(regname.COSMIC2INPIPE).connect(world.get_region(regname.COSMIC2WATERPA),
                                                  "Cosmic Cove 2: Green Pipe in Cave",
                                                    rule=RB.CanPipe & RB.CanSwim & RB.CanWallJump)
    world.get_region(regname.COSMIC2WATERPA).connect(world.get_region(regname.COSMIC2LANDING),
                                                  "Cosmic Cove 2: Return Green Pipe",
                                                     rule=RB.CanSwim & RB.CanPipe)
    world.get_region(regname.COSMIC2LANDING).connect(world.get_region(regname.COSMIC2TOADSHI),
                                                  "Cosmic Cove 2: Landing Launch Star",
                                                     rule=RB.CanLaunchStar & CanReachEntrance("Cosmic Cove 2: Return Green Pipe"))
    world.get_region(regname.COSMIC2TOADSHI).connect(world.get_region(regname.COSMIC2WATERPL1),
                                                  "Cosmic Cove 2: Toadship Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.COSMIC2WATERPL1).connect(world.get_region(regname.COSMIC2WATERPL2),
                                                      rule=RB.CanSwim & RB.DRILLMASTER)
    # Honeybloom
    world.get_region(regname.WORLD2).connect(world.get_region(regname.HONEYBLOOM), "World 2 Slot 6 Galaxy")
    world.get_region(regname.HONEYBLOOM).connect(world.get_region(regname.HONEYBLOOM1LANDING), "Honeybloom Star")
    world.get_region(regname.HONEYBLOOM1LANDING).connect(world.get_region(regname.HONEYBLOOM1SECRET),
                                                         rule=RB.CanSwing & RB.CanWallJump & (RB.CanAirSpin | RB.HardLogic))
    world.get_region(regname.HONEYBLOOM1LANDING).connect(world.get_region(regname.HONEYBLOOM1WALL2),
                                                         rule=(RB.CanSwing | RB.CanGrabLedge | RB.CanLongJump)
                                                              & RB.CanWallJump
                                                              & (RB.BeeFlight | RB.JumpHeight5 | RB.MediumLogic))
    world.get_region(regname.HONEYBLOOM1WALL2).connect(world.get_region(regname.HONEYBLOOM1WALL3),
                                                       rule=RB.BeeFlight
                                                       | (RB.HellLogic & RB.CanSideflip & RB.CanAirSpin))
    world.get_region(regname.HONEYBLOOM1WALL3).connect(world.get_region(regname.HONEYBLOOM1HONELOG),
                                                       rule=RB.CanSwing&RB.BeeFlight) #Check once beta is out: How not having swings works
    # Lava Lair
    world.get_region(regname.WORLD2).connect(world.get_region(regname.BOWSER1), "World 2 Slot 7 Galaxy")
    world.get_region(regname.BOWSER1).connect(world.get_region(regname.LAVALAIR1LANDING), "Lava Lair Grand Star")
    world.get_region(regname.LAVALAIR1LANDING).connect(world.get_region(regname.LAVALAIR1LAVACYL1),
                                                       "Lava Lair: Pull Star to Lava")
    world.get_region(regname.LAVALAIR1LAVACYL1).connect(world.get_region(regname.LAVALAIR1LAVACYL2),
                                                        rule=RB.CanPound | RB.JumpHeight5 | RB.HardLogic)
    world.get_region(regname.LAVALAIR1LAVACYL2).connect(world.get_region(regname.LAVALAIR1LAVAPLA1B),
                                                       "Lava Lair: Lava Cylinder Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.LAVALAIR1LAVAPLA1B).connect(world.get_region(regname.LAVALAIR1LAVAPLA1W),
                                                       "Lava Lair: Lava Sling Star",
                                                         rule=RB.CanLaunchStar | (RB.JumpHeight5 & RB.CanAirSpin)
                                                              | (RB.CanTriple & RB.CanGrabLedge) | RB.CanWallSpin)
    world.get_region(regname.LAVALAIR1LAVAPLA1W).connect(world.get_region(regname.LAVALAIR1LAVAPLA2C),
                                                       "Lava Lair: Purple Bowser Door",
                                                         rule=RB.CanPound)
    world.get_region(regname.LAVALAIR1LAVAPLA2C).connect(world.get_region(regname.LAVALAIR1LAVAPLA2S))
    world.get_region(regname.LAVALAIR1LAVAPLA2S).connect(world.get_region(regname.LAVALAIR1BOSSPLA),
                                                       "Lava Lair: Red Bowser Door",
                                                         rule=RB.CanPound)
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
                                                       "Lava Lair Comet: Lava Sling Star",
                                                        rule=(RB.CanLaunchStar | (RB.JumpHeight5 & RB.CanAirSpin)
                                                        | (RB.CanTriple & RB.CanGrabLedge) | RB.CanWallSpin))
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
                                                        rule=RB.CanLaunchStar & (RB.CanDinoBlimp
                                                                                 | (RB.HardLogic & RB.CanBackflip & RB.CanWallSpin)))
    world.get_region(regname.TALLTRUNK1BIGTREE).connect(world.get_region(regname.TALLTRUNK1PIRANHABONUS),
                                                        "Tall Trunk 1: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1WOODCIRClE),
                                                        "Tall Trunk 1: Carved Log Launch Star",
                                                    rule=RB.CanLaunchStar & RB.CanDinoBlimp & RB.CanCollectStarChips)
    world.get_region(regname.TALLTRUNK1LOG).connect(world.get_region(regname.TALLTRUNK1DICEPIPE),
                                                        "Tall Trunk 1: Carved Log Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.TALLTRUNK).connect(world.get_region(regname.TALLTRUNK2BIGTREE), "Tall Trunk Star 2")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2PIRANHABONUS),
                                                        "Tall Trunk 2: Piranha Bonus Teleporter")
    world.get_region(regname.TALLTRUNK2BIGTREE).connect(world.get_region(regname.TALLTRUNK2SLIDE),
                                                        "Tall Trunk 2: Big Tree Launch Star",
                                                        rule=RB.CanLaunchStar & RB.CanSwing) #Test: Can climb tree, what's needed?
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
    world.get_region(regname.TALLTRUNK3PCOINSLIDE).connect(world.get_region(regname.TALLTRUNK3PCOINEND),
                                                           rule=RB.CanSlide)
    # Cloudy Court
    world.get_region(regname.WORLD3).connect(world.get_region(regname.CLOUCOUR), "World 3 Slot 2 Galaxy")
    world.get_region(regname.CLOUCOUR).connect(world.get_region(regname.CLOUCOUR1LANDING), "Cloudy Court Star")
    world.get_region(regname.CLOUCOUR1LANDING).connect(world.get_region(regname.CLOUCOUR1CYMBAL),
                                                       rule=RB.CanMakeCloud)
    world.get_region(regname.CLOUCOUR1CYMBAL).connect(world.get_region(regname.CLOUCOUR1TOWERS),
                                                      "Cloudy Court: Cymbal Launch Star",
                                                      rule=RB.CanLaunchStar
                                                           & (RB.CanMakeCloud | (RB.CloudMario & RB.CanPound & RB.HardLogic)))
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR3PCOINS),
                                                      "Cloudy Court: Hungry Luma",
                                                      rule=RB.CanLaunchStar & ((RB.CoinLumaBase |
                                                             (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL5)))
                                                            & RB.CoinLumaRule(world.options.coin_luma_counts.value[
                                                                              "Cloudy Court Coin Luma"])))
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1PARAGOOMBONUS),
                                                      "Cloudy Court: Paragoomba Bonus Teleporter",
                                                      rule=RB.CanMakeCloud)
    world.get_region(regname.CLOUCOUR1TOWERS).connect(world.get_region(regname.CLOUCOUR1CASTLE),
                                                      "Cloudy Court: Tower Launch Star",
                                                      rule=RB.CanLaunchStar & RB.CanMakeCloud)
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
                                                       rule=RB.CanLaunchStar & RB.CanCollectStarChips)
    world.get_region(regname.CLOUCOUR2CASTLE1).connect(world.get_region(regname.CLOUCOUR2CASTLE2),
                                                       "Cloudy Court Comet: Wall Jump Sling Star",
                                                       rule=RB.CanWallJump & RB.CanLaunchStar)
    world.get_region(regname.CLOUCOUR2CASTLE2).connect(world.get_region(regname.CLOUCOUR2FINAL),
                                                       "Cloudy Court Comet: Final Sling Star",
                                                       rule=RB.CanLaunchStar)
    # Haunty Halls
    world.get_region(regname.WORLD3).connect(world.get_region(regname.HAUNHALL), "World 3 Slot 3 Galaxy")
    world.get_region(regname.HAUNHALL).connect(world.get_region(regname.HAUNHALL1HALLWAY), "Haunty Halls Star 1")
    world.get_region(regname.HAUNHALL1HALLWAY).connect(world.get_region(regname.HAUNHALL1JACKBON),
                                               "Haunty Halls 1: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.HAUNHALL1HALLWAY).connect(world.get_region(regname.HAUNHALL1DISAPPE),
                                               "Haunty Halls 1: Hallway Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.HAUNHALL1DISAPPE).connect(world.get_region(regname.HAUNHALL1BULBBER),
                                               "Haunty Halls 1: Green Pipe",
                                                       rule=RB.CanPipe)
    world.get_region(regname.HAUNHALL).connect(world.get_region(regname.HAUNHALL2HALLWAY), "Haunty Halls Star 2")
    world.get_region(regname.HAUNHALL2HALLWAY).connect(world.get_region(regname.HAUNHALL2JACKBON),
                                               "Haunty Halls 2: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.HAUNHALL2HALLWAY).connect(world.get_region(regname.HAUNHALL2CREEPYC),
                                               "Haunty Halls 2: Hallway Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.HAUNHALL2CREEPYC).connect(world.get_region(regname.HAUNHALL2CREEPYH),
                                               "Haunty Halls 2: Creepy Platforms Sling Star",
                                                       rule=RB.CanLaunchStar) #Test: Maybe able to skip with long spin?
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
                                                       rule=RB.FireMario & RB.CanLaunchStar)
    world.get_region(regname.FREEFLAK1SNOWBYH).connect(world.get_region(regname.FREEFLAK3CHIMP),
                                                       "Freezy Flake 1: Snowy Hill 1 Green Pipe",
                                                       rule=RB.CanPipe & RB.FireMario)
    world.get_region(regname.FREEFLAK1SNOWBYH).connect(world.get_region(regname.FREEFLAK1SLIDELA),
                                                       "Freezy Flake 1: Snow Slide",
                                                       rule=RB.CanSlide & RB.FireMario)
    world.get_region(regname.FREEFLAK1SLIDELA).connect(world.get_region(regname.FREEFLAK1LAVASNO),
                                                       "Freezy Flake 1: Slide Landing Green Pipe",
                                                       rule=RB.CanPipe & RB.FireMario)
    world.get_region(regname.FREEFLAKE).connect(world.get_region(regname.FREEFLAK2LOGCABI), "Freezy Flake 2")
    world.get_region(regname.FREEFLAK2LOGCABI).connect(world.get_region(regname.FREEFLAK2SNOWBYH),
                                                       "Freezy Flake 2: Log Cabin Launch Star",
                                                       rule=RB.CanLaunchStar & RB.ROCKNROLLIN)
    world.get_region(regname.FREEFLAK2SNOWBYH).connect(world.get_region(regname.FREEFLAK3CHIMP),
                                                       "Freezy Flake 2: Snowy Hill 2 Green Pipe",
                                                       rule=RB.CanPipe & RB.ROCKNROLLIN)
    world.get_region(regname.FREEFLAK2SNOWBYH).connect(world.get_region(regname.FREEFLAK2WHITOUT),
                                                       "Freezy Flake 2: Snowy Hill Launch Star",
                                                       rule=RB.CanLaunchStar & RB.ROCKNROLLIN & RB.CanCollectStarChips)
    world.get_region(regname.FREEFLAK2WHITOUT).connect(world.get_region(regname.FREEFLAK2DICEROOM),
                                                       "Freezy Flake 2: Whiteout Green Pipe",
                                                       rule=RB.CanPipe)
    world.get_region(regname.FREEFLAK2WHITOUT).connect(world.get_region(regname.FREEFLAK2SORBHEA),
                                                       "Freezy Flake 2: Whiteout Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.FREEFLAK2SORBHEA).connect(world.get_region(regname.FREEFLAK2SORBETT),
                                                       "Freezy Flake 2: Sorbetti's Head Sling Star",
                                                       rule=RB.CanLaunchStar)
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
    #Rolling Masterpiece
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
                                                       rule=RB.CanRideDino & (RB.CanLaunchStar | RB.HellLogic))
    world.get_region(regname.FEARFLET1BULLETB).connect(world.get_region(regname.FEARFLET1AIRSHIP),
                                                       rule=RB.CanRideDino)
    world.get_region(regname.FEARFLET1AIRSHIP).connect(world.get_region(regname.FEARFLET1MEGAHAM),
                                                       "Fearsome Fleet: Airship Launch Star",
                                                       rule=RB.CanLaunchStar)
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
                                                    rule=RB.CanWallJump | (RB.JumpHeight6 & RB.CanGrabLedge & RB.HardLogic))
    world.get_region(regname.SUPMASS1PIPES).connect(world.get_region(regname.SUPMASS1THWOMPS),
                                                    rule=RB.CanAirSpin | RB.CanLongJump)
    #world.get_region(regname.SUPMASS1PIPES).connect(world.get_region(regname.SUPMASS1GSTAR2), #requires Luigi
    #                                                rule=RB.CanLongSpin)
    world.get_region(regname.SUPMASS1THWOMPS).connect(world.get_region(regname.SUPMASS1GSTAR2),
                                                      rule=RB.CanAirSpin | RB.MediumLogic)
    world.get_region(regname.SUPMASS1THWOMPS).connect(world.get_region(regname.SUPMASS1KOOPAS),
                                                      "Supermassive: Thwomps Launch Star",
                                                      rule=RB.CanLaunchStar & (RB.CanWallJump|RB.JumpHeight4))
    world.get_region(regname.SUPMASS1KOOPAS).connect(world.get_region(regname.SUPMASS1STARCHIPS),
                                                     "Supermassive: Koopa Launch Star",
                                                     rule=RB.CanLaunchStar & RB.DRILLMASTER)
    world.get_region(regname.SUPMASS1STARCHIPS).connect(world.get_region(regname.SUPMASS1GARDEN),
                                                        "Supermassive: ? Block Launch Star",
                                                        rule=RB.CanLaunchStar)
    #world.create_entrance(world.get_region(regname.SUPMASS1STARCHIPS),world.get_region(regname.SUPMASS1WIGGLERS)) #Trick Entrance, requires Luigi
    world.get_region(regname.SUPMASS1GARDEN).connect(world.get_region(regname.SUPMASS1WIGGLERS),
                                                     "Supermassive: Garden Planet Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.SUPMASS).connect(world.get_region(regname.SUPMASS2START), "Supermassive Comet Star",
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
    world.get_region(regname.SUPMASS2PIPES).connect(world.get_region(regname.SUPMASS2THWOMPS),
                                                    rule=RB.CanLongJump | RB.CanAirSpin)
    world.get_region(regname.SUPMASS2THWOMPS).connect(world.get_region(regname.SUPMASS2KOOPAS),
                                                      "Supermassive Comet: Thwomps Launch Star",
                                                      rule=RB.CanLaunchStar & (RB.CanWallJump | RB.JumpHeight4))
    world.get_region(regname.SUPMASS2KOOPAS).connect(world.get_region(regname.SUPMASS2STARCHIPS),
                                                     "Supermassive Comet: Koopa Launch Star",
                                                     rule=RB.CanLaunchStar & RB.DRILLMASTER)
    world.get_region(regname.SUPMASS2STARCHIPS).connect(world.get_region(regname.SUPMASS2GARDEN),
                                                        "Supermassive Comet: ? Block Launch Star",
                                                        rule=RB.CanLaunchStar)
    #world.create_entrance(world.get_region(regname.SUPMASS2STARCHIPS),world.get_region(regname.SUPMASS2WIGGLERS)) #Trick Entrance, requires Luigi
    world.get_region(regname.SUPMASS2GARDEN).connect(world.get_region(regname.SUPMASS2WIGGLERS),
                                                     "Supermassive Comet: Garden Planet Launch Star",
                                                     rule=RB.CanLaunchStar)
    # Sweet Mystery
    world.get_region(regname.WORLD4).connect(world.get_region(regname.SWEETMYS), "World 4 Slot 2 Galaxy")
    world.get_region(regname.SWEETMYS).connect(world.get_region(regname.SWEETMYS1START), "Sweet Mystery Star")
    world.get_region(regname.SWEETMYS1START).connect(world.get_region(regname.SWEETMYS1COOKIE),
                                                     rule=RB.CanDinoGlow | RB.CanInfiniteFlutter)
    world.get_region(regname.SWEETMYS1COOKIE).connect(world.get_region(regname.SWEETMYS1CHOCO),
                                                      rule=RB.CanDinoGlow | RB.CanInfiniteFlutter)
    world.get_region(regname.SWEETMYS1CHOCO).connect(world.get_region(regname.SWEETMYS1BISCUIT),
                                                     rule=RB.CanDinoGlow | RB.CanInfiniteFlutter)
    world.get_region(regname.SWEETMYS1BISCUIT).connect(world.get_region(regname.SWEETMYS1SWITCHES),
                                                       rule=RB.CanDinoGlow | RB.CanInfiniteFlutter)
    world.get_region(regname.SWEETMYS1SWITCHES).connect(world.get_region(regname.SWEETMYS1CAKE),
                                                        "Sweet Mystery: Flipswitch Launch Star",
                                                        (RB.CanDinoGlow & RB.CanLaunchStar) | RB.CanInfiniteFlutter)
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
    world.get_region(regname.FLIPVILL1MAZESTART).connect(world.get_region(regname.FLIPVILL1MAZEBOTTOM),
                                                         rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1MAZESTART).connect(world.get_region(regname.FLIPVILL1MAZEBACK),
                                                         rule=RB.MediumLogic & RB.CanAirSpin)
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1MAZEBACK),
                                                          rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1MAZETOP),
                                                          rule=RB.CanPound)
    world.create_entrance(world.get_region(regname.FLIPVILL1MAZEBACK),world.get_region(regname.FLIPVILL1MAZETOP),
                          RB.CanBackOrSideflip & RB.CanWallSpin & RB.HardLogic) #Trick Entrance
    world.get_region(regname.FLIPVILL1MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL1COMETMEDAL))
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1COMETMEDAL),
                                                        rule=RB.MediumLogic & RB.CanAirSpin)
    world.get_region(regname.FLIPVILL1MAZEBACK).connect(world.get_region(regname.FLIPVILL1TWIRLIP),
                                                        "Flipsville 1: Twirlip Bonus Teleporter")
    world.get_region(regname.FLIPVILL1MAZETOP).connect(world.get_region(regname.FLIPVILL1WANWANSTART),
                                                       "Flipsville 1: Dollhouse Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.FLIPVILL1WANWANSTART).connect(world.get_region(regname.FLIPVILL1WANWANALLEY),
                                                           rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1WANWANSTART).connect(world.get_region(regname.FLIPVILL1WANWANLANE),
                                                           rule = RB.HardLogic & RB.CanBackOrSideflip & RB.CanWallJump) #Advanced Logic
    world.get_region(regname.FLIPVILL1WANWANALLEY).connect(world.get_region(regname.FLIPVILL1WANWANLANE),
                                                           rule=RB.CanPound)
    world.create_entrance(world.get_region(regname.FLIPVILL1MAZEBOTTOM),world.get_region(regname.FLIPVILL1WANWANLANE),
                          RB.CanLongSpin & RB.HellLogic & RB.CanWallJump,
                          "Flipsville 1: Jump to Chomp Planet") # Trick Entrance
    world.get_region(regname.FLIPVILL1WANWANLANE).connect(world.get_region(regname.FLIPVILL1WANWANBACK),
                                                          rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1WANWANBACK).connect(world.get_region(regname.FLIPVILL1LIFTSTART),
                                                          "Flipsville 1: Chomps Launch Star",
                                                          rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.FLIPVILL1MAZEBACK),world.get_region(regname.FLIPVILL1LIFTSTART)) # Trick Entrance
    world.get_region(regname.FLIPVILL1LIFTSTART).connect(world.get_region(regname.FLIPVILL1LIFTBELOW),
                                                         rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1LIFTSTART).connect(world.get_region(regname.FLIPVILL1LIFTTOP),
                                                         rule=RB.MediumLogic & RB.CanWallSpin)
    world.get_region(regname.FLIPVILL1LIFTBELOW).connect(world.get_region(regname.FLIPVILL1LIFTTOP),
                                                         rule=RB.CanPound)
    world.get_region(regname.FLIPVILL1LIFTTOP).connect(world.get_region(regname.FLIPVILL1STARSHROOM),
                                                       "Flipsville 1: Lifts Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.CanPound | (RB.CanWallSpin & RB.HardLogic)))
    world.create_entrance(world.get_region(regname.FLIPVILL1WANWANLANE),world.get_region(regname.FLIPVILL1STARSHROOM),
                          RB.JumpHeight6 & RB.CanWallJump & RB.CanBackflip & RB.HellLogic
                          & CanReachEntrance("Flipsville 1: Jump to Chomp Planet",
                                             parent_region_name=regname.FLIPVILL1MAZEBOTTOM)) # Trick Entrance
    world.get_region(regname.FLIPVILL1STARSHROOM).connect(world.get_region(regname.FLIPVILL1GLAM),
                                                          "Flipsville 1: Starshroom Launch Star",
                                                          rule=RB.CanLaunchStar)
    world.create_entrance(world.get_region(regname.FLIPVILL1WANWANLANE),world.get_region(regname.FLIPVILL1GLAM),
                          RB.JumpHeight6 & RB.CanWallJump & RB.CanBackflip & RB.HellLogic
                          & CanReachEntrance("Flipsville 1: Jump to Chomp Planet",
                                             parent_region_name=regname.FLIPVILL1MAZEBOTTOM)) # Trick Entrance
    world.get_region(regname.FLIPVILL1GLAM).connect(world.get_region(regname.FLIPVILL1STAR),
                                                    rule=RB.CanPound)
    world.get_region(regname.FLIPVILL).connect(world.get_region(regname.FLIPVILL2MAZESTART), "Flipsville Star 2")
    world.get_region(regname.FLIPVILL2MAZESTART).connect(world.get_region(regname.FLIPVILL2MAZEBOTTOM),
                                                         rule=RB.DRILLMASTER)
    world.get_region(regname.FLIPVILL2MAZESTART).connect(world.get_region(regname.FLIPVILL2MAZEBACK),
                                                         rule=RB.CanAirSpin & RB.MediumLogic)
    world.get_region(regname.FLIPVILL2MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL2MAZEBACK),
                                                          rule=RB.DRILLMASTER)
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2TWIRLIP),
                                                        "Flipsville 2: Twirlip Bonus Teleporter")
    world.get_region(regname.FLIPVILL2MAZEBOTTOM).connect(world.get_region(regname.FLIPVILL2MAZETOP),
                                                          rule=RB.DRILLMASTER)
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2MAZETOP),
                                                        rule=RB.MediumLogic | RB.CanWallSpin & (RB.JumpHeight5 | RB.HardLogic))
    world.get_region(regname.FLIPVILL2MAZETOP).connect(world.get_region(regname.FLIPVILL2MAZELAUNCH))
    world.get_region(regname.FLIPVILL2MAZEBACK).connect(world.get_region(regname.FLIPVILL2MAZELAUNCH),
                                                        rule=RB.CanAirSpin)
    world.get_region(regname.FLIPVILL2MAZELAUNCH).connect(world.get_region(regname.FLIPVILL2TOWERSTART),
                                                          "Flipsville 2: Dollhouse Planet Launch Star",
                                                          rule=RB.CanLaunchStar)
    world.get_region(regname.FLIPVILL2TOWERSTART).connect(world.get_region(regname.FLIPVILL2TOWERBELOW),
                                                          rule=RB.DRILLMASTER)
    world.get_region(regname.FLIPVILL2TOWERSTART).connect(world.get_region(regname.FLIPVILL2PIPE),
                                                          rule=RB.JumpHeight4 & RB.CanWallSpin)
    world.get_region(regname.FLIPVILL2TOWERBELOW).connect(world.get_region(regname.FLIPVILL2PIPE),
                                                          rule=RB.DRILLMASTER)
    world.get_region(regname.FLIPVILL2PIPE).connect(world.get_region(regname.FLIPVILL2GRAVITYSTART),
                                                    "Flipsville 2: Spin-Drill Tower Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.FLIPVILL2GRAVITYSTART).connect(world.get_region(regname.FLIPVILL2GRAVITYMAIN),
                                                            rule=RB.DRILLMASTER)
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
                                                     "Flipsville Comet: Spin-Drill Tower Pipe",
                                                     rule=RB.CanPipe)
    # Honeyhop
    world.get_region(regname.WORLD4).connect(world.get_region(regname.HONEYHOP), "World 4 Slot 4 Galaxy")
    world.get_region(regname.HONEYHOP).connect(world.get_region(regname.HONEYHOP1START), "Honeyhop Star 1")
    world.get_region(regname.HONEYHOP1START).connect(world.get_region(regname.HONEYHOP1POND),
                                                     rule=(RB.BeeFlight
                                                           | (RB.CanWallJump & RB.JumpHeight6 & RB.CanSwing & RB.HellLogic)))
    world.get_region(regname.HONEYHOP1POND).connect(world.get_region(regname.HONEYHOP1CLOUDS),
                                                    rule=(RB.BeeFlight & (RB.CanSwing | RB.HardLogic))
                                                    | (RB.HellLogic & RB.CanWallSpin & RB.CanSwing & RB.CanBackflip))
    world.get_region(regname.HONEYHOP1POND).connect(world.get_region(regname.HONEYHOP1DICEROOM),
                                                    "Honeyhop: Pond Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.HONEYHOP1CLOUDS).connect(world.get_region(regname.HONEYHOP1QBBASE),
                                                      rule=RB.BeeFlight)
    world.get_region(regname.HONEYHOP1QBBASE).connect(world.get_region(regname.HONEYHOP1QBBUBBLE),
                                                      rule=RB.BeeFlight | RB.JumpHeight4 | RB.CanSideflip | RB.CanAirSpin
                                                           | RB.CanLongJump)
    world.get_region(regname.HONEYHOP1QBBUBBLE).connect(world.get_region(regname.HONEYHOP1QBTOP),
                                                        rule=(RB.BeeFlight | RB.CanWallJump)
                                                             & (RB.CanSwing | RB.BeeFlight | RB.CanWallSpin | (RB.HardLogic & RB.JumpHeight6)))
    world.get_region(regname.HONEYHOP).connect(world.get_region(regname.HONEYHOP2QBBASE), "Honeyhop Chimp Star")
    world.get_region(regname.HONEYHOP2QBBASE).connect(world.get_region(regname.HONEYHOP2QBBUBBLE),
                                                      "Honeyhop Chimp: Base Sling Star",
                                                      rule=RB.CanLaunchStar | RB.JumpHeight4 | RB.CanSideflip | RB.CanAirSpin
                                                           | RB.CanLongJump)
    world.get_region(regname.HONEYHOP2QBBUBBLE).connect(world.get_region(regname.HONEYHOP2QBTOP),
                                                        "Honeyhop Chimp: Cliff Pond Sling Star",
                                                        rule=(RB.CanLaunchStar | RB.CanWallJump)
                                                             & (RB.CanSwing | RB.CanWallSpin | (RB.HardLogic & RB.JumpHeight6)))
    # Starshine Beach
    world.get_region(regname.WORLD4).connect(world.get_region(regname.STARBEACH), "World 4 Slot 5 Galaxy")
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH1WATER), "Starshine Beach Star 1")
    world.get_region(regname.STARBEACH1WATER).connect(world.get_region(regname.STARBEACH1MAIN),
                                                      "Starshine Beach 1: Waterdrop Launch Star",
                                                      rule=RB.CanSwim & RB.CanLaunchStar)
    world.get_region(regname.STARBEACH1MAIN).connect(world.get_region(regname.STARBEACH1BONUS),
                                                      "Starshine Beach 1: Crabber Bonus Teleporter")
    world.get_region(regname.STARBEACH1MAIN).connect(world.get_region(regname.STARBEACH1COINR),
                                                      "Starshine Beach 1: Tropical Beach Green Pipe",
                                                     rule=RB.CanPipe)
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH2WATER), "Starshine Beach Star 2")
    world.get_region(regname.STARBEACH2WATER).connect(world.get_region(regname.STARBEACH2MAIN),
                                                      "Starshine Beach 2: Waterdrop Launch Star",
                                                      rule=RB.CanSwim)
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2DEEPW),
                                                     rule=RB.CanSwim)
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2BONUS),
                                                      "Starshine Beach 2: Crabber Bonus Teleporter")
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.STARBEACH2COINR),
                                                      "Starshine Beach 2: Tropical Beach Green Pipe",
                                                     rule=RB.CanPipe)
    world.get_region(regname.STARBEACH).connect(world.get_region(regname.STARBEACH3MAIN), "Starshine Beach Comet Star",
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
                                                     rule=RB.CanLaunchStar & (RB.JumpHeight3 | (RB.JumpHeight2 & RB.CanGrabLedge)))
    world.get_region(regname.CHOMWORK1ROLLING).connect(world.get_region(regname.CHOMWORK1BONUS),
                                                       "Chompworks 1: Bonus Room Pipe",
                                                       rule=RB.CanPipe)
    world.get_region(regname.CHOMWORK1ROLLING).connect(world.get_region(regname.CHOMWORK1FLIPSWAP),
                                                       "Chompworks 1: Rolling Chomps Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.CHOMWORK1FLIPSWAP).connect(world.get_region(regname.CHOMWORK1LAVA),
                                                        "Chompworks 1: Flipping Platforms Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.CHOMWORK).connect(world.get_region(regname.CHOMWORK2START), "Chompworks Star 2")
    world.get_region(regname.CHOMWORK2START).connect(world.get_region(regname.CHOMWORK2ROLLING),
                                                     "Chompworks 2: Start Launch Star",
                                                     rule=RB.CanLaunchStar & (RB.SPRONGIN | RB.HardLogic
                                                                              | ((RB.JumpHeight6 | RB.CanLongSpin) & RB.CanWallJump & RB.MediumLogic)
                                                                              | (RB.CanWallSpin & RB.CanBackflip & RB.MediumLogic)))
    world.get_region(regname.CHOMWORK2ROLLING).connect(world.get_region(regname.CHOMWORK2TOWER),
                                                       "Chompworks 2: Rolling Chomps Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.SPRONGIN
                                                                                | (RB.MediumLogic & ((RB.JumpHeight5 & RB.CanAirSpin) | RB.CanWallSpin))))
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
                                                       rule=RB.MediumLogic | (RB.CanBackflip & RB.CanAirSpin))
    world.get_region(regname.GRAVGAUN1WATERCO).connect(world.get_region(regname.GRAVGAUN1WHOMPWA))
    world.get_region(regname.GRAVGAUN1WHOMPWA).connect(world.get_region(regname.GRAVGAUNGSTAR2),
                                                       rule=RB.CanBackOrSideflip & RB.CanAirSpin)
    world.get_region(regname.GRAVGAUN1WHOMPWA).connect(world.get_region(regname.GRAVGAUN1DOORTOD),
                                                       "Gravity Gauntlet: Fire Wheel Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.GRAVGAUN1DOORTOD).connect(world.get_region(regname.GRAVGAUN1BOSSARE), rule=RB.CanPound)
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
    world.get_region(regname.GRAVGAUN2WATERCO).connect(world.get_region(regname.GRAVGAUN2WHOMPWA))
    # World 5
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD5), "World 5 Map",
                                           rule=(Has(itemname.GRAND, 4)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND5) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Space Storm
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SPACSTOR), "World 5 Slot 1 Galaxy")
    world.get_region(regname.SPACSTOR).connect(world.get_region(regname.SPACSTOR1PULL), "Space Storm Star 1")
    world.get_region(regname.SPACSTOR1PULL).connect(world.get_region(regname.SPACSTOR1SATELLITE),
                                                    "Space Storm 1: Pull to Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SPACSTOR1SATELLITE).connect(world.get_region(regname.SPACSTOR1REDCANOUT),
                                                    "Space Storm 1: Satellite Launch Star",
                                                         rule=RB.CanLaunchStar & (RB.CanLongJump | RB.MediumLogic))
    world.get_region(regname.SPACSTOR1REDCANOUT).connect(world.get_region(regname.SPACSTOR1REDCANIN))
    world.get_region(regname.SPACSTOR1REDCANIN).connect(world.get_region(regname.SPACSTOR1TOPMAN),
                                                    "Space Storm 1: Canister Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.SPACSTOR1TOPMAN).connect(world.get_region(regname.SPACSTOR1PULLPATH),
                                                    "Space Storm 1: Pull Star Path")
    world.get_region(regname.SPACSTOR).connect(world.get_region(regname.SPACSTOR2PULL), "Space Storm Star 2")
    world.get_region(regname.SPACSTOR2PULL).connect(world.get_region(regname.SPACSTOR2TOPTOWERBASE),
                                                    "Space Storm 2: Pull to Launch Star")
    world.get_region(regname.SPACSTOR2TOPTOWERBASE).connect(world.get_region(regname.SPACSTOR2TOPTOWER),
                                                    "Space Storm 2: Tower Base Sling Star",
                                                            rule=(RB.CanPound | RB.MediumLogic)
                                                                 & (RB.CanLaunchStar
                                                                    | (RB.JumpHeight4 & RB.CanWallSpin & RB.MediumLogic)))
    world.get_region(regname.SPACSTOR2TOPTOWERBASE).connect(world.get_region(regname.SPACSTOR2GSTAR2),
                                                            rule=(RB.JumpHeight4 & RB.CanWallSpin & RB.MediumLogic))
    world.get_region(regname.SPACSTOR2TOPTOWER).connect(world.get_region(regname.SPACSTOR2COINROOM),
                                                    "Space Storm 2: Tower Green Pipe",
                                                        rule=RB.CanPipe)
    world.get_region(regname.SPACSTOR2TOPTOWER).connect(world.get_region(regname.SPACSTOR2GSTAR2))
    # Boo Moon
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOOMOON), "World 5 Slot 2 Galaxy")
    world.get_region(regname.BOOMOON).connect(world.get_region(regname.BOOMOON1DARK), "Boo Moon Star 1")
    world.get_region(regname.BOOMOON1DARK).connect(world.get_region(regname.BOOMOON1GOOMBONUS),
                                                   "Boo Moon 1: Jack O'Goomba Bonus Teleporter")
    world.get_region(regname.BOOMOON1DARK).connect(world.get_region(regname.BOOMOON1POISON),
                                                   "Boo Moon 1: Dark Planet Launch Star",
                                                   rule=RB.CanLaunchStar)
    world.get_region(regname.BOOMOON1POISON).connect(world.get_region(regname.BOOMOON1MOON),
                                                   "Boo Moon 1: Poison Swamp Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.BOOMOON1MOON).connect(world.get_region(regname.BOOMOON1POPUP),
                                                   "Boo Moon 1: Moon Launch Star",
                                                   rule=RB.CanCollectStarChips & RB.CanLaunchStar
                                                        & (RB.JumpHeight3 | (RB.CanPound & RB.MediumLogic) | RB.HardLogic))
    world.get_region(regname.BOOMOON).connect(world.get_region(regname.BOOMOON2DARK), "Boo Moon Star 2")
    world.get_region(regname.BOOMOON2DARK).connect(world.get_region(regname.BOOMOON2GOOMBONUS),
                                                   "Boo Moon 2: Jack O'Gomba Bonus Teleporter")
    world.get_region(regname.BOOMOON2DARK).connect(world.get_region(regname.BOOMOON2TOWER),
                                                   "Boo Moon 2: Dark Planet Pipe",
                                                   rule=RB.CanPipe)
    # Upside Dizzy
    world.get_region(regname.WORLD5).connect(world.get_region(regname.UPDOWN), "World 5 Slot 3 Galaxy")
    world.get_region(regname.UPDOWN).connect(world.get_region(regname.UPDOWNCASTLE), "Upside Dizzy Castle")
    world.get_region(regname.UPDOWNCASTLE).connect(world.get_region(regname.UPDOWNINSTART),
                                                   "Upside Dizzy: Castle Pipe",
                                                   rule=RB.CanPipe)
    world.get_region(regname.UPDOWNINSTART).connect(world.get_region(regname.UPDOWNFIRE),
                                                   "Upside Dizzy: 1st Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.UPDOWNFIRE).connect(world.get_region(regname.UPDOWNBREAKER),
                                                   "Upside Dizzy: Fiery Orange Pipe",
                                                 rule=RB.CanPipe & RB.FireMario)
    world.get_region(regname.UPDOWNINSTART).connect(world.get_region(regname.UPDOWNINEND),
                                                    rule=RB.JumpHeight3 | (RB.HellLogic & RB.CanLongJump))
    world.get_region(regname.UPDOWNINEND).connect(world.get_region(regname.UPDOWNGRAV),
                                                   "Upside Dizzy: Final Green Pipe",
                                                   rule=RB.CanPipe & (RB.CanPound | (RB.HardLogic & RB.CanAirSpin)
                                                   | (RB.CanBackflip & RB.CanWallJump & RB.HellLogic)))
    # Slipsand
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SLIPSAND), "World 5 Slot 4 Galaxy")
    world.get_region(regname.SLIPSAND).connect(world.get_region(regname.SLIPSAND1LONG), "Slipsand Star 1")
    world.get_region(regname.SLIPSAND1LONG).connect(world.get_region(regname.SLIPSAND1COINROOM),
                                                    "Slipsand 1: Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.SLIPSAND1LONG).connect(world.get_region(regname.SLIPSAND1CUBE),
                                                    "Slipsand 1: Long Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SLIPSAND1CUBE).connect(world.get_region(regname.SLIPSAND1SLIDE),
                                                    "Slipsand 1: Cube Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SLIPSAND1SLIDE).connect(world.get_region(regname.SLIPSAND1BOSS),
                                                    "Slipsand 1: Slide Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.SLIPSAND).connect(world.get_region(regname.SLIPSAND2LONG1), "Slipsand Star 2")
    world.get_region(regname.SLIPSAND2LONG1).connect(world.get_region(regname.SLIPSAND2GRAV),
                                                    "Slipsand 2: Green Pipe",
                                                     rule=RB.CanPipe)
    world.get_region(regname.SLIPSAND2LONG1).connect(world.get_region(regname.SLIPSAND2LONG2),
                                                     rule=RB.MediumLogic & RB.CanAirSpin)
    world.get_region(regname.SLIPSAND2GRAV).connect(world.get_region(regname.SLIPSAND2LONG2),
                                                    "Slipsand 2: Orange Pipe",
                                                    rule=RB.CanPipe & (RB.CanWallJump | RB.CanGrabLedge
                                                         | RB.JumpHeight3 | (RB.HardLogic & RB.CanDouble)))
    world.get_region(regname.SLIPSAND2LONG2).connect(world.get_region(regname.SLIPSAND2LONG3))
    world.get_region(regname.SLIPSAND2LONG2).connect(world.get_region(regname.SLIPSAND2BIRD),
                                                    "Slipsand 2: Long Launch Star",
                                                     rule=RB.CanLaunchStar)
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
    world.get_region(regname.FLEETGLIDE).connect(world.get_region(regname.FLEETGLIDE1START))
    world.get_region(regname.FLEETGLIDE1START).connect(world.get_region(regname.FLEETGLIDE1COURSE),
                                                      rule=RB.CanRideBird)
    world.get_region(regname.FLEETGLIDE).connect(world.get_region(regname.FLEETGLIDE2START),
                                                 rule=(CanReachLocation(locname.BATTBELTSTAR1,
                                                                          parent_region_name=regname.BATTBELT1CHOM)
                                                       & RB.MailtoadOpen))
    world.get_region(regname.FLEETGLIDE2START).connect(world.get_region(regname.FLEETGLIDE2COURSE),
                                                       rule=RB.CanRideBird)
    #Shiverburn
    world.get_region(regname.WORLD5).connect(world.get_region(regname.SHIVBURN), "World 5 Slot 6 Galaxy")
    world.get_region(regname.SHIVBURN).connect(world.get_region(regname.SHIVBURN1VOLCANO), "Shiverburn Star")
    world.get_region(regname.SHIVBURN1VOLCANO).connect(world.get_region(regname.SHIVBURN3CHIMP),
                                                       "Shiverburn: Green Pipe",
                                                       rule=RB.CanPipe & ((RB.CanMakeCloud & (RB.CanPound | RB.CanLongJump | RB.HardLogic))
                                                       | (RB.HardLogic & RB.CanPound & (RB.CanLongJump | RB.HellLogic))))
    world.get_region(regname.SHIVBURN1VOLCANO).connect(world.get_region(regname.SHIVBURN1LAVA),
                                                       "Shiverburn: Volcano Launch Star",
                                                       rule=RB.CanLaunchStar & ((RB.CanMakeCloud & (RB.CanPound | RB.CanLongJump | RB.HardLogic))
                                                       | (RB.HardLogic & RB.CanPound & (RB.CanLongJump | RB.HellLogic))))
    world.get_region(regname.SHIVBURN1LAVA).connect(world.get_region(regname.SHIVBURN1FIREICE),
                                                       "Shiverburn: Lava Ball Launch Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.SHIVBURN1FIREICE).connect(world.get_region(regname.SHIVBURN1TOAD),
                                                       "Shiverburn: Lava Ice Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.SHIVBURN1TOAD).connect(world.get_region(regname.SHIVBURN1BOSS),
                                                       "Shiverburn: Green Toadship Launch Star",
                                                    rule=RB.CanLaunchStar)
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
                                                       "Shiverburn Comet: Green Toadship Launch Star",
                                                    rule=RB.CanLaunchStar)
    # Boom Bunker
    world.get_region(regname.WORLD5).connect(world.get_region(regname.BOWJR3), "World 5 Slot 7 Galaxy")
    world.get_region(regname.BOWJR3).connect(world.get_region(regname.BOOMBUNK1HAMMER), "Boom Bunker Grand Star")
    world.get_region(regname.BOOMBUNK1HAMMER).connect(world.get_region(regname.BOOMBUNK1BOOMER),
                                                      "Boom Bunker: Hammer Hilt Cannon",
                                                      rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK1BOOMER).connect(world.get_region(regname.BOOMBUNK1CHECK),
                                                      "Boom Bunker: Fort Launch Star",
                                                      rule=RB.CanLaunchStar)
    world.get_region(regname.BOOMBUNK1CHECK).connect(world.get_region(regname.BOOMBUNK1PLAT),
                                                      "Boom Bunker: Checkpoint Cannon",
                                                     rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK1PLAT).connect(world.get_region(regname.BOOMBUNK1BOSS),
                                                      "Boom Bunker: Platform Launch Star",
                                                    rule=RB.CanLaunchStar & RB.CanPound & (RB.CanMakeCloud | RB.HardLogic))
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
                                                      "Boom Bunker Comet: Fort Launch Star",
                                                      rule=RB.CanLaunchStar)
    world.get_region(regname.BOOMBUNK2CHECK).connect(world.get_region(regname.BOOMBUNK2DARK),
                                                      "Boom Bunker Comet: Checkpoint Cannon",
                                                     rule=RB.CanCannon)
    world.get_region(regname.BOOMBUNK2DARK).connect(world.get_region(regname.BOOMBUNK2BOSS),
                                                      "Boom Bunker Comet: Dark Matter Launch Star",
                                                    rule=RB.CanMakeCloud & RB.CanLaunchStar)
    # World 6
    world.get_region(regname.SHIP).connect(world.get_region(regname.WORLD6), "World 6 Map",
                                           rule=(Has(itemname.GRAND, 5)&OptionFilter(WorldShuffle, WorldShuffle.option_Progressive))
                                                | (Has(itemname.GRAND6) & OptionFilter(WorldShuffle, WorldShuffle.option_Keyed_Grand_Stars))
                                                | RB.OpenWorlds)
    # Melty Monster
    world.get_region(regname.WORLD6).connect(world.get_region(regname.MELTY), "World 6 Slot 1 Galaxy")
    world.get_region(regname.MELTY).connect(world.get_region(regname.MELTY1LANDING), "Melty Monster Star 1")
    world.get_region(regname.MELTY1LANDING).connect(world.get_region(regname.MELTY3CHIMP),
                                                    "Melty Monster 1: Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.MELTY1LANDING).connect(world.get_region(regname.MELTY1MAGMAARG),
                                                    "Melty Monster 1: Pull Star Path")
    world.get_region(regname.MELTY1MAGMAARG).connect(world.get_region(regname.MELTY1LAVAWAVE1),
                                                    "Melty Monster 1: Magmaargh Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.MELTY1LAVAWAVE1).connect(world.get_region(regname.MELTY1LAVAWAVE2),
                                                      rule=(RB.CanClimbPole | RB.MediumLogic))
    world.get_region(regname.MELTY1LAVAWAVE2).connect(world.get_region(regname.MELTY1LAVAWAVE3))
    world.get_region(regname.MELTY1LAVAWAVE3).connect(world.get_region(regname.MELTY1MAGMAW),
                                                      "Melty Monster 1: Lava Wave Launch Star",
                                                      rule=RB.CanSwing & RB.CanLaunchStar)
    world.get_region(regname.MELTY).connect(world.get_region(regname.MELTY2LANDING), "Melty Monster Star 2")
    world.get_region(regname.MELTY2LANDING).connect(world.get_region(regname.MELTY3CHIMP),
                                                    "Melty Monster 2: Green Pipe")
    world.get_region(regname.MELTY2LANDING).connect(world.get_region(regname.MELTY2BOWLING),
                                                    "Melty Monster 2: Roll to Launch Star",
                                                    rule=RB.ROCKNROLLIN & RB.CanLaunchStar)
    # Clockwork Ruins
    world.get_region(regname.WORLD6).connect(world.get_region(regname.CLOCKWORK), "World 6 Slot 2 Galaxy")
    world.get_region(regname.CLOCKWORK).connect(world.get_region(regname.CLOCKWORK1COGS), "Clockwork Ruins Star")
    world.get_region(regname.CLOCKWORK1COGS).connect(world.get_region(regname.CLOCKWORK1PUSH),
                                                     "Clockwork Ruins: Cog Wall Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.CLOCKWORK1PUSH).connect(world.get_region(regname.CLOCKWORK1WHEELSB),
                                                     "Clockwork Ruins: Push Block Launch Star",
                                                     rule=RB.CanPound & RB.CanLaunchStar)
    world.get_region(regname.CLOCKWORK1WHEELSB).connect(world.get_region(regname.CLOCKWORK1WHEELST),
                                                        rule=RB.CanWallJump & RB.CanSwing & (RB.CanPound | RB.JumpHeight5))
    world.get_region(regname.CLOCKWORK1WHEELST).connect(world.get_region(regname.CLOCKWORK1COINROOM),
                                                     "Clockwork Ruins: Wheel Planet Green Pipe",
                                                        rule=RB.CanPipe)
    world.get_region(regname.CLOCKWORK1COGS).connect(world.get_region(regname.CLOCKWORK3HAMMER),
                                                     "Clockwork Ruins: Hungry Luma",
                                                     rule=RB.CanLaunchStar & ((RB.CoinLumaBase|
                                                           (OptionFilter(CoinLumaLocks,2)&Has(itemname.COINHL6)))
                                                     & RB.CoinLumaRule(world.options.coin_luma_counts.value["Clockwork Ruins Coin Luma"])))
    world.get_region(regname.CLOCKWORK3HAMMER).connect(world.get_region(regname.CLOCKWORK3HAMMERTOP),
                                                     "Clockwork Ruins Hungry Luma: Hammer Zone Green Pipe",
                                                       rule=RB.CanPipe | (RB.MediumLogic & RB.JumpHeight6 & RB.CanWallJump)
                                                       | (RB.HardLogic & RB.JumpHeight5 & RB.CanWallSpin))
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
                                                       rule=RB.CanDinoBlimp & RB.CanLaunchStar)
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
                                                      rule=RB.CanSwim)
    world.get_region(regname.SLIMSPRI1MOUTH1).connect(world.get_region(regname.SLIMSPRI1CHESTROOM),
                                                      "Slimy Spring: Green Pipe",
                                                      rule=RB.CanPipe & (RB.CanGrabLedge | RB.JumpHeight3 | (RB.CanDouble & RB.MediumLogic)))
    world.get_region(regname.SLIMSPRI1CAVE1).connect(world.get_region(regname.SLIMSPRI1MOUTH2),
                                                     "Slimy Spring: First Cave Launch Star",
                                                     rule=(RB.CanSwim & (RB.CanShell | RB.HardLogic)))
    world.get_region(regname.SLIMSPRI1MOUTH2).connect(world.get_region(regname.SLIMSPRI1CAVE2),
                                                      rule=RB.CanSwim)
    world.get_region(regname.SLIMSPRI).connect(world.get_region(regname.SLIMSPRI2MOUTH1), "Slimy Spring Chimp Star")
    world.get_region(regname.SLIMSPRI2MOUTH1).connect(world.get_region(regname.SLIMSPRI2CAVE1),
                                                      rule=RB.CanSwim)
    world.get_region(regname.SLIMSPRI2CAVE1).connect(world.get_region(regname.SLIMSPRI2MOUTH2),
                                                     "Slimy Spring Chimp: First Cave Launch Star",
                                                     rule=(RB.CanSwim & (RB.CanShell | RB.HardLogic)))
    world.get_region(regname.SLIMSPRI2MOUTH2).connect(world.get_region(regname.SLIMSPRI2CAVE2),
                                                      rule=RB.CanSwim)
    # Battle Belt
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BATTLEBELT), "World 6 Slot 6 Galaxy")
    world.get_region(regname.BATTLEBELT).connect(world.get_region(regname.BATTBELT1GOOM), "Battle Belt Star")
    world.get_region(regname.BATTBELT1GOOM).connect(world.get_region(regname.BATTBELT1LAVA),
                                                    "Battle Belt: Goomba Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1LAVA).connect(world.get_region(regname.BATTBELT1URCH),
                                                    "Battle Belt: Li'l Cinders Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1URCH).connect(world.get_region(regname.BATTBELT1CRAB),
                                                    "Battle Belt: Urchin Sling Star",
                                                    rule=RB.CanLaunchStar & (RB.FireMario | (RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.BATTBELT1CRAB).connect(world.get_region(regname.BATTBELT1PTOA),
                                                    "Battle Belt: Crabber Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1PTOA).connect(world.get_region(regname.BATTBELT1PUMP),
                                                    "Battle Belt: Pink Toadship Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1PUMP).connect(world.get_region(regname.BATTBELT1PUMI),
                                                    "Battle Belt: Jack O'Goomba Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.BATTBELT1PUMP).connect(world.get_region(regname.BATTBELT1RTOA),
                                                    "Battle Belt: Jack O'Goomba Sling Star",
                                                    rule=RB.CanLaunchStar & RB.CanPipe & (RB.CanShell & RB.CanSwim))
    world.get_region(regname.BATTBELT1RTOA).connect(world.get_region(regname.BATTBELT1ICEP),
                                                    "Battle Belt: Red Toadship Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1ICEP).connect(world.get_region(regname.BATTBELT3BOSS),
                                                    "Battle Belt: Hungry Luma",
                                                    rule=RB.CanLaunchStar
                                                         & ((RB.CoinLumaBase |
                                                           (OptionFilter(CoinLumaLocks, 2) & Has(itemname.COINHL7)))
                                                          & (True_() if world.options.coin_luma_counts.value[
                                                                            "Battle Belt Coin Luma"] < 100
                                                             else Has("Can Farm Coins"))))
    world.get_region(regname.BATTBELT1ICEP).connect(world.get_region(regname.BATTBELT1MOLE),
                                                    "Battle Belt: Li'l Brr Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT1MOLE).connect(world.get_region(regname.BATTBELT1MOLI),
                                                    "Battle Belt: Swaphopper Green Pipe",
                                                    rule=RB.CanPipe & RB.CanPound)
    world.get_region(regname.BATTBELT1MOLE).connect(world.get_region(regname.BATTBELT1CHOM),
                                                    "Battle Belt: Swaphopper Sling Star",
                                                    rule=RB.CanLaunchStar & CanReachEntrance("Battle Belt: Swaphopper Green Pipe"))
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
                                                    "Battle Belt Comet: Goomba Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2LAVA).connect(world.get_region(regname.BATTBELT2URCH),
                                                    "Battle Belt Comet: Li'l Cinders Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2URCH).connect(world.get_region(regname.BATTBELT2CRAB),
                                                    "Battle Belt Comet: Urchin Sling Star",
                                                    rule=RB.CanLaunchStar & (RB.FireMario | (RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.BATTBELT2CRAB).connect(world.get_region(regname.BATTBELT2PTOA),
                                                    "Battle Belt Comet: Crabber Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2PTOA).connect(world.get_region(regname.BATTBELT2PUMP),
                                                    "Battle Belt Comet: Yellow Toadship Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2PUMP).connect(world.get_region(regname.BATTBELT2PUMI),
                                                    "Battle Belt Comet: Jack O'Goomba Green Pipe",
                                                    rule=RB.CanPipe)
    world.get_region(regname.BATTBELT2PUMP).connect(world.get_region(regname.BATTBELT2RTOA),
                                                    "Battle Belt Comet: Jack O'Goomba Sling Star",
                                                    rule=RB.CanLaunchStar & RB.CanPipe & RB.CanShell & RB.CanSwim)
    world.get_region(regname.BATTBELT2RTOA).connect(world.get_region(regname.BATTBELT2ICEP),
                                                    "Battle Belt Comet: Red Toadship Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2ICEP).connect(world.get_region(regname.BATTBELT2MOLE),
                                                    "Battle Belt Comet: Li'l Brr Sling Star",
                                                    rule=RB.CanLaunchStar)
    world.get_region(regname.BATTBELT2MOLE).connect(world.get_region(regname.BATTBELT2MOLI),
                                                    "Battle Belt Comet: Swaphopper Green Pipe",
                                                    rule=RB.CanPipe & RB.CanPound)
    world.get_region(regname.BATTBELT2MOLE).connect(world.get_region(regname.BATTBELT2CHOM),
                                                    "Battle Belt Comet: Swaphopper Sling Star",
                                                    rule=RB.CanPound & RB.CanPipe & RB.CanLaunchStar)
    # Galaxy Generator
    world.get_region(regname.WORLD6).connect(world.get_region(regname.BOWSER3), "World 6 Slot 7 Galaxy")
    world.get_region(regname.BOWSER3).connect(world.get_region(regname.GALGEN1LANDING), "Galaxy Generator Grand Star")
    world.get_region(regname.GALGEN1LANDING).connect(world.get_region(regname.GALGEN1HAMMER),
                                                     "Galaxy Generator: Landing Launch Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.GALGEN1HAMMER).connect(world.get_region(regname.GALGEN1VOLCANO))
    world.get_region(regname.GALGEN1VOLCANO).connect(world.get_region(regname.GALGEN1LAVACYL),
                                                     rule=RB.DRILLMASTER)
    world.get_region(regname.GALGEN1LAVACYL).connect(world.get_region(regname.GALGEN1TOWER),
                                                     "Galaxy Generator: Lava Cylinder Launch Star",
                                                     rule=RB.DRILLMASTER & RB.CanLaunchStar)
    world.get_region(regname.GALGEN1TOWER).connect(world.get_region(regname.GALGEN1YOSHI),
                                                     "Galaxy Generator: Tower Launch Star",
                                                   rule=RB.CanLaunchStar & (RB.CanMakeCloud | RB.CanWallSpin | RB.CanLongSpin
                                                                            | (RB.CanAirSpin & RB.MediumLogic)))
    world.get_region(regname.GALGEN1YOSHI).connect(world.get_region(regname.GALGEN1DASHCAS),
                                                   rule=(RB.CanDinoSwing
                                                         | (RB.CanMakeCloud & CanLongJump & RB.CanWallJump & RB.HardLogic)))
    world.get_region(regname.GALGEN1DASHCAS).connect(world.get_region(regname.GALGEN1LAVASNA),
                                                     "Galaxy Generator: Dash Castle Sling Star",
                                                     rule=RB.CanLaunchStar & (RB.CanDinoRun
                                                           | (RB.CanMakeCloud & RB.CanLongJump & RB.JumpHeight6 & RB.HardLogic)))
    world.get_region(regname.GALGEN1LAVASNA).connect(world.get_region(regname.GALGEN1STATUE))
    world.get_region(regname.GALGEN1STATUE).connect(world.get_region(regname.GALGEN1THEDOOR),
                                                    rule=RB.CanClimbPole)
    world.create_entrance(world.get_region(regname.GALGEN1YOSHI),world.get_region(regname.GALGEN1THEDOOR), # Trick Entrance
                          RB.CanInfiniteFlutter&RB.CanAirSpin&RB.CanSideflip)
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
                                                     "Galaxy Generator Comet: Landing Sling Star",
                                                     rule=RB.CanLaunchStar)
    world.get_region(regname.GALGEN2BOOMER).connect(world.get_region(regname.GALGEN2VOLCANO))
    world.get_region(regname.GALGEN2VOLCANO).connect(world.get_region(regname.GALGEN2LAVACYL),
                                                     rule=RB.DRILLMASTER)
    world.get_region(regname.GALGEN2LAVACYL).connect(world.get_region(regname.GALGEN2TOWER),
                                                     "Galaxy Generator Comet: Lava Cylinder Launch Star",
                                                     rule=RB.DRILLMASTER & RB.CanLaunchStar)
    world.get_region(regname.GALGEN2TOWER).connect(world.get_region(regname.GALGEN2YOSHI),
                                                   "Galaxy Generator Comet: Tower Launch Star",
                                                   rule=RB.CanLaunchStar & (RB.CanMakeCloud | RB.CanWallSpin | RB.CanLongSpin
                                                         | (RB.CanAirSpin & RB.MediumLogic)))
    world.get_region(regname.GALGEN2YOSHI).connect(world.get_region(regname.GALGEN2DASHCAS),
                                                   rule=(RB.CanDinoSwing
                                                         | (RB.CanMakeCloud & CanLongJump & RB.CanWallJump & RB.HellLogic))
                                                   )
    world.get_region(regname.GALGEN2DASHCAS).connect(world.get_region(regname.GALGEN2LAVASNA),
                                                     "Galaxy Generator Comet: Dash Castle Sling Star",
                                                     rule=RB.CanLaunchStar & (RB.CanDinoRun
                                                           | (RB.CanMakeCloud & RB.CanLongJump & RB.JumpHeight6 & RB.HellLogic))                                                  )
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
                                                        "Boss Blitz: Dino Piranha Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ1KINGKAL).connect(world.get_region(regname.BOSSBLITZ1MAJORBU),
                                                        "Boss Blitz: King Kaliente Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ1MAJORBU).connect(world.get_region(regname.BOSSBLITZ1BOULDER),
                                                        "Boss Blitz: Major Burrows Launch Star",
                                                        rule=RB.CanPound & RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ1BOULDER).connect(world.get_region(regname.BOSSBLITZ1TINYMET),
                                                        "Boss Blitz: Bouldergeist Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ1TINYMET).connect(world.get_region(regname.BOSSBLITZ1FIREDIN),
                                                        "Boss Blitz: Tiny Meteor Launch Star",
                                                        rule=RB.CanLaunchStar)
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
                                                        "Boss Blitz Comet: Dino Piranha Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ2KINGKAL).connect(world.get_region(regname.BOSSBLITZ2MAJORBU),
                                                        "Boss Blitz Comet: King Kaliente Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ2MAJORBU).connect(world.get_region(regname.BOSSBLITZ2BOULDER),
                                                        "Boss Blitz Comet: Major Burrows Launch Star",
                                                        rule=RB.CanPound & RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ2BOULDER).connect(world.get_region(regname.BOSSBLITZ2TINYMET),
                                                        "Boss Blitz Comet: Bouldergeist Launch Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.BOSSBLITZ2TINYMET).connect(world.get_region(regname.BOSSBLITZ2FIREDIN),
                                                        "Boss Blitz Comet: Tiny Meteor Launch Star",
                                                        rule=RB.CanLaunchStar)
    # Flip-Out Galaxy
    world.get_region(regname.WORLD7).connect(world.get_region(regname.FLIPOUT), "World 7 Slot 6 Galaxy")
    world.get_region(regname.FLIPOUT).connect(world.get_region(regname.FLIPOUT1LANDING), "Flip-Out Star")
    world.get_region(regname.FLIPOUT1LANDING).connect(world.get_region(regname.FLIPOUT1CLIMB), "Flip-Out: Green Pipe",
                                                      rule=RB.CanPipe)
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
    world.get_region(regname.FLIPOUT2LANDING).connect(world.get_region(regname.FLIPOUT2CLIMB), "Flip-Out Comet: Green Pipe",
                                                      rule=RB.CanPipe)
    # Grandmaster Galaxy
    world.get_region(regname.WORLD7).connect(world.get_region(regname.GRANDMASTER), "World 7 Slot 7 Galaxy")
    world.get_region(regname.GRANDMASTER).connect(world.get_region(regname.GRANDMASTER1YOSHI), "Grandmaster Star")
    world.get_region(regname.GRANDMASTER1YOSHI).connect(world.get_region(regname.GRANDMASTER1SWITCH),
                                                        "Grandmaster: Yoshi Flower Launch Star",
                                                        rule=RB.CanDinoSwing & RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER1SWITCH).connect(world.get_region(regname.GRANDMASTER1CLOUD),
                                                        "Grandmaster: Flipswitch Launch Star",
                                                         rule=RB.CanLaunchStar),
    world.get_region(regname.GRANDMASTER1CLOUD).connect(world.get_region(regname.GRANDMASTER1SWAP),
                                                        "Grandmaster: Electric Clouds Launch Star",
                                                        rule=RB.CanMakeCloud & RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER1SWAP).connect(world.get_region(regname.GRANDMASTER1PULL),
                                                        "Grandmaster: Flip-Swap Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.JumpHeight4 | RB.MediumLogic))
    world.get_region(regname.GRANDMASTER1PULL).connect(world.get_region(regname.GRANDMASTER1BROS1),
                                                        "Grandmaster: Pull Star Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER1BROS1).connect(world.get_region(regname.GRANDMASTER1BROS2),
                                                        "Grandmaster: Bros Landing Sling Star",
                                                        rule=RB.CanLaunchStar)
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
                                                        rule=RB.CanDinoSwing & RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER2SWITCH).connect(world.get_region(regname.GRANDMASTER2CLOUD),
                                                        "Grandmaster Comet: Flipswitch Launch Star",
                                                         rule=RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER2CLOUD).connect(world.get_region(regname.GRANDMASTER2SWAP),
                                                        "Grandmaster Comet: Electric Clouds Launch Star",
                                                         rule=RB.CanMakeCloud & RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER2SWAP).connect(world.get_region(regname.GRANDMASTER2PULL),
                                                        "Grandmaster Comet: Flip-Swap Launch Star",
                                                       rule=RB.CanLaunchStar & (RB.JumpHeight4 | RB.MediumLogic))
    world.get_region(regname.GRANDMASTER2PULL).connect(world.get_region(regname.GRANDMASTER2BROS1),
                                                        "Grandmaster Comet: Pull Star Launch Star",
                                                       rule=RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER2BROS1).connect(world.get_region(regname.GRANDMASTER2BROS2),
                                                        "Grandmaster Comet: Bros Landing Sling Star",
                                                        rule=RB.CanLaunchStar)
    world.get_region(regname.GRANDMASTER2BROS2).connect(world.get_region(regname.GRANDMASTER2ROSA),
                                                        "Grandmaster Comet: Jumping Bros Launch Star",
                                                        rule=RB.CanLaunchStar)

    # Special connections if power-up rando is on
    # Rainbow Star
    world.get_region(regname.SKYOBS1OCTOBONUS).connect(world.get_region(regname.FIRSTSUPASTAR))
    world.get_region(regname.SKYOBS2STARTBOTTOM).connect(world.get_region(regname.FIRSTSUPASTAR))
    world.get_region(regname.SKYOBS2OCTOBONUS).connect(world.get_region(regname.FIRSTSUPASTAR))
    world.get_region(regname.SPINDIG1BONUS).connect(world.get_region(regname.FIRSTSUPASTAR))
    world.get_region(regname.GOODEGG3MUDDY).connect(world.get_region(regname.FIRSTSUPASTAR))
    world.get_region(regname.SHIVBURN2ROMP).connect(world.get_region(regname.FIRSTSUPASTAR))
    # Springshroom
    world.get_region(regname.CHOMWORK2ROLLING).connect(world.get_region(regname.FIRSTSPRING))
    # Fire Flower
    world.get_region(regname.RIGHTDOWNBREAKER).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.RIGHTDOWNCOINROOM).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.UPDOWNBREAKER).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.UPDOWNFIRE).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.SLIPSAND1CUBE).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.SLIPSAND1BOSS).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.SLIPSAND3BOSS).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.FREEFLAK1LOGCABI).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.BATTBELT1URCH).connect(world.get_region(regname.FIRSTFIREFLOWER))
    world.get_region(regname.BATTBELT2URCH).connect(world.get_region(regname.FIRSTFIREFLOWER))
    # Bee Mushroom
    world.get_region(regname.HONEYBLOOM1WALL2).connect(world.get_region(regname.FIRSTBEEMARIO))
    world.get_region(regname.HONEYHOP1START).connect(world.get_region(regname.FIRSTBEEMARIO))
    # Rockshroom
    world.get_region(regname.FREEFLAK2LOGCABI).connect(world.get_region(regname.FIRSTROCK))
    world.get_region(regname.MELTY2BOWLING).connect(world.get_region(regname.FIRSTROCK))
    world.get_region(regname.MELTY3CHIMP).connect(world.get_region(regname.FIRSTROCK))
    world.get_region(regname.BOULBOWL1CRYSTAL).connect(world.get_region(regname.FIRSTROCK))
    world.get_region(regname.BOULBOWL2CAGEPLA).connect(world.get_region(regname.FIRSTROCK))
    # Booshroom
    world.get_region(regname.BOOMOON2TOWER).connect(world.get_region(regname.FIRSTBOOMARIO))
    # Cloud Flower
    world.get_region(regname.FLUFFBLUFF1LANDING).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.PUZZPLAN3BUGABO).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.CLOUCOUR1LANDING).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.STARBEACH2MAIN).connect(world.get_region(regname.FIRSTCLOUD),
                                                     rule=RB.CanSwim & RB.CanPound)
    world.get_region(regname.WHOMP2FORT).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.WHOMP3FORT).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.BOOMBUNK1PLAT).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.GALGEN1TOWER).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.GALGEN2TOWER).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.SHIP2).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.TWISTY1PLAT1).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.GRANDMASTER1CLOUD).connect(world.get_region(regname.FIRSTCLOUD))
    world.get_region(regname.GRANDMASTER2CLOUD).connect(world.get_region(regname.FIRSTCLOUD))
    # Spin Drill
    world.get_region(regname.SPINDIG1TETRA).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.SPINDIG2DARKIN1).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.SUPMASS1KOOPAS).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.SUPMASS2KOOPAS).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.FLIPVILL2MAZESTART).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.FLIPVILL3GRAVITY).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.COSMIC2WATERPL1).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.GALGEN1VOLCANO).connect(world.get_region(regname.FIRSTSPINDRILL))
    world.get_region(regname.GALGEN2VOLCANO).connect(world.get_region(regname.FIRSTSPINDRILL))

    world.get_region(regname.SHIP).connect(world.get_region(regname.SHIP2)),
    world.get_region(regname.SHIP2).connect(world.get_region(regname.SHIPINSIDE)),
    world.get_region(regname.SHIP2).connect(world.get_region(regname.SHIPLEFTEAR), "Starship Mario Left Ear Pipe",
                                            rule=RB.CanPipe),
    world.get_region(regname.SHIP2).connect(world.get_region(regname.SHIPSTARSHROOM), "Starship Mario Right Ear Teleporter"),
    world.set_completion_rule(Has("Peach"))
