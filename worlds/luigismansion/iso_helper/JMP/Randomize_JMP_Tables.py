from gcbrickwork.JMP import JMP, JMPEntry

from JMP_Entry_Helpers import LOCATION_TO_INDEX, get_item_name, create_iteminfo_entry, add_new_jmp_data_entry, create_itemappear_entry

from ..LM_Randomize_ISO import LuigisMansionRandomizer


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
        bad_objects_to_remove = ["eldoor07", "eldoor08", "eldoor09", "eldoor10"]
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
