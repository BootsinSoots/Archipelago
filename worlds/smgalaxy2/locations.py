from typing import Dict, NamedTuple, Optional, Set
from BaseClasses import Location, Region

from.Constants.Names import region_names as regname

class SMG2Location(Location):
    game: str = "Super Mario Galaxy"

    def __init__(self, player: int, name: str, parent: Region):
        super(SMG2Location, self).__init__(player, name, address=location_table[name].code, parent=parent)
        self.code = location_table[name].code

class SMG2LocationData(NamedTuple):
    location_groups: list[str] # type of randomization option table and group []
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    game_address: Optional[int] = 0  #
    default_access: Optional[dict[str, int]] = {}

# good egg galaxy
locGE_table: dict[str, SMG2LocationData] = {
    "GE: Dino Piranha": SMG2LocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000000, game_address=0),
    "GE: A Snack of Cosmic Proportions": SMG2LocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000001, game_address=1),
    "GE: King Kaliente's Battle Fleet": SMG2LocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000002, game_address=2),
    "GE: Luigi on the Roof": SMG2LocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000003, game_address=3),
    "GE: Dino Piranha Speed Run": SMG2LocationData(["Good Egg Galaxy", "Power Star"], regname.GOODEGG, 17000004, game_address=4),
}

locHH_table: dict[str, SMG2LocationData]  = {
    "HH: Bee Mario Takes Flight": SMG2LocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000006, game_address=0),
    "HH: Trouble on the Tower": SMG2LocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000007, game_address=1),
    "HH: Big Bad Bugabooom": SMG2LocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000008, game_address=2),
    "HH: Luigi in the Honeyhive Kingdom": SMG2LocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 17000009, game_address=3),
    "HH: Honeyhive Cosmic Mario Race": SMG2LocationData(["Honeyhive Galaxy", "Power Star"], regname.HONEYHIVE, 170000010, game_address=4)
}

locspecialstages_table: dict[str, SMG2LocationData]  = {
    "LDL: Surfing 101": SMG2LocationData(["Loopdeloop Galaxy", "Power Star"], regname.LOOPDEELOOP, 170000012, game_address=0),
    "FS: Painting the Planet Yellow": SMG2LocationData(["Flipswitch Galaxy", "Power Star"], regname.FLIPSWITCH, 170000013, game_address=0),
    "RG: Rolling in the Clouds": SMG2LocationData(["Rolling Green Galaxy", "Power Star"], regname.ROLLINGGREEN, 170000014, game_address=0),
    "HS: Shrinking Satellite": SMG2LocationData(["Hurry-Scurry Galaxy", "Power Star"], regname.HURRYSCUR, 170000015, game_address=0),
    "BUB: Through the Poison Swamp": SMG2LocationData(["Bubble Breeze Galaxy", "Power Star"], regname.BUBBLEBREEZE, 170000016, game_address=0),
    "HC: Scaling the Sticky Wall": SMG2LocationData(["Honeyclimb Galaxy", "Power Star"], regname.HONEYCLIMB, 170000118, game_address=0),
    "BB: The Floating Fortress": SMG2LocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000017, game_address=0),
    "BB: The Secret of Buoy Base": SMG2LocationData(["Buoy Base Galaxy", "Power Star"], regname.BUOY, 170000018, game_address=0),
    #TODO: FIX duplicate abbreviation 
    "GG: Grand Star Rescue": SMG2LocationData([regname.SHIP, "Power Star"], regname.GATEWAY, 170000019, game_address=0),
    "BF: Kingfin's Fearsome Waters": SMG2LocationData(["Bonefin Galaxy", "Power Star"], regname.BONEFIN, 170000021, game_address=0),
    "MS: Watch Your Step": SMG2LocationData(["Matter Splatter Galaxy", "Power Star"], regname.MATTER, 170000022, game_address=0),
    "RGT: Gizmos, Gears, and Gadgets": SMG2LocationData(["Rolling Gizmo Galaxy", "Power Star"], regname.ROLLINGGIZ, 170000023, game_address=0),
    "LDT: The Galaxy's Greatest Wave": SMG2LocationData(["Loopdeeswoop Galaxy", "Power Star"], regname.LOOPDEESWOOP, 170000024, game_address=0),
    "BBT: The Electric Labyrinth": SMG2LocationData(["Bubble Blast Galaxy", "Power Star"], regname.BUBBLEBLAST, 170000025, game_address=0)
}

locbosses_table: dict[str, SMG2LocationData]  = {
    "BJ: Megaleg's Moon": SMG2LocationData([regname.BOWJR1, "Power Star", "Boss Star"], regname.BOWJR1, 170000026, game_address=0),
    "B: The Fiery Stronghold": SMG2LocationData([regname.BOWSER1, "Power Star", "Boss Star"], regname.BOWSER1, 170000027, game_address=0),
    "BJ: Sinking the Airships": SMG2LocationData([regname.BOWJR2, "Power Star", "Boss Star"], regname.BOWJR2, 170000028, game_address=0),
    "BJ: King Kaliente's Spicy Return": SMG2LocationData([regname.BOWJR3, "Power Star", "Boss Star"], regname.BOWJR3, 170000029, game_address=0),
    "B: Darkness on the Horizon": SMG2LocationData([regname.BOWSER2, "Power Star", "Boss Star"], regname.BOWSER2, 170000030, game_address=0),
    "B: The Fate of the Universe": SMG2LocationData([regname.BOWSER3, "Power Star", "Boss Star"], regname.BOWSER3, None, game_address=0)
}

locSJ_table: dict[str, SMG2LocationData]  = {
    "SJ: Pull Star Path": SMG2LocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000031, game_address=0),
    "SJ: Kamella's Airship Attack": SMG2LocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000032, game_address=1),
    "SJ: Tarantox's Tangled Web": SMG2LocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000033, game_address=2),
    "SJ: Yoshi's Unexpected Apparence": SMG2LocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000034, game_address=3),
    "SJ: Pull Star Path Speed Run": SMG2LocationData(["Space Junk Galaxy", "Power Star"], regname.SPACEJUNK, 170000035, game_address=4)
}

locBR_table: dict[str, SMG2LocationData]  = {
    "BR: Battlerock Barrage": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000037, game_address=0),
    "BR: Breaking into the Battlerock": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000038, game_address=1),
    "BR: Topmaniac and Topman Tribe": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000119, game_address=2),
    "BR: Battlerock's Garbage dump": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000039, game_address=3),
    "BR: Topmanic's Dardevil Run": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000040, game_address=4),
    "BR: Luigi under the Saucer": SMG2LocationData(["Battlerock Galaxy", "Power Star"], regname.BATTLEROCK, 170000042, game_address=5)
}
#TODO: note change abbreviation same as buoy base
locBB_table: dict[str, SMG2LocationData]  = {
    "BB: Sunken Treasure": SMG2LocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000043, game_address=0),
    "BB: Passing the Swim Test": SMG2LocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000044, game_address=1),
    "BB: The Secret Undersea Cavern": SMG2LocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000045, game_address=2),
    "BB: Fast Foes on the Cyclone Stone": SMG2LocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000046, game_address=3),
    "BB: Wall Jumping Up Waterfalls": SMG2LocationData(["Beach Bowl Galaxy", "Power Star"], regname.BEACHBOWL, 170000048, game_address=4)
}

locG_table: dict[str, SMG2LocationData]  = {
    "G: Luigi and the Haunted Mansion": SMG2LocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000049, game_address=0),
    "G: A Very Spooky Spirit": SMG2LocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000050, game_address=1),
    "G: Beware of Bouldergeist": SMG2LocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000051, game_address=2),
    "G: Bouldergeist's Daredevil Run": SMG2LocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000052, game_address=3),
    "G: Matter Splatter Mansion": SMG2LocationData([regname.GHOSTLY, "Power Star"], regname.GHOSTLY, 170000054, game_address=4)
}

locGG_table: dict[str, SMG2LocationData]  = {
    "GG: Bunnies in the Wind": SMG2LocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000055, game_address=0),
    "GG: The Dirty Tricks of Major Burrows": SMG2LocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000056, game_address=1),
    "GG: Gusty Garden's Gravity Scramble": SMG2LocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000057, game_address=2),
    "GG: Major Burrows's Daredevil Run": SMG2LocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000058, game_address=3),
    "GG: The Golden Chomp": SMG2LocationData(["Gusty Garden Galaxy", "Power Star"], regname.GUSTY, 170000060, game_address=4)
}

locFF_table: dict[str, SMG2LocationData]  = {
    "FF: The Frozen Peak of Baron Brr": SMG2LocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000061, game_address=0),
    "FF: Freezeflame's Blistering Coore": SMG2LocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000062, game_address=1),
    "FF: Hot and Cold Collide": SMG2LocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000063, game_address=2),
    "FF: Conquring the Summit": SMG2LocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000064, game_address=3),
    "FF: Frosty Cosmic Mario race": SMG2LocationData(["Freezeflame Galaxy", "Power Star"], regname.FREEZEFLAME, 170000065, game_address=4)
}

locDDune_table: dict[str, SMG2LocationData]  = {
    "DDune: Soaring on the Desert Winds": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000067, game_address=0),
    "DDune: Blasting through the Sand": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000068, game_address=1),
    "DDune: Sunbaked Sand Castle": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000069, game_address=2),
    "DDune: Sandblast Speed Run": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000071, game_address=3),
    "DDune: Bullet Bill on Your Back": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000072, game_address=4),
    "DDune: Treasure of the Pyramid": SMG2LocationData(["Dusty Dune Galaxy", "Power Star"], regname.DUSTY, 170000073, game_address=5)
} 

locGL_table: dict[str, SMG2LocationData]  = {
    "GL: Star Bunnies on the Hunt": SMG2LocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000074, game_address=0),
    "GL: Cataquack to the skies": SMG2LocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000075, game_address=1),
    "GL: When it Rains, it Pours": SMG2LocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000076, game_address=2),
    "GL: Cosmic Mario Forest Race": SMG2LocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000077, game_address=3),
    "GL: The Bell on the Big Trees": SMG2LocationData(["Gold Leaf Galaxy", "Power Star"], regname.GOLDLEAF, 170000079, game_address=4)
}
#TODO: Change abbrivation
locSS_table: dict[str, SMG2LocationData]  = {
    "SS: Going After Guppy": SMG2LocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000080, game_address=0),
    "SS: Faster Than a Speedrunning Penguin": SMG2LocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000081, game_address=1),
    "SS: The Silver Stars of Sea Slide": SMG2LocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000082, game_address=2),
    "SS: Underwater Cosmic Mario Race": SMG2LocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000083, game_address=3),
    "SS: Hurry, He's Hungry": SMG2LocationData(["Sea Slide Galaxy", "Power Star"], regname.SEASLIDE, 170000085, game_address=4)
}

locTT_table: dict[str, SMG2LocationData]  = {
    "TT: Heavy Metal Mecha Boswer": SMG2LocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000086, game_address=0),
    "TT: Mario (or Luigi) Meets Mario": SMG2LocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000087, game_address=1),
    "TT: Bouncing Down Cake Lane": SMG2LocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000088, game_address=2),
    "TT: The Flipswitch Chain": SMG2LocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000089, game_address=3),
    "TT: Fast Foes of Toy Time": SMG2LocationData(["Toy Time Galaxy", "Power Star"], regname.TOYTIME, 170000090, game_address=4)
}

locDD_table: dict[str, SMG2LocationData]  = {
    "DD: The Underground Ghost Ship": SMG2LocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000092, game_address=0),
    "DD: Bubble Blastoff": SMG2LocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000093, game_address=1),
    "DD: Guppy and the Underground Lake": SMG2LocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000094, game_address=2),
    "DD: Ghost Ship Daredevil Run": SMG2LocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000095, game_address=3),
    "DD: Boo in Box": SMG2LocationData(["Deep Dark Galaxy", "Power Star"], regname.DEEPDARK, 170000097, game_address=4)
}

locDN_table: dict[str, SMG2LocationData]  = {
    "DN: Inflitrating the Dreadnought": SMG2LocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000098, game_address=0),
    "DN: Dreadnought's Colossal Cannons": SMG2LocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000099, game_address=1),
    "DN: Revenge of the Topman Tribe": SMG2LocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000100, game_address=2),
    "DN: Topman Tribe Speed Run": SMG2LocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000101, game_address=3),
    "DN: Dreadnought's Garbage Dump": SMG2LocationData(["Dreadnought Galaxy", "Power Star"], regname.DREADNOUGHT, 170000103, game_address=4)
}

locMM_table: dict[str, SMG2LocationData]  = {
    "MM: The Sinking Lava Spire": SMG2LocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000104, game_address=0),
    "MM: Through the Meteor Storm": SMG2LocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000105, game_address=1),
    "MM: Fiery Dino Piranha": SMG2LocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000106, game_address=2),
    "MM: Lava Spire Daredevil Run": SMG2LocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000107, game_address=3),
    "MM Burning Tide": SMG2LocationData(["Melty Molten Galaxy", "Power Star"], regname.MELTY, 170000109, game_address=4)
}

locHL_table: dict[str, SMG2LocationData]  = {
    "SS: Rocky Road": SMG2LocationData(["Sweet Sweet Galaxy", "Power Star"], regname.SWEETSWEET, 170000110, game_address=0),
    "SP: A Very Sticky Situation": SMG2LocationData(["Sling Pod Galaxy", "Power Star"], regname.SLINGPOD, 170000111, game_address=0),
    "DDR: Giant Eel Breakout": SMG2LocationData(["Drip Drop Galaxy", "Power Star"], regname.DRIPDROP, 170000112, game_address=0),
    "BM: Bigmouth's Gold Bait": SMG2LocationData(["Bigmouth Galaxy", "Power Star"], regname.BIGMOUTH, 170000113, game_address=0),
    "Sandy Spiral: Choosing a Favorite Snack": SMG2LocationData(["Sand Spiral Galaxy", "Power Star"], regname.SANDSPIRAL, 170000114, game_address=0),
    "Bone's Boneyard: Racing the Spooky Speedster": SMG2LocationData(["Boo's Boneyard Galaxy", "Power Star"], regname.BOOBONE, 170000115, game_address=0),
    "SC: Star Bunnies in the Snow": SMG2LocationData(["Snow Cap Galaxy", "Power Star"], regname.SNOWCAP, 170000116, game_address=0)
}

locPC_table: dict[str, SMG2LocationData]  = {
    "TT: Luigi's Purple Coins": SMG2LocationData(["Toy Time Galaxy", "Power Star", "Purple Coins"], regname.TOYTIME, 170000091, game_address=5),
    "DN: Battlestation's Purple Coins": SMG2LocationData(["Dreadnought Galaxy", "Power Star", "Purple Coins"], regname.DREADNOUGHT, 170000102, game_address=5),
    "MM: Red-Hot Purple Coins": SMG2LocationData(["Melty Molten Galaxy", "Power Star", "Purple Coins"], regname.MELTY, 170000108, game_address=5),
    "DD: Plunder the Purple Coins": SMG2LocationData(["Deep Dark Galaxy", "Power Star", "Purple Coins"], regname.DEEPDARK, 170000096, game_address=5),
    "SS: Purple Coins by the Seaside": SMG2LocationData(["Sea Slide Galaxy", "Power Star", "Purple Coins"], regname.SEASLIDE, 170000084, game_address=5),
    "GE: Purple Coin Omelet": SMG2LocationData(["Good Egg Galaxy", "Power Star", "Purple Coins"], regname.GOODEGG, 170000005, game_address=5),
    "GG: Gateway's Purple coins": SMG2LocationData([regname.GATEWAY, "Power Star", "Purple Coins"], regname.GATEWAY, 170000020, game_address=2),
    "BR: Purple Coins on the Battlerock": SMG2LocationData(["Battlerock Galaxy", "Power Star", "Purple Coins"], regname.BATTLEROCK, 17000121, game_address=5),
    "SJ: Purple Coin Spacewalk": SMG2LocationData(["Space Junk Galaxy", "Power Star", "Purple Coins"], regname.SPACEJUNK, 170000036, game_address=5),
    "GG: Purple Coins on the Puzzle Cube": SMG2LocationData(["Gusty Garden Galaxy", "Power Star", "Purple Coins"], regname.GUSTY, 170000059, game_address=5),
    # TODO: change abbreviation for galaxy
    "BB: Beachcombing for Purple Coins": SMG2LocationData(["Bubble Breeze Galaxy", "Power Star", "Purple Coins"], regname.BUBBLEBREEZE, 170000047, game_address=5),
    "FF: Purple Coins on the Summit": SMG2LocationData(["Freezeflame Galaxy", "Power Star", "Purple Coins"], regname.FREEZEFLAME, 170000066, game_address=5),
    "G: Purple Coins in the Bone Pen": SMG2LocationData([regname.GHOSTLY, "Power Star", "Purple Coins"], regname.GHOSTLY, 170000053, game_address=5),
    "GL: Purple Coins in the Woods": SMG2LocationData(["Gold Leaf Galaxy", "Power Star", "Purple Coins"], regname.GOLDLEAF, 170000078, game_address=5),
    "DDune: Purple Coin in the Desert": SMG2LocationData(["Dusty Dune Galaxy", "Power Star", "Purple Coins"], regname.DUSTY, 170000070, game_address=5),
    "HH: The Honeyhive's Purple Coins": SMG2LocationData(["Honeyhive Galaxy", "Power Star", "Purple Coins"], regname.HONEYHIVE, 170000011, game_address=5)
}

base_stars_locations = {**locGE_table, **locHH_table,
                   **locSJ_table, **locBR_table, **locBB_table,
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table,
                   **locGL_table, **locSS_table, **locTT_table,
                   **locDD_table, **locDN_table, **locMM_table,
                   **locHL_table, **locspecialstages_table, **locbosses_table}

location_table = { **locGE_table, **locHH_table, 
                   **locSJ_table, **locBR_table, **locBB_table, 
                   **locGG_table, **locFF_table, **locDDune_table, **locG_table, 
                   **locGL_table, **locSS_table, **locTT_table, 
                   **locDD_table, **locDN_table, **locMM_table, 
                   **locHL_table, **locspecialstages_table, **locbosses_table, 
                   **locPC_table,
}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in location_table.items() if data.code is not None}

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories