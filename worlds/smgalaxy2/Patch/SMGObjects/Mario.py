from gclib import texture_utils
from gclib.j3d import BDL
from enum import StrEnum
from PIL import Image

from ...Options import MarioColors
from ..extensions import RARCExtended

MARIO_RELATIVE_PATH = "/DATA/files/ObjectData/Mario.arc"

class MarioParts(StrEnum):
    HATandSHIRT: str = "Hat & Shirt"
    OVERALLS: str = "Overalls"
    SHOES: str = "Shoes"
    GLOVES: str = "Gloves"

class MarioColours:
    """
    A utility class for modifying Mario's colours in Super Mario Galaxy.
    This class handles the extraction, manipulation, and replacement of colour values
    in Mario's character model textures (hat, overalls, gloves, and shoes) by working
    with BDL (Binary Display List) files. It uses pixel threshold detection to identify
    and replace specific colored regions in texture images.
    """
    HAT_THRESHOLD: tuple = (255,50,50)
    OVERALLS_THRESHOLD: tuple = (50,55,255)
    GLOVES_THRESHOLD: tuple = (0,0,0)
    SHOES_THRESHOLD: tuple = (0,0,0)

    colour_map: dict[str, tuple] = {"Red"   : (255,  0,  0),
                                    "Orange": (255,165,  0),
                                    "Yellow": (255,255,  0),
                                    "Green" : (  0,128,  0),
                                    "Blue"  : (  0,  0,255),
                                    "Purple": (128,  0,128),
                                    "Black" : (  0,  0,  0),
                                    "Brown" : (165, 42, 42),
                                    "White" : (255,255,255),
                                    "Pink"  : (255,192,203),
                                    "Gray"  : (128,128,128)}

    def __init__(self, mario: RARCExtended):
        self.mario = mario

        if "mario.bdl" not in [file.name for file in self.mario.file_entries]:
            raise ValueError("Arc file is not expected arc file: Mario.arc")            
        
        self.bdl = self.mario.get_file("mario.bdl", BDL)
        
    def get_img(self, texture_name: str) -> Image:    
        if texture_name not in self.bdl.tex1.textures_by_name:
            raise ValueError(f"Texture not found in bdl file: {texture_name}")

        bti = self.bdl.tex1.textures_by_name[texture_name][0]
        img = texture_utils.decode_image(bti.image_data, bti.palette_data,
                                         bti.image_format, bti.palette_format,
                                         bti.num_colors, bti.width, bti.height)
        self.img = img

    def set_img(self, texture_name: str) -> None:
        if texture_name not in self.bdl.tex1.textures_by_name:
            raise ValueError(f"Texture not found in bdl file: {texture_name}")

        bti = self.bdl.tex1.textures_by_name[texture_name][0]
        bti.replace_image(self.img)
        self.bdl.tex1.textures_by_name[texture_name][0] = bti

    def replace_pixels(self, threshold_values: tuple, new_colour: tuple) -> None:
        img = self.img
        pixels = img.load()
        width = img.size[0]
        height = img.size[1]

        for x in range(width):
            for y in range(height):
                if False not in [pixels[x,y][i] <= threshold_values[i] for i in [0,1,2]]:
                    pixels[x, y] = (*new_colour, 255)
    
    def update_part(self, mario_part: str, colour: str) -> None:
        if mario_part not in MarioColors.valid_keys:
            raise ValueError(f"Mario part is not an accepted part: {mario_part}")

        print(f"Updating {mario_part.lower()} to {colour.lower()}")

        colour = self.colour_map[colour]

        if mario_part == MarioParts.HATandSHIRT:
            texture_name = "MarioCap.0"
            threshold = self.HAT_THRESHOLD
        elif mario_part == MarioParts.OVERALLS:
            texture_name = "MarioBody.0"
            threshold = self.OVERALLS_THRESHOLD
        elif mario_part == MarioParts.SHOES:
            texture_name = "MarioBody.0"
            threshold = self.SHOES_THRESHOLD
        elif mario_part == MarioParts.GLOVES:
            texture_name = "MarioBody.0"
            threshold = self.GLOVES_THRESHOLD
        else:
            raise ValueError(f"Cannot find mario part: {mario_part}")

        self.get_img(texture_name)
        self.replace_pixels(threshold, colour)
        self.set_img(texture_name)

        self.bdl.save()
        for ch in self.bdl.chunks:
            ch.save()

class Mario(RARCExtended):
    def __init__(self):
        self.relative_path = MARIO_RELATIVE_PATH
        super().__init__()

        self.colours = MarioColours(self)
    
    def update_colours(self, items: dict[str, str]) -> None:
        for mario_part, colour in items.items():
            self.colours.update_part(mario_part, colour)
