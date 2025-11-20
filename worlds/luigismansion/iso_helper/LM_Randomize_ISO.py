# Python related imports.
import json, os
from logging import Logger, getLogger
from random import Random

# AP Related Imports
import Utils

# 3rd Party related imports
from gclib.gcm import GCM
from gclib.fs_helpers import read_str, write_str

# Internal Related imports.
from ..client.constants import CLIENT_VERSION, AP_WORLD_VERSION_NAME, RANDOMIZER_NAME, CLIENT_NAME, LM_GC_IDs
from .Update_GameUSA import LMGameUSAArc

class LuigisMansionRandomizer:
    random: Random
    debug: bool = False
    clean_iso_path: str = None
    output_file_path: str = None
    output_data: dict = None
    lm_gcm: GCM = None
    client_logger: Logger = None

    _seed: str = None

    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data: bytes, debug_flag=False):
        self.debug = debug_flag
        self.clean_iso_path = clean_iso_path
        self.output_file_path = randomized_output_file_path
        self.output_data = json.loads(ap_output_data.decode('utf-8'))

        # Init the logger based on the existing client name.
        self.client_logger = getLogger(CLIENT_NAME)

        # Set the random's seed for use in other files.
        self._seed = self.output_data["Seed"]
        self.random = Random()
        self.random.seed(self._seed)

    def create_randomized_iso(self):
        # Check if the file is in use and return an error if so.
        try:
            if os.path.isfile(self.output_file_path):
                temp_file = open(self.output_file_path, "r+")  # or "a+", whatever you need
                temp_file.close()
        except IOError:
            raise Exception(f"'{self.output_file_path}' is currently in use by another program.")

        # Make sure that the server and client versions match before attempting to patch ISO.
        self._check_server_version(self.output_data.get(AP_WORLD_VERSION_NAME, "<0.5.6"))

        # Change game ID so save files are different
        lm_regional_id: str = self._get_and_update_game_id()

        # After verifying, this will also read the entire iso, including system files and their content
        self.lm_gcm = GCM(self.clean_iso_path)
        self.lm_gcm.read_entire_disc()

        # Update the relevant Game RARC archive
        self._update_game_archive(lm_regional_id)


    def _check_server_version(self, ap_world_version: str):
        """
        Compares the version provided in the patch manifest against the client's version.

        :param ap_world_version: The output data's generated version.
        """
        if ap_world_version != CLIENT_VERSION:
            raise Utils.VersionException(f"Error! Server was generated with a different {RANDOMIZER_NAME} " +
                                         f"APWorld version.\nThe client version is {CLIENT_VERSION}!\nPlease verify you are using the " +
                                         f"same APWorld as the generator, which is '{ap_world_version}'")

    def _get_and_update_game_id(self) -> str:
        """
        Updates the ISO's game id to use AP's seed that was generated.
        This allows LM to have 3 brand new save files every time.
        """
        self.client_logger.info("Updating the ISO game id with the AP generated seed.")
        bin_data = self.lm_gcm.read_file_data("sys/boot.bin")
        regional_id: str = read_str(bin_data, 0x00, 6)
        write_str(bin_data, 0x01, self._seed, len(self._seed))
        self.lm_gcm.changed_files["sys/boot.bin"] = bin_data

        return regional_id

    def _update_game_archive(self, regional_id: str):
        # Load game_usa and prepare those changes. Leaves wiggle room for support to other LM regions (potentially)
        match regional_id:
            case LM_GC_IDs.USA_ID:
                game_arc: LMGameUSAArc = LMGameUSAArc(self.lm_gcm, "files/Game/game_usa.szp")
                game_arc.add_gold_ghost(self.lm_gcm)
                game_arc.update_game_usa(self.lm_gcm)