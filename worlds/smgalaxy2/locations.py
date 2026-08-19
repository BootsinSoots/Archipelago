from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, Has, True_, CanReachRegion, CanReachLocation, HasFromList, HasGroup, \
    CanReachEntrance

from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname
from . import Rules as RB


class SMG2Location(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, address: Optional[int], parent: Optional[Region]):
        super(SMG2Location, self).__init__(player, name,
                                           list(all_location_table.keys()).index(name)
                                           if name in all_location_table.keys() else None,
                                           parent)
        self.data = all_location_table[name] if name in all_location_table else \
            event_locations[name] if name in event_locations else None

class SMG2LocationData(NamedTuple):
    location_groups: list[str]
    galaxy: str # What galaxy the location is in
    region: str # The specific region the locations is in
    default_access: Optional[Rule[Any]] = None
    game_address: Optional[int] = 0
    locked_item: Optional[str] = None


# Sky Station S
SKYOBS_loc: dict[str, SMG2LocationData] = {
    locname.SKYSTASTAR1: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS1BOSS),
    locname.SKYSTASTAR2: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS2GRASSFLEET,
                                          (RB.CanClimbPole | RB.JumpHeight2 | RB.CanGrabLedge | RB.MediumLogic)),
    locname.SKYSTASTAR3: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS3BOSS),
}

# Yoshi Star St
YOSHTAR_loc: dict[str, SMG2LocationData] = {
    locname.YOSHSTARSTAR1: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG1FOSSIL, (RB.CanDinoSwing | RB.CanInfiniteFlutter)),
    locname.YOSHSTARSTAR2: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG2BOSS,
                                            (RB.CanDinoSwing | RB.CanInfiniteFlutter | RB.CanBackOrSideflip)),
    locname.YOSHSTARSTAR3: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG3MUDDY , RB.SUPAPOWA),
}

# Spin-Dig Star
SPINDIG_loc: dict[str, SMG2LocationData] = {
    locname.SPINDIGSTAR1: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG1BOSS, RB.DRILLMASTER),
    locname.SPINDIGSTAR2: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG2SQUARE, RB.DRILLMASTER),
    locname.SPINDIGSTAR3: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG3BOSS, RB.DRILLMASTER),
}

# Fluffy Bluff
FLUFBLUF_loc: dict[str, SMG2LocationData] = {
    locname.FLUFBLUFSTAR1: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF1TREECLIMB,
                                            RB.CanMakeCloud | (RB.JumpHeight6 & RB.CanLongJump & RB.HellLogic)),
    locname.FLUFBLUFSTAR2: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF2LANDING,
                                            ((CanReachRegion(regname.FLUFFBLUFF2CLIFF)&(RB.CanClimbPole|RB.JumpHeight5)
                                              &CanReachRegion(regname.FLUFFBLUFF2TREE)))
                                            & RB.PowerStarCount(15) & RB.MailtoadOpen
                                            & (RB.CanAirSpin | RB.MediumLogic)),
    locname.FLUFBLUFSTAR3: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF3TOWER, RB.CanMakeCloud
                                            | (RB.CloudMario & RB.HardLogic))
}


# Rightside Dow
RIGHTDOWN_loc: dict[str, SMG2LocationData] = {
    locname.RIGHTDOWNSTAR1: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN,
                                             regname.RIGHTDOWNTOPVIEW),
    locname.RIGHTDOWNSTAR2: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN,
                                             regname.RIGHTDOWNBREAKER, RB.FireMario),
}

# Flip-Swap Sta
FLIPSWAP_loc: dict[str, SMG2LocationData] = {
    locname.FLIPSWAPSTAR1: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP,
                                            regname.FLIPSWAP1,
                                            (RB.CanAirSpin | RB.CanLongJump | RB.HardLogic)),
    locname.FLIPSWAPSTAR2: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP,
                                            regname.FLIPSWAP2,
                                            RB.CanAirSpin | RB.HardLogic),
}

# Bowser Jr.s F
FIREFLOT_loc: dict[str, SMG2LocationData] = {
locname.FIREFLOTSTAR1:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT1BOSS),
locname.FIREFLOTSTAR2:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT2BOSS),
}

# World 2
# Puzzle Plank
PUZZPLANK_loc: dict[str, SMG2LocationData] = {
    locname.PUZZPLANKSTAR1:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN1MANDIB, RB.CanPound),
    locname.PUZZPLANKSTAR2:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN2COINRO),
    locname.PUZZPLANKSTAR3:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN3BUGABO, RB.CanMakeCloud&RB.CanPound),
}

# Hightail Fall
HIGHFALL_loc: dict[str, SMG2LocationData] = {
    locname.HIGHFALLSTAR1:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL1DASHWAL2),
    locname.HIGHFALLSTAR2:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL2DASHWAL2),
    locname.HIGHFALLSTAR3:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL3SILVERS),
}

# Boulder Bowl
ROCKBOWL_loc: dict[str, SMG2LocationData] = {
    locname.ROCKBOWLSTAR1:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL1BOSS),
    locname.ROCKBOWLSTAR2:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL2CAGEPLA, RB.ROCKNROLLIN),
    locname.ROCKBOWLSTAR3:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL1BOULDER, (RB.ROCKNROLLIN
                                                                        & CanReachLocation(locname.CHOMPWORKSTAR1,
                                                                                           parent_region_name=regname.CHOMWORK1LAVA)
                                                                        & CanReachLocation(locname.ROCKBOWLSTAR1)
                                                                        & RB.MailtoadOpen)),
}

# Cosmic Cove S
COSCCOVE_loc: dict[str, SMG2LocationData] = {
    locname.COSCCOVESTAR1:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC1WATERFA),
    locname.COSCCOVESTAR2:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC2WATERPL2, RB.CanSwim),
    locname.COSCCOVESTAR3:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC3WATER, RB.CanPound),
}

# Wild Glide St
WILDGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.WILDGLIDESTAR1: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                             regname.WILDGLIDE1COURSE),
    locname.WILDGLIDESTAR2: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                             regname.WILDGLIDE2COURSE, (CanReachLocation(locname.BEATBLOCKSTAR1,
                                                                                         parent_region_name=regname.BEATBLOK1)
                                                                       & RB.MailtoadOpen)),
}

# Honeybloom St
BEEBLOOM_loc: dict[str, SMG2LocationData] = {
    locname.BEEBLOOMSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                            regname.HONEYBLOOM1HONELOG, RB.BeeFlight),
    locname.BEEBLOOMSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                            regname.HONEYBLOOM1SECRET),
}

# Bowser's Lava
LAVALAIR_loc: dict[str, SMG2LocationData] = {
    locname.LAVALAIRSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1,
                                            regname.LAVALAIR1BOSSPLA, RB.CanPound),
    locname.LAVALAIRSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1,
                                            regname.LAVALAIR2LAVAPLA2S),
}

# World 3
# Tall Trunk St
TALLTREE_loc: dict[str, SMG2LocationData] = {
    locname.TALLTREESTAR1: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK1WOODCIRClE, RB.CanDinoBlimp),
    locname.TALLTREESTAR2: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK2SLIDEND),
    locname.TALLTREESTAR3: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK3PCOINEND),
}

# Cloudy Court
CLOUDCOURT_loc: dict[str, SMG2LocationData] = {
    locname.CLOUDCOURTSTAR1: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR1CASTLE, RB.CanMakeCloud),
    locname.CLOUDCOURTSTAR2: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR2FINAL),
    locname.CLOUDCOURTSTAR3: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR3PCOINS, RB.CloudMario),
}

    # Haunty Halls
HAUNTHALL_loc: dict[str, SMG2LocationData] = {
    locname.HAUNTHALLSTAR1: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL1BULBBER, (RB.CanDinoGlow&RB.CanDinoSwing)),
    locname.HAUNTHALLSTAR2: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL2CREEPYH),
    locname.HAUNTHALLSTAR3: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL3CREEPYH),
}

    # Freezy Flake
SNOWFLAKE_loc: dict[str, SMG2LocationData] = {
    locname.SNOWFLAKESTAR1: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK1LAVASNO, RB.FireMario),
    locname.SNOWFLAKESTAR2: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK2SORBETT),
    locname.SNOWFLAKESTAR3: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK3CHIMP),
}

    # Rolling Maste
ROLLMAST_loc: dict[str, SMG2LocationData] = {
    locname.ROLLMASTERSTAR1: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                              regname.ROLLMAST1SILVERC, RB.CanClimbPole),
    locname.ROLLMASTERSTAR2: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                              regname.ROLLMAST2SILVERC, RB.CanClimbPole),
}

    # Beat Block St
BEATBLOCK_loc: dict[str, SMG2LocationData] = {
    locname.BEATBLOCKSTAR1: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                             regname.BEATBLOK1),
    locname.BEATBLOCKSTAR2: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                             regname.BEATBLOK2),
}

    # Bowser Jr.'s
FEARFLET_loc: dict[str, SMG2LocationData] = {
    locname.FEARFLETSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2,
                                            regname.FEARFLET1MEGAHAM, RB.CanRideDino),
    locname.FEARFLETSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2,
                                            regname.FEARFLET2MEGAHAM, RB.CanRideDino),
}

    # World 4
    # Supermassive
SUPMASS_loc: dict[str, SMG2LocationData] = {
    locname.SUPERMASSSTAR1: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS1WIGGLERS, RB.CanClimbPole),
    locname.SUPERMASSSTAR2: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS1GARDEN),
    locname.SUPERMASSSTAR3: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS2WIGGLERS, RB.CanClimbPole),
}

    # Flipsville St
FLIPVILL_loc: dict[str, SMG2LocationData] = {
    locname.FLIPVILLESTAR1: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL1STAR),
    locname.FLIPVILLESTAR2: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL2GRAVITYMAIN, RB.DRILLMASTER),
    locname.FLIPVILLESTAR3: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL3GRAVITY, RB.DRILLMASTER),
}

    # Starshine Beach St
STARBEACH_loc: dict[str, SMG2LocationData] = {
    locname.STARBEACHSTAR1: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH1MAIN,
                                             (RB.CanDinoSwing & RB.CanDinoBlimp) | RB.CanInfiniteFlutter),
    locname.STARBEACHSTAR2: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH2MAIN, RB.CanMakeCloud&RB.CanSwim),
    locname.STARBEACHSTAR3: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH3MAIN, RB.CanDinoRun),
}

    # Chompworks St
CHOMWORK_loc: dict[str, SMG2LocationData] = {
    locname.CHOMPWORKSTAR1: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK1LAVA, RB.CanPound),
    locname.CHOMPWORKSTAR2: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK2TOWER, RB.SPRONGIN
                                             | (RB.HardLogic & RB.CanWallSpin & RB.CanTriple & RB.CanBackOrSideflip)),
    locname.CHOMPWORKSTAR3: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK3LAVA, RB.CanPound),
}

    # Honeyhop Star
HONEYHOP_loc: dict[str, SMG2LocationData] = {
    locname.HONEYHOPSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                            regname.HONEYHOP1QBTOP,
                                            RB.JumpHeight5 | (RB.HardLogic & RB.JumpHeight4 & RB.CanWallJump)),
    locname.HONEYHOPSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                            regname.HONEYHOP1QBBASE,
                                            (CanReachRegion(regname.HONEYHOP2QBBUBBLE)
                                             & CanReachRegion(regname.HONEYHOP2QBTOP)
                                             & CanReachLocation(locname.CLOCKRUINSTAR1,
                                                                parent_region_name=regname.CLOCKWORK1WHEELST)
                                             & RB.MailtoadOpen
                                             & (RB.CanAirSpin | RB.HardLogic) & (RB.CanLongJump | RB.MediumLogic))),
}

    # Sweet Mystery
SWEETMYS_loc: dict[str, SMG2LocationData] = {
    locname.SWEETMYSTSTAR1: SMG2LocationData(["Power Star Location", regname.SWEETMYS], regname.SWEETMYS,
                                             regname.SWEETMYS1CAKE, RB.CanDinoGlow),
    locname.SWEETMYSTSTAR2: SMG2LocationData(["Power Star Location", regname.SWEETMYS], regname.SWEETMYS,
                                             regname.SWEETMYS2END, RB.CanDinoGlow),
}

    # Bowser's Grav
GRAVGAUN_loc: dict[str, SMG2LocationData] = {
    locname.GRAVGAUNSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2,
                                            regname.GRAVGAUN1BOSSARE, RB.CanPound),
    locname.GRAVGAUNSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2,
                                            regname.GRAVGAUN2WHOMPWA),
}

    # World 5
    # Space Storm S
SPACSTOR_loc: dict[str, SMG2LocationData] = {
    locname.SPACESTORMSTAR1: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR1PULLPATH),
    locname.SPACESTORMSTAR2: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR2TOPTOWER, (RB.CanPound | RB.HardLogic)
                                              & (RB.CanGrabLedge | RB.CanBackOrSideflip | RB.CanAirSpin)),
    locname.SPACESTORMSTAR3: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR1TOPMAN, (CanReachLocation(locname.BOOMOONSTAR1,
                                                                                         parent_region_name=regname.BOOMOON1POPUP)
                                                                        & CanReachLocation(locname.SPACESTORMSTAR2)
                                                                        & RB.MailtoadOpen)),
}

    # Slipsand Star
SLIPSAND_loc: dict[str, SMG2LocationData] = {
    locname.SLIPSANDSTAR1: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND1BOSS, RB.FireMario),
    locname.SLIPSANDSTAR2: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND2BIRD),
    locname.SLIPSANDSTAR3: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND3BOSS, RB.FireMario),
}

    # Shiverburn St
COLDFIRE_loc: dict[str, SMG2LocationData] = {
    locname.COLDFIRESTAR1: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN1BOSS),
    locname.COLDFIRESTAR2: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN2ROMP, RB.SUPAPOWA | RB.HellLogic),
    locname.COLDFIRESTAR3: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN3CHIMP),
}

    # Boo Moon Star
BOOMOON_loc: dict[str, SMG2LocationData] = {
    locname.BOOMOONSTAR1: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON1POPUP, RB.CanPound),
    locname.BOOMOONSTAR2: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON2TOWER, RB.BooMario),
    locname.BOOMOONSTAR3: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON1POISON),
}

    # Upside Dizzy
UPDIZZY_loc: dict[str, SMG2LocationData] = {
    locname.UPDIZZYSTAR1: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN,
                                           regname.UPDOWNGRAV),
    locname.UPDIZZYSTAR2: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN,
                                           regname.UPDOWNBREAKER, RB.FireMario),
}

    # Fleet Glide S
FLETGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.FLEETFLYSTAR1: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                            regname.FLEETGLIDE1COURSE, RB.CanRideBird),
    locname.FLEETFLYSTAR2: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                            regname.FLEETGLIDE2COURSE, (RB.CanRideBird
                                                                       & CanReachLocation(locname.BATTBELTSTAR1,
                                                                                          parent_region_name=regname.BATTBELT1CHOM)
                                                                       & RB.MailtoadOpen)),
}

    # Bowser Jr.'s
BOOMBUNK_loc: dict[str, SMG2LocationData] = {
    locname.BOOMBUNKSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3,
                                            regname.BOOMBUNK1BOSS, RB.CanMakeCloud),
    locname.BOOMBUNKSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3,
                                            regname.BOOMBUNK2BOSS, RB.CanMakeCloud),
}

    # World 6
    # Melty Monster
MELTMONS_loc: dict[str, SMG2LocationData] = {
    locname.MELTMONSSTAR1: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY1MAGMAW),
    locname.MELTMONSSTAR2: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY2BOWLING, RB.ROCKNROLLIN),
    locname.MELTMONSSTAR3: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY3CHIMP, RB.ROCKNROLLIN),
}

    # Clockwork Rui
CLOCKRUIN_loc: dict[str, SMG2LocationData] = {
    locname.CLOCKRUINSTAR1: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK1WHEELST, RB.CanPound&RB.CanWallJump&RB.CanSwing),
    locname.CLOCKRUINSTAR2: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK2COGS),
    locname.CLOCKRUINSTAR3: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK3HAMMERTOP),
}

    # Throwback Sta
THROWBACK_loc: dict[str, SMG2LocationData] = {
    locname.THROWBACKSTAR1: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP1UNDER, RB.CanPound),
    locname.THROWBACKSTAR2: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP2FORT, RB.CanMakeCloud),
    locname.THROWBACKSTAR3: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP3FORT, RB.CanMakeCloud),
}

    # Battle Belt S
BATTBELT_loc: dict[str, SMG2LocationData] = {
    locname.BATTBELTSTAR1: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT1CHOM),
    locname.BATTBELTSTAR2: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT2CHOM),
    locname.BATTBELTSTAR3: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT3BOSS),
}

    # Flash Black S
FLASHBLACK_loc: dict[str, SMG2LocationData] = {
    locname.FLASHBLACKSTAR1: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                              regname.FLASHBLACK1PATH),
    locname.FLASHBLACKSTAR2: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                              regname.FLASHBLACK2PATH, RB.CanRideDino),
}

    # Slimy Spring
SLIMSPRI_loc: dict[str, SMG2LocationData] = {
    locname.SLIMYSPRISTAR1: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                             regname.SLIMSPRI1CAVE2, RB.CanShell),
    locname.SLIMYSPRISTAR2: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                             regname.SLIMSPRI2MOUTH1, (CanReachRegion(regname.SLIMSPRI2CAVE2)
                                                                       & CanReachLocation(locname.GALAXYGENSTAR2,
                                                                                          parent_region_name=regname.GALGEN1BOSS)
                                                                       & RB.MailtoadOpen
                                                                       & RB.CanShell)),
}

    # Bowser's Gala
GALGEN_loc: dict[str, SMG2LocationData] = {
    locname.GALAXYGENSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3,
                                             regname.GALGEN1BOSS, RB.CanPound),
    locname.GALAXYGENSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3,
                                             regname.GALGEN2STATUE),
}

    # World S
    # Mario Squared
MARIOSQ_loc: dict[str, SMG2LocationData] = {
    locname.MARIOSQRSTAR1: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO,
                                            regname.MARIOSQ1RIGHT),
    locname.MARIOSQRSTAR2: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO,
                                            regname.MARIOSQ2LEFT),
}

    # Rolling Coast
ROLLSLIDE_loc: dict[str, SMG2LocationData] = {
    locname.ROLLSLIDESTAR1: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                             regname.ROLLCOAST1, RB.CanBalance),
    locname.ROLLSLIDESTAR2: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                             regname.ROLLCOAST2, RB.CanBalance),
}

    # Twisty Trials
TWISTTRI_loc: dict[str, SMG2LocationData] = {
    locname.TWISTTRIALSTAR1: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                              regname.TWISTY1PLAT4),
    locname.TWISTTRIALSTAR2: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                              regname.TWISTY2PLAT4, (RB.CanLongSpin | RB.MediumLogic)),
}

    # Stone Cyclone
STONECYC_loc: dict[str, SMG2LocationData] = {
    locname.STONECYCLOSTAR1: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC,
                                              regname.STONECYC1),
    locname.STONECYCLOSTAR2: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC,
                                              regname.STONECYC2),
}

    # Boss Blitz St
BOSSBLITZ_loc: dict[str, SMG2LocationData] = {
    locname.BOSSBLITSTAR1: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                            regname.BOSSBLITZ1FIREDIN),
    locname.BOSSBLITSTAR2: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                            regname.BOSSBLITZ2FIREDIN),
}

    # Flip-Out Star
FLIPOUT_loc: dict[str, SMG2LocationData] = {
    locname.FLIPOUTSTAR1: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                           regname.FLIPOUT1CLIMB, RB.CanWallSpin),
    locname.FLIPOUTSTAR2: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                           regname.FLIPOUT2CLIMB, RB.CanWallSpin),
}

    # Grandmaster
GRANDMASTER_loc: dict[str, SMG2LocationData] = {
    locname.GRANDMASTSTAR1: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                             regname.GRANDMASTER1BROS2, RB.CanLongSpin | RB.MediumLogic),
    locname.GRANDMASTSTAR2: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                             regname.GRANDMASTER2ROSA),
}

green_star_locations: dict[str, SMG2LocationData]  = {
    locname.SKYSTASTARG1:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS1GSTAR1),
    locname.SKYSTASTARG2:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS1GREENHILL),
    locname.SKYSTASTARG3:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS2SKYFLEET),
    locname.YOSHSTARSTARG1:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGGGSTAR1,
                                                 (RB.CanSideflip&RB.CanAirSpin) | RB.CanRideDino),
    locname.YOSHSTARSTARG2:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGGGSTAR2),
    locname.YOSHSTARSTARG3:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGG1FOSSIL,
                                                 (RB.CanDinoSwing & (RB.CanBackflip | RB.CanInfiniteFlutter))),
    locname.SPINDIGSTARG1:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG1DRILL,
                                                 RB.JumpHeight3),
    locname.SPINDIGSTARG2:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG1STEEL,
                                                 RB.JumpHeight6),
    locname.SPINDIGSTARG3:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG2DARKIN1,
                                                 (RB.DRILLMASTER & ((RB.CanWallJump & (RB.CanSideflip | RB.CanTriple))
                                                                    | (RB.MediumLogic & RB.CanBackflip & RB.CanWallJump)
                                                                    | (RB.HardLogic & RB.JumpHeight6)))),
    locname.FLUFBLUFSTARG1:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1LANDING,
                                                 RB.CanMakeCloud & RB.JumpHeight5),
    locname.FLUFBLUFSTARG2:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1CLIFF1,
                                                 RB.CanMakeCloud),
    locname.FLUFBLUFSTARG3:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1TREECLIMB,
                                                 RB.CanMakeCloud),
    locname.RIGHTDOWNSTARG1:    SMG2LocationData(["Green Star Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                 regname.RIGHTDOWNTOPVIEW,
                                                 RB.CanAirSpin),
    locname.RIGHTDOWNSTARG2:    SMG2LocationData(["Green Star Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                 regname.RIGHTDOWNTOPVIEW,
                                                 (RB.JumpHeight4 | RB.CanWallSpin)),
    locname.FLIPSWAPSTARG1:     SMG2LocationData(["Green Star Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                                 regname.FLIPSWAP1, (RB.JumpHeight6 | (RB.HardLogic | RB.CanAirSpin))),
    locname.FLIPSWAPSTARG2:     SMG2LocationData(["Green Star Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                                 regname.FLIPSWAP1, (RB.JumpHeight6 | (RB.HardLogic | RB.CanAirSpin))),
    locname.FIREFLOTSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR1], regname.BOWJR1,
                                                 regname.FIREFLOT1LANDING,
                                                 RB.CanAirSpin | RB.CanBackflip
                                                 | (RB.MediumLogic & RB.CanSideflip & RB.CanGrabLedge)
                                                 | (RB.HardLogic & RB.CanTriple)),
    locname.FIREFLOTSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR1], regname.BOWJR1,
                                                 regname.FIREFLOT1LAVA,
                                                 RB.CanLongSpin | RB.MediumLogic),
    locname.PUZZPLANKSTARG1:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1BLOCK,
                                                 (RB.CanPound & RB.CanWallSpin & RB.CanBackOrSideflip)),
    locname.PUZZPLANKSTARG2:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA,
                                                 (RB.CanWallSpin | (RB.CanBackOrSideflip & RB.CanAirSpin)
                                                  | (RB.JumpHeight6 & RB.MediumLogic))),
    locname.PUZZPLANKSTARG3:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA,
                                                 RB.CanWallJump | (RB.HellLogic & RB.JumpHeight6)),
    locname.HIGHFALLSTARG1:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR1),
    locname.HIGHFALLSTARG2:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR2),
    locname.HIGHFALLSTARG3:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR3),
    locname.ROCKBOWLSTARG1:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1CRYSTAL, RB.CanWallSpin&RB.JumpHeight5),
    locname.ROCKBOWLSTARG2:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1CRYSTAL, RB.ROCKNROLLIN),
    locname.ROCKBOWLSTARG3:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1FALLING),
    locname.COSCCOVESTARG1:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC1WATERFA),
    locname.COSCCOVESTARG2:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC2WATERPA, RB.CanSwim),
    locname.COSCCOVESTARG3:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC2WATERPA,
                                                 (RB.CanSwim&RB.CanLongSpin)),
    locname.WILDGLIDESTARG1:    SMG2LocationData(["Green Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                                 regname.WILDGLIDE1COURSE),
    locname.WILDGLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                                 regname.WILDGLIDE1COURSE),
    locname.BEEBLOOMSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3),
    locname.BEEBLOOMSTARG2:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3, RB.CanSwing&RB.BeeFlight),
    locname.LAVALAIRSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA1W, RB.CanLongSpin | RB.MediumLogic),
    locname.LAVALAIRSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA2C),
    locname.TALLTREESTARG1:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1BIGTREE, (RB.CanDinoBlimp
                                                                             | (RB.CanBackflip & RB.CanWallSpin & RB.HardLogic)
                                                                             | RB.CanInfiniteFlutter)),
    locname.TALLTREESTARG2:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1LOG, RB.CanDinoBlimp),
    locname.TALLTREESTARG3:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK2SLIDE, RB.CanSlide),
    locname.CLOUDCOURTSTARG1:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1LANDING, (RB.CanMakeCloud
                                                                            | (RB.CloudMario & RB.CanBackOrSideflip & RB.HardLogic))),
    locname.CLOUDCOURTSTARG2:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CYMBAL, RB.CanMakeCloud & (RB.CanLongJump | RB.MediumLogic)),
    locname.CLOUDCOURTSTARG3:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CASTLE,
                                                 RB.CanMakeCloud),
    locname.HAUNTHALLSTARG1:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1HALLWAY, RB.CanAirSpin),
    locname.HAUNTHALLSTARG2:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1DISAPPE, RB.JumpHeight5),
    locname.HAUNTHALLSTARG3:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL2CREEPYH, RB.JumpHeight4),
    locname.SNOWFLAKESTARG1:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1SLIDELA, RB.CanSlide),
    locname.SNOWFLAKESTARG2:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1LAVASNO),
    locname.SNOWFLAKESTARG3:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK2WHITOUT),
    locname.ROLLMASTERSTARG1:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1ELEVATO),
    locname.ROLLMASTERSTARG2:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1SILVERC),
    locname.BEATBLOCKSTARG1:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, RB.JumpHeight6 | (RB.CanBackflip & RB.CanAirSpin)),
    locname.BEATBLOCKSTARG2:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, (RB.CanAirSpin & (RB.HardLogic | RB.CanBackOrSideflip)
                                                                     | (RB.CanTriple & RB.MediumLogic))),
    locname.FEARFLETSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1UNDERGR, RB.CanRideDino),
    locname.FEARFLETSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1AIRSHIP, RB.CanRideDino),
    locname.SUPERMASSSTARG1:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1PIPES, RB.JumpHeight6),
    locname.SUPERMASSSTARG2:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1GSTAR2),
    locname.SUPERMASSSTARG3:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1KOOPAS,
                                                 (RB.JumpHeight6 | RB.CanLongJump | RB.MediumLogic)),
    locname.FLIPVILLESTARG1:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1MAZETOP),
    locname.FLIPVILLESTARG2:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1WANWANLANE, RB.CanWallSpin),
    locname.FLIPVILLESTARG3:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1LIFTBELOW, RB.CanHomingPound | RB.HardLogic),
    locname.STARBEACHSTARG1:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN, RB.CanDinoBlimp | (RB.CanBackOrSideflip & RB.CanAirSpin)
                                                 | RB.CanInfiniteFlutter),
    locname.STARBEACHSTARG2:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN, RB.CanDinoRun | (RB.CanRideDino & RB.MediumLogic)),
    locname.STARBEACHSTARG3:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH2MAIN, RB.CanPound & RB.CanMakeCloud & RB.CanSwim),
    locname.CHOMPWORKSTARG1:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK1START, RB.CanLongSpin & (RB.CanBackflip | RB.HardLogic)),
    locname.CHOMPWORKSTARG2:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK1FLIPSWAP, RB.CanWallSpin | (RB.CanAirSpin & RB.CanBackOrSideflip)
                                                 | (RB.MediumLogic & RB.CanTriple)),
    locname.CHOMPWORKSTARG3:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK2TOWER, RB.SPRONGIN
                                                 | (RB.HardLogic & RB.CanWallSpin & RB.CanTriple & RB.CanBackOrSideflip & RB.CanLongJump)),
    locname.HONEYHOPSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                                 regname.HONEYHOP1CLOUDS),
    locname.HONEYHOPSTARG2:     SMG2LocationData(["Green Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                                 regname.HONEYHOP1QBTOP, RB.BeeFlight),
    locname.SWEETMYSTSTARG1:    SMG2LocationData(["Green Star Location", regname.SWEETMYS], regname.SWEETMYS,
                                                 regname.SWEETMYS1CHOCO, RB.CanDinoGlow),
    locname.SWEETMYSTSTARG2:    SMG2LocationData(["Green Star Location", regname.SWEETMYS], regname.SWEETMYS,
                                                 regname.SWEETMYS1CHOCO, RB.CanDinoGlow&RB.CanLongJump),
    locname.GRAVGAUNSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUNGSTAR1),
    locname.GRAVGAUNSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUNGSTAR2),
    locname.SPACESTORMSTARG1:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR1PULL),
    locname.SPACESTORMSTARG2:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR2GSTAR2),
    locname.SPACESTORMSTARG3:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR2TOPTOWERBASE),
    locname.SLIPSANDSTARG1:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1CUBE),
    locname.SLIPSANDSTARG2:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE),
    locname.SLIPSANDSTARG3:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE),
    locname.COLDFIRESTARG1:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1VOLCANO , RB.CanMakeCloud & RB.CanPound),
    locname.COLDFIRESTARG2:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1LAVA),
    locname.COLDFIRESTARG3:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1FIREICE, RB.CanMakeCloud&RB.CanPound
                                                 & (RB.JumpHeight3 | RB.MediumLogic)),
    locname.BOOMOONSTARG1:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POISON, RB.CanLongSpin),
    locname.BOOMOONSTARG2:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1MOON),
    locname.BOOMOONSTARG3:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POPUP, RB.CanLongSpin),
    locname.UPDIZZYSTARG1:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINSTART, RB.CanAirSpin | RB.CanBackflip
                                                 | (RB.CanTriple & RB.MediumLogic) | (RB.CanLongJump & RB.HardLogic)),
    locname.UPDIZZYSTARG2:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINEND,
                                                 (RB.HardLogic | RB.CanWallSpin | (RB.MediumLogic & RB.CanAirSpin))
                                                 & (RB.CanWallJump | RB.CanBackOrSideflip | RB.CanDouble | RB.CanAirSpin)),
    locname.FLEETFLYSTARG1:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDE1COURSE, RB.CanRideBird),
    locname.FLEETFLYSTARG2:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDE1COURSE, RB.CanRideBird),
    locname.BOOMBUNKSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1BOOMER, RB.CanCannon),
    locname.BOOMBUNKSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1CHECK, RB.CanCannon),
    locname.MELTMONSSTARG1:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1MAGMAARG),
    locname.MELTMONSSTARG2:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1LAVAWAVE3),
    locname.MELTMONSSTARG3:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY2BOWLING, RB.ROCKNROLLIN),
    locname.CLOCKRUINSTARG1:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1COGS, (RB.CanBackOrSideflip & (RB.CanAirSpin | RB.CanWallJump))
                                                 | (RB.HardLogic & RB.CanDouble & RB.CanWallJump)),
    locname.CLOCKRUINSTARG2:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1PUSH),
    locname.CLOCKRUINSTARG3:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1WHEELST),
    locname.THROWBACKSTARG1:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT, RB.CanAirSpin | RB.MediumLogic),
    locname.THROWBACKSTARG2:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT, RB.CanWallSpin
                                                 | RB.JumpHeight6
                                                 | (RB.HardLogic & RB.CanAirSpin)
                                                 | RB.HellLogic),
    locname.THROWBACKSTARG3:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP2FORT, RB.CanMakeCloud & RB.CanLongJump),
    locname.BATTBELTSTARG1:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT],regname.BATTLEBELT,
                                                 regname.BATTBELT1PUMP, RB.JumpHeight3 | (RB.CanDouble & RB.HardLogic)),
    locname.BATTBELTSTARG2:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1MOLE, (RB.CanBackOrSideflip & RB.CanAirSpin)
                                                 | (RB.HardLogic & RB.JumpHeight6)),
    locname.BATTBELTSTARG3:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1CHOM, RB.JumpHeight3),
    locname.FLASHBLACKSTARG1:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1TOWER, RB.CanDinoBlimp),
    locname.FLASHBLACKSTARG2:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1PATH),
    locname.SLIMYSPRISTARG1:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1, RB.CanShell | RB.MediumLogic),
    locname.SLIMYSPIRSTARG2:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1, RB.CanShell | RB.HardLogic),
    locname.GALAXYGENSTARG1:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1VOLCANO),
    locname.GALAXYGENSTARG2:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1DASHCAS, ((RB.CanMakeCloud & (RB.CanLongJump | (RB.MediumLogic & RB.CanWallJump)))
                                                                           | (RB.CanRideDino & RB.HellLogic))), #This will need more testing
    locname.MARIOSQRSTARG1:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN),
    locname.MARIOSQRSTARG2:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN),
    locname.ROLLSLIDESTARG1:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, RB.CanBalance),
    locname.ROLLSLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, RB.CanBalance),
    locname.TWISTTRIALSTARG1:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT2, RB.CanMakeCloud & (RB.CanLongJump | RB.MediumLogic)),
    locname.TWISTTRIALSTARG2:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT4, RB.CanMakeCloud & (RB.CanLongJump | RB.MediumLogic)),
    locname.STONECYCLOSTARG1:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, RB.JumpHeight6),
    locname.STONECYCLOSTARG2:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, RB.CanLongSpin),
    locname.BOSSBLITSTARG1:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1MAJORBU, RB.JumpHeight3 | (RB.CanDouble & RB.MediumLogic)),
    locname.BOSSBLITSTARG2:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1BOULDER),
    locname.FLIPOUTSTARG1:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT1LANDING, RB.CanWallSpin),
    locname.FLIPOUTSTARG2:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT2CLIMB, RB.CanWallSpin),
}

COMETMEDAL_loc:dict[str, SMG2LocationData] = {
    locname.SKYSTACM: SMG2LocationData(["Comet Medal Location", regname.SKYOBS], regname.SKYOBS,
                                       regname.SKYOBS1CYLINDER,
                                       (RB.JumpHeight2 | RB.HardLogic)), #Hard logic: Jump off of one of the final 3 Paragoombas.
    locname.YOSHSTARCM: SMG2LocationData(["Comet Medal Location", regname.GOODEGG], regname.GOODEGG,
                                         regname.GOODEGG1MUDDY),
    locname.SPINDIGCM: SMG2LocationData(["Comet Medal Location", regname.SPINDIG], regname.SPINDIG,
                                        regname.SPINDIG1DRILL, RB.DRILLMASTER),
    locname.FLUFBLUFCM: SMG2LocationData(["Comet Medal Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                         regname.FLUFFBLUFF1WATER,
                                         RB.JumpHeight4 | (RB.CanMakeCloud & (RB.CanLongJump | RB.MediumLogic))),
    locname.RIGHTDOWNCM: SMG2LocationData(["Comet Medal Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                          regname.RIGHTDOWNCORRIDOR, RB.CanWallJump),
    locname.FLIPSWAPCM: SMG2LocationData(["Comet Medal Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                         regname.FLIPSWAP1, RB.CanAirSpin),
    locname.FIREFLOTCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT1LANDING,
                                         RB.JumpHeight3 | RB.CanGrabLedge),
    locname.PUZZPLANKCM: SMG2LocationData(["Comet Medal Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                          regname.PUZZPLAN1SAWBLA),
    locname.HIGHFALLCM: SMG2LocationData(["Comet Medal Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                         regname.HIGHTAIL1DASHWAL1, RB.CanDinoRun),
    locname.ROCKBOWLCM: SMG2LocationData(["Comet Medal Location", regname.BOULBOWL], regname.BOULBOWL,
                                         regname.BOULBOWL1CRYSTAL, RB.ROCKNROLLIN),
    locname.COSCCOVECM: SMG2LocationData(["Comet Medal Location", regname.COSMICO], regname.COSMICO,
                                         regname.COSMIC1POOL),
    locname.WILDGLIDECM: SMG2LocationData(["Comet Medal Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                          regname.WILDGLIDE1COURSE),
    locname.BEEBLOOMCM: SMG2LocationData(["Comet Medal Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                         regname.HONEYBLOOM1WALL2, RB.BeeFlight),
    locname.LAVALAIRCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER1], regname.BOWSER1,
                                         regname.LAVALAIR1LAVAPLA1W, RB.JumpHeight5|RB.CanWallSpin),
    locname.TALLTREECM: SMG2LocationData(["Comet Medal Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                         regname.TALLTRUNK1LOG, RB.CanDinoBlimp),
    locname.CLOUDCOURTCM: SMG2LocationData(["Comet Medal Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                           regname.CLOUCOUR1CASTLE, RB.CanMakeCloud),
    locname.HAUNTHALLCM: SMG2LocationData(["Comet Medal Location", regname.HAUNHALL], regname.HAUNHALL,
                                          regname.HAUNHALL1DISAPPE),
    locname.SNOWFLAKECM: SMG2LocationData(["Comet Medal Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                          regname.FREEFLAK1SLIDELA, RB.FireMario),
    locname.ROLLMASTERCM: SMG2LocationData(["Comet Medal Location", regname.ROLLMAST], regname.ROLLMAST,
                                           regname.ROLLMAST1SAWBLAD),
    locname.BEATBLOCKCM: SMG2LocationData(["Comet Medal Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                          regname.BEATBLOK1),
    locname.FEARFLEETCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR2], regname.BOWJR2,
                                          regname.FEARFLET1AIRSHIP),
    locname.SUPERMASSCM: SMG2LocationData(["Comet Medal Location", regname.SUPMASS], regname.SUPMASS,
                                          regname.SUPMASS1START, RB.CanLongJump | RB.CanAirSpin | RB.MediumLogic),
    locname.FLIPVILLECM: SMG2LocationData(["Comet Medal Location", regname.FLIPVILL], regname.FLIPVILL,
                                          regname.FLIPVILL1COMETMEDAL),
    locname.STARBEACHCM: SMG2LocationData(["Comet Medal Location", regname.STARBEACH], regname.STARBEACH,
                                          regname.STARBEACH1MAIN, RB.CanSwim),
    locname.CHOMPWORKCM: SMG2LocationData(["Comet Medal Location", regname.CHOMWORK], regname.CHOMWORK,
                                          regname.CHOMWORK1START, RB.JumpHeight5),
    locname.HONEYHOPCM: SMG2LocationData(["Comet Medal Location", regname.HONEYHOP], regname.HONEYHOP,
                                         regname.HONEYHOP1QBBUBBLE, RB.CanWallJump | RB.BeeFlight),
    locname.SWEETMYSTCM: SMG2LocationData(["Comet Medal Location", regname.SWEETMYS], regname.SWEETMYS,
                                          regname.SWEETMYS1CHOCO, RB.CanDinoGlow),
    locname.GRAVGAUNTCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER2], regname.BOWSER2,
                                          regname.GRAVGAUN1LANDING, (RB.CanGrabLedge&RB.JumpHeight2) | RB.JumpHeight3
                                          | RB.HellLogic),
    locname.SPACESTORMCM: SMG2LocationData(["Comet Medal Location", regname.SPACSTOR], regname.SPACSTOR,
                                           regname.SPACSTOR1SATELLITE, RB.CanLongJump | RB.MediumLogic),
    locname.SLIPSANDCM: SMG2LocationData(["Comet Medal Location", regname.SLIPSAND], regname.SLIPSAND,
                                         regname.SLIPSAND1CUBE),
    locname.COLDFIRECM: SMG2LocationData(["Comet Medal Location", regname.SHIVBURN], regname.SHIVBURN,
                                         regname.SHIVBURN1LAVA),
    locname.BOOMOONCM: SMG2LocationData(["Comet Medal Location", regname.BOOMOON], regname.BOOMOON,
                                        regname.BOOMOON1POISON),
    locname.UPDIZZYCM: SMG2LocationData(["Comet Medal Location", regname.UPDOWN], regname.UPDOWN,
                                        regname.UPDOWNGRAV),
    locname.FLEETFLYCM: SMG2LocationData(["Comet Medal Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                         regname.FLEETGLIDE1COURSE, RB.CanRideBird),
    locname.BOOMBUNKCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR3], regname.BOWJR3,
                                         regname.BOOMBUNK1PLAT),
    locname.MELTMONSCM: SMG2LocationData(["Comet Medal Location", regname.MELTY], regname.MELTY,
                                         regname.MELTY1MAGMAW, RB.CanLongJump | RB.JumpHeight3 | RB.MediumLogic),
    locname.CLOCKRUINSCM: SMG2LocationData(["Comet Medal Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                           regname.CLOCKWORK1WHEELSB),
    locname.THROWBACKCM: SMG2LocationData(["Comet Medal Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                          regname.WHOMP1FORT, RB.CanAirSpin & (RB.CanClimbPole | RB.MediumLogic)),
    locname.BATTBELTCM: SMG2LocationData(["Comet Medal Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                         regname.BATTBELT1LAVA, RB.CanAirSpin | RB.CanLongJump | RB.MediumLogic),
    locname.FLASHBLACKCM: SMG2LocationData(["Comet Medal Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                           regname.FLASHBLACK1TOWER, RB.CanDinoBlimp),
    locname.SLIMYSPRICM: SMG2LocationData(["Comet Medal Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                          regname.SLIMSPRI1CAVE1, RB.CanShell | RB.MediumLogic),
    locname.GLXYGENCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER3], regname.BOWSER3,
                                        regname.GALGEN1LAVASNA),
    locname.MARIOSQRCM: SMG2LocationData(["Comet Medal Location", regname.MARIO], regname.MARIO,
                                         regname.MARIOSQ1LEFT),
    locname.ROLLSLIDECM: SMG2LocationData(["Comet Medal Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                          regname.ROLLCOAST1, RB.CanBalance),
    locname.TWISTTRIALCM: SMG2LocationData(["Comet Medal Location", regname.TWISTTRI], regname.TWISTTRI,
                                           regname.TWISTY1PLAT4),
    locname.STONECYCLOCM: SMG2LocationData(["Comet Medal Location", regname.STONECYC], regname.STONECYC,
                                           regname.STONECYC1),
    locname.BOSSBLITCM: SMG2LocationData(["Comet Medal Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                         regname.BOSSBLITZ1KINGKAL, RB.JumpHeight4),
    locname.FLIPOUTCM: SMG2LocationData(["Comet Medal Location", regname.FLIPOUT], regname.FLIPOUT,
                                        regname.FLIPOUT1CLIMB, RB.CanWallSpin & (RB.CanLongJump | RB.HardLogic)),
    locname.GRANDMASTRCM: SMG2LocationData(["Comet Medal Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                           regname.GRANDMASTER1BROS2, RB.CanAirSpin),
}

checkpoint_loc_table: dict[str, SMG2LocationData] = {
    locname.SKYOBS1GREENHILLCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS1GREENHILL),
    locname.SKYOBS1CYLINDERCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                regname.SKYOBS1CYLINDER),
    locname.SKYOBS1BEFOREBOSSCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                  regname.SKYOBS1BEFOREBOSS),
    locname.SKYOBS2SKYFLEETCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                regname.SKYOBS2SKYFLEET),
    locname.SKYOBS2FLIPSWITCHCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                  regname.SKYOBS2FLIPSWITCH),
    locname.SKYOBS2GRASSFLEETCP: SMG2LocationData(["Checkpoint Location", regname.SKYOBS], regname.SKYOBS,
                                                  regname.SKYOBS2GRASSFLEET),
    locname.GOODEGG1EARTHCP: SMG2LocationData(["Checkpoint Location", regname.GOODEGG], regname.GOODEGG,
                                              regname.GOODEGG1EARTH),
    locname.GOODEGG1FOSSILCP: SMG2LocationData(["Checkpoint Location", regname.GOODEGG], regname.GOODEGG,
                                               regname.GOODEGG1FOSSIL),
    locname.GOODEGG2SHOOTINGCP: SMG2LocationData(["Checkpoint Location", regname.GOODEGG], regname.GOODEGG,
                                                 regname.GOODEGG2SHOOTING),
    locname.GOODEGG2BOSSCP: SMG2LocationData(["Checkpoint Location", regname.GOODEGG], regname.GOODEGG,
                                             regname.GOODEGG2BOSS),
    locname.SPINDIG1STEELCP: SMG2LocationData(["Checkpoint Location", regname.SPINDIG], regname.SPINDIG,
                                              regname.SPINDIG1STEEL),
    locname.SPINDIG1TOADSCP: SMG2LocationData(["Checkpoint Location", regname.SPINDIG], regname.SPINDIG,
                                              regname.SPINDIG1TOADS),
    locname.SPINDIG2BTOADCP: SMG2LocationData(["Checkpoint Location", regname.SPINDIG], regname.SPINDIG,
                                              regname.SPINDIG2BTOAD),
    locname.FLUFFBLUFF1CLIFF1CP: SMG2LocationData(["Checkpoint Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                  regname.FLUFFBLUFF1CLIFF1),
    locname.FLUFFBLUFF1CLOUDCLIMBCP: SMG2LocationData(["Checkpoint Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                      regname.FLUFFBLUFF1CLOUDCLIMB),
    locname.FLUFFBLUFF3TOWERCP: SMG2LocationData(["Checkpoint Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF3TOWER),
    locname.FLIPSWAP1CP: SMG2LocationData(["Checkpoint Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                          regname.FLIPSWAP1, (RB.CanAirSpin | RB.CanLongJump | RB.MediumLogic)),
    locname.RIGHTDOWNCORRIDORCP1: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR),
    locname.RIGHTDOWNCORRIDORCP2: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR),
    locname.RIGHTDOWNCORRIDORCP3: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR, (RB.FireMario
                                                                               & (RB.CanWallJump | (RB.CanTriple & RB.MediumLogic)))),
    locname.FIREFLOT1LAVACP: SMG2LocationData(["Checkpoint Location", regname.BOWJR1], regname.BOWJR1,
                                              regname.FIREFLOT1LAVA),
    locname.PUZZPLAN1SAWBLACP: SMG2LocationData(["Checkpoint Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                regname.PUZZPLAN1SAWBLA),
    locname.PUZZPLAN1CHECKPCP: SMG2LocationData(["Checkpoint Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                regname.PUZZPLAN1CHECKP),
    locname.PUZZPLAN3BUGABOCP: SMG2LocationData(["Checkpoint Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                regname.PUZZPLAN3BUGABO),
    locname.HIGHTAIL1PLATDASCP: SMG2LocationData(["Checkpoint Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAIL1PLATDAS),
    locname.HIGHTAIL1DASHWALCP: SMG2LocationData(["Checkpoint Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAIL1DASHWAL1),
    locname.BOULBOWL1FALLINGCP: SMG2LocationData(["Checkpoint Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1FALLING),
    locname.BOULBOWL1DODECAHCP: SMG2LocationData(["Checkpoint Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1DODECAH),
    locname.COSMIC3WATERCP: SMG2LocationData(["Checkpoint Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC3WATER),
    locname.COSMIC2INPIPECP: SMG2LocationData(["Checkpoint Location", regname.COSMICO], regname.COSMICO,
                                              regname.COSMIC2INPIPE, RB.CanSwim),
    locname.COSMIC2WATERPACP: SMG2LocationData(["Checkpoint Location", regname.COSMICO], regname.COSMICO,
                                               regname.COSMIC2WATERPA),
    locname.COSMIC2TOADSHICP: SMG2LocationData(["Checkpoint Location", regname.COSMICO], regname.COSMICO,
                                               regname.COSMIC2TOADSHI),
    locname.HONEYBLOOM1WALL2CP: SMG2LocationData(["Checkpoint Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL2),
    locname.HONEYBLOOM1WALL3CP: SMG2LocationData(["Checkpoint Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3),
    locname.HONEYBLOOM1HONELOGCP: SMG2LocationData(["Checkpoint Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                   regname.HONEYBLOOM1HONELOG),
    locname.LAVALAIR1LAVAPLA1CP: SMG2LocationData(["Checkpoint Location", regname.BOWSER1], regname.BOWSER1,
                                                  regname.LAVALAIR1LAVAPLA1B),
    locname.LAVALAIR1LAVAPLA2CP1: SMG2LocationData(["Checkpoint Location", regname.BOWSER1], regname.BOWSER1,
                                                   regname.LAVALAIR1LAVAPLA2C),
    locname.LAVALAIR1LAVAPLA2CP2: SMG2LocationData(["Checkpoint Location", regname.BOWSER1], regname.BOWSER1,
                                                   regname.LAVALAIR1LAVAPLA2C),
    locname.TALLTRUNK1LOGCP: SMG2LocationData(["Checkpoint Location",regname.TALLTRUNK], regname.TALLTRUNK,
                                              regname.TALLTRUNK1LOG),
    locname.TALLTRUNK1WOODCIRClECP: SMG2LocationData(["Checkpoint Location",regname.TALLTRUNK], regname.TALLTRUNK,
                                                     regname.TALLTRUNK1WOODCIRClE),
    locname.TALLTRUNK2SLIDECP: SMG2LocationData(["Checkpoint Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                     regname.TALLTRUNK2SLIDE),
    locname.CLOUCOUR1TOWERSCP: SMG2LocationData(["Checkpoint Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1TOWERS),
    locname.CLOUCOUR1CASTLECP: SMG2LocationData(["Checkpoint Location", regname.CLOUCOUR],regname.CLOUCOUR ,
                                                 regname.CLOUCOUR1CASTLE),
    locname.CLOUCOUR3PCOINSCP: SMG2LocationData(["Checkpoint Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR3PCOINS),
    locname.HAUNHALL1DISAPPECP: SMG2LocationData(["Checkpoint Location", regname.HAUNHALL], regname.HAUNHALL,
                                                 regname.HAUNHALL1DISAPPE),
    locname.HAUNHALL1BULBBERCP: SMG2LocationData(["Checkpoint Location", regname.HAUNHALL], regname.HAUNHALL,
                                                 regname.HAUNHALL1BULBBER),
    locname.HAUNHALL2CREEPYCCP: SMG2LocationData(["Checkpoint Location", regname.HAUNHALL], regname.HAUNHALL,
                                                 regname.HAUNHALL2CREEPYC),
    locname.HAUNHALL2CREEPYHCP: SMG2LocationData(["Checkpoint Location", regname.HAUNHALL], regname.HAUNHALL,
                                                 regname.HAUNHALL2CREEPYH),
    locname.FREEFLAK1SNOWBYHCP: SMG2LocationData(["Checkpoint Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1SNOWBYH, RB.FireMario),
    locname.FREEFLAK1LAVASNOCP: SMG2LocationData(["Checkpoint Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1LAVASNO),
    locname.FREEFLAK2WHITOUTCP1: SMG2LocationData(["Checkpoint Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK2WHITOUT),
    locname.FREEFLAK2WHITOUTCP2: SMG2LocationData(["Checkpoint Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK2WHITOUT),
    locname.ROLLMAST1ELEVATOCP: SMG2LocationData(["Checkpoint Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1ELEVATO),
    locname.ROLLMAST1SAWBLADCP: SMG2LocationData(["Checkpoint Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1SAWBLAD),
    locname.BEATBLOK1CP: SMG2LocationData(["Checkpoint Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1),
    locname.BEATBLOK2CP1: SMG2LocationData(["Checkpoint Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK2),
    locname.BEATBLOK2CP2: SMG2LocationData(["Checkpoint Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK2),
    locname.FEARFLET1BULLETBCP: SMG2LocationData(["Checkpoint Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1BULLETB),
    locname.FEARFLET1AIRSHIPCP: SMG2LocationData(["Checkpoint Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1AIRSHIP),
    locname.SUPMASS1THWOMPSCP: SMG2LocationData(["Checkpoint Location", regname.SUPMASS],  regname.SUPMASS,
                                                regname.SUPMASS1THWOMPS),
    locname.SUPMASS1STARCHIPSCP: SMG2LocationData(["Checkpoint Location", regname.SUPMASS],  regname.SUPMASS,
                                                  regname.SUPMASS1STARCHIPS),
    locname.SUPMASS1WIGGLERSCP: SMG2LocationData(["Checkpoint Location", regname.SUPMASS],  regname.SUPMASS,
                                                 regname.SUPMASS1WIGGLERS),
    locname.FLIPVILL1WANWANCP: SMG2LocationData(["Checkpoint Location",regname.FLIPVILL], regname.FLIPVILL,
                                                regname.FLIPVILL1WANWANSTART),
    locname.FLIPVILL1LIFTCP: SMG2LocationData(["Checkpoint Location",regname.FLIPVILL], regname.FLIPVILL,
                                              regname.FLIPVILL1LIFTSTART),
    locname.FLIPVILL1STARSHROOMCP: SMG2LocationData(["Checkpoint Location",regname.FLIPVILL], regname.FLIPVILL,
                                                    regname.FLIPVILL1STARSHROOM),
    locname.FLIPVILL2TOWERSTARTCP: SMG2LocationData(["Checkpoint Location",regname.FLIPVILL], regname.FLIPVILL,
                                                    regname.FLIPVILL2TOWERSTART),
    locname.CHOMWORK1ROLLINGCP: SMG2LocationData(["Checkpoint Location",regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK1ROLLING),
    locname.CHOMWORK1LAVACP: SMG2LocationData(["Checkpoint Location",regname.CHOMWORK], regname.CHOMWORK,
                                              regname.CHOMWORK1LAVA),
    locname.CHOMWORK2ROLLINGCP: SMG2LocationData(["Checkpoint Location",regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK2ROLLING),
    locname.CHOMWORK2TOWERCP: SMG2LocationData(["Checkpoint Location",regname.CHOMWORK], regname.CHOMWORK,
                                               regname.CHOMWORK2TOWER),
    locname.SWEETMYS1COOKIECP: SMG2LocationData(["Checkpoint Location",regname.SWEETMYS], regname.SWEETMYS,
                                                regname.SWEETMYS1COOKIE),
    locname.SWEETMYS1SWITCHESCP: SMG2LocationData(["Checkpoint Location",regname.SWEETMYS], regname.SWEETMYS,
                                                  regname.SWEETMYS1SWITCHES),
    locname.SWEETMYS1CAKECP: SMG2LocationData(["Checkpoint Location",regname.SWEETMYS], regname.SWEETMYS,
                                              regname.SWEETMYS1CAKE),
    locname.HONEYHOP1QBBASECP: SMG2LocationData(["Checkpoint Location",regname.HONEYHOP], regname.HONEYHOP,
                                                regname.HONEYHOP1QBBASE),
    locname.GRAVGAUN1LANDINGCP: SMG2LocationData(["Checkpoint Location",regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUN1LANDING),
    locname.GRAVGAUN1WHOMPWACP: SMG2LocationData(["Checkpoint Location",regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUN1WHOMPWA),
    locname.GRAVGAUN1DOORTODCP: SMG2LocationData(["Checkpoint Location",regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUN1DOORTOD),
    locname.SPACSTOR1TOPMANCP: SMG2LocationData(["Checkpoint Location", regname.SPACSTOR], regname.SPACSTOR,
                                                regname.SPACSTOR1TOPMAN),
    locname.SPACSTOR2TOPTOWERCP: SMG2LocationData(["Checkpoint Location", regname.SPACSTOR], regname.SPACSTOR,
                                                  regname.SPACSTOR2TOPTOWER),
    locname.SLIPSAND1CUBECP: SMG2LocationData(["Checkpoint Location", regname.SLIPSAND], regname.SLIPSAND,
                                              regname.SLIPSAND1CUBE),
    locname.SLIPSAND1SLIDECP: SMG2LocationData(["Checkpoint Location", regname.SLIPSAND], regname.SLIPSAND,
                                               regname.SLIPSAND1SLIDE, RB.CanSlide),
    locname.SLIPSAND2BIRDCP: SMG2LocationData(["Checkpoint Location", regname.SLIPSAND], regname.SLIPSAND,
                                              regname.SLIPSAND2BIRD),
    locname.SHIVBURN1LAVACP: SMG2LocationData(["Checkpoint Location", regname.SHIVBURN], regname.SHIVBURN,
                                              regname.SHIVBURN1LAVA),
    locname.SHIVBURN1FIREICECP: SMG2LocationData(["Checkpoint Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1FIREICE),
    locname.SHIVBURN1TOADCP: SMG2LocationData(["Checkpoint Location", regname.SHIVBURN], regname.SHIVBURN,
                                              regname.SHIVBURN1TOAD),
    locname.BOOMOON1POISONCP: SMG2LocationData(["Checkpoint Location", regname.BOOMOON], regname.BOOMOON,
                                               regname.BOOMOON1POISON),
    locname.BOOMOON2TOWERCP: SMG2LocationData(["Checkpoint Location", regname.BOOMOON], regname.BOOMOON,
                                              regname.BOOMOON2TOWER),
    locname.UPDOWNINSIDECP: SMG2LocationData(["Checkpoint Location", regname.UPDOWN], regname.UPDOWN,
                                             regname.UPDOWNINEND),
    locname.BOOMBUNK1CHECKCP: SMG2LocationData(["Checkpoint Location", regname.BOWJR3], regname.BOWJR3,
                                               regname.BOOMBUNK1CHECK),
    locname.BOOMBUNK2DARKCP: SMG2LocationData(["Checkpoint Location", regname.BOWJR3], regname.BOWJR3,
                                              regname.BOOMBUNK2DARK),
    locname.MELTY1LAVAWAVE1CP: SMG2LocationData(["Checkpoint Location",  regname.MELTY,], regname.MELTY,
                                                regname.MELTY1LAVAWAVE1),
    locname.MELTY1LAVAWAVE3CP: SMG2LocationData(["Checkpoint Location",  regname.MELTY,], regname.MELTY,
                                                regname.MELTY1LAVAWAVE3),
    locname.MELTY2BOWLINGCP: SMG2LocationData(["Checkpoint Location",  regname.MELTY,], regname.MELTY,
                                              regname.MELTY2BOWLING),
    locname.MELTY3CHIMPCP: SMG2LocationData(["Checkpoint Location",  regname.MELTY,], regname.MELTY,
                                            regname.MELTY3CHIMP),
    locname.CLOCKWORK1PUSHCP: SMG2LocationData(["Checkpoint Location", regname.CLOCKWORK,],regname.CLOCKWORK,
                                               regname.CLOCKWORK1PUSH),
    locname.CLOCKWORK1WHEELSCP: SMG2LocationData(["Checkpoint Location", regname.CLOCKWORK,],regname.CLOCKWORK,
                                                 regname.CLOCKWORK1WHEELSB),
    locname.CLOCKWORK3HAMMERCP: SMG2LocationData(["Checkpoint Location", regname.CLOCKWORK,],regname.CLOCKWORK,
                                                 regname.CLOCKWORK3HAMMER),
    locname.WHOMP1FORTCP: SMG2LocationData(["Checkpoint Location", regname.WHOMPFORT,],regname.WHOMPFORT,
                                           regname.WHOMP1FORT),
    locname.BATTBELT1PTOACP: SMG2LocationData(["Checkpoint Location", regname.BATTLEBELT,],regname.BATTLEBELT,
                                              regname.BATTBELT1PTOA),
    locname.BATTBELT1RTOACP: SMG2LocationData(["Checkpoint Location", regname.BATTLEBELT,],regname.BATTLEBELT,
                                              regname.BATTBELT1RTOA),
    locname.BATTBELT2PTOACP: SMG2LocationData(["Checkpoint Location", regname.BATTLEBELT,],regname.BATTLEBELT,
                                              regname.BATTBELT2PTOA),
    locname.BATTBELT2RTOACP: SMG2LocationData(["Checkpoint Location", regname.BATTLEBELT,],regname.BATTLEBELT,
                                              regname.BATTBELT2RTOA),
    locname.FLASHBLACK1PATHCP: SMG2LocationData(["Checkpoint Location", regname.FLASHBLACK,],regname.FLASHBLACK,
                                                regname.FLASHBLACK1PATH),
    locname.SLIMSPRI1MOUTH2CP: SMG2LocationData(["Checkpoint Location", regname.SLIMSPRI,],regname.SLIMSPRI,
                                                regname.SLIMSPRI1MOUTH2),
    locname.GALGEN1LAVACYLCP: SMG2LocationData(["Checkpoint Location", regname.BOWSER3,],regname.BOWSER3,
                                               regname.GALGEN1LAVACYL),
    locname.GALGEN1TOWERCP: SMG2LocationData(["Checkpoint Location", regname.BOWSER3,],regname.BOWSER3,
                                             regname.GALGEN1TOWER),
    locname.GALGEN1YOSHICP: SMG2LocationData(["Checkpoint Location", regname.BOWSER3,],regname.BOWSER3,
                                             regname.GALGEN1YOSHI),
    locname.GALGEN1STATUECP: SMG2LocationData(["Checkpoint Location", regname.BOWSER3,],regname.BOWSER3,
                                              regname.GALGEN1STATUE),
    locname.GALGEN2YOSHICP: SMG2LocationData(["Checkpoint Location", regname.BOWSER3,],regname.BOWSER3,
                                             regname.GALGEN2YOSHI),
    locname.TWISTY2PLAT2CP: SMG2LocationData(["Checkpoint Location", regname.TWISTTRI,], regname.TWISTTRI,
                                             regname.TWISTY2PLAT2),
    locname.BOSSBLITZ1BOULDERCP: SMG2LocationData(["Checkpoint Location", regname.BOSSBLITZ,],  regname.BOSSBLITZ,
                                                  regname.BOSSBLITZ1BOULDER),
    locname.FLIPOUT1CLIMBCP1: SMG2LocationData(["Checkpoint Location", regname.FLIPOUT,], regname.FLIPOUT,
                                               regname.FLIPOUT1CLIMB, RB.CanWallSpin),
    locname.FLIPOUT1CLIMBCP2: SMG2LocationData(["Checkpoint Location", regname.FLIPOUT,], regname.FLIPOUT,
                                               regname.FLIPOUT1CLIMB, RB.CanWallSpin),
    locname.FLIPOUT2CLIMBCP1: SMG2LocationData(["Checkpoint Location", regname.FLIPOUT,], regname.FLIPOUT,
                                               regname.FLIPOUT2CLIMB, RB.CanWallSpin),
    locname.FLIPOUT2CLIMBCP2: SMG2LocationData(["Checkpoint Location", regname.FLIPOUT,], regname.FLIPOUT,
                                               regname.FLIPOUT2CLIMB, RB.CanWallSpin),
    locname.GRANDMASTER1CLOUDCP: SMG2LocationData(["Checkpoint Location", regname.GRANDMASTER,], regname.GRANDMASTER,
                                                  regname.GRANDMASTER1CLOUD),
    locname.GRANDMASTER1SWAPCP: SMG2LocationData(["Checkpoint Location", regname.GRANDMASTER,], regname.GRANDMASTER,
                                                 regname.GRANDMASTER1SWAP),
    locname.GRANDMASTER1PULLCP: SMG2LocationData(["Checkpoint Location", regname.GRANDMASTER,], regname.GRANDMASTER,
                                                 regname.GRANDMASTER1PULL),
}

mailtoad_locations: dict[str, SMG2LocationData] = {
    locname.GOLDGEARMO:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2,
                                                 CanReachLocation(locname.CHOMPWORKSTAR1)
                                                 & CanReachLocation(locname.ROCKBOWLSTAR1)
                                                 & RB.MailtoadOpen),
    locname.SILVGEARMO:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2,
                                                 (CanReachLocation(locname.BOOMOONSTAR1)
                                                  & CanReachLocation(locname.SPACESTORMSTAR2)
                                                  & RB.MailtoadOpen)),
    locname.JIBBERJAY1:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, (CanReachLocation(locname.BEATBLOCKSTAR1)
                                                                 & RB.MailtoadOpen)),
    locname.JIBBERJAY2:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, (CanReachLocation(locname.BATTBELTSTAR1)
                                                                 & RB.MailtoadOpen)),
    locname.CHIMPSTOMP:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2,
                                                 RB.PowerStarCount(15) & RB.MailtoadOpen),
    locname.CHIMPSCORE:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, (CanReachLocation(locname.CLOCKRUINSTAR1)
                                                                 & RB.MailtoadOpen)),
    locname.CHIMPCOINS:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, (CanReachLocation(locname.GALAXYGENSTAR2)
                                                                 & RB.MailtoadOpen)),
    locname.LUIGILETTR:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, (RB.MailtoadOpen
                                                                 & CanReachLocation(locname.GALAXYGENSTAR1))),
    locname.ROSALETTRL:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2,RB.MailtoadOpen),
    locname.ROSALETTR1:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
    locname.ROSALETTR2:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
    locname.ROSALETTR3:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
    locname.ROSALETTR4:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
    locname.ROSALETTR5:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
    locname.HONEYBEELTR:           SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                    regname.SHIP2, (RB.MailtoadOpen
                                                                    & RB.CanReachLocation(locname.BEEBLOOMSTAR2))),
    locname.STARBUNNYLTR:          SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                    regname.SHIP2, (RB.MailtoadOpen
                                                                    & CanReachLocation(locname.FLIPSWAPSTAR1))),
    locname.PEACHLETTR:         SMG2LocationData(["Letter Locations"], regname.SHIP2,
                                                 regname.SHIP2, RB.MailtoadOpen),
}

hungry_luma_loc: dict[str, SMG2LocationData] ={
    locname.WORLD1SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD1, regname.WORLD1,
                                       CanReachEntrance("World 1 Slot 4 Galaxy", parent_region_name=regname.WORLD1)),
    locname.WORLD2SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD2, regname.WORLD2,
                                       CanReachEntrance("World 2 Slot 6 Galaxy", parent_region_name=regname.WORLD2)),
    locname.WORLD3SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD3, regname.WORLD3,
                                       CanReachEntrance("World 3 Slot 5 Galaxy", parent_region_name=regname.WORLD3)),
    locname.WORLD4SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD4, regname.WORLD4,
                                       CanReachEntrance("World 4 Slot 2 Galaxy", parent_region_name=regname.WORLD4)),
    locname.WORLD5SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD5, regname.WORLD5,
                                       CanReachEntrance("World 5 Slot 5 Galaxy", parent_region_name=regname.WORLD5)),
    locname.WORLD6SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD6, regname.WORLD6,
                                       CanReachEntrance("World 6 Slot 3 Galaxy", parent_region_name=regname.WORLD6)),
    locname.WORLD7SL: SMG2LocationData(["Hungry Luma Location"], regname.WORLD7, regname.WORLD7,
                                       CanReachEntrance("World 7 Slot 6 Galaxy", parent_region_name=regname.WORLD7)),
    locname.FLUFFYCL: SMG2LocationData(["Hungry Luma Location"], regname.FLUFFBLUFF,
                                       regname.FLUFFBLUFF1BIGCLOUD,
                                       CanReachEntrance("Fluffy Bluff: Hungry Luma",
                                                        parent_region_name=regname.FLUFFBLUFF1BIGCLOUD)),
    locname.PUZZLECL: SMG2LocationData(["Hungry Luma Location"], regname.PUZZPLAN, regname.PUZZPLAN1GRUZZY,
                                       CanReachEntrance("Puzzle Plank: Hungry Luma",
                                                        parent_region_name=regname.PUZZPLAN1GRUZZY)),
    locname.HIGHTACL: SMG2LocationData(["Hungry Luma Location"], regname.HIGHTAIL, regname.HIGHTAIL1DASHWAL1,
                                       CanReachEntrance("Hightail Falls: Hungry Luma",
                                                        parent_region_name=regname.HIGHTAIL1DASHWAL1)),
    locname.COSMICCL: SMG2LocationData(["Hungry Luma Location"], regname.COSMICO, regname.COSMIC1POOL,
                                       CanReachEntrance("Cosmic Cove: Hungry Luma",
                                                        parent_region_name=regname.COSMIC1POOL)),
    locname.CLOUDYCL: SMG2LocationData(["Hungry Luma Location"], regname.CLOUCOUR, regname.CLOUCOUR1TOWERS,
                                       CanReachEntrance("Cloudy Court: Hungry Luma",
                                                        parent_region_name=regname.CLOUCOUR1TOWERS)),
    locname.CLOCKWCL: SMG2LocationData(["Hungry Luma Location"], regname.CLOCKWORK, regname.CLOCKWORK1COGS,
                                       CanReachEntrance("Clockwork Ruins: Hungry Luma",
                                                        parent_region_name=regname.CLOCKWORK1COGS)),
    locname.BATTLECL: SMG2LocationData(["Hungry Luma Location"], regname.BATTLEBELT, regname.BATTBELT1ICEP,
                                       CanReachEntrance("Battle Belt: Hungry Luma",
                                                        parent_region_name=regname.BATTBELT1ICEP)),
}

passenger_loc: dict[str, SMG2LocationData] = {
    locname.YOSHIPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.YOSHSTARSTAR1)),
    locname.YTOADPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.SPINDIGSTAR1)),
    locname.BTOADPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        RB.PowerStarCount(7)),
    locname.MTOADPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        RB.PowerStarCount(13)),
    locname.BUNNYPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.FLIPSWAPSTAR1)),
    locname.HONEYPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.BEEBLOOMSTAR2)),
    locname.PENGUPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.COSCCOVESTAR2)),
    locname.JIBBEPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.WILDGLIDESTAR2)),
    locname.LUMA1PASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIPLEFTEAR,
                                        RB.PowerStarCount(18)),
    locname.LUMA2PASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIPLEFTEAR,
                                        CanReachLocation(locname.MELTMONSSTAR1)),
    locname.WHITTPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.TALLTREESTAR2)),
    locname.GOLDGPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.ROCKBOWLSTAR3)),
    locname.SILVGPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.SPACESTORMSTAR3)),
    locname.BOBOMPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.THROWBACKSTAR1)),
    locname.GLUM1PASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.BOSSBLITSTAR1)),
    locname.GLUM2PASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        RB.PowerStarCount(120)),
    locname.ROSALPASS: SMG2LocationData(["Passenger Location"], regname.SHIP2, regname.SHIP2,
                                        CanReachLocation(locname.GRANDMASTSTAR2)),
}

lumalee_locations: dict[str, SMG2LocationData] = {
    locname.SHIPLUMALEE1: SMG2LocationData(["Lumalee Location"], regname.SHIP2, regname.SHIPLEFTEAR,
                                           RB.PowerStarCount(18)),
    locname.SHIPLUMALEE2: SMG2LocationData(["Lumalee Location"], regname.SHIP2, regname.SHIPLEFTEAR,
                                           CanReachLocation(locname.MELTMONSSTAR1) & Has("Can Farm Coins")),
    locname.SPINDIGLUMALEE: SMG2LocationData(["Lumalee Location"], regname.SPINDIG, regname.SPINDIG1TOADS,),
    locname.PUZPLANLUMALEE: SMG2LocationData(["Lumalee Location"], regname.PUZZPLAN, regname.PUZZPLAN1CHECKP,),
    locname.BOULDERLUMALEE: SMG2LocationData(["Lumalee Location"], regname.BOULBOWL, regname.BOULBOWL1DODECAH,),
    locname.FREEZYLUMALEE: SMG2LocationData(["Lumalee Location"], regname.FREEFLAKE, regname.FREEFLAK2WHITOUT,),
    locname.FEARSOMLUMALEE: SMG2LocationData(["Lumalee Location"], regname.BOWJR2, regname.FEARFLET1AIRSHIP,),
    locname.FLIPSVILUMALEE: SMG2LocationData(["Lumalee Location"], regname.FLIPVILL, regname.FLIPVILL1STARSHROOM,),
    locname.SLIPSANLUMALEE: SMG2LocationData(["Lumalee Location"], regname.SLIPSAND, regname.SLIPSAND1SLIDE,),
    locname.SHIVBURLUMALEE: SMG2LocationData(["Lumalee Location"], regname.SHIVBURN, regname.SHIVBURN1TOAD,),
    locname.BATTBELLUMALEE: SMG2LocationData(["Lumalee Location"], regname.BATTLEBELT, regname.BATTBELT1RTOA,),
    locname.BOSSBLILUMALEE: SMG2LocationData(["Lumalee Location"], regname.BOSSBLITZ, regname.BOSSBLITZ1BOULDER,),
}

launch_star_locs: dict[str, SMG2LocationData] = {
    locname.SKYOBS1HOULS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1TOPOFHOUSE, RB.CanLaunchStar),
    locname.SKYOBS1GRELS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1GREENHILL, RB.CanLaunchStar),
    locname.SKYOBS1MINLS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1MINIPLANETS, RB.CanLaunchStar),
    locname.SKYOBS1MINSS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1MINIPLANETS,
                                           RB.CanLaunchStar),
    locname.SKYOBS1QCOSS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1MINIPLANETS,
                                           RB.CanLaunchStar),
    locname.SKYOBS1CYLLS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1CYLINDER, RB.CanLaunchStar),
    locname.SKYOBS1TWOLS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS1BEFOREBOSS, RB.CanLaunchStar),
    locname.SKYOBS2HOULS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS2TOPOFHOUSE, RB.CanLaunchStar),
    locname.SKYOBS2FLELS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS2SKYFLEET, RB.CanLaunchStar),
    locname.SKYOBS2FLILS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS2FLIPSWITCH, RB.CanLaunchStar),
    locname.SKYOBS3HOULS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS3TOPOFHOUSE, RB.CanLaunchStar),
    locname.SKYOBS3CYLLS: SMG2LocationData(["Launch Stars"], regname.SKYOBS, regname.SKYOBS3CYLINDER, RB.CanLaunchStar),

    locname.GOODEGG1PLALS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG1MUDDY,
                                            CanReachEntrance("Yoshi Star 1: Yoshi Planet Launch Star", parent_region_name=regname.GOODEGG1MUDDY)),
    locname.GOODEGG1EARLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG1EARTH, RB.CanLaunchStar),
    locname.GOODEGG1TOWLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG1TOWER,
                                            CanReachEntrance("Yoshi Star 1: Tower Launch Star", parent_region_name=regname.GOODEGG1TOWER)),
    locname.GOODEGG2PLALS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG2MUDDY,
                                            RB.CanLaunchStar & RB.CanRideDino),
    locname.GOODEGG2MIDLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG2SHOOTING,
                                            RB.CanLaunchStar & RB.CanRideDino),
    locname.GOODEGG2PLTLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG2ORBITS,
                                            RB.CanLaunchStar & RB.CanRideDino),
    locname.GOODEGG2SHOLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG2SHOOTING,
                                            RB.CanLaunchStar & RB.CanRideDino),
    locname.GOODEGG2MARLS: SMG2LocationData(["Launch Stars"], regname.GOODEGG, regname.GOODEGG2MARBLE,
                                            RB.CanLaunchStar & RB.CanRideDino),

    locname.SPINDIG1DIGLS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG1TETRA,
                                            CanReachEntrance("Spin-Dig 1: Dig Dirt Launch Star", parent_region_name=regname.SPINDIG1TETRA)),
    locname.SPINDIG1DRILS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG1DRILL,
                                            RB.CanLaunchStar & RB.DRILLMASTER),
    locname.SPINDIG1STELS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG1STEEL, RB.CanLaunchStar),
    locname.SPINDIG1DIRLS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG1DIRTT,
                                            RB.CanLaunchStar & RB.DRILLMASTER),
    locname.SPINDIG1REDLS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG1TOADS, RB.CanLaunchStar),
    locname.SPINDIG2TETSS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG2TETRA, RB.CanLaunchStar),
    locname.SPINDIG2DARLS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG2DARKB, RB.CanLaunchStar),
    locname.SPINDIG2BLULS: SMG2LocationData(["Launch Stars"], regname.SPINDIG, regname.SPINDIG2BTOAD, RB.CanLaunchStar),

    locname.FLUFFBLUFF1WALLS: SMG2LocationData(["Launch Stars"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1CLIFF2,
                                               CanReachEntrance(locname.FLUFFBLUFF1WALLS, parent_region_name=regname.FLUFFBLUFF1CLIFF2)),
    locname.FLUFFBLUFF1WATLS: SMG2LocationData(["Launch Stars"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1WATER,
                                               RB.CanLaunchStar & RB.CanCollectStarChips),
    locname.FLUFFBLUFF1LANSS: SMG2LocationData(["Launch Stars"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1BIGTREE, RB.CanLaunchStar),
    locname.FLUFFBLUFF2BUISS: SMG2LocationData(["Launch Stars"], regname.FLUFFBLUFF, regname.FLUFFBLUFF2BUILDING, RB.CanLaunchStar),

    locname.FIREFLOT1LAVLS: SMG2LocationData(["Launch Stars"], regname.BOWJR1, regname.FIREFLOT1LAVA, RB.CanLaunchStar),
    locname.FIREFLOT1LANSS: SMG2LocationData(["Launch Stars"], regname.BOWJR1, regname.FIREFLOT1LANDING, RB.CanLaunchStar),

    locname.PUZZPLAN1WIGLS: SMG2LocationData(["Launch Stars"], regname.PUZZPLAN, regname.PUZZPLAN1GROUND,
                                             RB.CanLaunchStar & RB.CanPound),
    locname.PUZZPLAN1GRALS: SMG2LocationData(["Launch Stars"], regname.PUZZPLAN, regname.PUZZPLAN1GRUZZY,
                                             RB.CanLaunchStar & RB.CanPound),
    locname.PUZZPLAN1CHELS: SMG2LocationData(["Launch Stars"], regname.PUZZPLAN, regname.PUZZPLAN1CHECKP, RB.CanLaunchStar),
    locname.PUZZPLAN1SAWSS: SMG2LocationData(["Launch Stars"], regname.PUZZPLAN, regname.PUZZPLAN1SAWBLA,
                                             CanReachEntrance("Puzzle Plank: Saws & Planks Sling Star",
                                                              parent_region_name=regname.PUZZPLAN1SAWBLA)),

    locname.BOULBOWL1ROCLS: SMG2LocationData(["Launch Stars"], regname.BOULBOWL, regname.BOULBOWL1FALLING, RB.CanLaunchStar),
    locname.BOULBOWL1DODLS: SMG2LocationData(["Launch Stars"], regname.BOULBOWL, regname.BOULBOWL1DODECAH, RB.CanLaunchStar),
    locname.BOULBOWL2ASTLS: SMG2LocationData(["Launch Stars"], regname.BOULBOWL, regname.BOULBOWL2ASTEROI, RB.CanLaunchStar),
    locname.BOULBOWL1BOUSS: SMG2LocationData(["Launch Stars"], regname.BOULBOWL, regname.BOULBOWL1BOULDER,
                                             RB.CanLaunchStar & RB.ROCKNROLLIN),

    locname.HIGHTAIL1LANLS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL1LANDING,
                                             CanReachEntrance("Hightail Falls: Hot Pepper Landing Launch Star",
                                                              parent_region_name=regname.HIGHTAIL1LANDING)),
    locname.HIGHTAIL1CLILS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL1GIANTRA,
                                             RB.CanLaunchStar & RB.CanDinoRun),
    locname.HIGHTAIL1DASLS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL1PLATDAS,
                                             CanReachEntrance("Hightail Falls: Hot Pepper Dash Launch Star",
                                                              parent_region_name=regname.HIGHTAIL1PLATDAS)),
    locname.HIGHTAIL2LANLS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL2LANDING,
                                             CanReachEntrance("Hightail Falls Comet: Hot Pepper Landing Launch Star",
                                                              parent_region_name=regname.HIGHTAIL2LANDING)),
    locname.HIGHTAIL2CLILS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL2GIANTRA,
                                             RB.CanLaunchStar & RB.CanDinoRun),
    locname.HIGHTAIL2DASLS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL2PLATDAS,
                                             CanReachEntrance("Hightail Falls Comet: Hot Pepper Dash Launch Star",
                                                              parent_region_name=regname.HIGHTAIL2PLATDAS)),

    locname.COSMIC1LANSS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC2LANDING,
                                           RB.CanLaunchStar & RB.CanSwim),
    locname.COSMIC1CORSS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC2LANDING,
                                           RB.CanLaunchStar & RB.CanSwim),
    locname.COSMIC1PILSS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC2LANDING,
                                           RB.CanLaunchStar & RB.CanSwim),
    locname.COSMIC2LANLS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC2LANDING,
                                           CanReachEntrance("Cosmic Cove 2: Landing Launch Star", parent_region_name=regname.COSMIC2LANDING)),
    locname.COSMIC2TOALS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC2TOADSHI, RB.CanLaunchStar),

    locname.LAVALAIR1CYLLS: SMG2LocationData(["Launch Stars"], regname.BOWSER1, regname.LAVALAIR1LAVACYL2,
                                             CanReachEntrance(locname.LAVALAIR1CYLLS,
                                                              parent_region_name=regname.LAVALAIR1LAVACYL2) & RB.CanLaunchStar
                                             ),
    locname.LAVALAIR1LAVSS: SMG2LocationData(["Launch Stars"], regname.BOWSER1, regname.LAVALAIR1LAVAPLA1B,
                                             CanReachEntrance(locname.LAVALAIR1LAVSS,
                                                              parent_region_name=regname.LAVALAIR1LAVAPLA1B) & RB.CanLaunchStar
                                             ),
    locname.LAVALAIR2CYLLS: SMG2LocationData(["Launch Stars"], regname.BOWSER1, regname.LAVALAIR2LAVACYL2,
                                             CanReachEntrance(locname.LAVALAIR2CYLLS,
                                                              parent_region_name=regname.LAVALAIR2LAVACYL2) & RB.CanLaunchStar
                                             ),
    locname.LAVALAIR2LAVSS: SMG2LocationData(["Launch Stars"], regname.BOWSER1, regname.LAVALAIR2LAVAPLA1B,
                                             CanReachEntrance(locname.LAVALAIR2LAVSS,
                                                              parent_region_name=regname.LAVALAIR2LAVAPLA1B) & RB.CanLaunchStar),

    locname.TALLTRUNK1BIGLS: SMG2LocationData(["Launch Stars"], regname.TALLTRUNK, regname.TALLTRUNK1BIGTREE,
                                            CanReachEntrance(locname.TALLTRUNK1BIGLS, parent_region_name=regname.TALLTRUNK1BIGTREE)),
    locname.TALLTRUNK1LOGLS: SMG2LocationData(["Launch Stars"], regname.TALLTRUNK, regname.TALLTRUNK1LOG,
                                              CanReachEntrance(locname.TALLTRUNK1LOGLS, parent_region_name=regname.TALLTRUNK1LOG)),
    locname.TALLTRUNK2BIGLS: SMG2LocationData(["Launch Stars"], regname.TALLTRUNK, regname.TALLTRUNK2BIGTREE,
                                              CanReachEntrance(locname.TALLTRUNK2BIGLS, parent_region_name=regname.TALLTRUNK2BIGTREE)),

    locname.CLOUCOUR1CYMLS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR1CYMBAL,
                                             CanReachEntrance(locname.CLOUCOUR1CYMLS, parent_region_name=regname.CLOUCOUR1CYMBAL)),
    locname.CLOUCOUR1TOWLS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR1TOWERS,
                                             CanReachEntrance(locname.CLOUCOUR1TOWLS, parent_region_name=regname.CLOUCOUR1TOWERS)),
    locname.CLOUCOUR2LAULS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR2LANDING,
                                             CanReachEntrance(locname.CLOUCOUR2LAULS, parent_region_name=regname.CLOUCOUR2LANDING)),
    locname.CLOUCOUR2CS1SS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR2CASTLE1,
                                             CanReachEntrance(locname.CLOUCOUR2CS1SS, parent_region_name=regname.CLOUCOUR2CASTLE1)),
    locname.CLOUCOUR2CS2SS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR2CASTLE2,
                                             CanReachEntrance(locname.CLOUCOUR2CS2SS, parent_region_name=regname.CLOUCOUR2CASTLE2)),

    locname.HAUNHALL1HALLS: SMG2LocationData(["Launch Stars"], regname.HAUNHALL, regname.HAUNHALL1HALLWAY, RB.CanLaunchStar),
    locname.HAUNHALL2HALLS: SMG2LocationData(["Launch Stars"], regname.HAUNHALL, regname.HAUNHALL2HALLWAY, RB.CanLaunchStar),
    locname.HAUNHALL2CRESS: SMG2LocationData(["Launch Stars"], regname.HAUNHALL, regname.HAUNHALL2CREEPYC, RB.CanLaunchStar),

    locname.FREEFLAK1CABLS: SMG2LocationData(["Launch Stars"], regname.FREEFLAKE, regname.FREEFLAK1LOGCABI,
                                             CanReachEntrance(locname.FREEFLAK1CABLS, parent_region_name=regname.FREEFLAK1LOGCABI)),
    locname.FREEFLAK2CABLS: SMG2LocationData(["Launch Stars"], regname.FREEFLAKE, regname.FREEFLAK2LOGCABI,
                                             CanReachEntrance(locname.FREEFLAK2CABLS, parent_region_name=regname.FREEFLAK2LOGCABI)),
    locname.FREEFLAK2SNOLS: SMG2LocationData(["Launch Stars"], regname.FREEFLAKE, regname.FREEFLAK2SNOWBYH,
                                             CanReachEntrance(locname.FREEFLAK2SNOLS, parent_region_name=regname.FREEFLAK2SNOWBYH)),
    locname.FREEFLAK2WHILS: SMG2LocationData(["Launch Stars"], regname.FREEFLAKE, regname.FREEFLAK2WHITOUT, RB.CanLaunchStar),
    locname.FREEFLAK2SORSS: SMG2LocationData(["Launch Stars"], regname.FREEFLAKE, regname.FREEFLAK2SORBHEA, RB.CanLaunchStar),

    locname.FEARFLET1AIRLS: SMG2LocationData(["Launch Stars"], regname.BOWJR2, regname.FEARFLET1AIRSHIP,
                                             CanReachEntrance(locname.FEARFLET1AIRLS, parent_region_name=regname.FEARFLET1AIRSHIP)),
    locname.FEARFLET1FIRSS: SMG2LocationData(["Launch Stars"], regname.BOWJR2, regname.FEARFLET1UNDERGR, RB.CanLaunchStar),

    locname.SUPMASS1THWLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS1THWOMPS,
                                            CanReachEntrance(locname.SUPMASS1THWLS, parent_region_name=regname.SUPMASS1THWOMPS)),
    locname.SUPMASS1KOOLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS1KOOPAS,
                                            CanReachEntrance(locname.SUPMASS1KOOLS, parent_region_name=regname.SUPMASS1KOOPAS)),
    locname.SUPMASS1BLOLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS1STARCHIPS,
                                            CanReachEntrance(locname.SUPMASS1BLOLS, parent_region_name=regname.SUPMASS1STARCHIPS)),
    locname.SUPMASS1GARLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS1GARDEN, RB.CanLaunchStar),
    locname.SUPMASS2THWLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS2THWOMPS,
                                            CanReachEntrance(locname.SUPMASS2THWLS, parent_region_name=regname.SUPMASS2THWOMPS)),
    locname.SUPMASS2KOOLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS2KOOPAS,
                                            CanReachEntrance(locname.SUPMASS2KOOLS, parent_region_name=regname.SUPMASS2KOOPAS)),
    locname.SUPMASS2BLOLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS2STARCHIPS,
                                            CanReachEntrance(locname.SUPMASS1BLOLS, parent_region_name=regname.SUPMASS1STARCHIPS)),
    locname.SUPMASS2GARLS: SMG2LocationData(["Launch Stars"], regname.SUPMASS, regname.SUPMASS2GARDEN,
                                            RB.CanLaunchStar),

    locname.SWEETMYS1FLILS: SMG2LocationData(["Launch Stars"], regname.SWEETMYS, regname.SWEETMYS1SWITCHES,
                                             RB.CanLaunchStar & CanReachEntrance(locname.SWEETMYS1FLILS, parent_region_name=regname.SWEETMYS1SWITCHES)),

    locname.FLIPVILL1DOLLS: SMG2LocationData(["Launch Stars"], regname.FLIPVILL, regname.FLIPVILL1MAZETOP, RB.CanLaunchStar),
    locname.FLIPVILL1CHOLS: SMG2LocationData(["Launch Stars"], regname.FLIPVILL, regname.FLIPVILL1WANWANBACK, RB.CanLaunchStar),
    locname.FLIPVILL1LIFLS: SMG2LocationData(["Launch Stars"], regname.FLIPVILL, regname.FLIPVILL1LIFTTOP,
                                             CanReachEntrance(locname.FLIPVILL1LIFLS, parent_region_name=regname.FLIPVILL1LIFTTOP)),
    locname.FLIPVILL1STALS: SMG2LocationData(["Launch Stars"], regname.FLIPVILL, regname.FLIPVILL1STARSHROOM, RB.CanLaunchStar),
    locname.FLIPVILL2DOLLS: SMG2LocationData(["Launch Stars"], regname.FLIPVILL, regname.FLIPVILL2MAZELAUNCH, RB.CanLaunchStar),

    locname.HONEYHOP2BASSS: SMG2LocationData(["Launch Stars"], regname.HONEYHOP, regname.HONEYHOP2QBBASE, RB.CanLaunchStar),
    locname.HONEYHOP2BUBSS: SMG2LocationData(["Launch Stars"], regname.HONEYHOP, regname.HONEYHOP2QBBUBBLE, RB.CanLaunchStar),

    locname.STARBEACH1WATLS: SMG2LocationData(["Launch Stars"], regname.STARBEACH, regname.STARBEACH1WATER,
                                              RB.CanLaunchStar & RB.CanSwim),
    locname.STARBEACH2WATLS: SMG2LocationData(["Launch Stars"], regname.STARBEACH, regname.STARBEACH2WATER,
                                              RB.CanLaunchStar & RB.CanSwim),
    locname.STARBEACH2TUNSS: SMG2LocationData(["Launch Stars"], regname.STARBEACH, regname.STARBEACH2DEEPW,
                                              RB.CanLaunchStar & RB.CanSwim),

    locname.CHOMWORK1STALS: SMG2LocationData(["Launch Stars"], regname.CHOMWORK, regname.CHOMWORK1START,
                                             CanReachEntrance(locname.CHOMWORK1STALS, parent_region_name=regname.CHOMWORK1START)),
    locname.CHOMWORK1ROLLS: SMG2LocationData(["Launch Stars"], regname.CHOMWORK, regname.CHOMWORK1ROLLING, RB.CanLaunchStar),
    locname.CHOMWORK1FLILS: SMG2LocationData(["Launch Stars"], regname.CHOMWORK, regname.CHOMWORK1FLIPSWAP,
                                             CanReachEntrance(locname.CHOMWORK1FLILS, parent_region_name=regname.CHOMWORK1FLIPSWAP)),
    locname.CHOMWORK2STALS: SMG2LocationData(["Launch Stars"], regname.CHOMWORK, regname.CHOMWORK2START,
                                             CanReachEntrance(locname.CHOMWORK2STALS, parent_region_name=regname.CHOMWORK2START)),
    locname.CHOMWORK2ROLLS: SMG2LocationData(["Launch Stars"], regname.CHOMWORK, regname.CHOMWORK2ROLLING,
                                             CanReachEntrance(locname.CHOMWORK2ROLLS, parent_region_name=regname.CHOMWORK2ROLLING)),

    locname.GRAVGAUN1FIRLS: SMG2LocationData(["Launch Stars"], regname.BOWSER2, regname.GRAVGAUN1WHOMPWA, RB.CanLaunchStar),

    locname.SPACSTOR1PULLS: SMG2LocationData(["Launch Stars"], regname.SPACSTOR, regname.SPACSTOR1PULL, RB.CanLaunchStar),
    locname.SPACSTOR1SATLS: SMG2LocationData(["Launch Stars"], regname.SPACSTOR, regname.SPACSTOR1SATELLITE, RB.CanLaunchStar),
    locname.SPACSTOR1CANLS: SMG2LocationData(["Launch Stars"], regname.SPACSTOR, regname.SPACSTOR1REDCANIN, RB.CanLaunchStar),
    locname.SPACSTOR2PULLS: SMG2LocationData(["Launch Stars"], regname.SPACSTOR, regname.SPACSTOR2PULL, RB.CanLaunchStar),
    locname.SPACSTOR2TOWSS: SMG2LocationData(["Launch Stars"], regname.SPACSTOR, regname.SPACSTOR2TOPTOWERBASE, RB.CanLaunchStar),

    locname.BOOMOON1DARLS: SMG2LocationData(["Launch Stars"], regname.BOOMOON, regname.BOOMOON1DARK, RB.CanLaunchStar),
    locname.BOOMOON1POILS: SMG2LocationData(["Launch Stars"], regname.BOOMOON, regname.BOOMOON1POISON, RB.CanLaunchStar),
    locname.BOOMOON1MOOLS: SMG2LocationData(["Launch Stars"], regname.BOOMOON, regname.BOOMOON1MOON, RB.CanLaunchStar),
    locname.BOOMOON2DARLS: SMG2LocationData(["Launch Stars"], regname.BOOMOON, regname.BOOMOON2DARK, RB.CanLaunchStar),

    locname.SLIPSAND1LONLS: SMG2LocationData(["Launch Stars"], regname.SLIPSAND, regname.SLIPSAND1LONG, RB.CanLaunchStar),
    locname.SLIPSAND1CUBLS: SMG2LocationData(["Launch Stars"], regname.SLIPSAND, regname.SLIPSAND1CUBE, RB.CanLaunchStar),
    locname.SLIPSAND1SLILS: SMG2LocationData(["Launch Stars"], regname.SLIPSAND, regname.SLIPSAND1SLIDE, RB.CanLaunchStar),
    locname.SLIPSAND2LONLS: SMG2LocationData(["Launch Stars"], regname.SLIPSAND, regname.SLIPSAND2LONG2, RB.CanLaunchStar),

    locname.SHIVBURN1VOLLS: SMG2LocationData(["Launch Stars"], regname.SHIVBURN, regname.SHIVBURN1VOLCANO, RB.CanLaunchStar),
    locname.SHIVBURN1LAVLS: SMG2LocationData(["Launch Stars"], regname.SHIVBURN, regname.SHIVBURN1LAVA, RB.CanLaunchStar),
    locname.SHIVBURN1ICELS: SMG2LocationData(["Launch Stars"], regname.SHIVBURN, regname.SHIVBURN1FIREICE, RB.CanLaunchStar),
    locname.SHIVBURN1GRELS: SMG2LocationData(["Launch Stars"], regname.SHIVBURN, regname.SHIVBURN1TOAD, RB.CanLaunchStar),
    locname.SHIVBURN2GRELS: SMG2LocationData(["Launch Stars"], regname.SHIVBURN, regname.SHIVBURN2TOAD, RB.CanLaunchStar),

    locname.BOOMBUNK1FORLS: SMG2LocationData(["Launch Stars"], regname.BOWJR3, regname.BOOMBUNK1BOOMER, RB.CanLaunchStar),
    locname.BOOMBUNK1PLALS: SMG2LocationData(["Launch Stars"], regname.BOWJR3, regname.BOOMBUNK1PLAT, RB.CanLaunchStar),
    locname.BOOMBUNK2FORLS: SMG2LocationData(["Launch Stars"], regname.BOWJR3, regname.BOOMBUNK2BOOMER, RB.CanLaunchStar),
    locname.BOOMBUNK2DARLS: SMG2LocationData(["Launch Stars"], regname.BOWJR3, regname.BOOMBUNK2DARK, RB.CanLaunchStar),

    locname.MELTY1MAGLS: SMG2LocationData(["Launch Stars"], regname.MELTY, regname.MELTY1MAGMAARG, RB.CanLaunchStar),
    locname.MELTY1LAVLS: SMG2LocationData(["Launch Stars"], regname.MELTY, regname.MELTY1LAVAWAVE3, RB.CanLaunchStar),
    locname.MELTY2ROLLS: SMG2LocationData(["Launch Stars"], regname.MELTY, regname.MELTY2LANDING, RB.CanLaunchStar),

    locname.CLOCKWORK1COGLS: SMG2LocationData(["Launch Stars"], regname.CLOCKWORK, regname.CLOCKWORK1COGS, RB.CanLaunchStar),
    locname.CLOCKWORK1PUSLS: SMG2LocationData(["Launch Stars"], regname.CLOCKWORK, regname.CLOCKWORK1PUSH, RB.CanLaunchStar),

    locname.FLASHBLACK1TOWLS: SMG2LocationData(["Launch Stars"], regname.FLASHBLACK, regname.FLASHBLACK1TOWER, RB.CanLaunchStar),

    locname.SLIMSPRI1CAVLS: SMG2LocationData(["Launch Stars"], regname.SLIMSPRI, regname.SLIMSPRI1CAVE1, RB.CanLaunchStar),
    locname.SLIMSPRI2CAVLS: SMG2LocationData(["Launch Stars"], regname.SLIMSPRI, regname.SLIMSPRI2CAVE1, RB.CanLaunchStar),

    locname.BATTBELT1GOOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1GOOM, RB.CanLaunchStar),
    locname.BATTBELT1CINSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1LAVA, RB.CanLaunchStar),
    locname.BATTBELT1URCSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1URCH, RB.CanLaunchStar),
    locname.BATTBELT1CRASS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1CRAB, RB.CanLaunchStar),
    locname.BATTBELT1PTOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1PTOA, RB.CanLaunchStar),
    locname.BATTBELT1PUMSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1PUMP, RB.CanLaunchStar),
    locname.BATTBELT1RTOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1RTOA, RB.CanLaunchStar),
    locname.BATTBELT1BRRSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1ICEP, RB.CanLaunchStar),
    locname.BATTBELT1SWASS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1MOLE, RB.CanLaunchStar),
    locname.BATTBELT2GOOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2GOOM, RB.CanLaunchStar),
    locname.BATTBELT2CINSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2LAVA, RB.CanLaunchStar),
    locname.BATTBELT2URCSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2URCH, RB.CanLaunchStar),
    locname.BATTBELT2CRASS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2CRAB, RB.CanLaunchStar),
    locname.BATTBELT2PTOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2PTOA, RB.CanLaunchStar),
    locname.BATTBELT2PUMSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2PUMP, RB.CanLaunchStar),
    locname.BATTBELT2RTOSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2RTOA, RB.CanLaunchStar),
    locname.BATTBELT2BRRSS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2ICEP, RB.CanLaunchStar),
    locname.BATTBELT2SWASS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT2MOLE, RB.CanLaunchStar),

    locname.GALGEN1LANLS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN1LANDING, RB.CanLaunchStar),
    locname.GALGEN1LAVLS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN1LAVACYL, RB.CanLaunchStar),
    locname.GALGEN1TOWLS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN1TOWER, RB.CanLaunchStar),
    locname.GALGEN2LAVLS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN2LAVACYL, RB.CanLaunchStar),
    locname.GALGEN2TOWLS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN2TOWER, RB.CanLaunchStar),
    locname.GALGEN1DASSS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN1DASHCAS, RB.CanLaunchStar),
    locname.GALGEN2LANSS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN2LANDING, RB.CanLaunchStar),
    locname.GALGEN2DASSS: SMG2LocationData(["Launch Stars"], regname.BOWSER3, regname.GALGEN2DASHCAS, RB.CanLaunchStar),

    locname.BOSSBLITZ1DINLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ1DINOPIR, RB.CanLaunchStar),
    locname.BOSSBLITZ1KALLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ1KINGKAL, RB.CanLaunchStar),
    locname.BOSSBLITZ1MAJLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ1MAJORBU, RB.CanLaunchStar),
    locname.BOSSBLITZ1BOULS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ1BOULDER, RB.CanLaunchStar),
    locname.BOSSBLITZ1TINLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ1TINYMET, RB.CanLaunchStar),
    locname.BOSSBLITZ2DINLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ2DINOPIR, RB.CanLaunchStar),
    locname.BOSSBLITZ2KALLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ2KINGKAL, RB.CanLaunchStar),
    locname.BOSSBLITZ2MAJLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ2MAJORBU, RB.CanLaunchStar),
    locname.BOSSBLITZ2BOULS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ2BOULDER, RB.CanLaunchStar),
    locname.BOSSBLITZ2TINLS: SMG2LocationData(["Launch Stars"], regname.BOSSBLITZ, regname.BOSSBLITZ2TINYMET, RB.CanLaunchStar),

    locname.GRANDMASTER1YOSLS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1YOSHI, RB.CanLaunchStar),
    locname.GRANDMASTER1SWILS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1SWITCH, RB.CanLaunchStar),
    locname.GRANDMASTER1ELELS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1CLOUD, RB.CanLaunchStar),
    locname.GRANDMASTER1SWALS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1SWAP, RB.CanLaunchStar),
    locname.GRANDMASTER1PULLS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1PULL, RB.CanLaunchStar),
    locname.GRANDMASTER2YOSLS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2YOSHI, RB.CanLaunchStar),
    locname.GRANDMASTER2SWILS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2SWITCH, RB.CanLaunchStar),
    locname.GRANDMASTER2ELELS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2CLOUD, RB.CanLaunchStar),
    locname.GRANDMASTER2SWALS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2SWAP,  RB.CanLaunchStar),
    locname.GRANDMASTER2PULLS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2PULL,  RB.CanLaunchStar),
    locname.GRANDMASTER2JUMLS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2BROS2, RB.CanLaunchStar),
    locname.GRANDMASTER1BROSS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER1BROS1, RB.CanLaunchStar),
    locname.GRANDMASTER2BROSS: SMG2LocationData(["Launch Stars"], regname.GRANDMASTER, regname.GRANDMASTER2BROS1, RB.CanLaunchStar),

    locname.FLUFFY1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1BIGCLOUD,
                                              CanReachEntrance("Fluffy Bluff: Hungry Luma",
                                                               parent_region_name=regname.FLUFFBLUFF1BIGCLOUD) & RB.CanLaunchStar),
    locname.PUZZPL1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.PUZZPLAN, regname.PUZZPLAN1GRUZZY,
                                              CanReachEntrance("Puzzle Plank: Hungry Luma",
                                                               parent_region_name=regname.PUZZPLAN1GRUZZY) & RB.CanLaunchStar),
    locname.HIGHTA1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.HIGHTAIL, regname.HIGHTAIL1DASHWAL1,
                                              CanReachEntrance("Hightail Falls: Hungry Luma",
                                                               parent_region_name=regname.HIGHTAIL1DASHWAL1) & RB.CanLaunchStar),
    locname.COSMIC1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.COSMICO, regname.COSMIC1POOL,
                                              CanReachEntrance("Cosmic Cove: Hungry Luma",
                                                               parent_region_name=regname.COSMIC1POOL) & RB.CanLaunchStar),
    locname.CLOUDY1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.CLOUCOUR, regname.CLOUCOUR1TOWERS,
                                              CanReachEntrance("Cloudy Court: Hungry Luma",
                                                               parent_region_name=regname.CLOUCOUR1TOWERS) & RB.CanLaunchStar),
    locname.CLOCKW1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.CLOCKWORK, regname.CLOCKWORK1COGS,
                                              CanReachEntrance("Clockwork Ruins: Hungry Luma",
                                                               parent_region_name=regname.CLOCKWORK1COGS) & RB.CanLaunchStar),
    locname.BATTLE1HUNGRYLS: SMG2LocationData(["Launch Stars"], regname.BATTLEBELT, regname.BATTBELT1ICEP,
                                              CanReachEntrance("Battle Belt: Hungry Luma",
                                                               parent_region_name=regname.BATTBELT1ICEP) & RB.CanLaunchStar),
}

pipe_locations: dict[str, SMG2LocationData] = {
    locname.SKYOBS1HOUPIG: SMG2LocationData(["Pipe Location"], regname.SKYOBS, regname.SKYOBS1STARTTOPSIDE,
                                            RB.CanPipe),
    locname.SKYOBS1HOUPIO: SMG2LocationData(["Pipe Location"], regname.SKYOBS, regname.SKYOBS1STARTTOPSIDE,
                                            RB.CanPipe),
    locname.SKYOBS2HOUPIG: SMG2LocationData(["Pipe Location"], regname.SKYOBS, regname.SKYOBS2STARTTOPSIDE,
                                            RB.CanPipe),
    locname.SKYOBS3HOUPIG: SMG2LocationData(["Pipe Location"], regname.SKYOBS, regname.SKYOBS3STARTTOPSIDE,
                                            RB.CanPipe),
    locname.SKYOBS3HOUPIO: SMG2LocationData(["Pipe Location"], regname.SKYOBS, regname.SKYOBS3STARTTOPSIDE,
                                            RB.CanPipe),
    locname.SPIND2CAN1PIG: SMG2LocationData(["Pipe Location"], regname.SPINDIG, regname.SPINDIG2DARKT,
                                            RB.CanPipe),
    locname.SPIND2CAN2PIG: SMG2LocationData(["Pipe Location"], regname.SPINDIG, regname.SPINDIG2DARKIN1,
                                            RB.CanPipe & RB.DRILLMASTER),
    locname.SPINDI2CANPIO: SMG2LocationData(["Pipe Location"], regname.SPINDIG, regname.SPINDIG2DARKIN2,
                                            RB.CanPipe & RB.DRILLMASTER),
    locname.FLUFF1LANDPIG: SMG2LocationData(["Pipe Location"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1LANDING,
                                            RB.CanPipe),
    locname.RIGHTDOWN1LANPIG: SMG2LocationData(["Pipe Location"], regname.RIGHTDOWN, regname.RIGHTDOWNLANDING,
                                            RB.CanPipe),
    locname.RIGHTDOWN1CORPIG: SMG2LocationData(["Pipe Location"], regname.RIGHTDOWN, regname.RIGHTDOWNLANDING,
                                            RB.CanPipe),
    locname.RIGHTDOWN1PIO: SMG2LocationData(["Pipe Location"], regname.RIGHTDOWN, regname.RIGHTDOWNCORRIDOR,
                                            RB.CanPipe & RB.FireMario),
    locname.PUZZPL1GRUPIG: SMG2LocationData(["Pipe Location"], regname.PUZZPLAN, regname.PUZZPLAN1GRUZZY,
                                            RB.CanPipe),
    locname.PUZZPLAN2PIG:  SMG2LocationData(["Pipe Location"], regname.PUZZPLAN, regname.PUZZPLAN2GRUZZY,
                                            RB.CanPipe),
    locname.BOULBO1BOUPIG: SMG2LocationData(["Pipe Location"], regname.BOULBOWL, regname.BOULBOWL1BOULDER,
                                            RB.CanPipe & RB.CanSwim),
    locname.COSMIC1POOPIG: SMG2LocationData(["Pipe Location"], regname.COSMICO, regname.COSMIC1POOL,
                                            RB.CanPipe),
    locname.COSMIC2PIG1:   SMG2LocationData(["Pipe Location"], regname.COSMICO, regname.COSMIC2LANDING,
                                            RB.CanPipe),
    locname.COSMIC2PIG2:   SMG2LocationData(["Pipe Location"], regname.COSMICO, regname.COSMIC2INPIPE,
                                            RB.CanPipe & RB.CanWallJump & RB.CanSwim),
    locname.COSMIC2PIG3:   SMG2LocationData(["Pipe Location"], regname.COSMICO, regname.COSMIC2WATERPA,
                                            RB.CanPipe & RB.CanSwim),
    locname.TALLTR1LOGPIG: SMG2LocationData(["Pipe Location"], regname.TALLTRUNK, regname.TALLTRUNK1LOG,
                                            RB.CanPipe),
    locname.HAUNTY1DISPIG: SMG2LocationData(["Pipe Location"], regname.HAUNHALL, regname.HAUNHALL1DISAPPE,
                                            RB.CanPipe),
    locname.FREEZY1CHIPIG: SMG2LocationData(["Pipe Location"], regname.FREEFLAKE, regname.FREEFLAK1SNOWBYH,
                                            RB.CanPipe & RB.FireMario),
    locname.FREEZY1SLIPIG: SMG2LocationData(["Pipe Location"], regname.FREEFLAKE, regname.FREEFLAK1SLIDELA,
                                            RB.CanPipe & RB.FireMario),
    locname.FREEZY2CHIPIG: SMG2LocationData(["Pipe Location"], regname.FREEFLAKE, regname.FREEFLAK2SNOWBYH,
                                            RB.CanPipe & RB.ROCKNROLLIN),
    locname.FREEZY2WHIPIG: SMG2LocationData(["Pipe Location"], regname.FREEFLAKE, regname.FREEFLAK2WHITOUT,
                                            RB.CanPipe),
    locname.FLIPVI2TOWPIG: SMG2LocationData(["Pipe Location"], regname.FLIPVILL, regname.FLIPVILL2PIPE,
                                            RB.CanPipe),
    locname.FLIPVI3TOWPIG: SMG2LocationData(["Pipe Location"], regname.FLIPVILL, regname.FLIPVILL3TOWER,
                                            RB.CanPipe),
    locname.HONEYH1PONPIG: SMG2LocationData(["Pipe Location"], regname.HONEYHOP, regname.HONEYHOP1POND,
                                            RB.CanPipe),
    locname.STARSH1BEAPIG: SMG2LocationData(["Pipe Location"], regname.STARBEACH, regname.STARBEACH1MAIN,
                                            RB.CanPipe),
    locname.STARSH2BEAPIG: SMG2LocationData(["Pipe Location"], regname.STARBEACH, regname.STARBEACH2MAIN,
                                            RB.CanPipe),
    locname.CHOMPW1ROLPIG: SMG2LocationData(["Pipe Location"], regname.CHOMWORK, regname.CHOMWORK1ROLLING,
                                            RB.CanPipe),
    locname.SPACES2TOWPIG: SMG2LocationData(["Pipe Location"], regname.SPACSTOR, regname.SPACSTOR2TOPTOWER,
                                            RB.CanPipe),
    locname.UPDOWN1CASPIG: SMG2LocationData(["Pipe Location"], regname.UPDOWN, regname.UPDOWNCASTLE,
                                            RB.CanPipe),
    locname.UPDOWN1INPIG1: SMG2LocationData(["Pipe Location"], regname.UPDOWN, regname.UPDOWNINSTART,
                                            RB.CanPipe),
    locname.UPDOWN1BREPIO: SMG2LocationData(["Pipe Location"], regname.UPDOWN, regname.UPDOWNFIRE,
                                            RB.CanPipe & RB.FireMario),
    locname.UPDOWN1INPIG2: SMG2LocationData(["Pipe Location"], regname.UPDOWN, regname.UPDOWNINEND,
                                            RB.CanPipe & (RB.CanPound | (RB.HardLogic & RB.CanAirSpin)
                                                          | (RB.CanBackflip & RB.CanWallJump & RB.HellLogic))),
    locname.SLIPSA1LONPIG: SMG2LocationData(["Pipe Location"], regname.SLIPSAND, regname.SLIPSAND1LONG,
                                            RB.CanPipe),
    locname.SLIPSA2LONPIG: SMG2LocationData(["Pipe Location"], regname.SLIPSAND, regname.SLIPSAND2LONG1,
                                            RB.CanPipe),
    locname.SLIPSA2LONPIO: SMG2LocationData(["Pipe Location"], regname.SLIPSAND, regname.SLIPSAND2GRAV,
                                            RB.CanPipe & (RB.CanWallJump | RB.CanGrabLedge
                                                          | RB.JumpHeight3 | (RB.HardLogic & RB.CanDouble))), ########
    locname.SHIVBU1CHIPIG: SMG2LocationData(["Pipe Location"], regname.SHIVBURN, regname.SHIVBURN1VOLCANO,
                                            RB.CanPipe & ((RB.CanMakeCloud & (RB.CanPound | RB.CanLongJump | RB.HardLogic))
                                                       | (RB.HardLogic & RB.CanPound & (RB.CanLongJump | RB.HellLogic)))),
    locname.MELTYM1CHIPIG: SMG2LocationData(["Pipe Location"], regname.MELTY, regname.MELTY1LANDING,
                                            RB.CanPipe),
    locname.MELTYM2CHIPIG: SMG2LocationData(["Pipe Location"], regname.MELTY, regname.MELTY2LANDING,
                                            RB.CanPipe),
    locname.CLOCKW1WHEPIG: SMG2LocationData(["Pipe Location"], regname.CLOCKWORK, regname.CLOCKWORK1WHEELST,
                                            RB.CanPipe),
    locname.CLOCKW3HAMPIG: SMG2LocationData(["Pipe Location"], regname.CLOCKWORK, regname.CLOCKWORK3HAMMER,
                                            RB.CanPipe),
    locname.SLIMYS1LANPIG: SMG2LocationData(["Pipe Location"], regname.SLIMSPRI, regname.SLIMSPRI1MOUTH1,
                                            RB.CanPipe & (RB.CanGrabLedge | RB.JumpHeight3 | (RB.CanDouble & RB.MediumLogic))),
    locname.BATTLE1JACPIG: SMG2LocationData(["Pipe Location"], regname.BATTLEBELT, regname.BATTBELT1PUMP,
                                            RB.CanPipe),
    locname.BATTLE1SWAPIG: SMG2LocationData(["Pipe Location"], regname.BATTLEBELT, regname.BATTBELT1MOLE,
                                            RB.CanPipe & RB.CanPound),
    locname.BATTLE2JACPIG: SMG2LocationData(["Pipe Location"], regname.BATTLEBELT, regname.BATTBELT2PUMP,
                                            RB.CanPipe),
    locname.BATTLE2SWAPIG: SMG2LocationData(["Pipe Location"], regname.BATTLEBELT, regname.BATTBELT2MOLE,
                                            RB.CanPipe & RB.CanPound),
    locname.FLIPOU1LANPIG: SMG2LocationData(["Pipe Location"], regname.FLIPOUT, regname.FLIPOUT1LANDING,
                                            RB.CanPipe),
    locname.FLIPOU2LANPIG: SMG2LocationData(["Pipe Location"], regname.FLIPOUT, regname.FLIPOUT2LANDING,
                                            RB.CanPipe),
    locname.SHIP2EARPIPE:  SMG2LocationData(["Pipe Location"], regname.SHIP2, regname.SHIP2,
                                            RB.CanPipe),
}

event_locations: dict[str, SMG2LocationData] = {
    "Melty Monster 2 Starbit Farming": SMG2LocationData(["Event"], regname.MELTY, regname.MELTY2BOWLING,
                                                        RB.CanStarbitShoot, locked_item="Can Farm Starbits"),
    "Sweet Mystery Starbit Farming": SMG2LocationData(["Event"], regname.SWEETMYS, regname.SWEETMYS1CHOCO,
                                                        RB.CanStarbitShoot, locked_item="Can Farm Starbits"),
    "Rightside Down Coin Farming": SMG2LocationData(["Event"], regname.RIGHTDOWN, regname.RIGHTDOWNTOPVIEW,
                                                    locked_item="Can Farm Coins"),
    "Fluffy Bluff Coin Farming": SMG2LocationData(["Event"], regname.FLUFFBLUFF, regname.FLUFFBLUFF3TOWER,
                                                    locked_item="Can Farm Coins"),
    "Tall Trunk 2 Starbit Farming": SMG2LocationData(["Event"], regname.TALLTRUNK, regname.TALLTRUNK2SLIDE,
                                                     locked_item="Can Farm Starbits"),
    "Tall Trunk 2 Coin Farming": SMG2LocationData(["Event"], regname.TALLTRUNK, regname.TALLTRUNK2SLIDE,
                                                     locked_item="Can Farm Coins"),
    "Shiverburn Comet Starbit Farming": SMG2LocationData(["Event"], regname.SHIVBURN, regname.SHIVBURN2ROMP,
                                                         locked_item="Can Farm Starbits", default_access=RB.SUPAPOWA),
    "Puzzle Plank Comet Starbit Farming": SMG2LocationData(["Event"], regname.PUZZPLAN, regname.PUZZPLAN2COINRO,
                                                         locked_item="Can Farm Starbits"),
    "Cloudy Court Comet Starbit Farming": SMG2LocationData(["Event"], regname.PUZZPLAN, regname.PUZZPLAN2COINRO,
                                                           locked_item="Can Farm Starbits", default_access=RB.CanWallJump),
    "Twisty Trials Starbit Farming": SMG2LocationData(["Event"], regname.TWISTTRI, regname.TWISTY1PLAT4,
                                                           locked_item="Can Farm Starbits"),
}


special_locations: dict[str, SMG2LocationData] = {
    locname.VISITWORLD1: SMG2LocationData(["Specials"], regname.WORLD1, regname.WORLD1),
    locname.VISITWORLD2: SMG2LocationData(["Specials"], regname.WORLD2, regname.WORLD2),
    locname.VISITWORLD3: SMG2LocationData(["Specials"], regname.WORLD3, regname.WORLD3),
    locname.VISITWORLD4: SMG2LocationData(["Specials"], regname.WORLD4, regname.WORLD4),
    locname.VISITWORLD5: SMG2LocationData(["Specials"], regname.WORLD5, regname.WORLD5),
    locname.VISITWORLD6: SMG2LocationData(["Specials"], regname.WORLD6, regname.WORLD6),
    locname.VISITWORLD7: SMG2LocationData(["Specials"], regname.WORLD7, regname.WORLD7),
    locname.SPEAKTOLUBB: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIP),
    locname.OPENWORLDMP: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIP),
}

oneup_locations: dict[str, SMG2LocationData] = {

}

dice_block_locations: dict[str, SMG2LocationData] = {
    locname.SHIPABOVEGDIE: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIP),
    locname.LUMA1CHANCDIE: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            RB.PowerStarCount(18)),
    locname.LUMA2CHANDIE1: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            CanReachLocation(locname.MELTMONSSTAR1)),
    locname.LUMA2CHANDIE2: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            CanReachLocation(locname.MELTMONSSTAR1)),
    locname.LUMA2CHANDIE3: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            CanReachLocation(locname.MELTMONSSTAR1)),
    locname.LUMA2CHANDIE4: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            CanReachLocation(locname.MELTMONSSTAR1)),
    locname.LUMA2CHANDIE5: SMG2LocationData(["Specials"], regname.SHIP, regname.SHIPLEFTEAR,
                                            CanReachLocation(locname.MELTMONSSTAR1)),
    locname.YOSHIS1DIRDIE: SMG2LocationData(["Specials"], regname.GOODEGG, regname.GOODEGG1EARTH),
    locname.BOULDE1BODIE1: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.BOULDE1BODIE2: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.BOULDE1BODIE3: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.BOULDE1BODIE4: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.BOULDE1BODIE5: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.BOULDE1BODIE6: SMG2LocationData(["Specials"], regname.BOULBOWL, regname.BOULBOWL1DICEROOM),
    locname.TALLTR1BODIE1: SMG2LocationData(["Specials"], regname.TALLTRUNK, regname.TALLTRUNK1DICEPIPE),
    locname.TALLTR1BODIE2: SMG2LocationData(["Specials"], regname.TALLTRUNK, regname.TALLTRUNK1DICEPIPE),
    locname.TALLTR1BODIE3: SMG2LocationData(["Specials"], regname.TALLTRUNK, regname.TALLTRUNK1DICEPIPE),
    locname.FREFLASNOWDIE: SMG2LocationData(["Specials"], regname.FREEFLAKE, regname.FREEFLAK1SNOWBYH),
    locname.FREFLA2BODIE1: SMG2LocationData(["Specials"], regname.FREEFLAKE, regname.FREEFLAK2DICEROOM),
    locname.FREFLA2BODIE2: SMG2LocationData(["Specials"], regname.FREEFLAKE, regname.FREEFLAK2DICEROOM),
    locname.FREFLA2BODIE3: SMG2LocationData(["Specials"], regname.FREEFLAKE, regname.FREEFLAK2DICEROOM),
    locname.CHOMPW1BODIE1: SMG2LocationData(["Specials"], regname.CHOMWORK, regname.CHOMWORK1BONUS),
    locname.CHOMPW1BODIE2: SMG2LocationData(["Specials"], regname.CHOMWORK, regname.CHOMWORK1BONUS),
    locname.CHOMPW1BODIE3: SMG2LocationData(["Specials"], regname.CHOMWORK, regname.CHOMWORK1BONUS),
    locname.HONEYH1BODIE1: SMG2LocationData(["Specials"], regname.HONEYHOP, regname.HONEYHOP1DICEROOM),
    locname.HONEYH1BODIE2: SMG2LocationData(["Specials"], regname.HONEYHOP, regname.HONEYHOP1DICEROOM),
    locname.HONEYH1BODIE3: SMG2LocationData(["Specials"], regname.HONEYHOP, regname.HONEYHOP1DICEROOM),
    locname.BOOMBUSTRTDIE: SMG2LocationData(["Specials"], regname.BOWJR3, regname.BOOMBUNK1HAMMER),
    locname.THROWBASRTDIE: SMG2LocationData(["Specials"], regname.WHOMPFORT, regname.WHOMP1FORT),
}



base_stars_locations = {**SKYOBS_loc, **YOSHTAR_loc, **SPINDIG_loc, **FLUFBLUF_loc, **RIGHTDOWN_loc,
                        **FLIPSWAP_loc, **WILDGLIDE_loc, **ROLLMAST_loc, **HONEYHOP_loc, **UPDIZZY_loc,
                        **SLIMSPRI_loc, **BEEBLOOM_loc, **BEATBLOCK_loc, **SWEETMYS_loc, **FLETGLIDE_loc,
                        **FLASHBLACK_loc, **FLIPOUT_loc, **MARIOSQ_loc, **ROLLSLIDE_loc, **TWISTTRI_loc,
                        **STONECYC_loc, **BOSSBLITZ_loc, **GRANDMASTER_loc, **FIREFLOT_loc, **GRAVGAUN_loc,
                        **GALGEN_loc, **LAVALAIR_loc, **FEARFLET_loc, **BOOMBUNK_loc, **PUZZPLANK_loc,
                        **HIGHFALL_loc, **ROCKBOWL_loc, **COSCCOVE_loc, **TALLTREE_loc, **CLOUDCOURT_loc,
                        **HAUNTHALL_loc, **SNOWFLAKE_loc, **SUPMASS_loc, **FLIPVILL_loc, **STARBEACH_loc,
                        **CHOMWORK_loc, **SPACSTOR_loc, **SLIPSAND_loc, **COLDFIRE_loc, **BOOMOON_loc,
                        **MELTMONS_loc, **CLOCKRUIN_loc, **THROWBACK_loc, **BATTBELT_loc, **special_locations,
                        **oneup_locations, **dice_block_locations}

all_location_table = {**base_stars_locations, **green_star_locations, **COMETMEDAL_loc, **mailtoad_locations,
                      **checkpoint_loc_table, **hungry_luma_loc, **passenger_loc, **lumalee_locations,
                      **pipe_locations, **launch_star_locs, **special_locations}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: list(all_location_table.keys()).index(name) for name in all_location_table.keys() }

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in all_location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories