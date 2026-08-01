import hashlib, os, zipfile
import xml.etree.ElementTree as eT

from worlds.Files import APPlayerContainer
from ..Constants.constants import GAME_NAME, USA_GAME_ID

class InvalidCleanISOError(Exception): pass

# Can pull this from dolphin or a cmd command / bash command
CLEAN_MD5: int = 0 # Need to get the right MD5 value here.


def verify_base_rom(self):
    """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
    of the file matches against the one we expect, and third, we had a game id in the file that matches the games
    official one"""
    # Verifies we have a valid installation of Super Mario Galaxy USA. There are some regional file differences.
    print(f"Verifying if the provided ISO is a valid copy of {GAME_NAME}...")

    # Reads the file in chunks, as its too big as a file on its own and could lead to the python process slowing
    # down to process and read each byte. After reading each chunk, it updates and calculates the MD5
    base_md5 = hashlib.md5()
    with open(self.clean_iso_path, "rb") as f:
        while chunk := f.read(1024 * 1024):  # Read the file in chunks.
            base_md5.update(chunk)

        # Grab the Magic Code and Game_ID with the file still open
        f.seek(0)
        game_id = f.read(6).decode("shift_jis")
        magic = game_id[:4]
        print(f"Magic Code: {magic}; Game ID: {game_id}")

    # Verify that the file has the right has format first, as the wrong file could have been loaded.
    md5_conv = int(base_md5.hexdigest(), 16)
    if md5_conv != CLEAN_MD5:
        raise InvalidCleanISOError(f"Invalid vanilla {GAME_NAME} ISO.\nYour ISO may be corrupted or your " +
                                   f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {CLEAN_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

    # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
    # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
    if magic == "CISO":
        raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {GAME_NAME} randomizer " +
                                   "only supports ISOs in ISO format.")
    if game_id != USA_GAME_ID:
        # Checks this starts with "SB4" at least, otherwise user provided an entirely different game.
        if game_id and game_id.startswith(USA_GAME_ID[:3]):
            raise InvalidCleanISOError(f"Invalid version of {GAME_NAME}. " +
                                       "Currently, only the North American / English version is supported by this randomizer.")
        else:
            raise InvalidCleanISOError(f"Non-{GAME_NAME} game detected. Please re-select the vanilla " +
                                       f"{GAME_NAME}'s ISO (North American version).")
    return


def get_base_rom_path() -> str:
    from settings import get_settings, Settings
    import Utils

    """Gets the base rom path from the host.yml settings."""
    options: Settings = get_settings()
    file_name = options["smgalaxy2.world_options"]["iso_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def dict_to_xml(tag_key: str, d: dict):
    elem = eT.Element(tag_key)
    for key, val in d.items():
        if key.startswith('@'):
            elem.set(key[1:], val)
        elif isinstance(val, dict):
            elem.append(dict_to_xml(key, val))
        else:
            child = eT.Element(key)
            child.text = str(val)
            elem.append(child)
    return elem
        

class SMGPlayerContainer(APPlayerContainer):
    game = GAME_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsmg"

    def __init__(self, player_choices: dict, patch_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.xml", eT.tostring(dict_to_xml("root", self.output_data), encoding='unicode'))
        super().write_contents(opened_zipfile)