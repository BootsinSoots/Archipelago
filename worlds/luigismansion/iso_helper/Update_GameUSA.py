from gclib.gcm import GCM
from gclib.yaz0_yay0 import Yay0

from CommonClient import logger

from ..Helper_Functions import get_arc, find_rarc_file_entry

def update_game_usa(gcm: GCM):
    obake_copy = get_arc(gcm, "files/model/obake01.szp")
    game_usa_edit = get_arc(gcm, "files/Game/game_usa.szp")

    logger.info("Deleting Unused Skybox (vrbox) in iwamoto")
    vrbox_data = find_rarc_file_entry(game_usa_edit, "iwamoto", "vrbox")
    game_usa_edit.delete_directory(vrbox_data)

    logger.info("Deleting Unused Textbox in kawano")
    unused_window = find_rarc_file_entry(game_usa_edit, "dmman", "m_window3.bti")
    game_usa_edit.delete_file(unused_window)

    logger.info("Deleting Unused Image File in kawano")
    unused_image = find_rarc_file_entry(game_usa_edit, "base", "cgbk_v.tim")
    game_usa_edit.delete_file(unused_image)

    logger.info("Deleting Unused param File in iyapoo2")
    unused_params: list[str] = ["iyapoo21.prm", "iyapoo22.prm", "iyapoo23.prm", "iyapoo24.prm", "iyapoo25.prm"]
    for unused_prm in unused_params:
        prm_file = find_rarc_file_entry(game_usa_edit, "ctp", unused_prm)
        game_usa_edit.delete_file(prm_file)

    logger.info("Deleting Unused Image File in kt_static")
    unused_second_image = find_rarc_file_entry(game_usa_edit, "kt_static", "test.bti")
    game_usa_edit.delete_file(unused_second_image)

    logger.info("Deleting Unused Image File in model")
    unused_model = find_rarc_file_entry(game_usa_edit, "model", "takara1.arc")
    game_usa_edit.delete_file(unused_model)

    logger.info("Adding Gold Ghost image into the model folder")
    game_usa_edit.add_new_file("obake01.arc", obake_copy.data, game_usa_edit.get_node_by_path("model"))

    logger.info("Overwriting game_uza.szp with the new re-created file...")
    gcm.delete_file(gcm.files_by_path["files/Game/game_usa.szp"])
    gcm.add_new_file("files/Game/game_usa.szp", game_usa_edit)
    game_usa_edit.save_changes()
    logger.info("game_uza.szp Yay0 check...")
    gcm.changed_files["files/Game/game_usa.szp"] = Yay0.compress(game_usa_edit.data)