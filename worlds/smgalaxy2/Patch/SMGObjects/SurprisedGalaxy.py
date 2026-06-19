from ..extensions import RARCExtended
from gclib.j3d import BDL

OBJECT_DATA_RELATIVE_PATH = "/DATA/files/ObjectData/"
SURPRISED_GALAXY_RELATIVE_PATH = "/DATA/files/ObjectData/MiniSurprisedGalaxy.arc"

class SurprisedGalaxy(RARCExtended):
    bdl_base_name: str = "minisurprisedgalaxy.bdl"
    btk_base_name: str = "minisurprisedgalaxy.btk"

    scaled = False

    def __init__(self):
        self.object_data_absolute_path = self.iso_base_path +  OBJECT_DATA_RELATIVE_PATH
        self.relative_path = SURPRISED_GALAXY_RELATIVE_PATH
        super().__init__()

        self.bdl_entry = self.get_file_entry(self.bdl_base_name)
        self.btk_entry = self.get_file_entry(self.btk_base_name)
    
    def scale_joints(self, bdl: BDL):
        if not self.scaled:
            self.scaled = True
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

    def create_luma_miniature(self, luma_galaxy_name: str):
        name: str = luma_galaxy_name.lower()
        self.bdl_entry.name = name +'.bdl'
        
        bdl = BDL(self.bdl_entry)
        
        self.scale_joints(bdl)
        
        bdl.jnt1.save()
        for chunk in bdl.chunks:
            chunk.save()
        bdl.save()
        self.bdl_entry.save_changes()
        
        self.btk_entry.name = name +'.btk'
        self.btk_entry.save_changes()

        new_file_path = self.object_data_absolute_path + luma_galaxy_name + '.arc'

        print(f"Creating {luma_galaxy_name}.arc")

        self.save_to_new_file(new_file_path)
