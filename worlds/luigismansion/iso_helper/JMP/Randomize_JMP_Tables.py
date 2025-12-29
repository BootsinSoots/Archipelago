import copy, re
from io import BytesIO
from math import ceil
from typing import TYPE_CHECKING

from gcbrickwork.JMP import JMP, JMPEntry, JMPValue

from .JMP_Entry_Helpers import (LOCATION_TO_INDEX, SPEEDY_OBSERVER_INDEX, SPEEDY_ENEMY_INDEX, CEILING_FURNITURE_LIST,
    GHOST_LIST, MEDIUM_HEIGHT_FURNITURE_LIST, apply_new_ghost, add_new_jmp_data_entry, create_observer_entry,
    create_iteminfo_entry, create_itemappear_entry, get_item_chest_visual, get_chest_size_from_item, get_item_name,
    update_jmp_value, BOO_HIDING_SPOT_BANS, get_jmp_value, update_temp_jmp_value)

from ...Items import ALL_ITEMS_TABLE, LMItemData, CurrencyItemData, filler_items
from ...Regions import REGION_LIST, TOAD_SPAWN_LIST
from ...Locations import FLIP_BALCONY_BOO_EVENT_LIST, ALL_LOCATION_TABLE, LMLocationData
from ...game.Currency import CURRENCIES

if TYPE_CHECKING:
    from ..LM_Randomize_ISO import LuigisMansionRandomizer

