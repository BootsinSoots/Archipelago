import copy
from importlib.resources.abc import Traversable
from typing import NamedTuple, Optional, TYPE_CHECKING
import importlib.resources as resources
import re

if TYPE_CHECKING:
    from gclib.rarc import RARCFileEntry, RARC, RARCNode
    from gclib.gcm import GCM

PROJECT_ROOT: Traversable = resources.files("worlds.luigismansion")

IGNORE_RARC_NAMES: list[str] = [".", ".."]
RARC_FILE_STR_ENCODING: str = "shift_jis"
EVENT_FILE_STR_ENCODING: str = "utf-8"

class LMRamData(NamedTuple):
    ram_addr: Optional[int] = None
    bit_position: Optional[int] = None
    ram_byte_size: Optional[int] = None
    pointer_offset: Optional[int] = None
    in_game_room_id: Optional[int] = None
    item_count: Optional[int] = None


def string_to_bytes(user_string: str, encoded_byte_length: int | None = None) -> bytes:
    """
    Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
    If provided string is longer than expected length, raise an exception

    :param user_string: String that needs to be encoded to bytes.
    :param encoded_byte_length: Expected length of the provided string.
    """
    encoded_string = user_string.encode('utf-8')
    if encoded_byte_length is None:
        encoded_byte_length = len(encoded_string)

    if len(encoded_string) < encoded_byte_length:
        encoded_string += b'\x00' * (encoded_byte_length - len(encoded_string))
    elif len(encoded_string) > encoded_byte_length:
        raise Exception("Provided string '" + user_string + "' was longer than the expected byte length of '" +
                        str(encoded_byte_length) + "', which will not be accepted by the info file.")

    return encoded_string


def byte_string_strip(bytes_input: bytes):
    """
    Strips the un-necessary padding / bytes that are not a part of the core string.

    :param bytes_input: User provided byte array, which will convert to string.
    """
    result = []

    for single_byte in bytes_input:
        if single_byte < 32 or single_byte > 127:
            break
        result.append(chr(single_byte))

    return ''.join(result)


def byte_string_strip_null_terminator(bytes_input: bytes):
    return bytes_input.decode().strip("\0")



def find_rarc_file_entry(rarc_file: "RARC", directory_name: str, name_of_file: str) -> "RARCFileEntry | None":
    """Gets a file/if its from a specific directory."""
    for file_entry in rarc_file.file_entries:
      if file_entry.name == name_of_file and file_entry.parent_node.name == directory_name:
        return file_entry
    return None


def get_arc(gcm: "GCM", arc_path) -> "RARC":
    """Get an ARC / RARC / SZP file from within the ISO / ROM"""
    from gclib.rarc import RARC
    arc_path = arc_path.replace("\\", "/")
    if arc_path in gcm.changed_files:
        arc = RARC(gcm.get_changed_file_data(arc_path))
    else:
        arc = RARC(gcm.read_file_data(arc_path))  # Automatically decompresses Yay0
    arc.read()
    return arc


def read_custom_file(file_type: str, file_name: str) -> str:
    """
    Reads the provided file name from its provided sub_folder type and loads it as a txt file.

    :param file_type: Indicates which sub-folder in data to retrieve the file.
    :param file_name: Reads the provided file name in the sub-folder and decodes it via UTF-8
    """
    file_data = None

    match file_type:
        case "csv":
            file_data = (PROJECT_ROOT.joinpath('data', "custom_csvs", file_name)
                .read_text(encoding='utf-8').replace("\n", "\r\n"))
        case "txt":
            file_data = (PROJECT_ROOT.joinpath('data', "custom_events", file_name)
                .read_text(encoding='utf-8'))
        case _:
            raise Exception(f"Unhandled custom type provided: {file_type}")

    return file_data


def is_rarc_node_empty(rarc_node: "RARCNode", files_to_be_removed: list[str]=None) -> bool:
    """Checks if a given rarc now has any files left in it. Optionally checks a list of files that will be removed in the future."""
    assert rarc_node.name not in IGNORE_RARC_NAMES
    assert rarc_node is not None

    # If there are no files in this node, this node is empty
    if len(rarc_node.files) == 0:
        return True

    future_removed_files: list[str] = files_to_be_removed if not None else []
    return set([nfile.name for nfile in rarc_node.files if nfile.name not in future_removed_files]).issubset(set(IGNORE_RARC_NAMES))


class LMDynamicAddresses:

    dynamic_addresses: dict


    def __init__(self):
        self.dynamic_addresses = {}
        self._parse_custom_map()


    def _parse_custom_map(self):
        """Parses the list of custom addresses that go along with the custom code provided. A lot of names / functions
        are not relevant to the APWorld itself so we only care about the name_list provided."""
        custom_address_list: list[str] = (PROJECT_ROOT.joinpath("iso_helper").joinpath("dol")
            .joinpath("Custom_Addresses.map").read_text(encoding="utf-8").lstrip().rstrip().splitlines())

        for custom_line in custom_address_list:
            if custom_line.rstrip() == "" or custom_line.lstrip().lower().startswith(".text"):  # Ignore any whitespace lines.
                continue
            csv_line: list[str] = re.sub(r"[\s ]+", ",", custom_line, 0, flags=0).split(",")

            updated_addr: str = csv_line[1].replace("0x", "")
            self.dynamic_addresses[csv_line[2]] = updated_addr


    def update_item_addresses(self):
        # Call the custom address parser to get the dynamically changing addresses for several functions.
        # Since calling the unpacking operator (**) on a dict creates a shallow copy, all copies will have their updated values.
        from .Items import ALL_ITEMS_TABLE, trap_filler_items, BOO_ITEM_TABLE

        for custom_name, custom_addr in self.dynamic_addresses.items():
            converted_addr: int = int(custom_addr, 16)
            match custom_name:
                case "Generate_Ghost":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Ghost"].update_ram_addr[0]
                    LMRamData(converted_addr, curr_ram_data.bit_position, curr_ram_data.ram_byte_size,
                        curr_ram_data.pointer_offset, curr_ram_data.in_game_room_id, curr_ram_data.item_count)
                    ALL_ITEMS_TABLE["Ghost"].update_ram_addr[0] = LMRamData(converted_addr, curr_ram_data.bit_position,
                        curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "Player_Reaction":
                    for trap_name in trap_filler_items.keys():
                        if trap_name in ["Ghost", "Spooky Time"]:
                            continue

                        curr_ram_data: LMRamData = ALL_ITEMS_TABLE[trap_name].update_ram_addr[0]
                        ALL_ITEMS_TABLE[trap_name].update_ram_addr[0] = LMRamData(converted_addr,
                            curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                            curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "Monochrome_Trap_Timer":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Spooky Time"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["Spooky Time"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "GC2D_read_Boo_Counter_Bitfields":
                    for boo_idx, boo_name in enumerate(BOO_ITEM_TABLE.keys(), 0):
                        curr_ram_data: LMRamData = ALL_ITEMS_TABLE[boo_name].update_ram_addr[0]
                        boo_addr = copy.deepcopy(converted_addr) + int(boo_idx/8)
                        ALL_ITEMS_TABLE[boo_name].update_ram_addr[0] = LMRamData(boo_addr,
                            curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                            curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "Weapon_Action":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Poltergust 3000"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["Poltergust 3000"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "gTsuri_Speed":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Vacuum Upgrade"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["Vacuum Upgrade"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "gPlayer_Is_Training_Trap":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Tutorial Trap"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["Tutorial Trap"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "gPlayer_Is_Movie_Trap":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["Pikmin Trap"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["Pikmin Trap"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)

                case "gPlayer_First_Person_Trap_Timer":
                    curr_ram_data: LMRamData = ALL_ITEMS_TABLE["First Person Trap"].update_ram_addr[0]
                    ALL_ITEMS_TABLE["First Person Trap"].update_ram_addr[0] = LMRamData(converted_addr,
                        curr_ram_data.bit_position, curr_ram_data.ram_byte_size, curr_ram_data.pointer_offset,
                        curr_ram_data.in_game_room_id, curr_ram_data.item_count)


        for item_name, item_data in ALL_ITEMS_TABLE.items():
            for ram_details in item_data.update_ram_addr:
                if ram_details.ram_addr == 0:
                    raise Exception(f"Item with name '{item_name}' has a RAM address of 0, which is not expected.")