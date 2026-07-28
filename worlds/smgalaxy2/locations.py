from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, Has, True_, CanReachRegion

from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname
from .Options import EnableGreenStars
from . import Rules as RB


class SMG2Location(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMG2Location, self).__init__(player, name, address=all_location_table[name].code, parent=parent)
        self.code: int = list(all_location_table.keys()).index(name)

class SMG2LocationData(NamedTuple):
    location_groups: list[str]
    galaxy: str# type of randomization option table and group []
    region: str
    default_access: Rule[Any] = True_()
    game_address: Optional[int] = 0
    locked_item: str = None
#TODO Add Hungry Luma, Comets and Checkpoint locations to base table
# Sky Station S
SKYOBS_loc: dict[str, SMG2LocationData] = {
    locname.SKYSTASTAR1: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS1BOSS),
    locname.SKYSTASTAR2: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS2GRASSFLEET, 1,
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
                                              &CanReachRegion(regname.FLUFFBLUFF2TREE)))),
    locname.FLUFBLUFSTAR3: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF3TOWER, RB.CanMakeCloud),
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
                                             regname.BOULBOWL1BOULDER, RB.ROCKNROLLIN),
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
                                             regname.WILDGLIDECOURSE),
    locname.WILDGLIDESTAR2: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                             regname.WILDGLIDECOURSE),
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
                                             regname.FLIPVILL1STAR, RB.CanPound),
    locname.FLIPVILLESTAR2: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL2GRAVITYMAIN, RB.DRILLMASTER),
    locname.FLIPVILLESTAR3: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL3GRAVITY, RB.DRILLMASTER),
}

    # Starshine Bea
STARBEACH_loc: dict[str, SMG2LocationData] = {
    locname.STARBEACHSTAR1: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH1MAIN,
                                             RB.CanDinoSwing&RB.CanDinoBlimp&RB.CanDinoRun),
    locname.STARBEACHSTAR2: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH2MAIN, RB.CanMakeCloud&RB.CanSwim),
    locname.STARBEACHSTAR3: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH3MAIN, RB.CanDinoRun),
}

    # Chompworks St
CHOMWORK_loc: dict[str, SMG2LocationData] = {
    locname.CHOMPWORKSTAR1: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK1LAVA),
    locname.CHOMPWORKSTAR2: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK2TOWER, RB.SPRONGIN),
    locname.CHOMPWORKSTAR3: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                             regname.CHOMWORK3LAVA),
}

    # Honeyhop Star
HONEYHOP_loc: dict[str, SMG2LocationData] = {
    locname.HONEYHOPSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                            regname.HONEYHOP1QBTOP),
    locname.HONEYHOPSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                            regname.HONEYHOP1QBBASE,
                                            CanReachRegion(regname.HONEYHOP2QBBUBBLE)&CanReachRegion(regname.HONEYHOP2QBTOP)),
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
                                              regname.SPACSTOR2TOPTOWER, RB.JumpHeight5),
    locname.SPACESTORMSTAR3: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR1TOPMAN),
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
                                            regname.SHIVBURN2ROMP, RB.SUPAPOWA),
    locname.COLDFIRESTAR3: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN3CHIMP),
}

    # Boo Moon Star
BOOMOON_loc: dict[str, SMG2LocationData] = {
    locname.BOOMOONSTAR1: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON1POPUP, RB.CanWallJump),
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
                                            regname.FLEETGLIDECOURSE, RB.CanRideBird),
    locname.FLEETFLYSTAR2: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                            regname.FLEETGLIDECOURSE, RB.CanRideBird),
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
                                             regname.SLIMSPRI2MOUTH1, CanReachRegion(regname.SLIMSPRI2CAVE2)),
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
                                              regname.TWISTY2PLAT4, (RB.CanLongSpin|RB.MediumLogic)),
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
                                             regname.GRANDMASTER1BROS2),
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
                                                 ((RB.CanBackOrSideflip & (RB.CanAirSpin | RB.CanRideDino))
                                                 | RB.CanInfiniteFlutter)),
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
                                                 RB.CanMakeCloud | (RB.JumpHeight6 & RB.CanLongJump & RB.HellLogic)),
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
                                                 (RB.JumpHeight6|(RB.JumpHeight5&RB.CanWallSpin))),
    locname.PUZZPLANKSTARG2:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA, RB.CanWallJump),
    locname.PUZZPLANKSTARG3:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA),
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
                                                 regname.WILDGLIDECOURSE),
    locname.WILDGLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                                 regname.WILDGLIDECOURSE),
    locname.BEEBLOOMSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3),
    locname.BEEBLOOMSTARG2:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3, RB.CanSwing&RB.BeeFlight),
    locname.LAVALAIRSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA1W, RB.CanLongSpin),
    locname.LAVALAIRSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA2C),
    locname.TALLTREESTARG1:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1BIGTREE, RB.CanDinoBlimp),
    locname.TALLTREESTARG2:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1LOG, RB.CanDinoBlimp),
    locname.TALLTREESTARG3:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK2SLIDE, RB.CanSlide),
    locname.CLOUDCOURTSTARG1:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1LANDING, RB.CanMakeCloud&RB.JumpHeight5),
    locname.CLOUDCOURTSTARG2:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CYMBAL, RB.CanMakeCloud&RB.CanLongJump),
    locname.CLOUDCOURTSTARG3:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CASTLE,
                                                 (RB.CanMakeCloud&RB.CanLongJump)),
    locname.HAUNTHALLSTARG1:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1HALLWAY, RB.CanAirSpin),
    locname.HAUNTHALLSTARG2:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1DISAPPE, RB.JumpHeight5),
    locname.HAUNTHALLSTARG3:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL2CREEPYH, RB.JumpHeight4),
    locname.SNOWFLAKESTARG1:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1SLIDELA, RB.CanSlide),
    locname.SNOWFLAKESTARG2:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1LAVASNO, RB.CanLongJump|RB.JumpHeight4),
    locname.SNOWFLAKESTARG3:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK2WHITOUT),
    locname.ROLLMASTERSTARG1:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1ELEVATO),
    locname.ROLLMASTERSTARG2:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1SILVERC),
    locname.BEATBLOCKSTARG1:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, RB.JumpHeight5),
    locname.BEATBLOCKSTARG2:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, RB.JumpHeight5),
    locname.FEARFLETSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1UNDERGR, RB.CanRideDino),
    locname.FEARFLETSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1AIRSHIP, RB.JumpHeight4),
    locname.SUPERMASSSTARG1:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1PIPES, RB.JumpHeight6),
    locname.SUPERMASSSTARG2:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1GSTAR2),
    locname.SUPERMASSSTARG3:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1KOOPAS,
                                                 (RB.JumpHeight6|(RB.JumpHeight4&RB.MediumLogic))),
    locname.FLIPVILLESTARG1:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1MAZETOP),
    locname.FLIPVILLESTARG2:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1WANWANLANE, RB.CanWallSpin),
    locname.FLIPVILLESTARG3:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1LIFTBELOW, RB.CanAirSpin),
    locname.STARBEACHSTARG1:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN, RB.JumpHeight5),
    locname.STARBEACHSTARG2:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN),
    locname.STARBEACHSTARG3:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH2MAIN, RB.CanDinoRun&RB.CanAirSpin),
    locname.CHOMPWORKSTARG1:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK1START, RB.CanLongSpin),
    locname.CHOMPWORKSTARG2:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK1FLIPSWAP, RB.JumpHeight5|RB.CanWallSpin),
    locname.CHOMPWORKSTARG3:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK,
                                                 regname.CHOMWORK2TOWER, RB.SPRONGIN),
    locname.HONEYHOPSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYHOP], regname.HONEYHOP,
                                                 regname.HONEYHOP1CLOUDS, RB.BeeFlight),
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
                                                 regname.SPACSTOR2TOPTOWERBASE),
    locname.SPACESTORMSTARG3:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR2GSTAR2),
    locname.SLIPSANDSTARG1:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1CUBE, RB.CanAirSpin),
    locname.SLIPSANDSTARG2:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE, RB.CanSlide),
    locname.SLIPSANDSTARG3:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE, RB.CanSlide),
    locname.COLDFIRESTARG1:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1VOLCANO , RB.CanMakeCloud&RB.CanLongJump),
    locname.COLDFIRESTARG2:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1LAVA),
    locname.COLDFIRESTARG3:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1FIREICE, RB.CanMakeCloud&RB.JumpHeight5),
    locname.BOOMOONSTARG1:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POISON, RB.CanLongSpin),
    locname.BOOMOONSTARG2:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1MOON),
    locname.BOOMOONSTARG3:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POPUP, RB.CanLongSpin&RB.CanWallJump),
    locname.UPDIZZYSTARG1:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINSIDE),
    locname.UPDIZZYSTARG2:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINSIDE, RB.CanWallJump|RB.JumpHeight4),
    locname.FLEETFLYSTARG1:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDECOURSE, RB.CanRideBird),
    locname.FLEETFLYSTARG2:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDECOURSE, RB.CanRideBird),
    locname.BOOMBUNKSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1BOOMER, RB.CanCannon),
    locname.BOOMBUNKSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1CHECK, RB.CanCannon),
    locname.MELTMONSSTARG1:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1MAGMAARG),
    locname.MELTMONSSTARG2:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1LAVAWAVE3, RB.CanSwing&RB.CanAirSpin),
    locname.MELTMONSSTARG3:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY2BOWLING, RB.ROCKNROLLIN),
    locname.CLOCKRUINSTARG1:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1COGS, RB.JumpHeight5),
    locname.CLOCKRUINSTARG2:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1PUSH, RB.JumpHeight5),
    locname.CLOCKRUINSTARG3:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1WHEELST, RB.CanLongSpin),
    locname.THROWBACKSTARG1:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT, RB.JumpHeight5),
    locname.THROWBACKSTARG2:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT),
    locname.THROWBACKSTARG3:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP2FORT, RB.CanMakeCloud&RB.CanLongJump),
    locname.BATTBELTSTARG1:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT],regname.BATTLEBELT,
                                                 regname.BATTBELT1PUMP, RB.JumpHeight3|RB.CanWallSpin),
    locname.BATTBELTSTARG2:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1MOLE, RB.JumpHeight5),
    locname.BATTBELTSTARG3:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1CHOM, RB.JumpHeight3),
    locname.FLASHBLACKSTARG1:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1TOWER, RB.CanDinoBlimp),
    locname.FLASHBLACKSTARG2:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1PATH),
    locname.SLIMYSPRISTARG1:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1),
    locname.SLIMYSPIRSTARG2:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1),
    locname.GALAXYGENSTARG1:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1VOLCANO),
    locname.GALAXYGENSTARG2:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1DASHCAS, ((RB.CanMakeCloud&RB.CanLongJump)
                                                                             |(RB.CanRideDino&RB.CanAirSpin))),
    locname.MARIOSQRSTARG1:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN),
    locname.MARIOSQRSTARG2:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN),
    locname.ROLLSLIDESTARG1:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, RB.CanBalance),
    locname.ROLLSLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, RB.CanBalance),
    locname.TWISTTRIALSTARG1:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT2, RB.CanMakeCloud&RB.CanLongJump),
    locname.TWISTTRIALSTARG2:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT4, RB.CanMakeCloud&RB.CanLongJump),
    locname.STONECYCLOSTARG1:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, RB.JumpHeight5 | RB.CanWallSpin),
    locname.STONECYCLOSTARG2:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, RB.CanLongSpin),
    locname.BOSSBLITSTARG1:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1MAJORBU, RB.JumpHeight4|RB.CanWallSpin),
    locname.BOSSBLITSTARG2:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1BOULDER),
    locname.FLIPOUTSTARG1:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT1LANDING, RB.CanWallSpin),
    locname.FLIPOUTSTARG2:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT2CLIMB, RB.CanWallSpin),
}

#TODO Comet Medals Table
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
                                          regname.WILDGLIDECOURSE),
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
                                          regname.SUPMASS1START, RB.CanLongJump),
    locname.FLIPVILLECM: SMG2LocationData(["Comet Medal Location", regname.FLIPVILL], regname.FLIPVILL,
                                          regname.FLIPVILL1COMETMEDAL),
    locname.STARBEACHCM: SMG2LocationData(["Comet Medal Location", regname.STARBEACH], regname.STARBEACH,
                                          regname.STARBEACH1MAIN, RB.CanSwim),
    locname.CHOMPWORKCM: SMG2LocationData(["Comet Medal Location", regname.CHOMWORK], regname.CHOMWORK,
                                          regname.CHOMWORK1START, RB.JumpHeight5),
    locname.HONEYHOPCM: SMG2LocationData(["Comet Medal Location", regname.HONEYHOP], regname.HONEYHOP,
                                         regname.HONEYHOP1QBBUBBLE, RB.JumpHeight6|RB.CanWallJump),
    locname.SWEETMYSTCM: SMG2LocationData(["Comet Medal Location", regname.SWEETMYS], regname.SWEETMYS,
                                          regname.SWEETMYS1CHOCO, RB.CanDinoGlow),
    locname.GRAVGAUNTCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER2], regname.BOWSER2,
                                          regname.GRAVGAUN1LANDING, RB.CanGrabLedge|RB.JumpHeight2),
    locname.SPACESTORMCM: SMG2LocationData(["Comet Medal Location", regname.SPACSTOR], regname.SPACSTOR,
                                           regname.SPACSTOR1SATELLITE),
    locname.SLIPSANDCM: SMG2LocationData(["Comet Medal Location", regname.SLIPSAND], regname.SLIPSAND,
                                         regname.SLIPSAND1CUBE),
    locname.COLDFIRECM: SMG2LocationData(["Comet Medal Location", regname.SHIVBURN], regname.SHIVBURN,
                                         regname.SHIVBURN1LAVA, (RB.CanLongSpin|RB.JumpHeight4)),
    locname.BOOMOONCM: SMG2LocationData(["Comet Medal Location", regname.BOOMOON], regname.BOOMOON,
                                        regname.BOOMOON1POISON),
    locname.UPDIZZYCM: SMG2LocationData(["Comet Medal Location", regname.UPDOWN], regname.UPDOWN,
                                        regname.UPDOWNGRAV),
    locname.FLEETFLYCM: SMG2LocationData(["Comet Medal Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                         regname.FLEETGLIDECOURSE, RB.CanRideBird),
    locname.BOOMBUNKCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR3], regname.BOWJR3,
                                         regname.BOOMBUNK1PLAT),
    locname.MELTMONSCM: SMG2LocationData(["Comet Medal Location", regname.MELTY], regname.MELTY,
                                         regname.MELTY1MAGMAW, RB.CanLongJump|RB.JumpHeight3),
    locname.CLOCKRUINSCM: SMG2LocationData(["Comet Medal Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                           regname.CLOCKWORK1WHEELSB, RB.JumpHeight5),
    locname.THROWBACKCM: SMG2LocationData(["Comet Medal Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                          regname.WHOMP1FORT, (RB.JumpHeight5|RB.CanWallSpin)&RB.CanClimbPole),
    locname.BATTBELTCM: SMG2LocationData(["Comet Medal Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                         regname.BATTBELT1LAVA, RB.CanAirSpin),
    locname.FLASHBLACKCM: SMG2LocationData(["Comet Medal Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                           regname.FLASHBLACK1TOWER, RB.CanDinoBlimp),
    locname.SLIMYSPRICM: SMG2LocationData(["Comet Medal Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                          regname.SLIMSPRI1CAVE1),
    locname.GLXYGENCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER3], regname.BOWSER3,
                                        regname.GALGEN1LAVASNA),
    locname.MARIOSQRCM: SMG2LocationData(["Comet Medal Location", regname.MARIO], regname.MARIO,
                                         regname.MARIOSQ1LEFT),
    locname.ROLLSLIDECM: SMG2LocationData(["Comet Medal Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                          regname.ROLLCOAST1, RB.CanBalance),
    locname.TWISTTRIALCM: SMG2LocationData(["Comet Medal Location", regname.TWISTTRI], regname.TWISTTRI,
                                           regname.TWISTY1PLAT4, RB.JumpHeight3),
    locname.STONECYCLOCM: SMG2LocationData(["Comet Medal Location", regname.STONECYC], regname.STONECYC,
                                           regname.STONECYC1),
    locname.BOSSBLITCM: SMG2LocationData(["Comet Medal Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                         regname.BOSSBLITZ1KINGKAL, RB.JumpHeight4),
    locname.FLIPOUTCM: SMG2LocationData(["Comet Medal Location", regname.FLIPOUT], regname.FLIPOUT,
                                        regname.FLIPOUT1CLIMB, RB.CanWallSpin),
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
                                          regname.FLIPSWAP1),
    locname.RIGHTDOWNCORRIDORCP1: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR),
    locname.RIGHTDOWNCORRIDORCP2: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR),
    locname.RIGHTDOWNCORRIDORCP3: SMG2LocationData(["Checkpoint Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                   regname.RIGHTDOWNCORRIDOR, RB.FireMario),
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
}

#TODO Add Pipe Table

#TODO Add Launch Star table here

#TODO Add NPC table here - vanilla unlock requirement

#TODO Add Mailtoad Letters table here - vanilla unlock requirement

event_locations: dict[str, SMG2LocationData] = {
    "Melty Monster 2 Starbit Farming": SMG2LocationData(["Event"], regname.MELTY, regname.MELTY2BOWLING,
                                                        RB.CanStarbitShoot, locked_item="Can Farm Starbits"),
    "Sweet Mystery Starbit Farming": SMG2LocationData(["Event"], regname.SWEETMYS, regname.SWEETMYS1CHOCO,
                                                        RB.CanStarbitShoot, locked_item="Can Farm Starbits"),
    "Rightside Down Coin Farming": SMG2LocationData(["Event"], regname.RIGHTDOWN, regname.RIGHTDOWNTOPVIEW,
                                                    locked_item="Can Farm Coins"),
    "Fluffy Bluff Coin Farming": SMG2LocationData(["Event"], regname.FLUFFBLUFF, regname.FLUFFBLUFF1BIGCLOUD,
                                                    locked_item="Can Farm Coins")
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
                        **MELTMONS_loc, **CLOCKRUIN_loc, **THROWBACK_loc, **BATTBELT_loc}

all_location_table = {**base_stars_locations, **green_star_locations, **COMETMEDAL_loc}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: list(all_location_table.keys()).index(name) for name in all_location_table.keys() }

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in all_location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories