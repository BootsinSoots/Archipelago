from gcbrickwork.JMP import JMP, JMPEntry
from JMP_Entry_Helpers import LOCATION_TO_INDEX, get_item_name
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
        already_added_keys: list[str] = []
        hp_item_names: dict[str, int] = {"sheart": 20, "lheart": 50}
        map_two_info: JMP = self.lm_rando.map_files.get("map2").jmp_files["iteminfotable"]

        for info_entry in map_two_info.data_entries:
            item_name: str = map_two_info.get_jmp_header_name_value(info_entry, "name")
            if map_two_info.get_jmp_header_name_value(info_entry, "name") in hp_item_names.keys():
                map_two_info.update_jmp_header_name_value(info_entry, "name", hp_item_names[item_name])
            elif item_name.startswith("key_") and not item_name in already_added_keys:
                already_added_keys.append(item_name)

        # Get all the keys to add from the location data if door_id is greater than 0 AND
        # item is for current player.
        items_to_add: list[str] = ["key_" + str(item_data["door_id"]) for item_name, item_data in
            self.lm_rando.output_data["Locations"].items() if (int(item_data["door_id"]) > 0 and
            self.lm_rando.slot == int(item_data[item_data["player"]]))]
        items_to_add += ["rdiamond", "itembomb", "ice", "mstar", "banana", "diamond", "gameboy", "vbody"]

        for new_item in items_to_add:
            pass
            # TODO need to make a keyword function of some sort then add items appropriately to the data entry.


    def _map_two_key_info_changes(self):
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
