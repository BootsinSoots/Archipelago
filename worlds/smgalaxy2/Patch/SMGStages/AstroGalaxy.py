from enum import StrEnum
from typing import NamedTuple

from ..extensions import RARCExtended

ASTRO_GALAXY_RELATIVE_PATH: str = "/DATA/files/StageData/AstroGalaxy.arc"
ASTRO_DOME_ENTRANCE_NAME: str = "AstroDomeEntrance"

COMMON_PATH: str = "jmp/placement/common"
LAYERA_PATH: str = "jmp/placement/layera"
LAYERB_PATH: str = "jmp/placement/layerb"
FILE_NAME: str = "objinfo"

class ObjInfoFieldNames(StrEnum):
    NAME: str = "name"
    L_ID: str = "l_id"
    OBJECT_ARGUMENT0: str = "Obj_arg0"
    OBJECT_ARGUMENT1: str = "Obj_arg1"
    OBJECT_ARGUMENT2: str = "Obj_arg2"
    OBJECT_ARGUMENT3: str = "Obj_arg3"
    OBJECT_ARGUMENT4: str = "Obj_arg4"
    OBJECT_ARGUMENT5: str = "Obj_arg5"
    OBJECT_ARGUMENT6: str = "Obj_arg6"
    OBJECT_ARGUMENT7: str = "Obj_arg7"
    CAMERA_SET_ID: str = "CameraSetId"
    SWITCH_APPEAR: str = "SW_APPEAR"
    SWITCH_DEAD: str = "SW_DEAD"
    SWITCH_A: str = "SW_A"
    SWITCH_B: str = "SW_B"
    SWITCH_SLEEP: str = "SW_SLEEP"
    MESSAGE_ID: str = "MessageId"
    POSITION_X: str = "pos_x"
    POSITION_Y: str = "pos_y"
    POSITION_Z: str = "pos_z"
    DIRECTION_X: str = "dir_x"
    DIRECTION_Y: str = "dir_y"
    DIRECTION_Z: str = "dir_z"
    SCALE_X: str = "scale_x"
    SCALE_Y: str = "scale_y"
    SCALE_Z: str = "scale_z"
    CAST_ID: str = "CastId"
    VIEW_GROUP_ID: str = "ViewGroupId"
    SHAPE_MODEL_NUMBER: str = "ShapeModelNo"
    COMMON_PATH_ID: str = "CommonPath_ID"
    CLIPPING_GROUP_ID: str = "ClippingGroupId"
    GROUP_ID: str = "GroupId"
    DEMO_GROUP_ID: str = "DemoGroupId"
    MAP_PARTS_ID: str = "MapParts_ID"

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int
    orbit_index: int
    old_luma_name: str

class AstroGalaxy(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRO_GALAXY_RELATIVE_PATH
        super().__init__()

        # Get the objinfo bcsvs
        self.objinfo = self.get_bcsv_file(COMMON_PATH, FILE_NAME)
        self.objinfo_layera = self.get_bcsv_file(LAYERA_PATH, FILE_NAME)
        self.objinfo_layerb = self.get_bcsv_file(LAYERB_PATH, FILE_NAME)

        # Get the indices of the fields
        self.name_index = self.objinfo.get_field_index(ObjInfoFieldNames.NAME)
    
    def shuffle_lumas(self, new_galaxies: list[GalaxyDestination]) -> None:
        """
        Shuffle the lumas within the observatory. The list of new galaxies is expected to all have type "luma". The old luma name
        is used to determine which name to replace with the name. The old luma names are not checked for duplicates.
        """
        # Convert to a dict for easy lookup
        new_galaxies_dict: dict[str, str] = {galaxy.old_luma_name: galaxy.name for galaxy in new_galaxies}
        
        for entry_index in range(self.objinfo.entry_count):
            entry_name: str = self.objinfo.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo.save_changes()

        for entry_index in range(self.objinfo_layera.entry_count):
            entry_name: str = self.objinfo_layera.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo_layera.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo_layera.save_changes()

        for entry_index in range(self.objinfo_layerb.entry_count):
            entry_name: str = self.objinfo_layerb.get_value_by_index(entry_index, self.name_index)

            if entry_name.startswith("Surp"):
                entry_name = entry_name[4:]

                if entry_name in new_galaxies_dict.keys():
                    new_entry_name: str = "Surp" + new_galaxies_dict[entry_name]

                    print(f"Luma Surp{entry_name} -> {new_entry_name}")

                    self.objinfo_layerb.set_value_by_index(entry_index, self.name_index, new_entry_name)
        self.objinfo_layerb.save_changes()
