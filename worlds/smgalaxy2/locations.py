from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Rule, Has, True_

from .Constants.Names import region_names as regname
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname
from .Constants.Names.region_names import WILDGLIDECOURSE
from .Options import EnableGreenStars
from .Rules import GreenStarRule


class SMG2Location(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMG2Location, self).__init__(player, name, address=location_table[name].code, parent=parent)
        self.code = location_table[name].code

class SMG2LocationData(NamedTuple):
    location_groups: list[str]
    galaxy: str# type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    default_access: Rule[Any] = True_()
    game_address: Optional[int] = 0
#TODO Add Hungry Luma, Comets and Checkpoint locations to base table
# Sky Station S
SKYOBS_loc: dict[str, SMG2LocationData] = {
    locname.SKYSTASTAR1: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS1BOSS, 1, ),
    locname.SKYSTASTAR2: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS2GRASSFLEET, 1, ),
    locname.SKYSTASTAR3: SMG2LocationData([regname.SKYOBS, "Power Star Location"],
                                          regname.SKYOBS, regname.SKYOBS3BOSS, 1, ),
}

# Yoshi Star St
YOSHTAR_loc: dict[str, SMG2LocationData] = {
    locname.YOSHSTARSTAR1: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG1FOSSIL ,1),
    locname.YOSHSTARSTAR2: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG2BOSS ,1),
    locname.YOSHSTARSTAR3: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG,
                                            regname.GOODEGG3LANDING ,1),
}

# Spin-Dig Star
SPINDIG_loc: dict[str, SMG2LocationData] = {
    locname.SPINDIGSTAR1: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG1BOSS, 2),
    locname.SPINDIGSTAR2: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG2SQUARE, 2),
    locname.SPINDIGSTAR3: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG,
                                           regname.SPINDIG3BOSS, 2),
}

# Fluffy Bluff
FLUFBLUF_loc: dict[str, SMG2LocationData] = {
    locname.FLUFBLUFSTAR1: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF1TREECLIMB, 2),
    locname.FLUFBLUFSTAR2: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF2LANDING, 2),
    locname.FLUFBLUFSTAR3: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF,
                                            regname.FLUFFBLUFF3TOWER, 2),
}

# Rightside Dow
RIGHTDOWN_loc: dict[str, SMG2LocationData] = {
    locname.RIGHTDOWNSTAR1: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN,
                                             regname.RIGHTDOWNTOPVIEW, 1),
    locname.RIGHTDOWNSTAR2: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN,
                                             regname.RIGHTDOWNBREAKER, 1),
}

# Flip-Swap Sta
FLIPSWAP_loc: dict[str, SMG2LocationData] = {
    locname.FLIPSWAPSTAR1: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP,
                                            regname.FLIPSWAP1, 2),
    locname.FLIPSWAPSTAR2: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP,
                                            regname.FLIPSWAP2, 2),
}

# Bowser Jr.s F
FIREFLOT_loc: dict[str, SMG2LocationData] = {
locname.FIREFLOTSTAR1:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT1BOSS, 1),
locname.FIREFLOTSTAR2:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT2BOSS, 1),
}

# World 2
# Puzzle Plank
PUZZPLANK_loc: dict[str, SMG2LocationData] = {
    locname.PUZZPLANKSTAR1:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN1MANDIB, 1),
    locname.PUZZPLANKSTAR2:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN2COINRO, 1),
    locname.PUZZPLANKSTAR3:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                              regname.PUZZPLAN3BUGABO, 1),
}

# Hightail Fall
HIGHFALL_loc: dict[str, SMG2LocationData] = {
    locname.HIGHFALLSTAR1:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL1DASHWAL2, 1),
    locname.HIGHFALLSTAR2:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL2DASHWAL2, 1),
    locname.HIGHFALLSTAR3:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                             regname.HIGHTAIL3SILVERS, 1),
}

# Boulder Bowl
ROCKBOWL_loc: dict[str, SMG2LocationData] = {
    locname.ROCKBOWLSTAR1:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL1BOSS, 1),
    locname.ROCKBOWLSTAR2:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL2CAGEPLA, 1),
    locname.ROCKBOWLSTAR3:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                             regname.BOULBOWL1BOULDER, 1),
}

# Cosmic Cove S
COSCCOVE_loc: dict[str, SMG2LocationData] = {
    locname.COSCCOVESTAR1:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC1WATERFA,1 ),
    locname.COSCCOVESTAR2:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC2WATERPL2, 1),
    locname.COSCCOVESTAR3:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO,
                                             regname.COSMIC3WATER,1 ),
}

# Wild Glide St
WILDGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.WILDGLIDESTAR1: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                             WILDGLIDECOURSE, 1),
    locname.WILDGLIDESTAR2: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                             WILDGLIDECOURSE, 1),
}

# Honeybloom St
BEEBLOOM_loc: dict[str, SMG2LocationData] = {
    locname.BEEBLOOMSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                            regname.HONEYBLOOM1HONELOG,1),
    locname.BEEBLOOMSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                            regname.HONEYBLOOM1SECRET,1),
}

# Bowser's Lava
LAVALAIR_loc: dict[str, SMG2LocationData] = {
    locname.LAVALAIRSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1,
                                            regname.LAVALAIR1BOSSPLA,1 ),
    locname.LAVALAIRSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1,
                                            regname.LAVALAIR2LAVAPLA2S,1 ),
}

# World 3
# Tall Trunk St
TALLTREE_loc: dict[str, SMG2LocationData] = {
    locname.TALLTREESTAR1: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK1WOODCIRClE,1,),
    locname.TALLTREESTAR2: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK2SLIDEND,1,),
    locname.TALLTREESTAR3: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                            regname.TALLTRUNK3PCOINEND,1,),
}

# Cloudy Court
CLOUDCOURT_loc: dict[str, SMG2LocationData] = {
    locname.CLOUDCOURTSTAR1: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR1CASTLE,1),
    locname.CLOUDCOURTSTAR2: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR2FINAL,1),
    locname.CLOUDCOURTSTAR3: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                              regname.CLOUCOUR3PCOINS,1),
}

    # Haunty Halls
HAUNTHALL_loc: dict[str, SMG2LocationData] = {
    locname.HAUNTHALLSTAR1: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL1BULBBER, 1),
    locname.HAUNTHALLSTAR2: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL2CREEPYH, 1),
    locname.HAUNTHALLSTAR3: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL,
                                             regname.HAUNHALL3CREEPYH, 1),
}

    # Freezy Flake
SNOWFLAKE_loc: dict[str, SMG2LocationData] = {
    locname.SNOWFLAKESTAR1: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK1LAVASNO, 1),
    locname.SNOWFLAKESTAR2: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK2SORBETT, 1),
    locname.SNOWFLAKESTAR3: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                             regname.FREEFLAK3CHIMP, 1),
}

    # Rolling Maste
ROLLMAST_loc: dict[str, SMG2LocationData] = {
    locname.ROLLMASTERSTAR1: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                              regname.ROLLMAST1SILVERC, 1),
    locname.ROLLMASTERSTAR2: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                              regname.ROLLMAST2SILVERC, 1),
}

    # Beat Block St
BEATBLOCK_loc: dict[str, SMG2LocationData] = {
    locname.BEATBLOCKSTAR1: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                             regname.BEATBLOK1, 1),
    locname.BEATBLOCKSTAR2: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                             regname.BEATBLOK2, 1),
}

    # Bowser Jr.'s
FEARFLET_loc: dict[str, SMG2LocationData] = {
    locname.FEARFLETSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2,
                                            regname.FEARFLET1MEGAHAM, 1),
    locname.FEARFLETSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2,
                                            regname.FEARFLET2MEGAHAM, 1),
}

    # World 4
    # Supermassive
SUPMASS_loc: dict[str, SMG2LocationData] = {
    locname.SUPERMASSSTAR1: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS1WIGGLERS, 1),
    locname.SUPERMASSSTAR2: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS1GARDEN, 1),
    locname.SUPERMASSSTAR3: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS,
                                             regname.SUPMASS2WIGGLERS, 1),
}

    # Flipsville St
FLIPVILL_loc: dict[str, SMG2LocationData] = {
    locname.FLIPVILLESTAR1: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL1STAR, 1),
    locname.FLIPVILLESTAR2: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL2GRAVITYMAIN, 1),
    locname.FLIPVILLESTAR3: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                             regname.FLIPVILL3GRAVITY, 1),
}

    # Starshine Bea
STARBEACH_loc: dict[str, SMG2LocationData] = {
    locname.STARBEACHSTAR1: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH1MAIN, 1),
    locname.STARBEACHSTAR2: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH2MAIN, 1),
    locname.STARBEACHSTAR3: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH,
                                             regname.STARBEACH3MAIN, 1),
}

    # Chompworks St
CHOMWORK_loc: dict[str, SMG2LocationData] = {
    locname.CHOMPWORKSTAR1: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK),
    locname.CHOMPWORKSTAR2: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK),
    locname.CHOMPWORKSTAR3: SMG2LocationData(["Power Star Location", regname.CHOMWORK], regname.CHOMWORK),
}

    # Honeyhop Star
HONEYHOP_loc: dict[str, SMG2LocationData] = {
    locname.HONEYHOPSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP),
    locname.HONEYHOPSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYHOP], regname.HONEYHOP),
}

    # Sweet Mystery
SWEETMYS_loc: dict[str, SMG2LocationData] = {
    locname.SWEETMYSTSTAR1: SMG2LocationData(["Power Star Location", regname.SWEETMYS], regname.SWEETMYS),
    locname.SWEETMYSTSTAR2: SMG2LocationData(["Power Star Location", regname.SWEETMYS], regname.SWEETMYS),
}

    # Bowser's Grav
GRAVGAUN_loc: dict[str, SMG2LocationData] = {
    locname.GRAVGAUNSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2,
                                            regname.GRAVGAUN1BOSSARE, 1),
    locname.GRAVGAUNSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2,
                                            regname.GRAVGAUN2WHOMPWA, 1),
}

    # World 5
    # Space Storm S
SPACSTOR_loc: dict[str, SMG2LocationData] = {
    locname.SPACESTORMSTAR1: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR1PULLPATH, 1),
    locname.SPACESTORMSTAR2: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR2TOPTOWER, 1),
    locname.SPACESTORMSTAR3: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                              regname.SPACSTOR1TOPMAN, 1 ),
}

    # Slipsand Star
SLIPSAND_loc: dict[str, SMG2LocationData] = {
    locname.SLIPSANDSTAR1: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND1BOSS, 1),
    locname.SLIPSANDSTAR2: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND2BIRD, 1),
    locname.SLIPSANDSTAR3: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                            regname.SLIPSAND3BOSS, 1),
}

    # Shiverburn St
COLDFIRE_loc: dict[str, SMG2LocationData] = {
    locname.COLDFIRESTAR1: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN1BOSS ,1),
    locname.COLDFIRESTAR2: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN2ROMP ,1),
    locname.COLDFIRESTAR3: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                            regname.SHIVBURN3CHIMP ,1),
}

    # Boo Moon Star
BOOMOON_loc: dict[str, SMG2LocationData] = {
    locname.BOOMOONSTAR1: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON1POPUP , 1),
    locname.BOOMOONSTAR2: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON2TOWER , 1),
    locname.BOOMOONSTAR3: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON,
                                           regname.BOOMOON1POISON , 1),
}

    # Upside Dizzy
UPDIZZY_loc: dict[str, SMG2LocationData] = {
    locname.UPDIZZYSTAR1: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN,
                                           regname.UPDOWNGRAV, 1),
    locname.UPDIZZYSTAR2: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN,
                                           regname.UPDOWNBREAKER, 1),
}

    # Fleet Glide S
FLETGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.FLEETFLYSTAR1: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                            regname.FLEETGLIDECOURSE, 2),
    locname.FLEETFLYSTAR2: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                            regname.FLEETGLIDECOURSE, 2),
}

    # Bowser Jr.'s
BOOMBUNK_loc: dict[str, SMG2LocationData] = {
    locname.BOOMBUNKSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3,
                                            regname.BOOMBUNK1BOSS, 1),
    locname.BOOMBUNKSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3,
                                            regname.BOOMBUNK2BOSS, 1),
}

    # World 6
    # Melty Monster
MELTMONS_loc: dict[str, SMG2LocationData] = {
    locname.MELTMONSSTAR1: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY1MAGMAW, 2),
    locname.MELTMONSSTAR2: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY2BOWLING, 2),
    locname.MELTMONSSTAR3: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY,
                                            regname.MELTY3CHIMP, 2),
}

    # Clockwork Rui
CLOCKRUIN_loc: dict[str, SMG2LocationData] = {
    locname.CLOCKRUINSTAR1: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK1WHEELST, 1),
    locname.CLOCKRUINSTAR2: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK2COGS, 1),
    locname.CLOCKRUINSTAR3: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                             regname.CLOCKWORK3HAMMERTOP, 1),
}

    # Throwback Sta
THROWBACK_loc: dict[str, SMG2LocationData] = {
    locname.THROWBACKSTAR1: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP1UNDER, 1),
    locname.THROWBACKSTAR2: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP2FORT, 1),
    locname.THROWBACKSTAR3: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                             regname.WHOMP3FORT, 1),
}

    # Battle Belt S
BATTBELT_loc: dict[str, SMG2LocationData] = {
    locname.BATTBELTSTAR1: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT1CHOM, 1),
    locname.BATTBELTSTAR2: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT2CHOM, 1),
    locname.BATTBELTSTAR3: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                            regname.BATTBELT3BOSS, 1),
}

    # Flash Black S
FLASHBLACK_loc: dict[str, SMG2LocationData] = {
    locname.FLASHBLACKSTAR1: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                              regname.FLASHBLACK1PATH, 2),
    locname.FLASHBLACKSTAR2: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                              regname.FLASHBLACK2PATH, 2),
}

    # Slimy Spring
SLIMSPRI_loc: dict[str, SMG2LocationData] = {
    locname.SLIMYSPRISTAR1: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                             regname.SLIMSPRI1CAVE2, 1),
    locname.SLIMYSPRISTAR2: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                             regname.SLIMSPRI2MOUTH1, 1),
}

    # Bowser's Gala
GALGEN_loc: dict[str, SMG2LocationData] = {
    locname.GALAXYGENSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3,
                                             regname.GALGEN1BOSS, 1),
    locname.GALAXYGENSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3,
                                             regname.GALGEN2STATUE, 1),
}

    # World S
    # Mario Squared
MARIOSQ_loc: dict[str, SMG2LocationData] = {
    locname.MARIOSQRSTAR1: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO,
                                            regname.MARIOSQ1RIGHT, 1),
    locname.MARIOSQRSTAR2: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO,
                                            regname.MARIOSQ2LEFT, 1),
}

    # Rolling Coast
ROLLSLIDE_loc: dict[str, SMG2LocationData] = {
    locname.ROLLSLIDESTAR1: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                             regname.ROLLCOAST1, 1),
    locname.ROLLSLIDESTAR2: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                             regname.ROLLCOAST2, 1),
}

    # Twisty Trials
TWISTTRI_loc: dict[str, SMG2LocationData] = {
    locname.TWISTTRIALSTAR1: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                              regname.TWISTY1PLAT4, 1),
    locname.TWISTTRIALSTAR2: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                              regname.TWISTY2PLAT4, 1),
}

    # Stone Cyclone
STONECYC_loc: dict[str, SMG2LocationData] = {
    locname.STONECYCLOSTAR1: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC,
                                              regname.STONECYC1, 1),
    locname.STONECYCLOSTAR2: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC,
                                              regname.STONECYC2, 1),
}

    # Boss Blitz St
BOSSBLITZ_loc: dict[str, SMG2LocationData] = {
    locname.BOSSBLITSTAR1: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                            regname.BOSSBLITZ1DINOPIR, 1),
    locname.BOSSBLITSTAR2: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                            regname.BOSSBLITZ2DINOPIR, 1),
}

    # Flip-Out Star
FLIPOUT_loc: dict[str, SMG2LocationData] = {
    locname.FLIPOUTSTAR1: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                           regname.FLIPOUT1CLIMB, 1),
    locname.FLIPOUTSTAR2: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                           regname.FLIPOUT2CLIMB, 1),
}

    # Grandmaster
GRANDMASTER_loc: dict[str, SMG2LocationData] = {
    locname.GRANDMASTSTAR1: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                             regname.GRANDMASTER1BROS2,1),
    locname.GRANDMASTSTAR2: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                             regname.GRANDMASTER2ROSA,1),
}

green_star_locations: dict[str, SMG2LocationData]  = {
    locname.SKYSTASTARG1:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS1GSTAR1, 1, ),
    locname.SKYSTASTARG2:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS1GREENHILL, 1, ),
    locname.SKYSTASTARG3:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS,
                                                 regname.SKYOBS2SKYFLEET, 1, ),
    locname.YOSHSTARSTARG1:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGGGSTAR1 , 1,),
    locname.YOSHSTARSTARG2:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGGGSTAR2 , 1, ),
    locname.YOSHSTARSTARG3:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG, 
                                                 regname.GOODEGG1FOSSIL , 1, ),
    locname.SPINDIGSTARG1:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG1DRILL , 1, ),
    locname.SPINDIGSTARG2:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG1STEEL , 1, ),
    locname.SPINDIGSTARG3:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG,
                                                 regname.SPINDIG2DARKIN1 , 1, ),
    locname.FLUFBLUFSTARG1:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1LANDING, 1, ),
    locname.FLUFBLUFSTARG2:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1BUILDING, 1, ),
    locname.FLUFBLUFSTARG3:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                                 regname.FLUFFBLUFF1TREECLIMB, 1, ),
    locname.RIGHTDOWNSTARG1:    SMG2LocationData(["Green Star Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                 regname.RIGHTDOWNCORRIDOR,1,),
    locname.RIGHTDOWNSTARG2:    SMG2LocationData(["Green Star Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                                 regname.RIGHTDOWNTOPVIEW,1,),
    locname.FLIPSWAPSTARG1:     SMG2LocationData(["Green Star Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                                 regname.FLIPSWAP1, 1, ),
    locname.FLIPSWAPSTARG2:     SMG2LocationData(["Green Star Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                                 regname.FLIPSWAP1, 1, ),
    locname.FIREFLOTSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR1], regname.BOWJR1,
                                                 regname.FIREFLOT1LANDING, 1,),
    locname.FIREFLOTSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR1], regname.BOWJR1,
                                                 regname.FIREFLOT1LAVA, 1,),
    locname.PUZZPLANKSTARG1:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1BLOCK, 1,),
    locname.PUZZPLANKSTARG2:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA, 1,),
    locname.PUZZPLANKSTARG3:    SMG2LocationData(["Green Star Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                                 regname.PUZZPLAN1SAWBLA, 1,),
    locname.HIGHFALLSTARG1:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR1, 1,),
    locname.HIGHFALLSTARG2:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR2, 1,),
    locname.HIGHFALLSTARG3:     SMG2LocationData(["Green Star Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                                 regname.HIGHTAILGSTAR3, 1,),
    locname.ROCKBOWLSTARG1:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1CRYSTAL, 1,),
    locname.ROCKBOWLSTARG2:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1CRYSTAL, 1,),
    locname.ROCKBOWLSTARG3:     SMG2LocationData(["Green Star Location", regname.BOULBOWL], regname.BOULBOWL,
                                                 regname.BOULBOWL1FALLING, 1,),
    locname.COSCCOVESTARG1:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC1WATERFA, 1, ),
    locname.COSCCOVESTARG2:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC2WATERPA, 1, ),
    locname.COSCCOVESTARG3:     SMG2LocationData(["Green Star Location", regname.COSMICO], regname.COSMICO,
                                                 regname.COSMIC2WATERPA, 1, ),
    locname.WILDGLIDESTARG1:    SMG2LocationData(["Green Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                                 regname.WILDGLIDECOURSE, 1,),
    locname.WILDGLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                                 regname.WILDGLIDECOURSE, 1,),
    locname.BEEBLOOMSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3,1,),
    locname.BEEBLOOMSTARG2:     SMG2LocationData(["Green Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                                 regname.HONEYBLOOM1WALL3,1,),
    locname.LAVALAIRSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA1W, 1,),
    locname.LAVALAIRSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWSER1], regname.BOWSER1,
                                                 regname.LAVALAIR1LAVAPLA2C, 1,),
    locname.TALLTREESTARG1:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1BIGTREE, 1, ),
    locname.TALLTREESTARG2:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK1LOG, 1, ),
    locname.TALLTREESTARG3:     SMG2LocationData(["Green Star Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                                 regname.TALLTRUNK2SLIDE, 1, ),
    locname.CLOUDCOURTSTARG1:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1LANDING, 1, ),
    locname.CLOUDCOURTSTARG2:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CYMBAL, 1, ),
    locname.CLOUDCOURTSTARG3:   SMG2LocationData(["Green Star Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                                 regname.CLOUCOUR1CASTLE , 1, ),
    locname.HAUNTHALLSTARG1:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1HALLWAY, 1,),
    locname.HAUNTHALLSTARG2:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL1DISAPPE, 1,),
    locname.HAUNTHALLSTARG3:    SMG2LocationData(["Green Star Location",regname.HAUNHALL],regname.HAUNHALL,
                                                 regname.HAUNHALL2CREEPYH, 1,),
    locname.SNOWFLAKESTARG1:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1SLIDELA, 1,),
    locname.SNOWFLAKESTARG2:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK1LAVASNO, 1,),
    locname.SNOWFLAKESTARG3:    SMG2LocationData(["Green Star Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                                 regname.FREEFLAK2WHITOUT, 1,),
    locname.ROLLMASTERSTARG1:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1ELEVATO, 1,),
    locname.ROLLMASTERSTARG2:   SMG2LocationData(["Green Star Location", regname.ROLLMAST], regname.ROLLMAST,
                                                 regname.ROLLMAST1SILVERC, 1,),
    locname.BEATBLOCKSTARG1:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, 1,),
    locname.BEATBLOCKSTARG2:    SMG2LocationData(["Green Star Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                                 regname.BEATBLOK1, 1,),
    locname.FEARFLETSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1UNDERGR, 1,),
    locname.FEARFLETSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR2], regname.BOWJR2,
                                                 regname.FEARFLET1AIRSHIP, 1,),
    locname.SUPERMASSSTARG1:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1PIPES, 1,),
    locname.SUPERMASSSTARG2:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1GSTAR2, 1,),
    locname.SUPERMASSSTARG3:    SMG2LocationData(["Green Star Location", regname.SUPMASS], regname.SUPMASS,
                                                 regname.SUPMASS1KOOPAS, 1,),
    locname.FLIPVILLESTARG1:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1MAZETOP, 1,),
    locname.FLIPVILLESTARG2:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1WANWANLANE, 1,),
    locname.FLIPVILLESTARG3:    SMG2LocationData(["Green Star Location", regname.FLIPVILL], regname.FLIPVILL,
                                                 regname.FLIPVILL1LIFTBELOW, 1,),
    locname.STARBEACHSTARG1:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN, 1, ),
    locname.STARBEACHSTARG2:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH1MAIN, 1, ),
    locname.STARBEACHSTARG3:    SMG2LocationData(["Green Star Location", regname.STARBEACH], regname.STARBEACH,
                                                 regname.STARBEACH2MAIN, 1, ),
    locname.CHOMPWORKSTARG1:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK, 1,
                                                 ),
    locname.CHOMPWORKSTARG2:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK, 1,
                                                 ),
    locname.CHOMPWORKSTARG3:    SMG2LocationData(["Green Star Location", regname.CHOMWORK], regname.CHOMWORK, 1,
                                                 ),
    locname.HONEYHOPSTARG1:     SMG2LocationData(["Green Star Location", regname.HONEYHOP], regname.HONEYHOP, 1,
                                                 ),
    locname.HONEYHOPSTARG2:     SMG2LocationData(["Green Star Location", regname.HONEYHOP], regname.HONEYHOP, 1,
                                                 ),
    locname.SWEETMYSTSTARG1:    SMG2LocationData(["Green Star Location", regname.SWEETMYS], regname.SWEETMYS, 1,
                                                 ),
    locname.SWEETMYSTSTARG2:    SMG2LocationData(["Green Star Location", regname.SWEETMYS], regname.SWEETMYS, 1,
                                                 ),
    locname.GRAVGAUNSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUNGSTAR1, 1,),
    locname.GRAVGAUNSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWSER2], regname.BOWSER2,
                                                 regname.GRAVGAUNGSTAR2, 1,),
    locname.SPACESTORMSTARG1:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR1PULL, 1, ),
    locname.SPACESTORMSTARG2:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR2TOPTOWERBASE , 1, ),
    locname.SPACESTORMSTARG3:   SMG2LocationData(["Green Star Location", regname.SPACSTOR], regname.SPACSTOR,
                                                 regname.SPACSTOR2GSTAR2, 1, ),
    locname.SLIPSANDSTARG1:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1CUBE , 1, ),
    locname.SLIPSANDSTARG2:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE , 1, ),
    locname.SLIPSANDSTARG3:     SMG2LocationData(["Green Star Location", regname.SLIPSAND], regname.SLIPSAND,
                                                 regname.SLIPSAND1SLIDE , 1, ),
    locname.COLDFIRESTARG1:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1VOLCANO , 1, ),
    locname.COLDFIRESTARG2:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1LAVA , 1, ),
    locname.COLDFIRESTARG3:     SMG2LocationData(["Green Star Location", regname.SHIVBURN], regname.SHIVBURN,
                                                 regname.SHIVBURN1FIREICE , 1, ),
    locname.BOOMOONSTARG1:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POISON ,1, ),
    locname.BOOMOONSTARG2:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1MOON ,1, ),
    locname.BOOMOONSTARG3:      SMG2LocationData(["Green Star Location", regname.BOOMOON], regname.BOOMOON,
                                                 regname.BOOMOON1POPUP ,1, ),
    locname.UPDIZZYSTARG1:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINSIDE, 1,),
    locname.UPDIZZYSTARG2:      SMG2LocationData(["Green Star Location", regname.UPDOWN], regname.UPDOWN,
                                                 regname.UPDOWNINSIDE, 1,),
    locname.FLEETFLYSTARG1:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDECOURSE, 1, ),
    locname.FLEETFLYSTARG2:     SMG2LocationData(["Green Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                                 regname.FLEETGLIDECOURSE, 1, ),
    locname.BOOMBUNKSTARG1:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1BOOMER, 1, ),
    locname.BOOMBUNKSTARG2:     SMG2LocationData(["Green Star Location", regname.BOWJR3], regname.BOWJR3,
                                                 regname.BOOMBUNK1CHECK, 1, ),
    locname.MELTMONSSTARG1:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1MAGMAARG, 1, ),
    locname.MELTMONSSTARG2:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY1LAVAWAVE3, 1, ),
    locname.MELTMONSSTARG3:     SMG2LocationData(["Green Star Location", regname.MELTY], regname.MELTY,
                                                 regname.MELTY2BOWLING, 1, ),
    locname.CLOCKRUINSTARG1:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1COGS, 1, ),
    locname.CLOCKRUINSTARG2:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1PUSH, 1, ),
    locname.CLOCKRUINSTARG3:    SMG2LocationData(["Green Star Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                                 regname.CLOCKWORK1WHEELST, 1, ),
    locname.THROWBACKSTARG1:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT, 1, ),
    locname.THROWBACKSTARG2:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP1FORT, 1, ),
    locname.THROWBACKSTARG3:    SMG2LocationData(["Green Star Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                                 regname.WHOMP2FORT, 1, ),
    locname.BATTBELTSTARG1:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT],regname.BATTLEBELT,
                                                 regname.BATTBELT1PUMP, 1, ),
    locname.BATTBELTSTARG2:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1MOLE, 1, ),
    locname.BATTBELTSTARG3:     SMG2LocationData(["Green Star Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                                 regname.BATTBELT1CHOM, 1, ),
    locname.FLASHBLACKSTARG1:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1TOWER, 1,),
    locname.FLASHBLACKSTARG2:   SMG2LocationData(["Green Star Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                                 regname.FLASHBLACK1PATH, 1,),
    locname.SLIMYSPRISTARG1:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1, 1, ),
    locname.SLIMYSPIRSTARG2:    SMG2LocationData(["Green Star Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                                 regname.SLIMSPRI1CAVE1, 1, ),
    locname.GALAXYGENSTARG1:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1VOLCANO, 1,),
    locname.GALAXYGENSTARG2:    SMG2LocationData(["Green Star Location", regname.BOWSER3], regname.BOWSER3,
                                                 regname.GALGEN1DASHCAS, 1,),
    locname.MARIOSQRSTARG1:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN, 1,),
    locname.MARIOSQRSTARG2:     SMG2LocationData(["Green Star Location", regname.MARIO], regname.MARIO,
                                                 regname.MARIOSQ1MAIN, 1,),
    locname.ROLLSLIDESTARG1:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, 1, ),
    locname.ROLLSLIDESTARG2:    SMG2LocationData(["Green Star Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                                 regname.ROLLCOAST1, 1, ),
    locname.TWISTTRIALSTARG1:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT2, 1,),
    locname.TWISTTRIALSTARG2:   SMG2LocationData(["Green Star Location", regname.TWISTTRI], regname.TWISTTRI,
                                                 regname.TWISTY1PLAT4, 1,),
    locname.STONECYCLOSTARG1:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, 1,),
    locname.STONECYCLOSTARG2:   SMG2LocationData(["Green Star Location", regname.STONECYC], regname.STONECYC,
                                                 regname.STONECYC1, 1,),
    locname.BOSSBLITSTARG1:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1MAJORBU, 1,),
    locname.BOSSBLITSTARG2:     SMG2LocationData(["Green Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                                 regname.BOSSBLITZ1BOULDER, 1,),
    locname.FLIPOUTSTARG1:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT1CLIMB, 1,),
    locname.FLIPOUTSTARG2:      SMG2LocationData(["Green Star Location", regname.FLIPOUT], regname.FLIPOUT,
                                                 regname.FLIPOUT2CLIMB, 1,),
}

#TODO Comet Medals Table
COMETMEDAL_loc:dict[str, SMG2LocationData] = {
    locname.SKYSTACM: SMG2LocationData(["Comet Medal Location", regname.SKYOBS], regname.SKYOBS,
                                       regname.SKYOBS1CYLINDER,  1, ),
    locname.YOSHSTARCM: SMG2LocationData(["Comet Medal Location", regname.GOODEGG], regname.GOODEGG,
                                         regname.GOODEGG1LANDING,  1, ),
    locname.SPINDIGCM: SMG2LocationData(["Comet Medal Location", regname.SPINDIG], regname.SPINDIG,
                                        regname.SPINDIG1DRILL,  1, ),
    locname.FLUFBLUFCM: SMG2LocationData(["Comet Medal Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF,
                                         regname.FLUFFBLUFF1WATER,  1, ),
    locname.RIGHTDOWNCM: SMG2LocationData(["Comet Medal Location", regname.RIGHTDOWN], regname.RIGHTDOWN,
                                          regname.RIGHTDOWNCORRIDOR, 1, ),
    locname.FLIPSWAPCM: SMG2LocationData(["Comet Medal Location", regname.FLIPSWAP], regname.FLIPSWAP,
                                         regname.FLIPSWAP1,  1, ),
    locname.FIREFLOTCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR1], regname.BOWJR1,
                                         regname.FIREFLOT1LANDING, 1, ),
    locname.PUZZPLANKCM: SMG2LocationData(["Comet Medal Location", regname.PUZZPLAN], regname.PUZZPLAN,
                                          regname.PUZZPLAN1SAWBLA,  1, ),
    locname.HIGHFALLCM: SMG2LocationData(["Comet Medal Location", regname.HIGHTAIL], regname.HIGHTAIL,
                                         regname.HIGHTAIL1DASHWAL1,  1, ),
    locname.ROCKBOWLCM: SMG2LocationData(["Comet Medal Location", regname.BOULBOWL], regname.BOULBOWL,
                                         regname.BOULBOWL1CRYSTAL,  1, ),
    locname.COSCCOVECM: SMG2LocationData(["Comet Medal Location", regname.COSMICO], regname.COSMICO,
                                         regname.COSMIC1POOL,  1, ),
    locname.WILDGLIDECM: SMG2LocationData(["Comet Medal Location", regname.WILDGLIDE], regname.WILDGLIDE,
                                          regname.WILDGLIDECOURSE,  1, ),
    locname.BEEBLOOMCM: SMG2LocationData(["Comet Medal Location", regname.HONEYBLOOM], regname.HONEYBLOOM,
                                         regname.HONEYBLOOM1WALL2,  1, ),
    locname.LAVALAIRCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER1], regname.BOWSER1,
                                         regname.LAVALAIR1LAVAPLA1W,  1, ),
    locname.TALLTREECM: SMG2LocationData(["Comet Medal Location", regname.TALLTRUNK], regname.TALLTRUNK,
                                         regname.TALLTRUNK1LOG,  1, ),
    locname.CLOUDCOURTCM: SMG2LocationData(["Comet Medal Location", regname.CLOUCOUR], regname.CLOUCOUR,
                                           regname.CLOUCOUR1TOWERS,  1, ),
    locname.HAUNTHALLCM: SMG2LocationData(["Comet Medal Location", regname.HAUNHALL], regname.HAUNHALL,
                                          regname.HAUNHALL1DISAPPE,  1, ),
    locname.SNOWFLAKECM: SMG2LocationData(["Comet Medal Location", regname.FREEFLAKE], regname.FREEFLAKE,
                                          regname.FREEFLAK1SLIDELA,  1, ),
    locname.ROLLMASTERCM: SMG2LocationData(["Comet Medal Location", regname.ROLLMAST], regname.ROLLMAST,
                                           regname.ROLLMAST1SAWBLAD,  1, ),
    locname.BEATBLOCKCM: SMG2LocationData(["Comet Medal Location", regname.BEATBLOCK], regname.BEATBLOCK,
                                          regname.BEATBLOK1,  1, ),
    locname.FEARFLEETCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR2], regname.BOWJR2,
                                          regname.FEARFLET1AIRSHIP, 1, ),
    locname.SUPERMASSCM: SMG2LocationData(["Comet Medal Location", regname.SUPMASS], regname.SUPMASS,
                                          regname.SUPMASS1START,  1, ),
    locname.FLIPVILLECM: SMG2LocationData(["Comet Medal Location", regname.FLIPVILL], regname.FLIPVILL,
                                          regname.FLIPVILL1COMETMEDAL,  1, ),
    locname.STARBEACHCM: SMG2LocationData(["Comet Medal Location", regname.STARBEACH], regname.STARBEACH,
                                          regname.STARBEACH1MAIN, 1, ),
    locname.CHOMPWORKCM: SMG2LocationData(["Comet Medal Location", regname.CHOMWORK], regname.CHOMWORK,
                                          regname.,  1, ),
    locname.HONEYHOPCM: SMG2LocationData(["Comet Medal Location", regname.HONEYHOP], regname.HONEYHOP,
                                         regname.,  1, ),
    locname.SWEETMYSTCM: SMG2LocationData(["Comet Medal Location", regname.SWEETMYS], regname.SWEETMYS,
                                          regname.,  1, ),
    locname.GRAVGAUNTCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER2], regname.BOWSER2,
                                          regname.GRAVGAUN1LANDING,  1, ),
    locname.SPACESTORMCM: SMG2LocationData(["Comet Medal Location", regname.SPACSTOR], regname.SPACSTOR,
                                           regname.SPACSTOR1SATELLITE,  1, ),
    locname.SLIPSANDCM: SMG2LocationData(["Comet Medal Location", regname.SLIPSAND], regname.SLIPSAND,
                                         regname.SLIPSAND1CUBE,  1, ),
    locname.COLDFIRECM: SMG2LocationData(["Comet Medal Location", regname.SHIVBURN], regname.SHIVBURN,
                                         regname.SHIVBURN1LAVA,  1, ),
    locname.BOOMOONCM: SMG2LocationData(["Comet Medal Location", regname.BOOMOON], regname.BOOMOON,
                                        regname.BOOMOON1POISON,  1, ),
    locname.UPDIZZYCM: SMG2LocationData(["Comet Medal Location", regname.UPDOWN], regname.UPDOWN,
                                        regname.UPDOWNGRAV,  1, ),
    locname.FLEETFLYCM: SMG2LocationData(["Comet Medal Location", regname.FLEETGLIDE], regname.FLEETGLIDE,
                                         regname.FLEETGLIDECOURSE,  1, ),
    locname.BOOMBUNKCM: SMG2LocationData(["Comet Medal Location", regname.BOWJR3], regname.BOWJR3,
                                         regname.BOOMBUNK1PLAT,  1, ),
    locname.MELTMONSCM: SMG2LocationData(["Comet Medal Location", regname.MELTY], regname.MELTY,
                                         regname.MELTY1MAGMAW,  1, ),
    locname.CLOCKRUINSCM: SMG2LocationData(["Comet Medal Location", regname.CLOCKWORK], regname.CLOCKWORK,
                                           regname.CLOCKWORK1WHEELSB,  1, ),
    locname.THROWBACKCM: SMG2LocationData(["Comet Medal Location", regname.WHOMPFORT], regname.WHOMPFORT,
                                          regname.WHOMP1FORT,  1, ),
    locname.BATTBELTCM: SMG2LocationData(["Comet Medal Location", regname.BATTLEBELT], regname.BATTLEBELT,
                                         regname.BATTBELT1LAVA,  1, ),
    locname.FLASHBLACKCM: SMG2LocationData(["Comet Medal Location", regname.FLASHBLACK], regname.FLASHBLACK,
                                           regname.FLASHBLACK1TOWER,  1, ),
    locname.SLIMYSPRICM: SMG2LocationData(["Comet Medal Location", regname.SLIMSPRI], regname.SLIMSPRI,
                                          regname.SLIMSPRI1CAVE1,  1, ),
    locname.GLXYGENCM: SMG2LocationData(["Comet Medal Location", regname.BOWSER3], regname.BOWSER3,
                                        regname.GALGEN1LAVASNA,  1, ),
    locname.MARIOSQRCM: SMG2LocationData(["Comet Medal Location", regname.MARIO], regname.MARIO,
                                         regname.MARIOSQ1LEFT,  1, ),
    locname.ROLLSLIDECM: SMG2LocationData(["Comet Medal Location", regname.ROLLCOAST], regname.ROLLCOAST,
                                          regname.ROLLCOAST1,  1, ),
    locname.TWISTTRIALCM: SMG2LocationData(["Comet Medal Location", regname.TWISTTRI], regname.TWISTTRI,
                                           regname.TWISTY1PLAT4,  1, ),
    locname.STONECYCLOCM: SMG2LocationData(["Comet Medal Location", regname.STONECYC], regname.STONECYC,
                                           regname.STONECYC1,  1, ),
    locname.BOSSBLITCM: SMG2LocationData(["Comet Medal Location", regname.BOSSBLITZ], regname.BOSSBLITZ,
                                         regname.BOSSBLITZ1KINGKAL,  1, ),
    locname.FLIPOUTCM: SMG2LocationData(["Comet Medal Location", regname.FLIPOUT], regname.FLIPOUT,
                                        regname.FLIPOUT1CLIMB,  1, ),
    locname.GRANDMASTRCM: SMG2LocationData(["Comet Medal Location", regname.GRANDMASTER], regname.GRANDMASTER,
                                           regname.GRANDMASTER1BROS2,  1, ),
}

#TODO Checkpoint Table

#TODO Add Pipe Table

#TODO Add Launch Star table here

#TODO Add NPC table here - vanilla unlock requirement

#TODO Add Mailtoad Letters table here - vanilla unlock requirement

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

location_table = { **base_stars_locations, **green_star_locations
}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in location_table.items() if data.code is not None}

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories