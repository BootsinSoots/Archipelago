from typing import Any

from ..LM_Randomize_ISO import LuigisMansionRandomizer

# Used to update speedy spirit observers that spawn them in and switch them to the blackout only table instead.
SPEEDY_OBSERVER_INDEX: list[int] = [183, 182, 179, 178, 177, 101, 100, 99, 98, 97, 21, 19]
SPEEDY_ENEMY_INDEX: list[int] = [128, 125, 115, 114, 113, 67, 66, 60, 59, 58, 7, 6]

# Used to "fuzzy-match" chest colors for items from other games.
MONEY_ITEM_NAMES: list[str] = ["Bills", "Coin", "Gold Bar", "Rupee", "Leaf", "Green", "Gold", "Jewel"]
EXPLODE_ITEM_NAMES: list[str] = ["Bomb", "Missile", "Glove", "Red", "Tunic", "Cloth", "Armor", "Boot", "Shoe"]
ICY_ITEM_NAMES: list[str] = ["Ice Trap", "White", "Ice Beam", "Icy", "Freeze"]
LIGHT_ITEM_NAMES: list[str] = ["Light", "Big Key", "Yellow", "Banana", "Boss Key", "Sun", "Laser"]
BLUEISH_ITEM_NAMES: list[str] = ["Small Key", "Blue", "Ocean", "Sea", "Magic"]

# This is a list of furniture that is at ceiling height. These need to be adjusted to avoid spawning items out of bounds.
CEILING_FURNITURE_LIST: list[int] = [4, 38, 43, 62, 63, 76, 77, 81, 84, 85, 91, 92, 101, 110, 111, 137, 156, 158, 159,
    163, 173, 174, 189, 190, 195, 199, 200, 228, 240, 266, 310, 342, 352, 354, 355, 356, 357, 358, 359, 373, 374, 378,
    379, 380, 381, 399, 423, 426, 445, 446, 454, 459, 460, 463, 467, 485, 547, 595, 596, 631, 632, 636, 657, 671, 672]

# Similar to Ceiling furniture, except only needs a slight adjustment to prevent items from going out of bounds.
MEDIUM_HEIGHT_FURNITURE_LIST: list[int] = [0, 1, 104, 112, 113, 114, 124, 125, 135, 136, 204, 206, 210, 232, 234, 235,
    264, 265, 270, 315, 343, 344, 345, 346, 347, 353, 361, 362, 363, 368, 369, 370, 376, 388, 397, 398, 411, 418, 431,
    438, 444, 520, 526, 544, 552, 553, 554, 555, 557, 602, 603, 634, 635]

# List of ghosts that can be replaced/changed in game.
GHOST_LIST: list[str] = ["yapoo1", "mapoo1", "mopoo1", "yapoo2", "mapoo2", "mopoo2", "banaoba", "topoo1", "topoo2",
    "topoo3", "topoo4","heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8", "skul",
    "putcher1", "tenjyo", "tenjyo2"]

# List of ghosts that can be chosen from once a random selection has been made
RANDOM_GHOST_LISTS: list[list[str]] = [["yapoo1"], ["mapoo1"], ["mopoo1"], ["banaoba"], ["putcher1"],
    ["tenjyo", "tenjyo2"], ["heypo1", "heypo2", "heypo3", "heypo4", "heypo5", "heypo6", "heypo7", "heypo8"],
    ["topoo1", "topoo2", "topoo3", "topoo4"]]

# Dictionary of Freestanding Location names and their index in keyinfo.
LOCATION_TO_INDEX = {
    "The Well Key": 0,
    "Ghost Foyer Key": 1,
    "1F Bathroom Shelf Key": 3,
    "Fortune Teller Candles": 4,
    "Wardrobe Shelf Key": 5,
}

# Converts AP readable name to in-game name
def get_item_name(item_data: dict, slot: int) -> str:
    if int(item_data["player"]) != slot:
        return "nothing"  # TODO return AP item(s) here

    if item_data["door_id"] != 0:
        return "key_" + str(item_data["door_id"])
    elif "Bills" in item_data["name"] or "Coins" in item_data["name"] or "Gold Bar" in item_data["name"]:
        if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
            return "nothing" # Do not spawn the money physically let it be handled remotely
        return "money"

    match item_data["name"]:
        case "Fire Element Medal":
            return "elffst"
        case "Water Element Medal":
            return "elwfst"
        case "Ice Element Medal":
            return "elifst"

        case "Mario's Hat":
            return "mcap"
        case "Mario's Letter":
            return "mletter"
        case "Mario's Shoe":
            return "mshoes"
        case "Mario's Glove":
            return "mglove"
        case "Mario's Star":
            return "mstar"

        case "Gold Diamond":
            if item_data["type"] == "Freestanding" or item_data["type"] == "Chest":
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "rdiamond"
        case "Sapphire":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "sapphire"
        case "Emerald":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "emerald"
        case "Ruby":
            if item_data["type"] in ("Freestanding", "Chest", "BSpeedy", "Mouse"):
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "ruby"
        case "Diamond":
            if item_data["type"] == "Freestanding" or item_data["type"] == "Chest":
                return "nothing"  # Do not spawn the gem physically let it be handled remotely
            return "diamond"

        case "Poison Mushroom":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "mkinoko"
        case "Small Heart":
            return "sheart"
        case "Large Heart":
            return "lheart"
        case "Bomb":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "itembomb"
        case "Ice Trap":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "ice"
        case "Banana Trap":
            if item_data["type"] == "Freestanding":
                return "nothing"
            return "banana"

        case "Boo Radar":
            return "gameboy"
        case "Vacuum Upgrade"|"Poltergust 3000":
            return "vbody"

    return "nothing"

def create_observer_entry(pos_x: float, pos_y: float, pos_z: float, room_no: int, cond_type: int, do_type: int,
    arg0: int = 0, arg1: int = 0, arg2: int = 0, arg3: int = 0, arg4: int = 0, arg5: int = 0, code_name: str = "(null)",
    string_arg0: str = "(null)", cond_string_arg0: str = "(null)", cond_arg0: int = 0,
    appear_flag: int = 0, disappear_flag: int = 0) -> dict[str, Any]:

    return {
        "name": "observer", # Arbitrary, can be whatever
        "code_name": code_name,
        "string_arg0": string_arg0,
        "cond_string_arg0": cond_string_arg0,
        "pos_x": pos_x,
        "pos_y": pos_y,
        "pos_z": pos_z,
        "dir_x": 0.000000, # Useless, does not function in game
        "dir_y": 0.000000, # Useless, does not function in game
        "dir_z": 0.000000, # Useless, does not function in game
        "scale_x": 1.000000, # Useless, does not function in game
        "scale_y": 1.000000, # Useless, does not function in game
        "scale_z": 1.000000, # Useless, does not function in game
        "room_no": room_no,
        "cond_arg0": cond_arg0,
        "arg0": arg0,
        "arg1": arg1,
        "arg2": arg2,
        "arg3": arg3,
        "arg4": arg4,
        "arg5": arg5,
        "appear_flag": appear_flag,
        "disappear_flag": disappear_flag,
        "cond_type": cond_type,
        "do_type": do_type,
        "invisible": 1, # This makes the observer not visible in game.
        "(Undocumented)": 0 # This currently does not do anything but is recommended to be set to 0
    }

# Indicates the chest size that will be loaded in game based on item provided. 0 = small, 1 = medium, 2 = large
# TODO Consolidate arguments since most come from the item object anyways.
def get_chest_size_from_item(lm_gen: "LuigisMansionRandomizer", item_name: str, chest_option: int, classification: str,
    trap_option: int, slot: int, iplayer: str):
    if chest_option == 1 or chest_option == 3:
        if "Boo" in item_name and slot == iplayer:
            return 0
        if any(iname in item_name for iname in MONEY_ITEM_NAMES):
            item_name = "Money"
        match item_name:
            case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
                return 0

            case "Small Heart" | "Money":
                return 0
            case "Large Heart":
                return 1

            case "Poison Mushroom" | "Bomb" | "Ice Trap" | "Gold Diamond" | "Banana Trap":
                return 2

            case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
                return 2

            case "Sapphire" | "Emerald" | "Ruby" | "Diamond":
                return 1

        return 0

    elif chest_option == 4:
        if "progression" in classification:
            return 2
        elif "useful" in classification:
            return 1
        elif "filler" in classification:
            return 0
        elif "trap" in classification:
            if trap_option == 0:
                return 0
            elif trap_option == 1:
                return 2
            else:
                return lm_gen.random.choice(sorted([0,1,2]))

    elif chest_option == 2:
        return lm_gen.random.choice(sorted([0,1,2]))

    elif chest_option == 5:
        if "Boo" in item_name and slot == iplayer:
            return 0
        if any(iname in item_name for iname in MONEY_ITEM_NAMES) and slot == iplayer:
            item_name = "Money"

        if slot != iplayer:
            if "progression" in classification:
                return 2
            elif "useful" in classification:
                return 1
            elif "filler" in classification:
                return 0
            elif "trap" in classification:
                if trap_option == 0:
                    return 0
                elif trap_option == 1:
                    return 2
                else:
                    return lm_gen.random.choice(sorted([0, 1, 2]))

        match item_name:
            case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
                return 0

            case "Small Heart" | "Money":
                return 0
            case "Large Heart":
                return 1

            case "Poison Mushroom" | "Bomb" | "Ice Trap" | "Gold Diamond" | "Banana Trap":
                return 2

            case "Fire Element Medal" | "Water Element Medal" | "Ice Element Medal":
                return 2

            case "Sapphire" | "Emerald" | "Ruby" | "Diamond":
                return 1

        return 0

# Indicates the chest size that will be loaded in game based on key type. 0 = small, 1 = medium, 2 = large
def get_chest_size_from_key(key_id):
    match key_id:
        case 3 | 42 | 59 | 72:
            return 2
        case _:
            return 0

# Changes the type of chest loaded in game based on the type of item that is hidden inside
# TODO consolidate arguments since most come from the item object anyways.
def get_item_chest_visual(lm_gen: "LuigisMansionRandomizer", item_name, chest_option, classification, trap_option, slot, iplayer):
    if chest_option == 1:
        if "Boo" in item_name and slot == iplayer:
            return "wtakara1"
        if any(iname in item_name for iname in MONEY_ITEM_NAMES):
            item_name = "Money"
        elif any(iname in item_name for iname in EXPLODE_ITEM_NAMES):
            item_name = "Bomb"
        elif any(iname in item_name for iname in LIGHT_ITEM_NAMES):
            item_name = "Banana Trap"
        elif any(iname in item_name for iname in BLUEISH_ITEM_NAMES):
            item_name = "Sapphire"
        elif any(iname in item_name for iname in ICY_ITEM_NAMES):
            item_name = "Ice Trap"
        match item_name:
            case "Heart Key" | "Club Key" | "Diamond Key" | "Spade Key" :
                return "ytakara1"

            case "Small Heart" | "Large Heart" | "Banana Trap" :
                return "ytakara1"

            case "Fire Element Medal" | "Bomb" | "Ruby":
                return "rtakara1"
            case "Water Element Medal" | "Poison Mushroom" | "Sapphire":
                return "btakara1"
            case "Ice Element Medal" | "Ice Trap" | "Diamond":
                return "wtakara1"

            case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
                return "rtakara1"

            case "Gold Diamond" | "Emerald" | "Money":
                return "gtakara1"

        return "btakara1"
    elif chest_option == 3 or chest_option == 4:
        if "progression" in classification:
            return "ytakara1"
        elif "useful" in classification:
            return "btakara1"
        elif "filler" in classification:
            return "gtakara1"
        elif "trap" in classification:
            if trap_option == 0:
                return "rtakara1"
            elif trap_option == 1:
                return "ytakara1"
            else:
                return lm_gen.random.choice(sorted(["ytakara1", "rtakara1", "btakara1", "wtakara1", "gtakara1"]))

    elif chest_option == 2:
        return lm_gen.random.choice(sorted(["ytakara1", "rtakara1", "btakara1", "wtakara1", "gtakara1"]))

    elif chest_option == 5:
        if "Boo" in item_name and slot == iplayer:
            return "wtakara1"
        if any(iname in item_name for iname in MONEY_ITEM_NAMES) and slot == iplayer:
            item_name = "Money"

        if slot != iplayer:
            if "progression" in classification:
                return "ytakara1"
            elif "useful" in classification:
                return "btakara1"
            elif "filler" in classification:
                return "gtakara1"
            elif "trap" in classification:
                if trap_option == 0:
                    return "rtakara1"
                elif trap_option == 1:
                    return "ytakara1"
                else:
                    return lm_gen.random.choice(sorted(["ytakara1", "rtakara1", "btakara1", "wtakara1", "gtakara1"]))
        match item_name:
            case "Heart Key" | "Club Key" | "Diamond Key" | "Spade Key" :
                return "ytakara1"

            case "Small Heart" | "Large Heart" | "Banana Trap" :
                return "ytakara1"

            case "Fire Element Medal" | "Bomb" | "Ruby":
                return "rtakara1"
            case "Water Element Medal" | "Poison Mushroom" | "Sapphire":
                return "btakara1"
            case "Ice Element Medal" | "Ice Trap" | "Diamond":
                return "wtakara1"

            case "Mario's Hat" | "Mario's Letter" | "Mario's Shoe" | "Mario's Glove" | "Mario's Star":
                return "rtakara1"

            case "Gold Diamond" | "Emerald" | "Money":
                return "gtakara1"

        return "btakara1"