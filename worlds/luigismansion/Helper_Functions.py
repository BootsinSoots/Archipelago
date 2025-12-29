from importlib.resources.abc import Traversable
from typing import NamedTuple, Optional
import importlib.resources as resources

from gclib.rarc import RARCFileEntry, RARC, RARCNode
from gclib.gcm import GCM

PROJECT_ROOT: Traversable = resources.files(__name__)

IGNORE_RARC_NAMES: list[str] = [".", ".."]

class LMRamData(NamedTuple):
    ram_addr: Optional[int] = None
    bit_position: Optional[int] = None
    ram_byte_size: Optional[int] = None
    pointer_offset: Optional[int] = None
    in_game_room_id: Optional[int] = None
    item_count: Optional[int] = None

class StringByteFunction:
    @staticmethod
    def string_to_bytes(user_string: str, encoded_byte_length: int) -> bytes:
        """
        Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
        If provided string is longer than expected length, raise an exception

        :param user_string: String that needs to be encoded to bytes.
        :param encoded_byte_length: Expected length of the provided string.
        """
        encoded_string = user_string.encode('utf-8')

        if len(encoded_string) < encoded_byte_length:
            encoded_string += b'\x00' * (encoded_byte_length - len(encoded_string))
        elif len(encoded_string) > encoded_byte_length:
            raise Exception("Provided string '" + user_string + "' was longer than the expected byte length of '" +
                            str(encoded_byte_length) + "', which will not be accepted by the info file.")

        return encoded_string

    @staticmethod
    def string_to_bytes_with_limit(user_string: str, max_bytes_length: int) -> bytes:
        """
        Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
        If provided string is longer than expected length, chop it off at the max bytes length instead.

        :param user_string: String that needs to be encoded to bytes.
        :param max_bytes_length: Max length of the bytes.
        """
        encoded_string = user_string.encode('utf-8')
        if len(encoded_string) < max_bytes_length:
            encoded_string += b'\x00' * (max_bytes_length - len(encoded_string))
        return encoded_string[:max_bytes_length]

    @staticmethod
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

    @staticmethod
    def byte_string_strip_null_terminator(bytes_input: bytes):
        return bytes_input.decode().strip("\0")


def find_rarc_file_entry(rarc_file: RARC, directory_name: str, name_of_file: str) -> RARCFileEntry | None:
    """Gets a file/if its from a specific directory."""
    for file_entry in rarc_file.file_entries:
      if file_entry.name == name_of_file and file_entry.parent_node.name == directory_name:
        return file_entry
    return None


def get_arc(gcm: GCM, arc_path) -> RARC:
    """Get an ARC / RARC / SZP file from within the ISO / ROM"""
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


def is_rarc_node_empty(rarc_node: RARCNode, files_to_be_removed: list[str]=None) -> bool:
    assert rarc_node.name not in IGNORE_RARC_NAMES
    assert rarc_node is not None

    # If there are no files in this node, this node is empty
    if len(rarc_node.files) == 0:
        return True

    future_removed_files: list[str] = files_to_be_removed if not None else []
    return set([nfile.name for nfile in rarc_node.files if nfile.name not in future_removed_files]).issubset(set(IGNORE_RARC_NAMES))