import re
from io import BytesIO

from gclib.gcm import GCM
from gclib.yaz0_yay0 import Yay0

from ..Locations import FLIP_BALCONY_BOO_EVENT_LIST
from ..Helper_Functions import get_arc, PROJECT_ROOT
from ..Hints import ALWAYS_HINT, PORTRAIT_HINTS
from CommonClient import logger

from .LM_Randomize_ISO import LuigisMansionRandomizer



class EventChanges:

    lm_rando: LuigisMansionRandomizer = None
    hint_dist: int = None
    luigi_max_hp: str = None
    hint_list: dict[str, dict[str, str]] = None


    def __init__(self, rando_obj: LuigisMansionRandomizer):
        self.lm_rando = rando_obj
        self.hint_dist = int(self.lm_rando.output_data["Options"]["hint_distribution"])
        self.luigi_max_hp = str(self.lm_rando.output_data["Options"]["luigi_max_health"])
        self.hint_list = self.lm_rando.output_data["Hints"]


    def update_in_game_events(self):
        self.lm_rando.client_logger.info("Now updating all in-game events of various types...")
        self._update_common_events()
        self._update_intro_and_lab_events()
        self._update_boo_gates()
        self._update_blackout_event()
        self._randomize_clairvoya()
        self._write_in_game_hints()
        self._update_spawn_event()
        self._write_portrait_hints()
        self._randomize_music()


    def _update_common_events(self):
        """Updates all the common events to have their custom event text."""
        self.lm_rando.client_logger.info("Updating all of the common events with the customized version.")
        bool_randomize_mice: bool = bool(self.lm_rando.output_data["Options"]["gold_mice"])
        bool_start_vacuum: bool = bool(self.lm_rando.output_data["Options"]["vacuum_start"])

        list_custom_events = ["03", "10", "13", "22", "23", "24", "29", "33", "35", "37", "38", "50", "61", "64",
                              "65", "66", "67", "68", "71", "72", "74", "75", "82", "86", "87", "88", "89", "90"]
        if bool_randomize_mice:
            list_custom_events += ["95", "97", "98", "99", "100"]

        for custom_event in list_custom_events:
            lines = _read_custom_file("txt", "event" + custom_event + ".txt")
            if custom_event == "10" and not bool_start_vacuum:
                lines = lines.replace("<WEAPON>", "<NOWEAPON>")
            _update_custom_event(self.lm_rando.lm_gcm, custom_event, True, lines, None)


    def _update_intro_and_lab_events(self):
        """# Update the intro event and E. Gadd event as needed, including the Gallery map."""
        start_inv_list: list[str] = list(self.lm_rando.output_data["Options"]["start_inventory"])
        bool_start_vacuum: bool = bool(self.lm_rando.output_data["Options"]["vacuum_start"])
        bool_hidden_mansion: bool = bool(self.lm_rando.output_data["Options"]["hidden_mansion"])
        bool_start_boo_radar: bool = not bool(self.lm_rando.output_data["Options"]["boo_radar"])
        doors_to_close: dict[int, int] = dict(self.lm_rando.output_data["Entrances"])

        self.lm_rando.client_logger.info("Updating the Gallery event with the customized version.")
        lines = _read_custom_file("txt", "event28.txt")
        csv_lines = _read_custom_file("csv", "message28.csv")
        _update_custom_event(self.lm_rando.lm_gcm, "28", True, lines, csv_lines)

        self.lm_rando.client_logger.info("Updating the E. Gadd's lab event with the customized version.")
        lines = _read_custom_file("txt", "event08.txt")
        lines = lines.replace("{LUIGIMAXHP}", self.luigi_max_hp)
        csv_lines = _read_custom_file("csv", "message8.csv")
        _update_custom_event(self.lm_rando.lm_gcm, "08", True, lines, csv_lines)

        self.lm_rando.client_logger.info("Updating the main intro event with the customized version.")
        lines = _read_custom_file("txt", "event48.txt")
        lines = lines.replace("{MANSION_TYPE}", "<URALUIGI>" if bool_hidden_mansion else "<OMOTELUIGI>")
        if not bool_start_vacuum:
            lines = lines.replace("{WEAPON}", "<NOWEAPON>")
            lines = lines.replace("{VacStartFlag}", "<FLAGOFF>(82)")
        else:
            lines = lines.replace("{WEAPON}", "<WEAPON>")
            lines = lines.replace("{VacStartFlag}", "<FLAGON>(82)")

        include_radar = ""
        if any("Boo Radar" in key for key in start_inv_list) or bool_start_boo_radar:
            include_radar = "<FLAGON>(73)\r\n<FLAGON>(75)"
        lines = lines.replace("{BOO RADAR}", include_radar)

        event_door_list: list[str] = []

        for event_door in doors_to_close:
            event_door_list.append(("<KEYLOCK>" if doors_to_close.get(event_door) == 0 else "<KEYUNLOCK>") + f"({event_door})\r\n")

        lines = lines.replace("{DOOR_LIST}", ''.join(event_door_list))
        lines = lines.replace("{LUIGIMAXHP}", self.luigi_max_hp)

        _update_custom_event(self.lm_rando.lm_gcm, "48", False, lines, None)


    def _update_boo_gates(self):
        """Updates the boo gates events to ensure they have proper counts/triggers."""
        boo_gates_enabled: bool = bool(self.lm_rando.output_data["Options"]["boo_gates"])
        boosanity_enabled: bool = bool(self.lm_rando.output_data["Options"]["boosanity"])
        balcony_boo_count: int = int(self.lm_rando.output_data["Options"]["balcony_boo_count"])
        final_boo_count: int = int(self.lm_rando.output_data["Options"]["final_boo_count"])
        spawn_area: str = self.lm_rando.output_data["Options"]["spawn"]
        if not boo_gates_enabled:
            return

        self.lm_rando.client_logger.info("Boo Gates was enabled, updating all of the common events with the customized version.")
        boo_list_events = ["16", "96"]
        for event_no in boo_list_events:
            lines = _read_custom_file("txt", "event" + event_no + ".txt")

            if event_no == "96":
                req_boo_count = final_boo_count
            else:
                req_boo_count = balcony_boo_count
                str_move_type = "MOVEOUTSIDE" if spawn_area in FLIP_BALCONY_BOO_EVENT_LIST else "MOVEINSIDE"
                lines = lines.replace("{MoveType}", str_move_type)

            if req_boo_count == 0:
                continue

            if boosanity_enabled:
                str_begin_case = "not_enough"
                lines = lines.replace("{Count0}", str(0)).replace("{Count1}", str(0))
                lines = lines.replace("{Count2}", str(0)).replace("{Count3}", str(0))
                lines = lines.replace("{Count4}", str(req_boo_count)).replace("{CaseBegin}", str_begin_case)
                _update_custom_event(self.lm_rando.lm_gcm, event_no, True, lines, None)
                return

            str_begin_case = "CheckBoos"
            lines = lines.replace("{CaseBegin}", str_begin_case)

            str_not_enough = "not_enough"
            str_boo_captured = "boos_captured"
            match req_boo_count:
                case 1:
                    lines = lines.replace("{Count0}", "0")
                    lines = lines.replace("{Count1}", str(req_boo_count))
                    lines = lines.replace("{Count2}", str(req_boo_count))
                    lines = lines.replace("{Count3}", str(req_boo_count))
                    lines = lines.replace("{Count4}", str(req_boo_count))
                    lines = lines.replace("{Case0}", str_not_enough)
                    lines = lines.replace("{Case1}", str_boo_captured)
                    lines = lines.replace("{Case2}", str_boo_captured)
                    lines = lines.replace("{Case3}", str_boo_captured)
                    lines = lines.replace("{Case4}", str_boo_captured)
                case 2:
                    lines = lines.replace("{Count0}", "0")
                    lines = lines.replace("{Count1}", "1")
                    lines = lines.replace("{Count2}", str(req_boo_count))
                    lines = lines.replace("{Count3}", str(req_boo_count))
                    lines = lines.replace("{Count4}", str(req_boo_count))
                    lines = lines.replace("{Case0}", str_not_enough)
                    lines = lines.replace("{Case1}", str_not_enough)
                    lines = lines.replace("{Case2}", str_boo_captured)
                    lines = lines.replace("{Case3}", str_boo_captured)
                    lines = lines.replace("{Case4}", str_boo_captured)
                case 3:
                    lines = lines.replace("{Count0}", "0")
                    lines = lines.replace("{Count1}", "1")
                    lines = lines.replace("{Count2}", "2")
                    lines = lines.replace("{Count3}", str(req_boo_count))
                    lines = lines.replace("{Count4}", str(req_boo_count))
                    lines = lines.replace("{Case0}", str_not_enough)
                    lines = lines.replace("{Case1}", str_not_enough)
                    lines = lines.replace("{Case2}", str_not_enough)
                    lines = lines.replace("{Case3}", str_boo_captured)
                    lines = lines.replace("{Case4}", str_boo_captured)
                case _:
                    lines = lines.replace("{Count0}", str(req_boo_count - 4))
                    lines = lines.replace("{Count1}", str(req_boo_count - 3))
                    lines = lines.replace("{Count2}", str(req_boo_count - 2))
                    lines = lines.replace("{Count3}", str(req_boo_count - 1))
                    lines = lines.replace("{Count4}", str(req_boo_count))
                    lines = lines.replace("{Case0}", str_not_enough)
                    lines = lines.replace("{Case1}", str_not_enough)
                    lines = lines.replace("{Case2}", str_not_enough)
                    lines = lines.replace("{Case3}", str_not_enough)
                    lines = lines.replace("{Case4}", str_boo_captured)

            _update_custom_event(self.lm_rando.lm_gcm, event_no, True, lines, None)


    def _update_blackout_event(self):
        """Updates the event txt and csv for the blackout."""
        self.lm_rando.client_logger.info("Updating the blackout event with the customized version.")
        lines = _read_custom_file("txt", "event44.txt")
        csv_lines = _read_custom_file("csv", "message44.csv")
        _update_custom_event(self.lm_rando.lm_gcm, "44", True, lines, csv_lines)


    def _randomize_clairvoya(self):
        """Updates clairvoya's hints and mario item information based on the options selected."""
        self.lm_rando.client_logger.info("Updating Clairvoya's event with the customized version.")
        req_mario_count: int = int(self.lm_rando.output_data["Options"]["mario_items"])
        madame_hint: dict[str, str] = self.hint_list["Madame Clairvoya"] if "Madame Clairvoya" in self.hint_list else None

        lines = _read_custom_file("txt", "event36.txt")
        csv_lines = _read_custom_file("csv", "message36.csv")
        case_type = None
        item_color = None

        match self.hint_dist:
            case 4:
                match madame_hint["Class"]:
                    case "Prog":
                        item_color = "5"
                    case "Trap":
                        item_color = "2"
                    case _:
                        item_color = "6"
                csv_lines = csv_lines.replace("{RecPlayer}", madame_hint["Rec Player"])
                csv_lines = csv_lines.replace("{ItemColor}", item_color)
                csv_lines = csv_lines.replace("{ItemName}", madame_hint["Item"])
                csv_lines = csv_lines.replace("{SendPlayer}", madame_hint["Send Player"])
                csv_lines = csv_lines.replace("{WorldOrLoc}", madame_hint["Game"])
                case_type = "VagueHint"
            case 5:
                case_type = "DisabledHint"
            case 1:
                jokes = PROJECT_ROOT.joinpath('data', 'jokes.txt').read_text(encoding="utf-8")
                joke_hint = self.lm_rando.random.choice(sorted(str.splitlines(jokes)))
                csv_lines = csv_lines.replace("{JokeText}", joke_hint)
                case_type = "JokeHint"
            case _:
                match madame_hint["Class"]:
                    case "Prog":
                        item_color = "5"
                    case "Trap":
                        item_color = "2"
                    case _:
                        item_color = "6"
                csv_lines = csv_lines.replace("{RecPlayer}", madame_hint["Rec Player"])
                csv_lines = csv_lines.replace("{ItemColor}", item_color)
                csv_lines = csv_lines.replace("{ItemName}", madame_hint["Item"])
                csv_lines = csv_lines.replace("{SendPlayer}", madame_hint["Send Player"])
                csv_lines = csv_lines.replace("{WorldOrLoc}", madame_hint["Location"])
                case_type = "SpecificHint"

        csv_lines = csv_lines.replace("{MarioCount}", str(req_mario_count))
        csv_lines = csv_lines.replace("{BreakHere}", "\n")
        lines = lines.replace("{HintType}", case_type)

        cases_to_replace = ["{CaseZero}", "{CaseOne}", "{CaseTwo}", "{CaseThree}", "{CaseFour}", "{CaseFive}"]
        str_good_end = "GoodEnd"
        str_bad_end = "MissingItems"

        for i in range(0, 6):
            if i >= req_mario_count:
                lines = lines.replace(cases_to_replace[i], str_good_end)
            else:
                lines = lines.replace(cases_to_replace[i], str_bad_end)

        _update_custom_event(self.lm_rando.lm_gcm, "36", True, lines, csv_lines)


    def _write_in_game_hints(self):
        """Writes all the in game hints for everything except clairvoya"""
        self.lm_rando.client_logger.info("Updating common events with the generated in-game hints.")
        hint_data: dict[str, str] = {}

        # Add new event and csv to our special spawn toad
        lines = _read_custom_file("txt", "event12.txt")
        csv_lines = _read_custom_file("csv", "message12.csv")
        lines = lines.replace("{LUIGIMAXHP}", self.luigi_max_hp)
        _update_custom_event(self.lm_rando.lm_gcm, "12", True, lines, csv_lines)

        # Add various hints to their specific hint spots
        item_color = None
        case_type = None
        for hint_name in ALWAYS_HINT.keys():
            if hint_name == "Madame Clairvoya":
                continue
            event_no: int = 0
            match hint_name:
                case "Courtyard Toad":
                    event_no = 4
                case "Foyer Toad":
                    event_no = 17
                case "Wardrobe Balcony Toad":
                    event_no = 32
                case "1F Washroom Toad":
                    event_no = 63
                case "Center Telephone":
                    event_no = 92
                case "Left Telephone":
                    event_no = 93
                case "Right Telephone":
                    event_no = 94
            if self.hint_dist != 1 and self.hint_dist != 5:
                hint_data = self.hint_list[hint_name]

            if event_no == 4:
                lines = _read_custom_file("txt", "event04.txt")
            else:
                lines = _read_custom_file("txt", "event" + str(event_no) + ".txt")
            csv_lines = _read_custom_file("csv", "message" + str(event_no) + ".csv")

            match self.hint_dist:
                case 4:
                    match hint_data["Class"]:
                        case "Prog":
                            item_color = "5"
                        case "Trap":
                            item_color = "2"
                        case _:
                            item_color = "6"
                    csv_lines = csv_lines.replace("{RecPlayer}", hint_data["Rec Player"])
                    csv_lines = csv_lines.replace("{ItemColor}", item_color)
                    csv_lines = csv_lines.replace("{ItemName}", hint_data["Item"])
                    csv_lines = csv_lines.replace("{SendPlayer}", hint_data["Send Player"])
                    csv_lines = csv_lines.replace("{WorldOrLoc}", hint_data["Game"])
                    case_type = "VagueHint"
                case 5:
                    case_type = "DisabledHint"
                case 1:
                    jokes = PROJECT_ROOT.joinpath('data', 'jokes.txt').read_text(encoding="utf-8")
                    joke_hint = self.lm_rando.random.choice(sorted(str.splitlines(jokes)))
                    csv_lines = csv_lines.replace("{JokeText}", joke_hint)
                    case_type = "JokeHint"
                case _:
                    match hint_data["Class"]:
                        case "Prog":
                            item_color = "5"
                        case "Trap":
                            item_color = "2"
                        case _:
                            item_color = "6"
                    csv_lines = csv_lines.replace("{RecPlayer}", hint_data["Rec Player"])
                    csv_lines = csv_lines.replace("{ItemColor}", item_color)
                    csv_lines = csv_lines.replace("{ItemName}", hint_data["Item"])
                    csv_lines = csv_lines.replace("{SendPlayer}", hint_data["Send Player"])
                    csv_lines = csv_lines.replace("{WorldOrLoc}", hint_data["Location"])
                    case_type = "SpecificHint"

            csv_lines = csv_lines.replace("{BreakHere}", "\n")
            lines = lines.replace("{HintType}", case_type)
            if event_no in (4, 17, 32, 63):
                lines = lines.replace("{LUIGIMAXHP}", self.luigi_max_hp)

            if event_no == 4:
                _update_custom_event(self.lm_rando.lm_gcm, "04", True, lines, csv_lines)
            else:
                _update_custom_event(self.lm_rando.lm_gcm, str(event_no), True, lines, csv_lines)


    def _update_spawn_event(self):
        """Adds and updates the new custom spawn event"""
        self.lm_rando.client_logger.info("Updating the spawn event...")
        lines = _read_custom_file("txt", "event11.txt")
        _update_custom_event(self.lm_rando.lm_gcm, "11", True, lines, None)


    def _write_portrait_hints(self):
        """Updates all portrait ghost hints, if the option is turned on."""
        bool_portrait_hints: bool = bool(self.lm_rando.output_data["Options"]["portrait_hints"])
        if not bool_portrait_hints:
            return

        self.lm_rando.client_logger.info("Portrait Hints are enabled, updating portrait ghost hearts with the generated in-game hints.")
        csv_lines = _read_custom_file("csv", "message78.csv")
        item_color = None

        if self.hint_dist == 1:
            for portrait_name in PORTRAIT_HINTS.keys():
                jokes = PROJECT_ROOT.joinpath('data', 'jokes.txt').read_text(encoding="utf-8")
                joke_hint = self.lm_rando.random.choice(sorted(str.splitlines(jokes))).replace("{BreakHere}", "\n")
                csv_lines = csv_lines.replace(f"{portrait_name}", joke_hint)
        else:
            for portrait_name, portrait_hint in self.hint_list.items():
                if portrait_name not in PORTRAIT_HINTS.keys():
                    continue
                match self.hint_dist:
                    case 4:
                        match portrait_hint["Class"]:
                            case "Prog":
                                item_color = "5"
                            case "Trap":
                                item_color = "2"
                            case _:
                                item_color = "6"
                        hintfo = (portrait_hint["Rec Player"] + "'s \n<COLOR>(" + item_color + ") " + portrait_hint[
                            "Item"] +
                                  "\n<COLOR>(0) is somewhere in \n<COLOR>(3)" + portrait_hint["Send Player"] + "'s \n" +
                                  portrait_hint["Game"])
                        csv_lines = csv_lines.replace(f"{portrait_name}", hintfo)
                    case _:
                        match portrait_hint["Class"]:
                            case "Prog":
                                item_color = "5"
                            case "Trap":
                                item_color = "2"
                            case _:
                                item_color = "6"
                        hintfo = (portrait_hint["Rec Player"] + "'s \n<COLOR>(" + item_color + ")" + portrait_hint[
                            "Item"] +
                                  "\n<COLOR>(0) can be found at \n<COLOR>(1)" + portrait_hint["Send Player"] + "'s \n" +
                                  portrait_hint["Location"])
                        csv_lines = csv_lines.replace(f"{portrait_name}", hintfo)

        _update_custom_event(self.lm_rando.lm_gcm, "78", True, None, csv_lines)


    def _randomize_music(self):
        """Randomizes all the music in all the event.txt files."""
        bool_randomize_music: bool = bool(self.lm_rando.output_data["Options"]["random_music"])
        if not bool_randomize_music:
            return

        self.lm_rando.client_logger.info("Randomized Music is enabled, updating all events with various in-game music.")
        list_ignore_events = ["event00.szp"]
        event_dir = self.lm_rando.lm_gcm.get_or_create_dir_file_entry("files/Event")

        for lm_event in [event_file for event_file in event_dir.children if not event_file.is_dir]:
            if lm_event.name in list_ignore_events or not re.match(r"event\d+\.szp", lm_event.name):
                continue

            event_arc = get_arc(self.lm_rando.lm_gcm, lm_event.file_path)
            name_to_find = lm_event.name.replace(".szp", ".txt")

            if not any(event_file for event_file in event_arc.file_entries if event_file.name == name_to_find):
                continue

            event_text_data = next(event_file for event_file in event_arc.file_entries if
                                    event_file.name == name_to_find).data
            event_str = event_text_data.getvalue().decode('utf-8', errors='replace')
            music_to_replace = re.findall(r'<BGM>\(\d+\)', event_str)

            if music_to_replace:
                for music_match in music_to_replace:
                    list_of_bad_music: list[int] = [13, 17, 21, 24, 28, 41]
                    music_list: list[int] = [i for i in range(0, 53) if i not in list_of_bad_music]
                    int_music_selection: int = self.lm_rando.random.choice(sorted(music_list))
                    event_str = event_str.replace(music_match, "<BGM>(" + str(int_music_selection) + ")")

            updated_event = BytesIO(event_str.encode('utf-8'))

            next(event_file for event_file in event_arc.file_entries if
                 event_file.name == name_to_find).data = updated_event

            event_arc.save_changes()
            logger.info("Randomize music Yay0 check...")
            self.lm_rando.lm_gcm.changed_files[lm_event.file_path] = Yay0.compress(event_arc.data)


# Using the provided txt or csv lines for a given event file, updates the actual szp file in memory with this data.
def _update_custom_event(gcm: GCM, event_number: str, delete_all_other_files: bool,
    event_txt=None, event_csv=None):
    if not event_txt and not event_csv:
        raise Exception("Cannot have both the event text and csv text be null/empty.")

    custom_event = get_arc(gcm, "files/Event/event" + event_number + ".szp")
    event_txt_file = "event" + event_number + ".txt"
    event_csv_file = "message" + (event_number if not event_number.startswith("0") else event_number[1:]) + ".csv"

    if event_txt:
        if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_txt_file):
            raise Exception(f"Unable to find an info file with name '{event_txt_file}' in provided RARC file.")
        next((info_files for info_files in custom_event.file_entries if
              info_files.name == event_txt_file)).data = BytesIO(event_txt.encode('utf-8'))

    if event_csv:
        if not any(info_files for info_files in custom_event.file_entries if info_files.name == event_csv_file):
            raise Exception(f"Unable to find an info file with name '{event_csv_file}' in provided RARC file.")
        next((info_files for info_files in custom_event.file_entries if
              info_files.name == event_csv_file)).data = BytesIO(event_csv.encode('utf-8'))

    if delete_all_other_files:
        files_to_keep: list[str] = [event_txt_file, ".", ".."]
        if event_csv:
            files_to_keep += [event_csv_file]

        node_list = list(reversed([node for node in custom_event.nodes[1:]]))
        for node in node_list:
            node_files: list[str] = [rarc_file.name for rarc_file in node.files]
            files_to_delete: list[str] = list(set(node_files) - (set(files_to_keep)))
            node_files_left_after_delete: list[str] = list(set(node_files) - (set(files_to_delete)))
            if not len(files_to_delete):
                continue

            # If there is only the current directory entry / parent directory entry left, delete the directory.
            # Note: Removing the directory automatically removes the file entries as well.
            elif set(node_files_left_after_delete).issubset({".", ".."}):
                custom_event.delete_directory(node.dir_entry)
                continue

            # Assuming there will always be at least one file to delete in this node, but other files remain.
            for node_file in node.files:
                if node_file.name in files_to_delete:
                    custom_event.delete_file(node_file)

    logger.info(f"Event{event_number} Yay0 check...")
    custom_event.save_changes()
    gcm.changed_files["files/Event/event" + event_number + ".szp"] = Yay0.compress(custom_event.data)

def _read_custom_file(file_type: str, file_name: str) -> str:
    """
    Reads the provided file name from its provided sub_folder type and loads it as a txt file.

    :param file_type: Indicates which sub-folder in data to retrieve the file.
    :param file_name: Reads the provided file name in the sub-folder and decodes it via UTF-8
    """
    file_data = None

    match file_type:
        case "csv":
            file_data = PROJECT_ROOT.joinpath('data', "custom_csvs", file_name).read_text(encoding='utf-8').replace("\n", "\r\n")
        case "txt":
            file_data = PROJECT_ROOT.joinpath('data', "custom_events", file_name).read_text(encoding='utf-8')
        case _:
            raise Exception(f"Unhandled custom type provided: {file_type}")

    return file_data