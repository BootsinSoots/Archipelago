from gclib.rarc import RARC
from gclib.j3d import BDL
from gclib import fs_helpers as fs

from ..extensions import RARCExtended
from ..SMGDOL import SMGDOL

OBJECT_DATA_RELATIVE_PATH = "/DATA/files/ObjectData/"
GATEWAY_RELATIVE_PATH: str = "/DATA/files/ObjectData/AstroChildRoom.arc"
MINIATURE_GATEWAY_NAME: str = "MiniHeavensDoorGalaxy"

class Gateway(RARCExtended):
    bdl_base_name = "astrochildroom.bdl"

    def __init__(self):
        self.object_data_absolute_path = self.iso_base_path +  OBJECT_DATA_RELATIVE_PATH
        self.relative_path = GATEWAY_RELATIVE_PATH
        super().__init__()

        self.bdl_entry = self.get_file_entry(self.bdl_base_name)

    def create_miniature(self):
        # Scale the BDL to the desired size
        bdl: BDL = BDL(self.bdl_entry)

        for joint in bdl.jnt1.joints:
            scale = 3.14
            joint.bounding_sphere_radius *= scale
            joint.scale.x *= scale
            joint.scale.y *= scale
            joint.scale.z *= scale
            joint.bounding_box_min.x *= scale
            joint.bounding_box_min.y *= scale
            joint.bounding_box_min.z *= scale
            joint.bounding_box_max.x *= scale
            joint.bounding_box_max.y *= scale
            joint.bounding_box_max.z *= scale
        
        bdl.jnt1.save()
        for chunk in bdl.chunks:
            chunk.save()
        bdl.save()
        self.bdl_entry.save_changes()

        # Instantiate an empty ARC file and populate it with they BDL entry
        name: str = MINIATURE_GATEWAY_NAME.lower()
        empty_arc: RARC = RARC()

        empty_arc.add_root_directory()

        root_node = empty_arc.get_node_by_path('')
        root_node.name = "minisurprisedgalaxy"

        empty_arc.add_new_file(name + ".bdl", self.bdl_entry.data, root_node)
        empty_arc.save_changes()
        
        self.data = empty_arc.data
        self.read()

        new_file_path = self.object_data_absolute_path + MINIATURE_GATEWAY_NAME + ".arc"

        print(f"Creating {MINIATURE_GATEWAY_NAME}.arc")

        self.save_to_new_file(new_file_path)

    def replace_loading(self, dol: SMGDOL, name_address: int) -> None:
        """
        Replaces typical loading of gateway galaxy of the gateway island. Replaces both the entrance and exit.
        """
        self.replace_entrance(dol, name_address)
        self.replace_exit(dol, name_address)

    def replace_entrance(self, dol: SMGDOL, name_address: int) -> None:
        upper_bytes: int = name_address >> 16
        lower_bytes: int = name_address & 0xFFFF

        address = 0x8001f024
        new_instruction = b'\x3c\x60' + int.to_bytes(upper_bytes, 2)
        dol.write_data(fs.write_bytes, address, new_instruction)

        address = 0x8001f028
        new_instruction = b'\x60\x63' + int.to_bytes(lower_bytes, 2)
        dol.write_data(fs.write_bytes, address, new_instruction)

    def replace_exit(self, dol: SMGDOL, name_address: int) -> None:
        upper_bytes: int = name_address >> 16
        lower_bytes: int = name_address & 0xFFFF

        address = 0x803bb2fc
        new_instruction = b'\x3c\x60' + int.to_bytes(upper_bytes, 2)
        dol.write_data(fs.write_bytes, address, new_instruction)

        address = 0x803bb300
        new_instruction = b'\x60\x63' + int.to_bytes(lower_bytes, 2)
        dol.write_data(fs.write_bytes, address, new_instruction)
