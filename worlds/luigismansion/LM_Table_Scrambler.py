import copy
import re
from math import ceil
from typing import TYPE_CHECKING

from .Regions import REGION_LIST, LMRegionInfo
from .Items import ALL_ITEMS_TABLE, filler_items, LMItemData, CurrencyItemData
from .Locations import LMLocationData
from .Locations import FLIP_BALCONY_BOO_EVENT_LIST, ALL_LOCATION_TABLE
from .game.Currency import CURRENCIES

if TYPE_CHECKING:
    from .LM_ISO_Modifier import LuigisMansionRandomizer

def update_map_one_event_info(event_info):
    for x in event_info.info_file_field_entries:
        if x["EventNo"] == 8:
            x["EventIf"] = 5

def update_event_info(event_info, boo_checks: bool, output_data):
    # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
    # boss battles / grabbing boss keys, and various cutscenes etc. Also remove Mario Items/Elemental Item events
    events_to_remove = [7, 9, 15, 18, 19, 20, 21, 31, 41, 42, 45, 47, 51, 54, 69, 70, 73, 80, 81, 85, 91]

    # Only remove the boo checks if the player does not want them.
    if not boo_checks:
        events_to_remove += [16, 96]
    if output_data["Options"]["spawn"] in ("Foyer", "Courtyard", "Wardrobe Balcony", "1F Washroom"):
        events_to_remove += [12]

    event_info.info_file_field_entries = list(filter(
        lambda info_entry: not (info_entry["EventNo"] in events_to_remove or (info_entry["EventNo"] == 93 and
            info_entry["pos_x"] == 0)), event_info.info_file_field_entries))

    spawn_data = REGION_LIST[output_data["Options"]["spawn"]]

    for x in event_info.info_file_field_entries:
        # Move Telephone rings to third phone, make an A press and make always on
        if x["EventNo"] == 92:
            x["EventFlag"] = 0
            x["disappear_flag"] = 0
            x["EventLoad"] = 0
            x["EventArea"] = 150
            x["EventIf"] = 1
            x["PlayerStop"] = 1
            x["pos_x"] = 0.000000
            x["pos_y"] = 1100.000000
            x["pos_z"] = -25.000000

        # Telephone room event for the telephones, make an A press and make always on
        if x["EventNo"] == 94:
            x["EventFlag"] = 0
            x["disappear_flag"] = 0
            x["EventArea"] = 150
            x["EventLoad"] = 0
            x["EventIf"] = 1
            x["pos_x"] = 755.000000
            x["pos_y"] = 1100.000000
            x["pos_z"] = -25.000000

        # Telephone room event for the telephones, make an A press and make always on
        if x["EventNo"] == 93:
            x["EventFlag"] = 0
            x["disappear_flag"] = 0
            x["EventArea"] = 150
            x["EventLoad"] = 0
            x["EventIf"] = 1
            x["pos_x"] = -755.000000
            x["pos_y"] = 1100.000000
            x["pos_z"] = -25.000000

        # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
        # This prevents being soft locked in Boolossus and having to reset the game without saving.
        if x["EventNo"] == 71:
            x["EventFlag"] = 45
            x["EventLoad"] = 0

        # Allows Jarvis' (Ceramics Room) to only appear when the Ice Medal has been collected.
        # This prevents being kicked out by Jarvis' and being unable to participate in his game.
        if x["EventNo"] == 33:
            x["EventFlag"] = 45

        # Since we have a custom blackout event, we need to update event 44's trigger condition to be A-pressed based.
        # We also update the area ad trigger location to be the same as event45
        if x["EventNo"] == 44:
            x["pos_x"] = 3500.277000
            x["pos_y"] = -550.000000
            x["pos_z"] = -2150.792000
            x["EventFlag"] = 0  # 25
            x["EventArea"] = 230
            x["EventIf"] = 1
            x["EventLock"] = 0
            x["PlayerStop"] = 0
            x["EventLoad"] = 0

        # Update the spawn in event trigger to wherever spawn is
        if x["EventNo"] == 48:
            x["pos_y"] = spawn_data.pos_y
            x["pos_z"] = spawn_data.pos_z
            x["pos_x"] = spawn_data.pos_x

        # Removes the Mr. Bones requirement. He will spawn instantly
        if x["EventNo"] == 23:
            x["EventFlag"] = 0
            x["disappear_flag"] = 74

        # Turn off Event 74 (Warp to King Boo Fight) in blackout by disabling event if King Boo isn't present
        if x["EventNo"] == 74:
            x["CharacterName"] = "dltelesa"

        # Make Van Gogh load more than once
        if x["EventNo"] == 38:
            x["EventLoad"] = 0
            x["disappear_flag"] = 22
            x["EventIf"] = 2

        # # Update the Washroom event trigger to be area entry based
        # # Also updates the event disappear trigger to be flag 28
        # # Also updates the EventFlag to 0, so this event always plays
        # if boo_checks and x["EventNo"] == 47:
        #     x["pos_x"] = -1725.000000
        #     x["pos_y"] = 100.000000
        #     x["pos_z"] = -4150.000000
        #     x["EventFlag"] = 0
        #     x["disappear_flag"] = 28
        #     x["EventIf"] = 5
        #     x["EventArea"] = 380
        #     x["EventLock"] = 1
        #     x["PlayerStop"] = 1
        #     x["EventLoad"] = 0

        # Update the King Boo event trigger to be area entry based
        if boo_checks and x["EventNo"] == 16:
            x["pos_x"] = 2260.000000
            x["pos_y"] = -450.000000
            x["pos_z"] = -5300.000000
            x["EventIf"] = 5
            x["EventArea"] = 200
            x["EventLock"] = 1
            x["PlayerStop"] = 1
            x["EventLoad"] = 0

        # Update the Balcony Boo event trigger to be area entry based
        if boo_checks and x["EventNo"] == 96:
            if str(output_data["Options"]["spawn"]) in FLIP_BALCONY_BOO_EVENT_LIST:
                x["pos_x"] = 1800.000000
                x["pos_y"] = 1200.000000
                x["pos_z"] = -2950.000000
                x["EventArea"] = 350
            else:
                x["pos_x"] = 1800.000000
                x["pos_y"] = 1200.000000
                x["pos_z"] = -2600.000000
                x["EventArea"] = 200
            x["EventIf"] = 5
            x["EventLock"] = 1
            x["PlayerStop"] = 1
            x["EventLoad"] = 0

        # Update the Intro event to talk about save anywhere and healing.
        if x["EventNo"] == 11:
            x["EventFlag"] = 0
            x["disappear_flag"] = 0
            x["EventArea"] = 65535
            x["EventLoad"] = 1
            x["EventIf"] = 2
            x["PlayerStop"] = 1
            x["EventLock"] = 1
            x["event_parameter"] = 0
            x["room_no"] = spawn_data.room_id
            x["pos_y"] = spawn_data.pos_y
            x["pos_x"] = spawn_data.pos_x
            x["pos_z"] = spawn_data.pos_z

        # Change Training room second visit to always be on
        if x["EventNo"] == 10:
            x["EventFlag"] = 0

        # Update Starting Toad Event (event07) to move to the spawn region.
        if x["EventNo"] == 12:
            if not output_data["Options"]["spawn"] in ("Foyer", "Courtyard", "Wardrobe Balcony", "1F Washroom"):
                x["EventFlag"] = 0
                x["disappear_flag"] = 0
                x["EventLoad"] = 0
                x["EventArea"] = 330
                x["EventIf"] = 1
                x["PlayerStop"] = 1
                x["pos_y"] = spawn_data.pos_y
                x["pos_z"] = int(spawn_data.pos_z) - 150
                x["pos_x"] = int(spawn_data.pos_x) - 150 + 2

def update_character_info(character_info, output_data):
    # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
    bad_actors_to_remove = ["vhead", "vbody", "dhakase", "demobak1", "dluige01"]
    character_info.info_file_field_entries = list(filter(
        lambda info_entry: not info_entry["name"] in bad_actors_to_remove, character_info.info_file_field_entries))

    for x in character_info.info_file_field_entries:
        # Replace the mstar Observatory item with its randomized item.
        if x["name"] == "mstar":
            x["name"] = _get_item_name(output_data["Locations"]["Observatory Shoot the Moon"], int(output_data["Slot"]))
            x["appear_flag"] = 50
            x["invisible"] = 1
            x["pos_y"] = 600.000000

        # Allow Chauncey, Lydia, and the Twins to spawn as soon as a new game is created.
        if x["name"] in ("baby", "mother", "dboy", "dboy2"):
            x["appear_flag"] = 0

        # Fix a Nintendo mistake where the Cellar chest has a room ID of 0 instead of 63.
        if x["create_name"] == "63_2":
            x["room_no"] = 63

        # Remove King Boo in the hallway, since his event was removed.
        if x["name"] == "dltelesa" and x["room_no"] == 68:
            character_info.info_file_field_entries.remove(x)

        # Remove Miss Petunia to never disappear, unless captured.
        if x["name"] == "fat" and x["room_no"] == 45:
            x["disappear_flag"] = 0

        # Make Shivers / Butler not disappear by doing a different appear flag.
        if x["name"] == "situji":
            x["appear_flag"] = 7

        # Make Luggs stay gone if the light are on in the room
        if x["name"] == "eater":
            x["disappear_flag"] = 31

        # Editing the starting room spawn coordinates (regardless of it random spawn is turned on).
        if x["room_no"] == 2 and x["name"] == "luige":
            spawn_region: LMRegionInfo = REGION_LIST[output_data["Options"]["spawn"]]
            x["room_no"] = spawn_region.room_id
            x["pos_y"] = spawn_region.pos_y
            x["pos_x"] = spawn_region.pos_x
            x["pos_z"] = spawn_region.pos_z

def update_treasure_table(lm_gen: "LuigisMansionRandomizer", treasure_info, character_info, output_data):
    chest_option: int = int(output_data["Options"]["chest_types"])
    trap_option: int = int(output_data["Options"]["trap_chests"])
    slot_num: int = int(output_data["Slot"])

    for item_name, item_data in output_data["Locations"].items():
        # Ignore output data not related to checks that are not chests.
        if not item_data["type"] == "Chest":
            continue

        for char_entry in list([charinfo for charinfo in character_info.info_file_field_entries if
            int(charinfo["room_no"]) == int(item_data["room_no"]) and ("takara" in charinfo["name"] or
            charinfo["name"] == "nut")]):

            # Special Case: Move the Laundry room chest back from Butler door
            if char_entry["room_no"] == 5:
                char_entry["pos_z"] = -1100.000000

            # Special Case: Move 2F Bathroom chest back from wall
            elif char_entry["room_no"] == 45:
                char_entry["pos_x"] = -1900.000000
                char_entry["pos_z"] = -4830.000000

            # Change chest appearance based of player cosmetic choices
            chest_size = int(treasure_info.info_file_field_entries[item_data["loc_enum"]]["size"])
            if item_data["room_no"] != 11 and chest_option > 0:
                char_entry["name"] = _get_item_chest_visual(lm_gen, item_data["name"], chest_option,
                    item_data["classification"], trap_option, slot_num, item_data["player"])
                if item_data["door_id"] == 0:
                    chest_size = _get_chest_size_from_item(lm_gen, item_data["name"], chest_option,
                        item_data["classification"], trap_option, slot_num, item_data["player"])
                else:
                    chest_size = _get_chest_size_from_key(item_data["door_id"])

            # Define the actor name to use from the Location in the generation output. Act differently if it's a key.
            treasure_item_name = _get_item_name(item_data, slot_num) #nothing

            # Setting all curriences to 0 value by default.
            for currency_name in CURRENCIES:
                treasure_info.info_file_field_entries[item_data["loc_enum"]][currency_name] = 0

            # Don't give any items that are not from our game, leave those 0 / blank.
            if int(item_data["player"]) == slot_num and item_data["name"] in ALL_ITEMS_TABLE.keys():
                lm_item_data: type[LMItemData|CurrencyItemData] = ALL_ITEMS_TABLE[item_data["name"]]

                # If it's a money item, set the currencies based on our defined bundles
                if hasattr(lm_item_data, 'currencies'):
                    for currency_name, currency_amount in lm_item_data.currencies.items():
                        treasure_info.info_file_field_entries[item_data["loc_enum"]][currency_name] = currency_amount

            treasure_info.info_file_field_entries[item_data["loc_enum"]]["cdiamond"] = 0
            treasure_info.info_file_field_entries[item_data["loc_enum"]]["other"] = treasure_item_name
            treasure_info.info_file_field_entries[item_data["loc_enum"]]["size"] = chest_size
            treasure_info.info_file_field_entries[item_data["loc_enum"]]["effect"] = 0
            treasure_info.info_file_field_entries[item_data["loc_enum"]]["camera"] = 0

def update_gallery_furniture_info(furniture_info, item_appear_info, output_data):
    ceiling_furniture_list: list[int] = [0, 1]
    for furniture_jmp_id in ceiling_furniture_list:
        current_y_offset = furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"]
        adjust_y_offset = 225.0
        furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"] = current_y_offset - adjust_y_offset

    for item_name, item_data in output_data["Locations"].items():
        location_data: LMLocationData = ALL_LOCATION_TABLE[item_name]
        if not (location_data.region == "Gallery" and item_data["type"] == "Furniture"):
            continue

        actor_item_name = _get_item_name(item_data, int(output_data["Slot"]))

        # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
        # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
        filtered_item_appear = list(item_appear_entry for item_appear_entry in
            item_appear_info.info_file_field_entries if  item_appear_entry["item0"] == actor_item_name)
        item_appear_entry_idx = filtered_item_appear[len(filtered_item_appear) - 1]

        furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
            item_appear_info.info_file_field_entries.index(item_appear_entry_idx))

        # TODO update using ALL items table instead
        if any((key, val) for (key, val) in filler_items.items() if
               key == item_data["name"] and key != "Diamond" and val.type == "Money") \
                and item_data["player"] == output_data["Slot"]:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = 11
            int_money_amt = 1
            if re.search(r"^\d+", item_data["name"]):
                int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = int_money_amt
            if "Coins" in item_data["name"]:
                if "Bills" in item_data["name"]:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 3
                else:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 1
            elif "Bills" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 2
            elif "Sapphire" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 4
            elif "Emerald" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 6
            elif "Ruby" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 5
            elif "Gold Bar" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 7
            elif item_data["name"] == "Diamond":
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 9
            elif item_data["name"] == "Gold Diamond":
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 10
            else:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0
        else:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0


def update_furniture_info(furniture_info, item_appear_info, output_data):
    # Adjust the item spawn height based on if the item spawns from the ceiling or high up on the wall.
    # Otherwise items are sent into the floor above or out of bounds, which makes it almost impossible to get.
    ceiling_furniture_list = [4, 38, 43, 62, 63, 76, 77, 81, 84, 85, 91, 92, 101, 110, 111, 137, 156, 158, 159, 163,
        173, 174, 189, 190, 195, 199, 200, 228, 240, 266, 310, 342, 352, 354, 355, 356, 357, 358, 359, 373, 374,
        378, 379, 380, 381, 399, 423, 426, 445, 446, 454, 459, 460, 463, 467, 485, 547, 595, 596, 631, 632, 636,
        657, 671, 672]
    medium_height_furniture_list = [0, 1, 104, 112, 113, 114, 124, 125, 135, 136, 204, 206, 210, 232, 234, 235,
        264, 265, 270, 315, 343, 344, 345, 346, 347, 353, 361, 362, 363, 368, 369, 370, 376, 388, 397, 398,
        411, 418, 431, 438, 444, 520, 526, 544, 552, 553, 554, 555, 557, 602, 603, 634, 635]
    for furniture_jmp_id in (ceiling_furniture_list + medium_height_furniture_list):
        current_y_offset = furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"]
        adjust_y_offset = 125.0
        if furniture_jmp_id in ceiling_furniture_list:
            adjust_y_offset += 100.0
        furniture_info.info_file_field_entries[furniture_jmp_id]["item_offset_y"] = current_y_offset - adjust_y_offset

    # Foyer Chandelier will never ever hurt anyone ever again.
    furniture_info.info_file_field_entries[101]["move"] = 7
    furniture_info.info_file_field_entries[277]["move"] = 23

    for x in furniture_info.info_file_field_entries:
        # If this is a book/bookshelf, set it to just shake, no book interaction.
        # Make sure to exclude Nana's knit ball bowl so they can drop on the floor properly.
        if x["move"] == 16 and x["dmd_name"] != "o_tuku1":
            x["move"] = 0

        # Removes the red diamond from furniture as this will break our custom code fix we have for king boo.
        if x["generate"] == 8:
            x["item_table"] = 0
            x["generate"] = 0
            x["generate_num"] = 0

        # If one of Vincent's painting, update the flag to disable zoom instead.
        # if furniture_info_entry.info_file_field_entries.index(x) in {692, 693, 694, 695, 696, 697}:
        # x["move"] = 0

    for item_name, item_data in output_data["Locations"].items():
        if not (item_data["type"] == "Furniture" or item_data["type"] == "Plant"):
            continue

        if ((item_data["type"] == "Furniture" and item_name != "Kitchen Oven") and
            output_data["Options"]["extra_boo_spots"] == 1):
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["telesa_hide"] = 10

        # If our furniture location is remote only, do not add any values to the table and make sure it remains blank
        if ALL_LOCATION_TABLE[item_name].remote_only:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = 0
            continue

        actor_item_name = _get_item_name(item_data, int(output_data["Slot"]))

        # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
        # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
        filtered_item_appear = list(item_appear_entry for item_appear_entry in
            item_appear_info.info_file_field_entries if  item_appear_entry["item0"] == actor_item_name)
        item_appear_entry_idx = filtered_item_appear[len(filtered_item_appear) - 1]

        # Adjust move types for WDYM furniture items. Trees require water, obviously
        if item_data["loc_enum"] in (184, 185, 138, 139, 140, 141):
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["move"] = 34
        if item_data["loc_enum"] in (9, 23, 314, 538, 539, 628, 629, 683):
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["move"] = 0

        furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = (
            item_appear_info.info_file_field_entries.index(item_appear_entry_idx))

        # TODO update using ALL items table instead
        if any((key, val) for (key, val) in filler_items.items() if
               key == item_data["name"] and key != "Diamond" and val.type == "Money") \
                and item_data["player"] == output_data["Slot"]:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["item_table"] = 11
            int_money_amt = 1
            if re.search(r"^\d+", item_data["name"]):
                int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = int_money_amt
            if "Coins" in item_data["name"]:
                if "Bills" in item_data["name"]:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 3
                else:
                    furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 1
            elif "Bills" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 2
            elif "Sapphire" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 4
            elif "Emerald" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 6
            elif "Ruby" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 5
            elif "Gold Bar" in item_data["name"]:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 7
            elif item_data["name"] == "Diamond":
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 9
            elif item_data["name"] == "Gold Diamond":
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 10
            else:
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
                furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0
        else:
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate"] = 0
            furniture_info.info_file_field_entries[item_data["loc_enum"]]["generate_num"] = 0


