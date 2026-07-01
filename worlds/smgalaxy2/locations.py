from typing import Dict, NamedTuple, Optional, Set, Any
from BaseClasses import Location, Region
from rule_builder.rules import Rule

from .Constants.Names import region_names as regname
from .Constants.Names import location_names as locname

class SMG2Location(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMG2Location, self).__init__(player, name, address=location_table[name].code, parent=parent)
        self.code = location_table[name].code

class SMG2LocationData(NamedTuple):
    location_groups: list[str] # type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    default_access: Rule[Any] = True
    game_address: Optional[int] = 0

# Sky Station S
SKYOBS_loc: dict[str, SMG2LocationData] = {
    locname.SKYSTASTAR1: SMG2LocationData([regname.SKYOBS, "Power Star Location"], regname.SKYOBS),
    locname.SKYSTASTAR2: SMG2LocationData([regname.SKYOBS, "Power Star Location"], regname.SKYOBS),
    locname.SKYSTASTAR3: SMG2LocationData([regname.SKYOBS, "Power Star Location"], regname.SKYOBS),
}

# Yoshi Star St
YOSHTAR_loc: dict[str, SMG2LocationData] = {
    locname.YOSHSTARSTAR1: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG),
    locname.YOSHSTARSTAR2: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG),
    locname.YOSHSTARSTAR3: SMG2LocationData([regname.GOODEGG, "Power Star Location"], regname.GOODEGG),
}

# Spin-Dig Star
SPINDIG_loc: dict[str, SMG2LocationData] = {
    locname.SPINDIGSTAR1: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG),
    locname.SPINDIGSTAR2: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG),
    locname.SPINDIGSTAR3: SMG2LocationData([regname.SPINDIG, "Power Star Location"],regname.SPINDIG),
}

# Fluffy Bluff
FLUFBLUF_loc: dict[str, SMG2LocationData] = {
    locname.FLUFBLUFSTAR1: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF),
    locname.FLUFBLUFSTAR2: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF),
    locname.FLUFBLUFSTAR3: SMG2LocationData(["Power Star Location",regname.FLUFFBLUFF],regname.FLUFFBLUFF),
}

# Rightside Dow
RIGHTDOWN_loc: dict[str, SMG2LocationData] = {
    locname.RIGHTDOWNSTAR1: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN),
    locname.RIGHTDOWNSTAR2: SMG2LocationData(["Power Star Location",regname.RIGHTDOWN],regname.RIGHTDOWN),
}

# Flip-Swap Sta
FLIPSWAP_loc: dict[str, SMG2LocationData] = {
    locname.FLIPSWAPSTAR1: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP),
    locname.FLIPSWAPSTAR2: SMG2LocationData(["Power Star Location",regname.FLIPSWAP],regname.FLIPSWAP),
}

# Bowser Jr.s F
FIREFLOT_loc: dict[str, SMG2LocationData] = {
locname.FIREFLOTSTAR1:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1),
locname.FIREFLOTSTAR2:  SMG2LocationData(["Power Star Location", regname.BOWJR1], regname.BOWJR1),
}

# World 2
# Puzzle Plank
PUZZPLANK_loc: dict[str, SMG2LocationData] = {
    locname.PUZZPLANKSTAR1:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN),
    locname.PUZZPLANKSTAR2:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN),
    locname.PUZZPLANKSTAR3:  SMG2LocationData(["Power Star Location", regname.PUZZPLAN], regname.PUZZPLAN),
}

# Hightail Fall
HIGHFALL_loc: dict[str, SMG2LocationData] = {
    locname.HIGHFALLSTAR1:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL),
    locname.HIGHFALLSTAR2:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL),
    locname.HIGHFALLSTAR3:  SMG2LocationData(["Power Star Location", regname.HIGHTAIL], regname.HIGHTAIL),
}

# Boulder Bowl
ROCKBOWL_loc: dict[str, SMG2LocationData] = {
    locname.ROCKBOWLSTAR1:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL),
    locname.ROCKBOWLSTAR2:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL),
    locname.ROCKBOWLSTAR3:  SMG2LocationData(["Power Star Location", regname.BOULBOWL], regname.BOULBOWL),
}

# Cosmic Cove S
COSCCOVE_loc: dict[str, SMG2LocationData] = {
    locname.COSCCOVESTAR1:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO),
    locname.COSCCOVESTAR2:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO),
    locname.COSCCOVESTAR3:  SMG2LocationData(["Power Star Location", regname.COSMICO], regname.COSMICO),
}

# Wild Glide St
WILDGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.WILDGLIDESTAR1: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE),
    locname.WILDGLIDESTAR2: SMG2LocationData(["Power Star Location", regname.WILDGLIDE], regname.WILDGLIDE),
}

# Honeybloom St
BEEBLOOM_loc: dict[str, SMG2LocationData] = {
    locname.BEEBLOOMSTAR1: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM),
    locname.BEEBLOOMSTAR2: SMG2LocationData(["Power Star Location", regname.HONEYBLOOM], regname.HONEYBLOOM),
}

# Bowser's Lava
LAVALAIR_loc: dict[str, SMG2LocationData] = {
    locname.LAVALAIRSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1),
    locname.LAVALAIRSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER1], regname.BOWSER1),
}

# World 3
# Tall Trunk St
TALLTREE_loc: dict[str, SMG2LocationData] = {
    locname.TALLTREESTAR1: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK),
    locname.TALLTREESTAR2: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK),
    locname.TALLTREESTAR3: SMG2LocationData(["Power Star Location", regname.TALLTRUNK], regname.TALLTRUNK),
}

# Cloudy Court
CLOUDCOURT_loc: dict[str, SMG2LocationData] = {
    locname.CLOUDCOURTSTAR1: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR),
    locname.CLOUDCOURTSTAR2: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR),
    locname.CLOUDCOURTSTAR3: SMG2LocationData(["Power Star Location", regname.CLOUCOUR], regname.CLOUCOUR),
}

    # Haunty Halls
HAUNTHALL_loc: dict[str, SMG2LocationData] = {
    locname.HAUNTHALLSTAR1: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL),
    locname.HAUNTHALLSTAR2: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL),
    locname.HAUNTHALLSTAR3: SMG2LocationData(["Power Star Location", regname.HAUNHALL], regname.HAUNHALL),
}

    # Freezy Flake
SNOWFLAKE_loc: dict[str, SMG2LocationData] = {
    locname.SNOWFLAKESTAR1: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE),
    locname.SNOWFLAKESTAR2: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE),
    locname.SNOWFLAKESTAR3: SMG2LocationData(["Power Star Location", regname.FREEFLAKE], regname.FREEFLAKE),
}

    # Rolling Maste
ROLLMAST_loc: dict[str, SMG2LocationData] = {
    locname.ROLLMASTERSTAR1: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST),
    locname.ROLLMASTERSTAR2: SMG2LocationData(["Power Star Location", regname.ROLLMAST], regname.ROLLMAST),
}

    # Beat Block St
BEATBLOCK_loc: dict[str, SMG2LocationData] = {
    locname.BEATBLOCKSTAR1: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK),
    locname.BEATBLOCKSTAR2: SMG2LocationData(["Power Star Location", regname.BEATBLOCK], regname.BEATBLOCK),
}

    # Bowser Jr.'s
FEARFLET_loc: dict[str, SMG2LocationData] = {
    locname.FEARFLETSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2),
    locname.FEARFLETSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR2], regname.BOWJR2),
}

    # World 4
    # Supermassive
SUPMASS_loc: dict[str, SMG2LocationData] = {
    locname.SUPERMASSSTAR1: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS),
    locname.SUPERMASSSTAR2: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS),
    locname.SUPERMASSSTAR3: SMG2LocationData(["Power Star Location", regname.SUPMASS], regname.SUPMASS),
}

    # Flipsville St
FLIPVILL_loc: dict[str, SMG2LocationData] = {
    locname.FLIPVILLESTAR1: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL),
    locname.FLIPVILLESTAR2: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL),
    locname.FLIPVILLESTAR3: SMG2LocationData(["Power Star Location", regname.FLIPVILL], regname.FLIPVILL),
}

    # Starshine Bea
STARBEACH_loc: dict[str, SMG2LocationData] = {
    locname.STARBEACHSTAR1: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH),
    locname.STARBEACHSTAR2: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH),
    locname.STARBEACHSTAR3: SMG2LocationData(["Power Star Location", regname.STARBEACH], regname.STARBEACH),
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
    locname.GRAVGAUNSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2),
    locname.GRAVGAUNSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER2], regname.BOWSER2),
}

    # World 5
    # Space Storm S
SPACSTOR_loc: dict[str, SMG2LocationData] = {
    locname.SPACESTORMSTAR1: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR),
    locname.SPACESTORMSTAR2: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR),
    locname.SPACESTORMSTAR3: SMG2LocationData(["Power Star Location", regname.SPACSTOR], regname.SPACSTOR),
}

    # Slipsand Star
SLIPSAND_loc: dict[str, SMG2LocationData] = {
    locname.SLIPSANDSTAR1: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND),
    locname.SLIPSANDSTAR2: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND),
    locname.SLIPSANDSTAR3: SMG2LocationData(["Power Star Location", regname.SLIPSAND], regname.SLIPSAND),
}

    # Shiverburn St
COLDFIRE_loc: dict[str, SMG2LocationData] = {
    locname.COLDFIRESTAR1: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN),
    locname.COLDFIRESTAR2: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN),
    locname.COLDFIRESTAR3: SMG2LocationData(["Power Star Location", regname.SHIVBURN], regname.SHIVBURN),
}

    # Boo Moon Star
BOOMOON_loc: dict[str, SMG2LocationData] = {
    locname.BOOMOONSTAR1: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON),
    locname.BOOMOONSTAR2: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON),
    locname.BOOMOONSTAR3: SMG2LocationData(["Power Star Location", regname.BOOMOON], regname.BOOMOON),
}

    # Upside Dizzy
UPDIZZY_loc: dict[str, SMG2LocationData] = {
    locname.UPDIZZYSTAR1: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN),
    locname.UPDIZZYSTAR2: SMG2LocationData(["Power Star Location", regname.UPDOWN], regname.UPDOWN),
}

    # Fleet Glide S
FLETGLIDE_loc: dict[str, SMG2LocationData] = {
    locname.LEETFLYSTAR1: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE),
    locname.LEETFLYSTAR2: SMG2LocationData(["Power Star Location", regname.FLEETGLIDE], regname.FLEETGLIDE),
}

    # Bowser Jr.'s
BOOMBUNK_loc: dict[str, SMG2LocationData] = {
    locname.BOOMBUNKSTAR1: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3),
    locname.BOOMBUNKSTAR2: SMG2LocationData(["Power Star Location", regname.BOWJR3], regname.BOWJR3),
}

    # World 6
    # Melty Monster
MELTMONS_loc: dict[str, SMG2LocationData] = {
    locname.MELTMONSSTAR1: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY),
    locname.MELTMONSSTAR2: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY),
    locname.MELTMONSSTAR3: SMG2LocationData(["Power Star Location", regname.MELTY], regname.MELTY),
}

    # Clockwork Rui
CLOCKRUIN_loc: dict[str, SMG2LocationData] = {
    locname.CLOCKRUINSTAR1: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK),
    locname.CLOCKRUINSTAR2: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK),
    locname.CLOCKRUINSTAR3: SMG2LocationData(["Power Star Location", regname.CLOCKWORK], regname.CLOCKWORK),
}

    # Throwback Sta
THROWBACK_loc: dict[str, SMG2LocationData] = {
    locname.THROWBACKSTAR1: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT),
    locname.THROWBACKSTAR2: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT),
    locname.THROWBACKSTAR3: SMG2LocationData(["Power Star Location", regname.WHOMPFORT], regname.WHOMPFORT),
}

    # Battle Belt S
BATTBELT_loc: dict[str, SMG2LocationData] = {
    locname.BATTBELTSTAR1: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT),
    locname.BATTBELTSTAR2: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT),
    locname.BATTBELTSTAR3: SMG2LocationData(["Power Star Location", regname.BATTLEBELT], regname.BATTLEBELT),
}

    # Flash Black S
FLASHBLACK_loc: dict[str, SMG2LocationData] = {
    locname.FLASHBLACKSTAR1: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK),
    locname.FLASHBLACKSTAR2: SMG2LocationData(["Power Star Location", regname.FLASHBLACK], regname.FLASHBLACK),
}

    # Slimy Spring
SLIMSPRI_loc: dict[str, SMG2LocationData] = {
    locname.SLIMYSPRISTAR1: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI),
    locname.SLIMYSPRISTAR2: SMG2LocationData(["Power Star Location", regname.SLIMSPRI], regname.SLIMSPRI),
}

    # Bowser's Gala
GALGEN_loc: dict[str, SMG2LocationData] = {
    locname.GALAXYGENSTAR1: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3),
    locname.GALAXYGENSTAR2: SMG2LocationData(["Power Star Location", regname.BOWSER3], regname.BOWSER3),
}

    # World S
    # Mario Squared
MARIOSQ_loc: dict[str, SMG2LocationData] = {
    locname.MARIOSQRSTAR1: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO),
    locname.MARIOSQRSTAR2: SMG2LocationData(["Power Star Location", regname.MARIO], regname.MARIO),
}

    # Rolling Coast
ROLLSLIDE_loc: dict[str, SMG2LocationData] = {
    locname.ROLLSLIDESTAR1: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST),
    locname.ROLLSLIDESTAR2: SMG2LocationData(["Power Star Location", regname.ROLLCOAST], regname.ROLLCOAST),
}

    # Twisty Trials
TWISTTRI_loc: dict[str, SMG2LocationData] = {
    locname.TWISTTRIALSTAR1: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI),
    locname.TWISTTRIALSTAR2: SMG2LocationData(["Power Star Location", regname.TWISTTRI], regname.TWISTTRI),
}

    # Stone Cyclone
STONECYC_loc: dict[str, SMG2LocationData] = {
    locname.STONECYCLOSTAR1: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC),
    locname.STONECYCLOSTAR2: SMG2LocationData(["Power Star Location", regname.STONECYC], regname.STONECYC),
}

    # Boss Blitz St
BOSSBLITZ_loc: dict[str, SMG2LocationData] = {
    locname.BOSSBLITSTAR1: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ),
    locname.BOSSBLITSTAR2: SMG2LocationData(["Power Star Location", regname.BOSSBLITZ], regname.BOSSBLITZ),
}

    # Flip-Out Star
FLIPOUT_loc: dict[str, SMG2LocationData] = {
    locname.FLIPOUTSTAR1: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT),
    locname.FLIPOUTSTAR2: SMG2LocationData(["Power Star Location", regname.FLIPOUT], regname.FLIPOUT),
}

    # Grandmaster
GRANDMASTER_loc: dict[str, SMG2LocationData] = {
    locname.GRANDMASTSTAR1: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER),
    locname.GRANDMASTSTAR2: SMG2LocationData(["Power Star Location", regname.GRANDMASTER], regname.GRANDMASTER),
}

green_star_locations: dict[str, SMG2LocationData]  = {
    locname.SKYSTASTARG1:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS),
    locname.SKYSTASTARG2:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS),
    locname.SKYSTASTARG3:       SMG2LocationData(["Green Star Location", regname.SKYOBS], regname.SKYOBS),
    locname.YOSHSTARSTARG1:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG),
    locname.YOSHSTARSTARG2:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG),
    locname.YOSHSTARSTARG3:     SMG2LocationData(["Green Star Location", regname.GOODEGG], regname.GOODEGG),
    locname.SPINDIGSTARG1:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG),
    locname.SPINDIGSTARG2:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG),
    locname.SPINDIGSTARG3:      SMG2LocationData(["Green Star Location", regname.SPINDIG], regname.SPINDIG),
    locname.FLUFBLUFSTARG1:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF),
    locname.FLUFBLUFSTARG2:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF),
    locname.FLUFBLUFSTARG3:     SMG2LocationData(["Green Star Location", regname.FLUFFBLUFF], regname.FLUFFBLUFF),
    locname.RIGHTDOWNSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.RIGHTDOWNSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.FLIPSWAPSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.FLIPSWAPSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.FIREFLOTSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.FIREFLOTSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.PUZZPLANKSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.PUZZPLANKSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.PUZZPLANKSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.HIGHFALLSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.HIGHFALLSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.HIGHFALLSTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.ROCKBOWLSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.ROCKBOWLSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.ROCKBOWLSTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.COSCCOVESTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.COSCCOVESTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.COSCCOVESTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.WILDGLIDESTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.WILDGLIDESTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.BEEBLOOMSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.BEEBLOOMSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.LAVALAIRSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.LAVALAIRSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.TALLTREESTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.TALLTREESTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.TALLTREESTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.CLOUDCOURTSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.CLOUDCOURTSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.CLOUDCOURTSTARG3:   SMG2LocationData(["Green Star Location"]),
    locname.HAUNTHALLSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.HAUNTHALLSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.HAUNTHALLSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.SNOWFLAKESTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.SNOWFLAKESTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.SNOWFLAKESTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.ROLLMASTERSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.ROLLMASTERSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.BEATBLOCKSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.BEATBLOCKSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.FEARFLETSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.FEARFLETSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.SUPERMASSSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.SUPERMASSSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.SUPERMASSSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.FLIPVILLESTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.FLIPVILLESTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.FLIPVILLESTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.STARBEACHSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.STARBEACHSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.STARBEACHSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.CHOMPWORKSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.CHOMPWORKSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.CHOMPWORKSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.HONEYHOPSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.HONEYHOPSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.SWEETMYSTSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.SWEETMYSTSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.GRAVGAUNSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.GRAVGAUNSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.SPACESTORMSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.SPACESTORMSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.SPACESTORMSTARG3:   SMG2LocationData(["Green Star Location"]),
    locname.SLIPSANDSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.SLIPSANDSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.SLIPSANDSTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.COLDFIRESTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.COLDFIRESTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.COLDFIRESTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.BOOMOONSTARG1:      SMG2LocationData(["Green Star Location"]),
    locname.BOOMOONSTARG2:      SMG2LocationData(["Green Star Location"]),
    locname.BOOMOONSTARG3:      SMG2LocationData(["Green Star Location"]),
    locname.UPDIZZYSTARG1:      SMG2LocationData(["Green Star Location"]),
    locname.UPDIZZYSTARG2:      SMG2LocationData(["Green Star Location"]),
    locname.FLEETFLYSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.FLEETFLYSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.BOOMBUNKSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.BOOMBUNKSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.MELTMONSSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.MELTMONSSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.MELTMONSSTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.CLOCKRUINSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.CLOCKRUINSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.CLOCKRUINSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.THROWBACKSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.THROWBACKSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.THROWBACKSTARG3:    SMG2LocationData(["Green Star Location"]),
    locname.BATTBELTSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.BATTBELTSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.BATTBELTSTARG3:     SMG2LocationData(["Green Star Location"]),
    locname.FLASHBLACKSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.FLASHBLACKSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.SLIMYSPRISTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.SLIMYSPIRSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.GALAXYGENSTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.GALAXYGENSTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.MARIOSQRSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.MARIOSQRSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.ROLLSLIDESTARG1:    SMG2LocationData(["Green Star Location"]),
    locname.ROLLSLIDESTARG2:    SMG2LocationData(["Green Star Location"]),
    locname.TWISTTRIALSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.TWISTTRIALSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.STONECYCLOSTARG1:   SMG2LocationData(["Green Star Location"]),
    locname.STONECYCLOSTARG2:   SMG2LocationData(["Green Star Location"]),
    locname.BOSSBLITSTARG1:     SMG2LocationData(["Green Star Location"]),
    locname.BOSSBLITSTARG2:     SMG2LocationData(["Green Star Location"]),
    locname.FLIPOUTSTARG1:      SMG2LocationData(["Green Star Location"]),
    locname.FLIPOUTSTARG2:      SMG2LocationData(["Green Star Location"]),
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