class RandomizeJMPTables:

    lm_rando: "LuigisMansionRandomizer"


    def __init__(self, rando_obj: "LuigisMansionRandomizer"):
        self.lm_rando = rando_obj


    def randomize_jmp_tables(self):
        self._map_two_changes()
        self._add_hearts_to_other_maps()
        self._map_one_changes()
        self._map_three_changes()
        self._map_six_changes()


    def _map_one_changes(self):
        """Updates all the jmp files with their relevant changes on the Lab map"""
        self.lm_rando.client_logger.info("Now updating all changes for the Lab map. Starting with events...")
        map_one_events: JMP = self.lm_rando.map_files["map1"].jmp_files["eventinfo"]

        for event_entry in map_one_events.data_entries:
            if int(map_one_events.get_jmp_header_name_value(event_entry, "EventNo")) == 8:
                map_one_events.update_jmp_header_name_value(event_entry, "EventIf", 5)

    def _map_three_changes(self):
        """Updates the relevant changes on the training map."""
        map_three_events: JMP = self.lm_rando.map_files["map3"].jmp_files["eventinfo"]
        # Remove the event 9 entry and only leave event 10 here.
        map_three_events.data_entries.remove(map_three_events.data_entries[0])

    def _map_six_changes(self):
        """Updates all the jmp files with their relevant changes on the Gallery map"""
        wdym_enabled: bool = bool(self.lm_rando.output_data["Options"]["WDYM_checks"])
        if not wdym_enabled:
            return

        self.lm_rando.client_logger.info("Now updating all changes for the Gallery map. Starting with furniture...")
        ceiling_furniture_list: list[int] = [0, 1]

        map_six_furniture: JMP = self.lm_rando.map_files["map6"].jmp_files["furnitureinfo"]
        map_six_item_appear: JMP = self.lm_rando.map_files["map6"].jmp_files["itemappeartable"]
        for furniture_jmp_id in ceiling_furniture_list:
            curr_y_offset: int = int(map_six_furniture.get_jmp_header_name_value(
                map_six_furniture.data_entries[furniture_jmp_id], "item_offset_y"))
            adjust_y_offset = 225.0
            map_six_furniture.update_jmp_header_name_value(map_six_furniture.data_entries[furniture_jmp_id],
                "item_offset_y", curr_y_offset - adjust_y_offset)

        for item_name, item_data in self.lm_rando.output_data["Locations"]["Furniture"].items():
            location_data: LMLocationData = ALL_LOCATION_TABLE[item_name]
            if not location_data.region == "Gallery":
                continue

            actor_item_name = get_item_name(item_data, self.lm_rando.slot)

            furniture_entry: JMPEntry = map_six_furniture.data_entries[item_data["loc_enum"]]

            # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
            # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
            filtered_item_appear: list[JMPValue] = [index for index, item_appear_entry in enumerate(map_six_item_appear.data_entries)
                if map_six_item_appear.get_jmp_header_name_value(item_appear_entry, "item0") == actor_item_name]
            map_six_furniture.update_jmp_header_name_value(furniture_entry, "item_table",
                filtered_item_appear.index(filtered_item_appear[len(filtered_item_appear) - 1]))

            # TODO update using ALL items table instead
            if any((key, val) for (key, val) in filler_items.items() if
                   key == item_data["name"] and key != "Diamond" and val.type == "Money") \
                    and item_data["player"] == self.lm_rando.slot:

                map_six_furniture.update_jmp_header_name_value(furniture_entry, "item_table", 11)
                int_money_amt = 1
                if re.search(r"^\d+", item_data["name"]):
                    int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
                map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", int_money_amt)
                if "Coins" in item_data["name"]:
                    if "Bills" in item_data["name"]:
                        map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 3)
                    else:
                        map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 1)
                elif "Bills" in item_data["name"]:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 2)
                elif "Sapphire" in item_data["name"]:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 4)
                elif "Emerald" in item_data["name"]:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 6)
                elif "Ruby" in item_data["name"]:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 5)
                elif "Gold Bar" in item_data["name"]:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 7)
                elif item_data["name"] == "Diamond":
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 9)
                elif item_data["name"] == "Gold Diamond":
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 10)
                else:
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 0)
                    map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", 0)
            else:
                map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate", 0)
                map_six_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", 0)


    def _map_two_changes(self):
        """Updates all the jmp files with their relevant changes on the main mansion map"""
        self.lm_rando.client_logger.info("Now updating all changes for the main Mansion map (map2).")

        self._map_two_generator_changes()
        self._map_two_obj_changes()
        self._map_two_room_info_changes()
        self._map_two_boo_table_changes()
        self._map_two_teiden_observer_changes()
        self._map_two_observer_changes()
        self._map_two_enemy_changes()
        self._map_two_event_changes()

        self._map_two_item_info_changes()
        self._map_two_item_appear_changes()
        self._map_two_key_info_changes()
        self._map_two_character_changes()
        self._map_two_treasure_changes()
        self._map_two_iyapoo_changes()
        self._map_two_furniture_changes()


    def _map_two_generator_changes(self):
        """Updates various actors (such as enemies, items, elements, portraits) that will be spawned in/generated."""
        self.lm_rando.client_logger.info("Now updating all generator changes for map2.")
        map_two_gen: JMP = self.lm_rando.map_files["map2"].jmp_files["generatorinfo"]
        for gen_entry in map_two_gen.data_entries:
            # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
            # This prevents being softlocked in Boolossus and having to reset the game without saving.
            if map_two_gen.check_header_name_has_value(gen_entry, "type", "demotel2"):
                map_two_gen.update_jmp_header_name_value(gen_entry, "appear_flag", 45)
                map_two_gen.update_jmp_header_name_value(gen_entry, "disappear_flag", 81)


    def _map_two_obj_changes(self):
        """Updates various objects found on map 2, alot of which have very hardcoded behaviours."""
        self.lm_rando.client_logger.info("Now updating all object changes for map2.")
        # Removes the vines on Area doors, as those require the Area Number of the game to be changed
        # to have them disappear.
        bad_objects_to_remove: list[str] = ["eldoor07", "eldoor08", "eldoor09", "eldoor10"]
        map_two_obj: JMP = self.lm_rando.map_files["map2"].jmp_files["objinfo"]
        map_two_obj.data_entries = [obj_entry for obj_entry in map_two_obj.data_entries if
            not map_two_obj.get_jmp_header_name_value(obj_entry, "name") in bad_objects_to_remove]


    def _map_two_item_info_changes(self):
        """Updates/Adds items that can be spawned in via the other JMP tables.
        To avoid item row duplication, items are only added once."""
        self.lm_rando.client_logger.info("Now updating all item_info changes for map2.")
        already_exist_items: list[str] = []
        hp_item_names: dict[str, int] = {"sheart": 20, "lheart": 50}
        map_two_info: JMP = self.lm_rando.map_files["map2"].jmp_files["iteminfotable"]

        for info_entry in map_two_info.data_entries:
            item_name: str = map_two_info.get_jmp_header_name_value(info_entry, "name")
            if map_two_info.get_jmp_header_name_value(info_entry, "name") in hp_item_names.keys():
                map_two_info.update_jmp_header_name_value(info_entry, "HPAmount", hp_item_names[item_name])
            if not item_name in already_exist_items:
                already_exist_items.append(item_name)

        for location_type in self.lm_rando.output_data["Locations"].keys():
            for item_data in self.lm_rando.output_data["Locations"][location_type].values():
                lm_item_name: str = get_item_name(item_data, self.lm_rando.slot)
                if not lm_item_name in already_exist_items:
                    add_new_jmp_data_entry(map_two_info, create_iteminfo_entry(item_data["room_no"], lm_item_name))
                    already_exist_items.append(lm_item_name)


    def _map_two_key_info_changes(self):
        """Updates all the key item information, which is used for spawning free-standing items."""
        self.lm_rando.client_logger.info("Now updating all keyinfo changes for map2.")
        map_two_key: JMP = self.lm_rando.map_files["map2"].jmp_files["keyinfo"]

        # For every Freestanding Key in the game, replace its entry with the proper item from the generation output.
        for item_name, item_data in self.lm_rando.output_data["Locations"]["Freestanding"].items():
            curr_entry: JMPEntry = map_two_key.data_entries[LOCATION_TO_INDEX[item_name]]
            map_two_key.update_jmp_header_name_value(curr_entry, "name", get_item_name(item_data, self.lm_rando.slot))
            map_two_key.update_jmp_header_name_value(curr_entry, "open_door_no", int(item_data["door_id"]))
            map_two_key.update_jmp_header_name_value(curr_entry, "appear_flag", 0)
            map_two_key.update_jmp_header_name_value(curr_entry, "disappear_flag", 0)
            if map_two_key.get_jmp_header_name_value(curr_entry, "CodeName") == "demo_key2":
                map_two_key.update_jmp_header_name_value(curr_entry, "invisible", 0)

        # Remove the cutscene HD key from the Foyer, which only appears in the cutscene.
        map_two_key.data_entries.remove(map_two_key.data_entries[2])


    def _map_two_room_info_changes(self):
        """Updates the spookiness ambience noises in all the rooms."""
        self.lm_rando.client_logger.info("Now updating all room changes for map2.")
        spooky_rating: int = int(self.lm_rando.output_data["Options"]["spookiness"])
        if spooky_rating == 0:
            return

        map_two_room: JMP = self.lm_rando.map_files["map2"].jmp_files["roominfo"]
        match spooky_rating:
            case 1:
                for room_entry in map_two_room.data_entries:
                    map_two_room.update_jmp_header_name_value(room_entry, "Thunder", 3) # MANY THUNDER
                    map_two_room.update_jmp_header_name_value(room_entry, "sound_echo_parameter", 20) # LONG ECHO
                    map_two_room.update_jmp_header_name_value(room_entry, "sound_room_code", 5)  # CREAKY CREAKY
            case 2:
                for room_entry in map_two_room.data_entries:
                    coin_flip = self.lm_rando.random.choice(sorted([0, 1]))
                    if coin_flip == 1:
                        map_two_room.update_jmp_header_name_value(room_entry, "Thunder", 3)  # MANY THUNDER
                        map_two_room.update_jmp_header_name_value(room_entry, "sound_echo_parameter", 20)  # LONG ECHO
                        map_two_room.update_jmp_header_name_value(room_entry, "sound_room_code", 5)  # CREAKY CREAKY


    def _map_two_item_appear_changes(self):
        """Updates the items that can appear from various objects, like chests or furniture."""
        self.lm_rando.client_logger.info("Now updating all item_appear changes for map2.")
        map_two_item_appear: JMP = self.lm_rando.map_files["map2"].jmp_files["itemappeartable"]

        # Gets the list of keys already added in the item appear table
        already_exist_items: list[str] = list(set([map_two_item_appear.get_jmp_header_name_value(item_entry,
            "item0") for item_entry in map_two_item_appear.data_entries]))

        for location_type in self.lm_rando.output_data["Locations"].keys():
            for item_data in self.lm_rando.output_data["Locations"][location_type].values():
                lm_item_name: str = get_item_name(item_data, self.lm_rando.slot)
                if not lm_item_name in already_exist_items:
                    add_new_jmp_data_entry(map_two_item_appear, create_itemappear_entry(lm_item_name))
                    already_exist_items.append(lm_item_name)


    def _map_two_boo_table_changes(self):
        """Updates boos health, speed, acceleration, anger, and time to escape rooms."""
        self.lm_rando.client_logger.info("Now updating all boo/telesa changes for map2.")
        boo_health_choice: int = int(self.lm_rando.output_data["Options"]["boo_health_option"])
        boo_speed: int = int(self.lm_rando.output_data["Options"]["boo_speed"])
        boo_escape_time: int = int(self.lm_rando.output_data["Options"]["boo_escape_time"])
        boo_anger: int = int(self.lm_rando.output_data["Options"]["boo_anger"])
        boo_chosen_hp: int = int(self.lm_rando.output_data["Options"]["boo_health_value"])

        map_two_telesa: JMP = self.lm_rando.map_files["map2"].jmp_files["telesa"]
        boo_hp_unit: int = 0

        if boo_health_choice == 2:
            boo_hp_unit = max([int(boo_loc["boo_sphere"]) for boo_loc in self.lm_rando.output_data["Locations"]["Boo"].values()])
        for boo_entry in self.lm_rando.output_data["Locations"]["Boo"].values():
            curr_boo_entry: JMPEntry = map_two_telesa.data_entries[int(boo_entry["loc_enum"])]
            map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "accel", 3.000000)
            map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "max_speed", boo_speed)
            map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "move_time", boo_escape_time)
            map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "attack", boo_anger)
            match boo_health_choice:
                case 0:
                    map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "str_hp", boo_chosen_hp)
                case 1:
                    boo_random_hp: int = self.lm_rando.random.randint(1, boo_chosen_hp)
                    map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "str_hp", boo_random_hp)
                case 2:
                    boo_sphere_hp: int = ceil(boo_hp_unit * boo_entry["boo_sphere"]) if ceil(
                        boo_hp_unit * boo_entry["boo_sphere"]) <= boo_chosen_hp else boo_chosen_hp
                    map_two_telesa.update_jmp_header_name_value(curr_boo_entry, "str_hp", boo_sphere_hp)
                case _:
                    continue


    def _map_two_teiden_observer_changes(self):
        """Updates the observers that are created during the blackout sequence."""
        self.lm_rando.client_logger.info("Now updating all blackout observer changes for map2.")
        enable_speedy_spirits: bool = bool(self.lm_rando.output_data["Options"]["speedy_spirits"])
        map_two_teiden_observer: JMP = self.lm_rando.map_files["map2"].jmp_files["teidenobserverinfo"]
        map_two_normal_observer: JMP = self.lm_rando.map_files["map2"].jmp_files["observerinfo"]

        if enable_speedy_spirits:
            for entry_no in SPEEDY_OBSERVER_INDEX:
                speedy_entry: JMPEntry = map_two_normal_observer.data_entries[entry_no]
                map_two_teiden_observer.data_entries.append(speedy_entry)
                map_two_normal_observer.data_entries.remove(speedy_entry)

        # This one checks for luigi entering the wardrobe in blackout, triggering the Grimmly hint
        add_new_jmp_data_entry(map_two_teiden_observer, create_observer_entry(-2040.000000, 760.000000, -3020.000000,
            38, 15, 7, arg0=157))

        # Adds an observer in Blackout Breaker room (event44) to turn on spikes on the doors when room flag 115 is on.
        add_new_jmp_data_entry(map_two_teiden_observer, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 11, cond_arg0=115))

        # Adds a teiden observer in Blackout Breaker room (event44) to turn off spikes on the doors when room flag 120 on.
        add_new_jmp_data_entry(map_two_teiden_observer, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 12, cond_arg0=120))


    def _map_two_observer_changes(self):
        """Updates the observers that are created during normal gameplay."""
        self.lm_rando.client_logger.info("Now updating all normal observer changes for map2.")
        spawn_area: str = self.lm_rando.output_data["Options"]["spawn"]
        spawn_data = REGION_LIST[spawn_area]

        # Load the normal map2 observer
        map_two_nobserver: JMP = self.lm_rando.map_files["map2"].jmp_files["observerinfo"]
        temp_new_entries: list[JMPEntry] = []
        toad_char_name_list: list[str] = ["dm_kinopio5", "dm_kinopio4", "dm_kinopio3", "dm_kinopio2"]

        for observer_entry in map_two_nobserver.data_entries:
            # Allows the Toads to spawn by default.
            observer_name: str = get_jmp_value(map_two_nobserver, observer_entry, "name")
            code_name: str = get_jmp_value(map_two_nobserver, observer_entry, "code_name")
            room_num: int = int(get_jmp_value(map_two_nobserver, observer_entry, "room_no"))
            curr_x_pos: float = float(get_jmp_value(map_two_nobserver, observer_entry, "pos_x"))
            do_num: int = int(get_jmp_value(map_two_nobserver, observer_entry, "do_type"))

            if observer_name == "kinopio":
                if code_name in toad_char_name_list:
                    continue
                update_jmp_value(map_two_nobserver, observer_entry, "cond_arg0", 0)
                update_jmp_value(map_two_nobserver, observer_entry, "appear_flag", 0)
                update_jmp_value(map_two_nobserver, observer_entry, "cond_type", 0)

                if not spawn_area in TOAD_SPAWN_LIST:
                    new_entry: JMPEntry = copy.deepcopy(observer_entry)
                    update_temp_jmp_value(new_entry, "room_no", spawn_data.room_id)
                    update_temp_jmp_value(new_entry, "pos_x", int(spawn_data.pos_x) - 150)
                    update_temp_jmp_value(new_entry, "pos_y", spawn_data.pos_y)
                    update_temp_jmp_value(new_entry, "pos_z", int(spawn_data.pos_z) - 150)
                    update_temp_jmp_value(new_entry, "code_name", "dm_kinopio5")
                    temp_new_entries.append(new_entry)

            # Allows the Master Bedroom to be lit after clearing it, even if Neville hasn't been caught.
            if room_num == 33:
                update_jmp_value(map_two_nobserver, observer_entry, "appear_flag", 0)

            # Allows Twins Room to be lit after clearing it, even if Chauncey hasn't been caught.
            elif room_num == 25:
                update_jmp_value(map_two_nobserver, observer_entry, "appear_flag", 0)

            # Remove locking doors behind Luigi in dark rooms to prevent soft locks
            if do_num == 11:
                update_jmp_value(map_two_nobserver, observer_entry, "do_type", 0)

            # Add CodeNames to iphone entries out of blackout
            if observer_name == "iphone" and curr_x_pos == -748.401100:
                update_jmp_value(map_two_nobserver, observer_entry, "code_name", "tel2")
            elif observer_name == "iphone" and curr_x_pos == 752.692200:
                update_jmp_value(map_two_nobserver, observer_entry, "code_name", "tel3")
            elif observer_name == "iphone" and curr_x_pos == 0.000000:
                update_jmp_value(map_two_nobserver, observer_entry, "code_name", "tel1")

        map_two_nobserver.data_entries += temp_new_entries

        # This one checks for the candles being lit in the Fortune-Teller's Room, flagging that key spawn
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(1870.000000, 190.000000, 140.000000,
            3, 9, 7, arg0=110))

        # This one checks for lights on in the 1F Bathroom, flagging that key spawn
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-2130.000000, 180.000000, -4550.000000,
            20, 13, 7, arg0=110))

        # This one checks for lights on in the Well, flagging that key spawn
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(590.000000, -445.000000, -5910.000000,
            69, 13, 7, arg0=110))

        # This one checks for lights on in the Wardrobe, flagging that key spawn
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-2040.000000, 760.000000, -3020.000000,
            38, 13, 7, arg0=110))

        # Turn on Flag 22 to stop Van Gogh from reloading
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2970.000000, 1550.000000, -2095.000000,
            57, 13, 7, arg0=22))

        # This one checks for lights on in the Dining Room, to prevent Luggs Respawning
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-400.000000, 420.000000, -1800.000000,
            9, 13, 7, arg0=31))

        # Adds an observer in Clairvoya's room (event36) to turn on spikes on the doors when room flag 120 is on.
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2074.000000, 100.000000, -261.000000,
            3, 18, 11, cond_arg0=120))

        # Adds an observer in Clairvoya's room (event36) to turn off spikes on the doors when room flag 120 is off.
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2074.000000, 100.000000, -261.000000,
            3, 19, 12, cond_arg0=120))

        # Adds an observer in Blackout Breaker room (event44) to turn on spikes on the doors when room flag 115 is on.
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 11, cond_arg0=115))

        # Adds an observer in Blackout Breaker room (event44) to turn off spikes on the doors when room flag 120 is on.
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 12, cond_arg0=120))

        # Check that Shivers is caught to turn on Conservatory Hallway Light
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(3250.000000, 0.000000, -100.000000,
            0, 13, 7, arg0=60))

        # This one enables the Conservatory 1F hallway after catching Shivers / Butler
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(1400.000000, 0.000000, -4100.000000,
            18, 18, 1, cond_arg0=60))

        # This one adds an observer into the Foyer where if Luigi is in the room anywhere, it will turn on the lights.
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(0.000000, 0.000000, 0.000000,
            2, 15, 1))

        # This one checks for luigi entering the clockwork room, triggering the doll hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=157))

        # This one checks for luigi entering the clockwork room, triggering the doll2 hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=158))

        # This one checks for luigi entering the clockwork room, triggering the doll3 hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=159))

        # This one checks for luigi entering the artist's room, triggering the gaka hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2890.000000, 1100.000000, -1640.000000,
            57, 15, 7, arg0=157))

        # This one checks for luigi entering the study, triggering the father hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-2440.000000, 550.000000, -2700.000000,
            34, 15, 7, arg0=157))

        # This one checks for luigi entering the master bedroom, triggering the mother hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-3760.000000, 550.000000, -1800.000000,
            33, 15, 7, arg0=157))

        # This one checks for luigi entering the nursery, triggering the baby hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-3340.000000, 550.000000, -220.000000,
            24, 15, 7, arg0=157))

        # This one checks for luigi entering the twins room, triggering the dboy hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-1820.000000, 550.000000, -220.000000,
            25, 15, 7, arg0=157))

        # This one checks for luigi entering the nanas room, triggering the nana hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(300.000000, 550.000000, -4960.000000,
            46, 15, 7, arg0=157))

        # This one checks for luigi entering the 2f bathroom, triggering the petunia hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-2100.000000, 550.000000, -4640.000000,
            45, 15, 7, arg0=157))

        # This one checks for luigi entering the guest room, triggering the girl hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(3340.000000, 550.000000, -220.000000,
            28, 15, 7, arg0=157))

        # This one checks for luigi entering the back hallway, triggering the butler hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-3600.000000, 0.000000, 150.000000,
            18, 15, 7, arg0=157))

        # This one checks for luigi entering the dining room, triggering the luggs hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-280.000000, 0.000000, -1480.000000,
            9, 15, 7, arg0=157))

        # This one checks for luigi entering the ballroom, triggering the dancer hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2540.000000, 0.000000, -2800.000000,
            10, 15, 7, arg0=157))

        # This one checks for luigi entering the billiard room, triggering the hustler hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-1200.000000, 0.000000, -3840.000000,
            12, 15, 7, arg0=157))

        # This one checks for luigi entering the conservatory, triggering the pianist hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(1360.000000, 0.000000, -4920.000000,
            21, 15, 7, arg0=157))

        # This one checks for luigi entering the rec room, triggering the builder hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(2840.000000, 0.000000, -4940.000000,
            22, 15, 7, arg0=157))

        # This one checks for luigi entering the boneyard, triggering the dog hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(-3360.000000, 0.000000, -3080.000000,
            11, 15, 7, arg0=157))

        # This one checks for luigi entering the cold storage, triggering the snowman hint
        add_new_jmp_data_entry(map_two_nobserver, create_observer_entry(1180.000000, -445.000000, -690.000000,
            61, 15, 7, arg0=157))


    def _map_two_enemy_changes(self):
        """Handles changes to enemy table for both normal and blackout."""
        enemizer_enabled: int = int(self.lm_rando.output_data["Options"]["enemizer"])
        speedy_enabled: bool = bool(self.lm_rando.output_data["Options"]["speedy_spirits"])

        # If randomize ghosts options are not enabled or speedy spirits are not enabled.
        if not speedy_enabled or enemizer_enabled == 0:
            return

        self.lm_rando.client_logger.info("Now updating all enemy changes (both normal and blackout) for map2.")
        map_two_teiden_enemy: JMP = self.lm_rando.map_files["map2"].jmp_files["teidenenemyinfo"]
        map_two_normal_enemy: JMP = self.lm_rando.map_files["map2"].jmp_files["enemyinfo"]

        if speedy_enabled:
            for entry_no in SPEEDY_ENEMY_INDEX:
                speedy_entry: JMPEntry = map_two_normal_enemy.data_entries[entry_no]
                map_two_teiden_enemy.data_entries.append(speedy_entry)
                map_two_normal_enemy.data_entries.remove(speedy_entry)

        if enemizer_enabled == 0:
            return

        for key, val in self.lm_rando.output_data["Room Enemies"].items():
            room_id: int = REGION_LIST[key].room_id
            for normal_enemy in map_two_normal_enemy.data_entries:
                curr_room_no: int = int(map_two_normal_enemy.get_jmp_header_name_value(normal_enemy, "room_no"))
                curr_enemy_name: str = map_two_normal_enemy.get_jmp_header_name_value(normal_enemy, "name")
                if curr_room_no != room_id or not curr_enemy_name in GHOST_LIST:
                    continue

                if "16_1" in curr_enemy_name:
                    map_two_normal_enemy.update_jmp_header_name_value(normal_enemy, "pos_y", 30.000000)

                room_element: str = "No Element" if (room_id in [27, 35, 40]) else val
                apply_new_ghost(self.lm_rando, map_two_normal_enemy, normal_enemy, room_element)

            for blackout_enemy in map_two_teiden_enemy.data_entries:
                curr_room_no: int = int(map_two_teiden_enemy.get_jmp_header_name_value(blackout_enemy, "room_no"))
                curr_enemy_name: str = map_two_teiden_enemy.get_jmp_header_name_value(blackout_enemy, "name")
                if curr_room_no != room_id or not curr_enemy_name in GHOST_LIST:
                    continue
                apply_new_ghost(self.lm_rando, map_two_teiden_enemy, blackout_enemy, val)


    def _map_two_event_changes(self):
        """Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
        boss battles / grabbing boss keys, and various cutscenes etc. Also remove Mario Items/Elemental Item events"""
        self.lm_rando.client_logger.info("Now updating all event changes for map2.")
        events_to_remove: list[int] = [7, 9, 15, 18, 19, 20, 21, 31, 41, 42, 45, 47, 51, 54, 69, 70, 73, 80, 81, 85, 91]
        map_two_events: JMP = self.lm_rando.map_files["map2"].jmp_files["eventinfo"]

        boo_gates_enabled: bool = bool(self.lm_rando.output_data["Options"]["boo_gates"])
        spawn_area: str = self.lm_rando.output_data["Options"]["spawn"]
        spawn_data = REGION_LIST[spawn_area]
        balcony_boo_count: int = int(self.lm_rando.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.lm_rando.output_data["Options"]["final_boo_count"])

        # Only remove the boo checks if the player does not want them.
        if not boo_gates_enabled:
            events_to_remove += [16, 96]
        elif balcony_boo_count == 0:
            events_to_remove += [96]
        elif final_boo_count == 0:
            events_to_remove += [16]
        if spawn_area in TOAD_SPAWN_LIST:
            events_to_remove += [12]

        map_two_events.data_entries = [event_entry for event_entry in map_two_events.data_entries if not
            map_two_events.get_jmp_header_name_value(event_entry, "EventNo") in events_to_remove]

        map_two_events.data_entries = [event_entry for event_entry in map_two_events.data_entries if not
            (int(map_two_events.get_jmp_header_name_value(event_entry, "EventNo")) == 93 and
            float(map_two_events.get_jmp_header_name_value(event_entry, "pos_x")) == 0.000000)]

        for event_info in map_two_events.data_entries:
            event_num: int = int(map_two_events.get_jmp_header_name_value(event_info, "EventNo"))

            # Move Telephone rings to third phone, make an A press and make always on
            if event_num == 92:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 150)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 1)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", 0.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", 1100.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -25.000000)

            # Telephone room event for the telephones, make an A press and make always on
            elif event_num == 94:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 150)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 1)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", 755.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", 1100.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -25.000000)

            # Telephone room event for the telephones, make an A press and make always on
            elif event_num == 93:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 150)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 1)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", -755.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", 1100.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -25.000000)

            # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
            # This prevents being soft locked in Boolossus and having to reset the game without saving.
            elif event_num == 71:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 45)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)

            # Allows Jarvis' (Ceramics Room) to only appear when the Ice Medal has been collected.
            # This prevents being kicked out by Jarvis' and being unable to participate in his game.
            elif event_num == 33:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 45)

            # Since we have a custom blackout event, we need to update event 44's trigger condition to be A-pressed based.
            # We also update the area ad trigger location to be the same as event45
            elif event_num == 44:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 230)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventLock", 0)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 0)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", 3500.277000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", -550.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -2150.792000)

            # Update the spawn in event trigger to wherever spawn is
            elif event_num == 48:
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", spawn_data.pos_x)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", spawn_data.pos_y)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", spawn_data.pos_z)

            # Removes the Mr. Bones requirement. He will spawn instantly
            elif event_num == 23:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 74)

            # Turn off Event 74 (Warp to King Boo Fight) in blackout by disabling event if King Boo isn't present
            elif event_num == 74:
                map_two_events.update_jmp_header_name_value(event_info, "CharacterName", "dltelesa")

            # Make Van Gogh load more than once
            elif event_num == 38:
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 22)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 2)

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
            elif boo_gates_enabled and event_num == 16:
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 5)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 200)
                map_two_events.update_jmp_header_name_value(event_info, "EventLock", 1)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", 2260.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", -450.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -5300.000000)

            # Update the Balcony Boo event trigger to be area entry based
            elif boo_gates_enabled and event_num == 96:
                if spawn_area in FLIP_BALCONY_BOO_EVENT_LIST:
                    map_two_events.update_jmp_header_name_value(event_info, "pos_x", 1800.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "pos_y", 1200.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "pos_z", -2950.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "EventArea", 350)
                else:
                    map_two_events.update_jmp_header_name_value(event_info, "pos_x", 1800.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "pos_y", 1200.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "pos_z", -2600.000000)
                    map_two_events.update_jmp_header_name_value(event_info, "EventArea", 200)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 5)
                map_two_events.update_jmp_header_name_value(event_info, "EventLock", 1)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)

            # Update the Intro event to talk about save anywhere and healing.
            elif event_num == 11:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 65535)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 2)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventLock", 1)
                map_two_events.update_jmp_header_name_value(event_info, "event_parameter", 0)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", spawn_data.pos_x)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", spawn_data.pos_y)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", spawn_data.pos_z)

            # Change Training room second visit to always be on
            elif event_num == 10:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)

            # Update Starting Toad Event (event12) to move to the spawn region.
            elif event_num == 12:
                map_two_events.update_jmp_header_name_value(event_info, "EventFlag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "disappear_flag", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 330)
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 1)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", int(spawn_data.pos_x) - 150 + 2)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", spawn_data.pos_y)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", int(spawn_data.pos_z) - 150)


    def _map_two_character_changes(self):
        """Updates the character info table to remove un-necessary actors. Also update existing spawns to new items."""
        self.lm_rando.client_logger.info("Now updating all character changes for map2.")
        map_two_characters: JMP = self.lm_rando.map_files["map2"].jmp_files["characterinfo"]

        spawn_data = REGION_LIST[self.lm_rando.output_data["Options"]["spawn"]]

        bad_actors_to_remove: list[str] = ["vhead", "vbody", "dhakase", "demobak1", "dluige01"]
        update_spawn_actors: list[str] = ["baby", "mother", "dboy", "dboy2"]

        # Removes useless cutscene objects and the vacuum in the Parlor under the closet.
        map_two_characters.data_entries = [char_entry for char_entry in map_two_characters.data_entries if not
            map_two_characters.get_jmp_header_name_value(char_entry, "name") in bad_actors_to_remove]

        # Also removes King Boo in the hallway, since his event was removed.
        map_two_characters.data_entries = [char_entry for char_entry in map_two_characters.data_entries if
            not (map_two_characters.get_jmp_header_name_value(char_entry, "name") == "dltelesa" and
            int(map_two_characters.get_jmp_header_name_value(char_entry, "room_no")) == 68)]

        for character_entry in map_two_characters.data_entries:
            char_name: str = map_two_characters.get_jmp_header_name_value(character_entry, "name")
            char_room_num: int = int(map_two_characters.get_jmp_header_name_value(character_entry, "room_no"))
            # Replace the mstar Observatory item with its randomized item.
            if char_name == "mstar":
                shoot_moon_char: dict = self.lm_rando.output_data["Locations"]["Special"]["Observatory Shoot the Moon"]
                map_two_characters.update_jmp_header_name_value(character_entry, "name", get_item_name(shoot_moon_char, self.lm_rando.slot))
                map_two_characters.update_jmp_header_name_value(character_entry, "appear_flag", 50)
                map_two_characters.update_jmp_header_name_value(character_entry, "invisible", 1)
                map_two_characters.update_jmp_header_name_value(character_entry, "pos_y", 600.000000)

            # Allow Chauncey, Lydia, and the Twins to spawn as soon as a new game is created.
            elif char_name in update_spawn_actors:
                map_two_characters.update_jmp_header_name_value(character_entry, "appear_flag", 0)

            # Fix a Nintendo mistake where the Cellar chest has a room ID of 0 instead of 63.
            elif char_name == "63_2":
                map_two_characters.update_jmp_header_name_value(character_entry, "room_no", 63)

            # Remove Miss Petunia to never disappear, unless captured.
            elif char_name == "fat" and char_room_num == 45:
                map_two_characters.update_jmp_header_name_value(character_entry, "disappear_flag", 0)

            # Make Shivers / Butler not disappear by doing a different appear flag.
            elif char_name == "situji":
                map_two_characters.update_jmp_header_name_value(character_entry, "appear_flag", 7)

            # Make Luggs stay gone if the light are on in the room
            elif char_name == "eater":
                map_two_characters.update_jmp_header_name_value(character_entry, "disappear_flag", 31)

            # Editing the starting room spawn coordinates (regardless of it random spawn is turned on).
            elif char_name == "luige" and char_room_num == 2:
                map_two_characters.update_jmp_header_name_value(character_entry, "room_no", spawn_data.room_id)
                map_two_characters.update_jmp_header_name_value(character_entry, "pos_x", spawn_data.pos_x)
                map_two_characters.update_jmp_header_name_value(character_entry, "pos_y", spawn_data.pos_y)
                map_two_characters.update_jmp_header_name_value(character_entry, "pos_z", spawn_data.pos_z)


    def _map_two_iyapoo_changes(self):
        """Updates what the speedy spirits/golden rats drop upon capturing them."""
        self.lm_rando.client_logger.info("Now updating all speedy spirits/golden mice changes for map2.")
        speedy_enabled: bool = bool(self.lm_rando.output_data["Options"]["speedy_spirits"])
        mice_enabled: bool = bool(self.lm_rando.output_data["Options"]["gold_mice"])
        if not (speedy_enabled and mice_enabled):
            return

        map_two_iyapoo: JMP = self.lm_rando.map_files["map2"].jmp_files["iyapootable"]

        for iyapoo_entry in map_two_iyapoo.data_entries:
            iyapoo_name = map_two_iyapoo.get_jmp_header_name_value(iyapoo_entry, "name")
            item_data: dict = {}

            if speedy_enabled and "iyapoo" in iyapoo_name:
                match iyapoo_name:
                    case "iyapoo1":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Storage Room Speedy Spirit"]
                    case "iyapoo2":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Billiards Room Speedy Spirit"]
                    case "iyapoo3":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Dining Room Speedy Spirit"]
                    case "iyapoo4":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Study Speedy Spirit"]
                    case "iyapoo5":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Twins' Room Speedy Spirit"]
                    case "iyapoo6":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Nana's Room Speedy Spirit"]
                    case "iyapoo7":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Kitchen Speedy Spirit"]
                    case "iyapoo8":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Sealed Room Speedy Spirit"]
                    case "iyapoo9":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Rec Room Speedy Spirit"]
                    case "iyapoo10":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Wardrobe Speedy Spirit"]
                    case "iyapoo11":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Cellar Speedy Spirit"]
                    case "iyapoo12":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Breaker Room Speedy Spirit"]
                    case "iyapoo13":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Hidden Room Speedy Spirit"]
                    case "iyapoo14":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Conservatory Speedy Spirit"]
                    case "iyapoo15":
                        item_data = self.lm_rando.output_data["Locations"]["BSpeedy"]["Nursery Speedy Spirit"]

            if mice_enabled and "goldrat" in iyapoo_name:
                match iyapoo_name:
                    case "goldrat0":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["1F Hallway Chance Mouse"]
                    case "goldrat1":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["2F Rear Hallway Chance Mouse"]
                    case "goldrat2":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Kitchen Chance Mouse"]
                    case "goldrat3":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Tea Room Chance Mouse"]
                    case "goldrat4":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Sealed Room Chance Mouse"]
                    case "goldrat5":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Dining Room Cheese Mouse"]
                    case "goldrat6":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Fortune Teller Cheese Mouse"]
                    case "goldrat7":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Study Cheese Gold Mouse"]
                    case "goldrat8":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Tea Room Cheese Mouse"]
                    case "goldrat9":
                        item_data = self.lm_rando.output_data["Locations"]["Mouse"]["Safari Room Cheese Mouse"]

            if not item_data:
                continue

            coin_amount = 0
            bill_amount = 0
            gold_bar_amount = 0
            sapphire_amount = 0
            emerald_amount = 0
            ruby_amount = 0

            if int(item_data["player"]) == self.lm_rando.slot and item_data["name"] in ALL_ITEMS_TABLE.keys():
                lm_item_data = ALL_ITEMS_TABLE[item_data["name"]]
                if lm_item_data.update_ram_addr and any(update_addr.item_count for update_addr in
                                                        lm_item_data.update_ram_addr if
                                                        update_addr.item_count and update_addr.item_count > 0):
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

            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "coin", coin_amount)
            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "bill", bill_amount)
            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "gold", gold_bar_amount)
            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "sapphire", sapphire_amount)
            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "emerald", emerald_amount)
            map_two_iyapoo.update_jmp_header_name_value(iyapoo_entry, "ruby", ruby_amount)


    def _map_two_treasure_changes(self):
        """Updates the treasure chests drop (and updates visuals/size)"""
        self.lm_rando.client_logger.info("Now updating all treasure chest contents/size/visual changes for map2.")
        map_two_characters: JMP = self.lm_rando.map_files["map2"].jmp_files["characterinfo"]
        map_two_treasure: JMP = self.lm_rando.map_files["map2"].jmp_files["treasuretable"]

        for item_name, item_data in self.lm_rando.output_data["Locations"]["Chest"].items():
            for char_entry in map_two_characters.data_entries:
                char_name: str = map_two_characters.get_jmp_header_name_value(char_entry, "name")
                char_room: int = int(map_two_characters.get_jmp_header_name_value(char_entry, "room_no"))
                # If the name is not a chest or the outside flower/nut
                if not ("takara" in char_name or char_name == "nut"):
                    continue
                # If the character is not the same room as the current chest.
                elif not char_room == int(item_data["room_no"]):
                    continue

                # Special Case: Move the Laundry room chest back from Butler door
                if char_room == 5:
                    map_two_characters.update_jmp_header_name_value(char_entry, "pos_z", -1100.000000)

                # Special Case: Move 2F Bathroom chest back from wall
                elif char_room == 45:
                    map_two_characters.update_jmp_header_name_value(char_entry, "pos_x", -1900.000000)
                    map_two_characters.update_jmp_header_name_value(char_entry, "pos_z", -4830.000000)

                # Change chest appearance and size based of player cosmetic choices
                chest_visual: str = get_item_chest_visual(self.lm_rando, item_data, char_name)
                map_two_characters.update_jmp_header_name_value(char_entry, "name", chest_visual)

                treasure_entry: JMPEntry = map_two_treasure.data_entries[item_data["loc_enum"]]

                # Setting all currencies to 0 value by default.
                for currency_name in CURRENCIES:
                    map_two_treasure.update_jmp_header_name_value(treasure_entry, currency_name, 0)

                # Don't give any items that are not from our game, leave those 0 / blank.
                if int(item_data["player"]) == self.lm_rando.slot and item_data["name"] in ALL_ITEMS_TABLE.keys():
                    lm_item_data: type[LMItemData | CurrencyItemData] = ALL_ITEMS_TABLE[item_data["name"]]

                    # If it's a money item, set the currencies based on our defined bundles
                    if hasattr(lm_item_data, 'currencies'):
                        for currency_name, currency_amount in lm_item_data.currencies.items():
                            map_two_treasure.update_jmp_header_name_value(treasure_entry, currency_name, currency_amount)

                map_two_treasure.update_jmp_header_name_value(treasure_entry, "cdiamond", 0)
                map_two_treasure.update_jmp_header_name_value(treasure_entry, "effect", 0)
                map_two_treasure.update_jmp_header_name_value(treasure_entry, "camera", 0)

                chest_size: int = int(map_two_treasure.get_jmp_header_name_value(treasure_entry, "size"))
                chest_size = get_chest_size_from_item(self.lm_rando, item_data, chest_size)
                map_two_treasure.update_jmp_header_name_value(treasure_entry, "size", chest_size)

                # Define the actor name to use from the Location in the generation output. Act differently if it's a key.
                lm_item_name: str = get_item_name(item_data, self.lm_rando.slot)
                map_two_treasure.update_jmp_header_name_value(treasure_entry, "other", lm_item_name)


    def _map_two_furniture_changes(self):
        """Updates the items that will appear out of the relevant furniture."""
        self.lm_rando.client_logger.info("Now updating all furniture changes for map2.")
        extra_boo_spots: bool = bool(self.lm_rando.output_data["Options"]["extra_boo_spots"])

        map_two_furniture: JMP = self.lm_rando.map_files["map2"].jmp_files["furnitureinfo"]
        map_two_item_appear: JMP = self.lm_rando.map_files["map2"].jmp_files["itemappeartable"]

        for furniture_jmp_id in (CEILING_FURNITURE_LIST + MEDIUM_HEIGHT_FURNITURE_LIST):
            curr_y_offset: int = int(map_two_furniture.get_jmp_header_name_value(
                map_two_furniture.data_entries[furniture_jmp_id], "item_offset_y"))
            adjust_y_offset = 125.0
            if furniture_jmp_id in CEILING_FURNITURE_LIST:
                adjust_y_offset += 100.0
            map_two_furniture.update_jmp_header_name_value(map_two_furniture.data_entries[furniture_jmp_id],
                "item_offset_y",  curr_y_offset - adjust_y_offset)

        # Foyer Chandelier will never ever hurt anyone ever again.
        map_two_furniture.update_jmp_header_name_value(map_two_furniture.data_entries[101], "move", 7)
        map_two_furniture.update_jmp_header_name_value(map_two_furniture.data_entries[277], "move", 23)

        for furn_entry in map_two_furniture.data_entries:
            # If this is a book/bookshelf, set it to just shake, no book interaction.
            # Make sure to exclude Nana's knit ball bowl so they can drop on the floor properly.

            if (int(map_two_furniture.get_jmp_header_name_value(furn_entry, "move")) == 16 and
                map_two_furniture.get_jmp_header_name_value(furn_entry, "dmd_name") != "o_tuku1"):
                map_two_furniture.update_jmp_header_name_value(furn_entry, "move", 0)

            # Removes the red diamond from furniture as this will break our custom code fix we have for king boo.
            if int(map_two_furniture.get_jmp_header_name_value(furn_entry, "generate")) == 8:
                map_two_furniture.update_jmp_header_name_value(furn_entry, "item_table", 0)
                map_two_furniture.update_jmp_header_name_value(furn_entry, "generate", 0)
                map_two_furniture.update_jmp_header_name_value(furn_entry, "generate_num", 0)

        furniture_to_patch: dict = {**self.lm_rando.output_data["Locations"]["Furniture"]}
        if "Plant" in self.lm_rando.output_data["Locations"].keys():
            furniture_to_patch = {
                **furniture_to_patch,
                **self.lm_rando.output_data["Locations"]["Plant"]}
        for item_name, item_data in furniture_to_patch.items():
            # Ignore any Gallery region locations
            location_data: LMLocationData = ALL_LOCATION_TABLE[item_name]
            if location_data.region == "Gallery":
                continue

            furniture_entry: JMPEntry = map_two_furniture.data_entries[item_data["loc_enum"]]

            if (item_data["type"] == "Furniture" and item_name not in BOO_HIDING_SPOT_BANS) and extra_boo_spots:
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "telesa_hide", 10)

            # If our furniture location is remote only, do not add any values to the table and make sure it remains blank
            if ALL_LOCATION_TABLE[item_name].remote_only:
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 0)
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", 0)
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "item_table", 0)
                continue

            actor_item_name = get_item_name(item_data, self.lm_rando.slot)

            # Replace the furnitureinfo entry to spawn an item from the "itemappeartable".
            # If the entry is supposed to be money, then generate a random amount of coins and/or bills from it.
            filtered_item_appear: list[JMPValue] = [index for index, item_appear_entry in enumerate(map_two_item_appear.data_entries)
                if map_two_item_appear.get_jmp_header_name_value(item_appear_entry, "item0") == actor_item_name]
            map_two_furniture.update_jmp_header_name_value(furniture_entry, "item_table",
                filtered_item_appear.index(filtered_item_appear[0]))

            # Adjust move types for WDYM furniture items. Trees require water, obviously
            if item_data["loc_enum"] in [184, 185, 138, 139, 140, 141]:
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "move", 34)
            elif item_data["loc_enum"] in [9, 23, 314, 538, 539, 628, 629, 683]:
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "move", 0)

            # TODO update using ALL items table instead
            if any((key, val) for (key, val) in filler_items.items() if
                key == item_data["name"] and key != "Diamond" and val.type == "Money") \
                and item_data["player"] == self.lm_rando.slot:

                map_two_furniture.update_jmp_header_name_value(furniture_entry, "item_table", 11)
                int_money_amt = 1
                if re.search(r"^\d+", item_data["name"]):
                    int_money_amt = int(re.search(r"^\d+", item_data["name"]).group())
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", int_money_amt)
                if "Coins" in item_data["name"]:
                    if "Bills" in item_data["name"]:
                        map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 3)
                    else:
                        map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 1)
                elif "Bills" in item_data["name"]:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 2)
                elif "Sapphire" in item_data["name"]:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 4)
                elif "Emerald" in item_data["name"]:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 6)
                elif "Ruby" in item_data["name"]:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 5)
                elif "Gold Bar" in item_data["name"]:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 7)
                elif item_data["name"] == "Diamond":
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 9)
                elif item_data["name"] == "Gold Diamond":
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 10)
                else:
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 0)
                    map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", 0)
            else:
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate", 0)
                map_two_furniture.update_jmp_header_name_value(furniture_entry, "generate_num", 0)

    def _add_hearts_to_other_maps(self):
        """Adds the necessary heart drop for the ghosts on boss maps and gallery."""
        self.lm_rando.client_logger.info("Now adding item_appear/item_info entries to the boss maps and gallery map...")
        from ..LM_Map_File import LMMapFile
        # Copy the existing item_appear entries from map2, as these should be the same for the other map files.
        item_appear: JMP = copy.deepcopy(self.lm_rando.empty_jmp_files["itemappeartable"])
        item_appear.data_entries = self.lm_rando.map_files["map2"].jmp_files["itemappeartable"].data_entries[:15]
        item_appear_data: BytesIO = item_appear.create_new_jmp()

        # Create the generic item_info that will be used for all other map files.
        item_info: JMP = copy.deepcopy(self.lm_rando.empty_jmp_files["iteminfotable"])
        add_new_jmp_data_entry(item_info, create_iteminfo_entry(0, "nothing"))
        add_new_jmp_data_entry(item_info, create_iteminfo_entry(0, "sheart", 10))
        add_new_jmp_data_entry(item_info, create_iteminfo_entry(0, "mheart", 20))
        add_new_jmp_data_entry(item_info, create_iteminfo_entry(0, "move_sheart", 10, 1))
        add_new_jmp_data_entry(item_info, create_iteminfo_entry(0, "move_mheart", 20, 1))
        item_info_data: BytesIO = item_info.create_new_jmp()

        for map_name in ["map6.szp", "map9.szp", "map10.szp", "map11.szp", "map13.szp"]:
            # If this current map is the gallery map, add the load JMP files for immediate use later. We will also need
            # all items available to us, in case keys or other things are chosen to hide in the furniture.
            if map_name == "map6.szp":
                curr_map: LMMapFile = self.lm_rando.map_files[map_name.replace(".szp", "")]
                curr_map.jmp_files["iteminfotable"] = self.lm_rando.map_files["map2"].jmp_files["iteminfotable"]
                curr_map.add_new_jmp_file("iteminfotable", curr_map.jmp_files["iteminfotable"].create_new_jmp())
                curr_map.jmp_files["itemappeartable"] = self.lm_rando.map_files["map2"].jmp_files["itemappeartable"]
                curr_map.add_new_jmp_file("itemappeartable", curr_map.jmp_files["itemappeartable"].create_new_jmp())
                continue

            # Add these files directly so these can be saved properly
            curr_map: LMMapFile = LMMapFile(self.lm_rando.lm_gcm, "files/Map/" + map_name)
            curr_map.add_new_jmp_file("itemappeartable", item_appear_data)
            curr_map.add_new_jmp_file("iteminfotable", item_info_data)
            curr_map.update_and_save_map(self.lm_rando.lm_gcm)