def update_iyapoo_table(iyapoo_table, output_data):
    if output_data["Options"]["speedy_spirits"] == 0 and output_data["Options"]["gold_mice"] == 0:
        return

    slot_num: int = int(output_data["Slot"])
    output_loc = output_data["Locations"]
    for iyapoo in iyapoo_table.info_file_field_entries:
        item_data = {}
        if output_data["Options"]["speedy_spirits"] == 0 and "iyapoo" in iyapoo["name"]:
            continue
        match iyapoo["name"]:
            case "iyapoo1":
                item_data = output_loc["Storage Room Speedy Spirit"]
            case "iyapoo2":
                item_data = output_loc["Billiards Room Speedy Spirit"]
            case "iyapoo3":
                item_data = output_loc["Dining Room Speedy Spirit"]
            case "iyapoo4":
                item_data = output_loc["Study Speedy Spirit"]
            case "iyapoo5":
                item_data = output_loc["Twins' Room Speedy Spirit"]
            case "iyapoo6":
                item_data = output_loc["Nana's Room Speedy Spirit"]
            case "iyapoo7":
                item_data = output_loc["Kitchen Speedy Spirit"]
            case "iyapoo8":
                item_data = output_loc["Sealed Room Speedy Spirit"]
            case "iyapoo9":
                item_data = output_loc["Rec Room Speedy Spirit"]
            case "iyapoo10":
                item_data = output_loc["Wardrobe Speedy Spirit"]
            case "iyapoo11":
                item_data = output_loc["Cellar Speedy Spirit"]
            case "iyapoo12":
                item_data = output_loc["Breaker Room Speedy Spirit"]
            case "iyapoo13":
                item_data = output_loc["Hidden Room Speedy Spirit"]
            case "iyapoo14":
                item_data = output_loc["Conservatory Speedy Spirit"]
            case "iyapoo15":
                item_data = output_loc["Nursery Speedy Spirit"]
            case "iyapoo15":
                item_data = output_loc["Nursery Speedy Spirit"]

        if output_data["Options"]["gold_mice"] == 0 and "goldrat" in iyapoo["name"]:
            continue
        match iyapoo["name"]:
            case "goldrat0":
                item_data = output_loc["1F Hallway Chance Mouse"]
            case "goldrat1":
                item_data = output_loc["2F Rear Hallway Chance Mouse"]
            case "goldrat2":
                item_data = output_loc["Kitchen Chance Mouse"]
            case "goldrat3":
                item_data = output_loc["Tea Room Chance Mouse"]
            case "goldrat4":
                item_data = output_loc["Sealed Room Chance Mouse"]
            case "goldrat5":
                item_data = output_loc["Dining Room Cheese Mouse"]
            case "goldrat6":
                item_data = output_loc["Fortune Teller Cheese Mouse"]
            case "goldrat7":
                item_data = output_loc["Study Cheese Gold Mouse"]
            case "goldrat8":
                item_data = output_loc["Tea Room Cheese Mouse"]
            case "goldrat9":
                item_data = output_loc["Safari Room Cheese Mouse"]

        treasure_item_name = _get_item_name(item_data, slot_num)
        coin_amount = 0
        bill_amount = 0
        gold_bar_amount = 0
        sapphire_amount = 0
        emerald_amount = 0
        ruby_amount = 0

        if int(item_data["player"]) == slot_num and item_data["name"] in ALL_ITEMS_TABLE.keys():
            lm_item_data = ALL_ITEMS_TABLE[item_data["name"]]
            if lm_item_data.update_ram_addr and any(update_addr.item_count for update_addr in
                    lm_item_data.update_ram_addr if update_addr.item_count and update_addr.item_count > 0):
                item_amt = next(update_addr.item_count for update_addr in lm_item_data.update_ram_addr if
                   update_addr.item_count and update_addr.item_count > 0)

                if "Coins" in item_data["name"]:
                    if "Bills" in item_data["name"]:
                        coin_amount = item_amt
                        bill_amount = item_amt
                    else:
                        coin_amount = item_amt
                elif "Bills" in item_data["name"]:
                    bill_amount = item_amt
                elif "Gold Bar" in item_data["name"]:
                    gold_bar_amount = item_amt
                elif "Sapphire" in item_data["name"]:
                    sapphire_amount = item_amt
                elif "Emerald" in item_data["name"]:
                    emerald_amount = item_amt
                elif "Ruby" in item_data["name"]:
                    ruby_amount = item_amt

        index = iyapoo_table.info_file_field_entries.index(iyapoo)
        iyapoo_table.info_file_field_entries[index]["coin"] = coin_amount
        iyapoo_table.info_file_field_entries[index]["bill"] = bill_amount
        iyapoo_table.info_file_field_entries[index]["gold"] = gold_bar_amount
        iyapoo_table.info_file_field_entries[index]["sapphire"] = sapphire_amount
        iyapoo_table.info_file_field_entries[index]["emerald"] = emerald_amount
        iyapoo_table.info_file_field_entries[index]["ruby"] = ruby_amount
        iyapoo_table.info_file_field_entries[index].update({"other": treasure_item_name})