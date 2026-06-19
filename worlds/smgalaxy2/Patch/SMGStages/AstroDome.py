from typing import NamedTuple
from enum import StrEnum

from ..extensions import RARCExtended
from ..SMGObjects.SurprisedGalaxy import SurprisedGalaxy
from ..SMGObjects.Gateway import Gateway
from ...Constants.Names.region_names import GATEWAY
from ...regions import region_list

ASTRODOME_RELATIVE_PATH = "/DATA/files/StageData/AstroDome.arc"
PLACEMENT_PATH = "jmp/placement/"
FILE_NAME = "objinfo"

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

index_to_layer = {1: 'layera',
                  2: 'layerb',
                  3: 'layerc',
                  4: 'layerd',
                  5: 'layere',
                  6: 'layerf'}

class AstroDome(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRODOME_RELATIVE_PATH
        super().__init__()

        self.surprised_galaxy: SurprisedGalaxy = SurprisedGalaxy()
        self.gateway_galaxy: Gateway = Gateway()

        # Get the in-game names from the region list
        self.major_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                             if data.type == "Major"]
        self.minor_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                             if data.type == "Minor"]
        self.boss_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                            if data.type == "Boss"]
        self.special_galaxy_list: list[str] = [region_list[galaxy].in_game_name for galaxy, data in region_list.items()
                                      if data.type == "Special"]
        self.gateway: str = region_list[GATEWAY].in_game_name

    def update_dome(self, new_galaxies: list[GalaxyDestination], dome_index: int, interior_dome_index: int):
        """
        Update the dome with new galaxies. The dome to update is determined by the dome index (from 1 to 6). The list of new galaxies
        is expected to all have type "dome" and contain all the galaxies that should be in the dome. The dome index of the new galaxies
        are ignored and should be used to determine the list to input in this function. The orbit index of the new galaxies is not
        checked for duplicates. Creates mini gateway and surprised galaxies if necessary. Interior dome index determines what the inside
        of the dome should look like in correspondance with the given index.
        """
        # Get the objinfo of the dome corresponding to the dome index.
        layer = index_to_layer[dome_index]
        objinfo = self.get_bcsv_file(PLACEMENT_PATH + layer, FILE_NAME)
        
        # Get the indices of the fields
        name_index = objinfo.get_field_index(ObjInfoFieldNames.NAME)
        objarg0_index = objinfo.get_field_index(ObjInfoFieldNames.OBJECT_ARGUMENT0)
        miniature_indices = []

        # Get the entry indices of the current miniatures in the dome
        # and set the AstroDome and AstroDomeSky values
        for entry_index in range(objinfo.entry_count):
            name: str = objinfo.get_value_by_index(entry_index, name_index)
            if name.startswith("Mini"):
                miniature_indices.append(entry_index)
            
            if name.startswith("AstroDome"):
                objinfo.set_value_by_index(entry_index, objarg0_index, interior_dome_index)

        # Iterate over all the galaxies in the new_galaxies list and update the corresponding entry
        index = 0
        for galaxy in new_galaxies:
            entry_index = miniature_indices[index]
            index += 1
            name = "Mini" + galaxy.name
            
            print(f"Dome {dome_index} orbit {galaxy.orbit_index + 1} -> {name}")

            objinfo.set_value_by_index(entry_index, name_index, name)
            
            # Store the orbit index in the upper bits
            obj_arg0 = galaxy.orbit_index << 16

            # Store the galaxy type in the lower bits
            if galaxy.name in self.major_galaxy_list:
                obj_arg0 += 0
            elif galaxy.name in self.minor_galaxy_list or galaxy.name in self.special_galaxy_list:
                obj_arg0 += 1

                if galaxy.name == self.gateway:
                    self.gateway_galaxy.create_miniature()
                elif galaxy.name in self.special_galaxy_list:
                    self.surprised_galaxy.create_luma_miniature(name)
            elif galaxy.name in self.boss_galaxy_list:
                obj_arg0 += 2

            objinfo.set_value_by_index(entry_index, objarg0_index, obj_arg0)

        objinfo.save_changes()
