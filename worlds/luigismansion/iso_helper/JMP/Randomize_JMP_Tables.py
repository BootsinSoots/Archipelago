import copy
from math import ceil

from gcbrickwork.JMP import JMP, JMPEntry

from JMP_Entry_Helpers import (LOCATION_TO_INDEX, SPEEDY_OBSERVER_INDEX, SPEEDY_ENEMY_INDEX, GHOST_LIST, get_item_name,
    create_iteminfo_entry, add_new_jmp_data_entry, create_itemappear_entry, create_observer_entry, apply_new_ghost)

from ..LM_Randomize_ISO import LuigisMansionRandomizer
from ...Regions import REGION_LIST, TOAD_SPAWN_LIST
from ...Locations import FLIP_BALCONY_BOO_EVENT_LIST


class RandomizeJMPTables:

    lm_rando: LuigisMansionRandomizer = None


    def __init__(self, rando_obj: LuigisMansionRandomizer):
        self.lm_rando = rando_obj


    def randomize_jmp_tables(self):
        self._map_two_changes()


    def _map_two_changes(self):
        self._map_two_generator_changes()
        self._map_two_obj_changes()
        self._map_two_room_info_changes()
        self._map_two_boo_table_changes()
        self._map_two_teiden_observer_changes()
        self._map_two_observer_changes()
        self._map_two_enemy_changes()
        self._map_two_event_changes()

        self._map_two_item_info_changes()
        self._map_two_key_info_changes()


    def _map_two_generator_changes(self):
        """Updates various actors (such as enemies, items, elements, portraits) that will be spawned in/generated."""
        map_two_gen: JMP = self.lm_rando.map_files.get("map2").jmp_files["generatorinfo"]
        for gen_entry in map_two_gen.data_entries:
            # Allows the Ring of Boos on the 3F Balcony to only appear when the Ice Medal has been collected.
            # This prevents being softlocked in Boolossus and having to reset the game without saving.
            if map_two_gen.check_header_name_has_value(gen_entry, "type", "demotel2"):
                map_two_gen.update_jmp_header_name_value(gen_entry, "appear_flag", 45)
                map_two_gen.update_jmp_header_name_value(gen_entry, "disappear_flag", 81)


    def _map_two_obj_changes(self):
        """Updates various objects found on map 2, alot of which have very hardcoded behaviours."""
        # Removes the vines on Area doors, as those require the Area Number of the game to be changed
        # to have them disappear.
        bad_objects_to_remove: list[str] = ["eldoor07", "eldoor08", "eldoor09", "eldoor10"]
        map_two_obj: JMP = self.lm_rando.map_files.get("map2").jmp_files["objinfo"]
        map_two_obj.data_entries = [obj_entry for obj_entry in map_two_obj.data_entries if
            not map_two_obj.get_jmp_header_name_value(obj_entry, "name") in bad_objects_to_remove]


    def _map_two_item_info_changes(self):
        """Updates/Adds items that can be spawned in via the other JMP tables.
        To avoid item row duplication, items are only added once."""
        already_exist_items: list[str] = []
        hp_item_names: dict[str, int] = {"sheart": 20, "lheart": 50}
        map_two_info: JMP = self.lm_rando.map_files.get("map2").jmp_files["iteminfotable"]

        for info_entry in map_two_info.data_entries:
            item_name: str = map_two_info.get_jmp_header_name_value(info_entry, "name")
            if map_two_info.get_jmp_header_name_value(info_entry, "name") in hp_item_names.keys():
                map_two_info.update_jmp_header_name_value(info_entry, "name", hp_item_names[item_name])
            if not item_name in already_exist_items:
                already_exist_items.append(item_name)

        for location_type in self.lm_rando.output_data["Locations"].keys():
            for item_data in self.lm_rando.output_data["Locations"][location_type].vals():
                lm_item_name: str = get_item_name(item_data, self.lm_rando.slot)
                if not lm_item_name in already_exist_items:
                    add_new_jmp_data_entry(map_two_info, create_iteminfo_entry(item_data["room_no"], lm_item_name))
                    already_exist_items.append(lm_item_name)


    def _map_two_key_info_changes(self):
        """Updates all the key item information, which is used for spawning free-standing items."""
        map_two_key: JMP = self.lm_rando.map_files.get("map2").jmp_files["keyinfo"]

        # For every Freestanding Key in the game, replace its entry with the proper item from the generation output.
        for item_name, item_data in self.lm_rando.output_data["Locations"]["Freestanding"].items():
            curr_entry: JMPEntry = map_two_key.data_entries[LOCATION_TO_INDEX[item_name]]
            map_two_key.update_jmp_header_name_value(curr_entry, "name", get_item_name(item_data, self.lm_rando.slot))
            map_two_key.update_jmp_header_name_value(curr_entry, "open_door_no", int(item_data["door_id"]))
            map_two_key.update_jmp_header_name_value(curr_entry, "appear_flag", 0)
            map_two_key.update_jmp_header_name_value(curr_entry, "disappear_flag", 0)
            if map_two_key.get_jmp_header_name_value(curr_entry, "code_name") == "demo_key2":
                map_two_key.update_jmp_header_name_value(curr_entry, "invisible", 0)

        # Remove the cutscene HD key from the Foyer, which only appears in the cutscene.
        map_two_key.data_entries.remove(map_two_key.data_entries[2])


    def _map_two_room_info_changes(self):
        """Updates the spookiness ambience noises in all the rooms."""
        spooky_rating: int = int(self.lm_rando.output_data["spookiness"])
        if spooky_rating == 0:
            return

        map_two_room: JMP = self.lm_rando.map_files.get("map2").jmp_files["roominfo"]
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
        map_two_item_appear: JMP = self.lm_rando.map_files.get("map2").jmp_files["itemappeartable"]

        # Gets the list of keys already added in the item appear table
        already_exist_items: list[str] = list(set([map_two_item_appear.get_jmp_header_name_value(item_entry,
            "item0") for item_entry in map_two_item_appear.data_entries]))

        for location_type in self.lm_rando.output_data["Locations"].keys():
            for item_data in self.lm_rando.output_data["Locations"][location_type].vals():
                lm_item_name: str = get_item_name(item_data, self.lm_rando.slot)
                if not lm_item_name in already_exist_items:
                    add_new_jmp_data_entry(map_two_item_appear, create_itemappear_entry(lm_item_name))
                    already_exist_items.append(lm_item_name)


    def _map_two_boo_table_changes(self):
        """Updates boos health, speed, acceleration, anger, and time to escape rooms."""
        boo_health_choice: int = int(self.lm_rando.output_data["Options"]["boo_health_option"])
        boo_speed: int = int(self.lm_rando.output_data["Options"]["boo_speed"])
        boo_escape_time: int = int(self.lm_rando.output_data["Options"]["boo_escape_time"])
        boo_anger: int = int(self.lm_rando.output_data["Options"]["boo_anger"])
        boo_chosen_hp: int = int(self.lm_rando.output_data["Options"]["boo_health_value"])

        map_two_telesa: JMP = self.lm_rando.map_files.get("map2").jmp_files["telesa"]
        boo_hp_unit: int = 0

        if boo_health_choice == 2:
            boo_hp_unit = max([int(boo_loc["boo_sphere"]) for boo_loc in self.lm_rando.output_data["Locations"]["Boo"].vals()])
        for boo_entry in self.lm_rando.output_data["Locations"]["Boo"].vals():
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
        enable_speedy_spirits: bool = bool(self.lm_rando.output_data["Options"]["speedy_spirits"])
        map_two_teiden_observer: JMP = self.lm_rando.map_files.get("map2").jmp_files["teidenobserverinfo"]
        map_two_normal_observer: JMP = self.lm_rando.map_files.get("map2").jmp_files["observerinfo"]

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
        spawn_region_name: str = str(self.lm_rando.output_data["Options"]["spawn"])

        map_two_normal_observer: JMP = self.lm_rando.map_files.get("map2").jmp_files["observerinfo"]
        temp_new_entries: list[JMPEntry] = []

        for observer_entry in map_two_normal_observer.data_entries:
            # Allows the Toads to spawn by default.
            observer_name: str = map_two_normal_observer.get_jmp_header_name_value(observer_entry, "name")
            code_name: str = map_two_normal_observer.get_jmp_header_name_value(observer_entry, "code_name")
            room_num: int = int(map_two_normal_observer.get_jmp_header_name_value(observer_entry, "room_no"))
            curr_x_pos: float = float(map_two_normal_observer.get_jmp_header_name_value(observer_entry, "pos_x"))
            do_num: int = int(map_two_normal_observer.get_jmp_header_name_value(observer_entry, "do_type"))

            if observer_name == "kinopio":
                if code_name in ["dm_kinopio5", "dm_kinopio4", "dm_kinopio3", "dm_kinopio2"]:
                    continue
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "cond_arg0", 0)
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "appear_flag", 0)
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "cond_type", 13)

                new_entry: JMPEntry = copy.deepcopy(observer_entry)
                if not spawn_region_name in TOAD_SPAWN_LIST:
                    spawn_data = REGION_LIST[spawn_region_name]
                    map_two_normal_observer.update_jmp_header_name_value(new_entry, "room_no", spawn_data.room_id)
                    map_two_normal_observer.update_jmp_header_name_value(new_entry,"pos_y", spawn_data.pos_y)
                    map_two_normal_observer.update_jmp_header_name_value(new_entry, "pos_z", int(spawn_data.pos_z) - 150)
                    map_two_normal_observer.update_jmp_header_name_value(new_entry, "pos_x", int(spawn_data.pos_x) - 150)
                    map_two_normal_observer.update_jmp_header_name_value(new_entry, "code_name", "dm_kinopio5")
                    temp_new_entries.append(new_entry)

            # Allows the Master Bedroom to be lit after clearing it, even if Neville hasn't been caught.
            if room_num == 33:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "appear_flag", 0)

            # Allows Twins Room to be lit after clearing it, even if Chauncey hasn't been caught.
            elif room_num == 25:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "appear_flag", 0)

            # Remove locking doors behind Luigi in dark rooms to prevent soft locks
            if do_num == 11:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "do_type", 0)

            # Add CodeNames to iphone entries out of blackout
            if observer_name == "iphone" and curr_x_pos == -748.401100:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "code_name", "tel2")
            elif observer_name == "iphone" and curr_x_pos == 752.692200:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "code_name", "tel3")
            elif observer_name == "iphone" and curr_x_pos == 0.000000:
                map_two_normal_observer.update_jmp_header_name_value(observer_entry, "code_name", "tel1")

        map_two_normal_observer.data_entries += temp_new_entries

        # This one checks for the candles being lit in the Fortune-Teller's Room, flagging that key spawn
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(1870.000000, 190.000000, 140.000000,
            3, 9, 7, arg0=110))

        # This one checks for lights on in the 1F Bathroom, flagging that key spawn
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-2130.000000, 180.000000, -4550.000000,
            20, 13, 7, arg0=110))

        # This one checks for lights on in the Well, flagging that key spawn
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(590.000000, -445.000000, -5910.000000,
            69, 13, 7, arg0=110))

        # This one checks for lights on in the Wardrobe, flagging that key spawn
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-2040.000000, 760.000000, -3020.000000,
            38, 13, 7, arg0=110))

        # Turn on Flag 22 to stop Van Gogh from reloading
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2970.000000, 1550.000000, -2095.000000,
            57, 13, 7, arg0=22))

        # This one checks for lights on in the Dining Room, to prevent Luggs Respawning
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-400.000000, 420.000000, -1800.000000,
            9, 13, 7, arg0=31))

        # Adds an observer in Clairvoya's room (event36) to turn on spikes on the doors when room flag 120 is on.
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2074.000000, 100.000000, -261.000000,
            3, 18, 11, cond_arg0=120))

        # Adds an observer in Clairvoya's room (event36) to turn off spikes on the doors when room flag 120 is off.
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2074.000000, 100.000000, -261.000000,
            3, 19, 12, cond_arg0=120))

        # Adds an observer in Blackout Breaker room (event44) to turn on spikes on the doors when room flag 115 is on.
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 11, cond_arg0=115))

        # Adds an observer in Blackout Breaker room (event44) to turn off spikes on the doors when room flag 120 is on.
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(3250.000000, -500.000000, -1480.000000,
            67, 18, 12, cond_arg0=120))

        # Check that Shivers is caught to turn on Conservatory Hallway Light
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(3250.000000, 0.000000, -100.000000,
            0, 13, 7, arg0=60))

        # This one enables the Conservatory 1F hallway after catching Shivers / Butler
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(1400.000000, 0.000000, -4100.000000,
            18, 18, 1, cond_arg0=60))

        # This one adds an observer into the Foyer where if Luigi is in the room anywhere, it will turn on the lights.
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(0.000000, 0.000000, 0.000000,
            2, 15, 1))

        # This one checks for luigi entering the clockwork room, triggering the doll hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=157))

        # This one checks for luigi entering the clockwork room, triggering the doll2 hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=158))

        # This one checks for luigi entering the clockwork room, triggering the doll3 hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(10.000000, 1100.000000, -1650.000000,
            56, 15, 7, arg0=159))

        # This one checks for luigi entering the artist's room, triggering the gaka hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2890.000000, 1100.000000, -1640.000000,
            57, 15, 7, arg0=157))

        # This one checks for luigi entering the study, triggering the father hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-2440.000000, 550.000000, -2700.000000,
            34, 15, 7, arg0=157))

        # This one checks for luigi entering the master bedroom, triggering the mother hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-3760.000000, 550.000000, -1800.000000,
            33, 15, 7, arg0=157))

        # This one checks for luigi entering the nursery, triggering the baby hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-3340.000000, 550.000000, -220.000000,
            24, 15, 7, arg0=157))

        # This one checks for luigi entering the twins room, triggering the dboy hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-1820.000000, 550.000000, -220.000000,
            25, 15, 7, arg0=157))

        # This one checks for luigi entering the nanas room, triggering the nana hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(300.000000, 550.000000, -4960.000000,
            46, 15, 7, arg0=157))

        # This one checks for luigi entering the 2f bathroom, triggering the petunia hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-2100.000000, 550.000000, -4640.000000,
            45, 15, 7, arg0=157))

        # This one checks for luigi entering the guest room, triggering the girl hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(3340.000000, 550.000000, -220.000000,
            28, 15, 7, arg0=157))

        # This one checks for luigi entering the back hallway, triggering the butler hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-3600.000000, 0.000000, 150.000000,
            18, 15, 7, arg0=157))

        # This one checks for luigi entering the dining room, triggering the luggs hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-280.000000, 0.000000, -1480.000000,
            9, 15, 7, arg0=157))

        # This one checks for luigi entering the ballroom, triggering the dancer hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2540.000000, 0.000000, -2800.000000,
            10, 15, 7, arg0=157))

        # This one checks for luigi entering the billiard room, triggering the hustler hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-1200.000000, 0.000000, -3840.000000,
            12, 15, 7, arg0=157))

        # This one checks for luigi entering the conservatory, triggering the pianist hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(1360.000000, 0.000000, -4920.000000,
            21, 15, 7, arg0=157))

        # This one checks for luigi entering the rec room, triggering the builder hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(2840.000000, 0.000000, -4940.000000,
            22, 15, 7, arg0=157))

        # This one checks for luigi entering the boneyard, triggering the dog hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(-3360.000000, 0.000000, -3080.000000,
            11, 15, 7, arg0=157))

        # This one checks for luigi entering the cold storage, triggering the snowman hint
        add_new_jmp_data_entry(map_two_normal_observer, create_observer_entry(1180.000000, -445.000000, -690.000000,
            61, 15, 7, arg0=157))


    def _map_two_enemy_changes(self):
        """Handles changes to enemy table for both normal and blackout."""
        map_two_teiden_enemy: JMP = self.lm_rando.map_files.get("map2").jmp_files["teidenenemyinfo"]
        map_two_normal_enemy: JMP = self.lm_rando.map_files.get("map2").jmp_files["enemyinfo"]

        for entry_no in SPEEDY_ENEMY_INDEX:
            speedy_entry: JMPEntry = map_two_normal_enemy.data_entries[entry_no]
            map_two_teiden_enemy.data_entries.append(speedy_entry)
            map_two_normal_enemy.data_entries.remove(speedy_entry)

        # If randomize ghosts options are enabled
        if self.lm_rando.output_data["Options"]["enemizer"] == 0:
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
                curr_room_no: int = int(map_two_normal_enemy.get_jmp_header_name_value(blackout_enemy, "room_no"))
                curr_enemy_name: str = map_two_normal_enemy.get_jmp_header_name_value(blackout_enemy, "name")
                if curr_room_no != room_id or not curr_enemy_name in GHOST_LIST:
                    continue
                apply_new_ghost(self.lm_rando, map_two_teiden_enemy, blackout_enemy, val)


    def _map_two_event_changes(self):
        # Removes events that we don't want to trigger at all in the mansion, such as some E. Gadd calls, warps after
        # boss battles / grabbing boss keys, and various cutscenes etc. Also remove Mario Items/Elemental Item events
        events_to_remove: list[int] = [7, 9, 15, 18, 19, 20, 21, 31, 41, 42, 45, 47, 51, 54, 69, 70, 73, 80, 81, 85, 91]
        map_two_events: JMP = self.lm_rando.map_files.get("map2").jmp_files["eventinfo"]

        boo_checks: bool = bool(self.lm_rando.output_data["Options"]["boo_gates"])
        spawn_area: str = self.lm_rando.output_data["Options"]["spawn"]

        # Only remove the boo checks if the player does not want them.
        if not boo_checks:
            events_to_remove += [16, 96]
        if spawn_area in TOAD_SPAWN_LIST:
            events_to_remove += [12]

        map_two_events.data_entries = [event_entry for event_entry in map_two_events.data_entries
            if not map_two_events.get_jmp_header_name_value(event_entry, "EventNo") in events_to_remove
            or (int(map_two_events.get_jmp_header_name_value(event_entry, "EventNo")) == 93 and
            float(map_two_events.get_jmp_header_name_value(event_entry, "pos_x")) == 0.000000)]

        spawn_data = REGION_LIST[spawn_area]

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
            elif boo_checks and event_num == 16:
                map_two_events.update_jmp_header_name_value(event_info, "EventIf", 5)
                map_two_events.update_jmp_header_name_value(event_info, "EventArea", 200)
                map_two_events.update_jmp_header_name_value(event_info, "EventLock", 1)
                map_two_events.update_jmp_header_name_value(event_info, "PlayerStop", 1)
                map_two_events.update_jmp_header_name_value(event_info, "EventLoad", 0)
                map_two_events.update_jmp_header_name_value(event_info, "pos_x", 2260.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_y", -450.000000)
                map_two_events.update_jmp_header_name_value(event_info, "pos_z", -5300.000000)

            # Update the Balcony Boo event trigger to be area entry based
            elif boo_checks and event_num == 96:
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
                map_two_events.update_jmp_header_name_value(event_info, "room_no", spawn_data.room_id)
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