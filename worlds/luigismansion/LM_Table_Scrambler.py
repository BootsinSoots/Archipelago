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