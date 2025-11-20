from logging import getLogger

from gclib.gcm import GCM
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yay0

from ..Helper_Functions import get_arc, find_rarc_file_entry
from ..client.constants import CLIENT_NAME

class LMGameUSAArc:
    _arc_path: str = None
    game_usa_arc: RARC = None

    def __init__(self, lm_gcm: GCM, arc_path: str):
        self._arc_path = arc_path
        self.game_usa_arc: RARC = get_arc(lm_gcm, arc_path)
        self.client_logger = getLogger(CLIENT_NAME)

    def add_gold_ghost(self, lm_gcm: GCM):
        """
        In order to trigger the Gold Ghost trap properly, we need to copy its file into the game_usa archive.
        However, since game_usa is very full, we must also delete and remove some unused files, otherwise game_usa
            is too large to load and will crash the emulator.
        """
        self._remove_unused_files()
        obake_copy = get_arc(lm_gcm, "files/model/obake01.szp")
        self.client_logger.info("Adding Gold Ghost image into the model folder")
        self.game_usa_arc.add_new_file("obake01.arc", obake_copy.data, self.game_usa_arc.get_node_by_path("model"))

    def _remove_unused_files(self):
        """
        In order to keep game_usa loadable, several un-used files such as sky boxes, textboxes, images, and param files
            will be removed in order to make space, so the emulator can properly load this file.
        """
        self.client_logger.info("Deleting Unused Skybox (vrbox) in iwamoto")
        vrbox_data = find_rarc_file_entry(self.game_usa_arc, "iwamoto", "vrbox")
        self.game_usa_arc.delete_directory(vrbox_data)

        self.client_logger.info("Deleting Unused Textbox in kawano")
        unused_window = find_rarc_file_entry(self.game_usa_arc, "dmman", "m_window3.bti")
        self.game_usa_arc.delete_file(unused_window)

        self.client_logger.info("Deleting Unused Image File in kawano")
        unused_image = find_rarc_file_entry(self.game_usa_arc, "base", "cgbk_v.tim")
        self.game_usa_arc.delete_file(unused_image)

        self.client_logger.info("Deleting Unused param files iyapoo21 through iyapoo25")
        unused_params: list[str] = ["iyapoo21.prm", "iyapoo22.prm", "iyapoo23.prm", "iyapoo24.prm", "iyapoo25.prm"]
        for unused_prm in unused_params:
            prm_file = find_rarc_file_entry(self.game_usa_arc, "ctp", unused_prm)
            self.game_usa_arc.delete_file(prm_file)

        self.client_logger.info("Deleting Unused Image File in kt_static")
        unused_second_image = find_rarc_file_entry(self.game_usa_arc, "kt_static", "test.bti")
        self.game_usa_arc.delete_file(unused_second_image)

        self.client_logger.info("Deleting Unused Image File in model")
        unused_model = find_rarc_file_entry(self.game_usa_arc, "model", "takara1.arc")
        self.game_usa_arc.delete_file(unused_model)

    def update_game_usa(self, lm_gcm: GCM):
        """
        Updates the game_usa arc into the GCM
        """
        self.client_logger.info("Overwriting game_uza.szp with the new re-created file...")
        lm_gcm.delete_file(lm_gcm.files_by_path[self._arc_path])
        lm_gcm.add_new_file(self._arc_path, self.game_usa_arc)
        self.game_usa_arc.save_changes()
        self.client_logger.info("game_uza.szp Yay0 check...")
        lm_gcm.changed_files[self._arc_path] = Yay0.compress(self.game_usa_arc.data)