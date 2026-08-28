import struct
from PIL import Image

BTI_FRMT = 0x05 # RGB5A3
BLOCK_WIDTH = 4
BLOCK_HEIGHT = 4
BLOCK_SIZE_BYTES = 32

class BTICreator:
    def __init__(self, filepath: str | None = None):
        self.image_format = BTI_FRMT
        self.alpha_setting = 0x01 # Needs to be at least 1, can be anything really
        self.width = 0
        self.height = 0
        self.wrap_s = 0x00 # 0: clamp to edge; 1: repeat; 2: mirror
        self.wrap_t = 0x00 # See above
        self.palettes_enabled = False
        self.palette_format = 0x00
        self.num_colors = 0
        self.palette_offset = 0 # Relative to file header start
        self.mipmap_enable = False
        self.min_filter = 0x00
        self.mag_filter = 0x00
        self.min_lod = 0x00
        self.max_lod = 0x00
        self.mipmap_count = 1 # Image count
        self.lod_bias = 0
        self.data_offset = 0x20 # Offset to Image data
        self.image_data = b""

        if filepath and isinstance(filepath, str):
            self.load_png(filepath)

    def load_png(self, filepath: str):
        """Loads a PNG file using Pillow and update relevant BTI header bytes."""
        img = Image.open(filepath).convert("RGBA")
        self.width, self.height = img.size

        # Calculate block dimensions. GC reads in tiles/blocks rather than line by line
        blocks_x = (self.width + BLOCK_WIDTH - 1) // BLOCK_WIDTH
        blocks_y = (self.height + BLOCK_HEIGHT - 1) // BLOCK_HEIGHT

        pixels = img.load()
        encoded_data = bytearray(blocks_x * blocks_y * BLOCK_SIZE_BYTES)
        offset = 0

        for by in range(blocks_y):
            for bx in range(blocks_x):

                # Iterate over a given block, then convert to pixels from original img
                for y in range(BLOCK_HEIGHT):
                    for x in range(BLOCK_WIDTH):
                        px = bx * BLOCK_WIDTH + x
                        py = by * BLOCK_HEIGHT + y

                        if px < self.width and py < self.height:
                            r, g, b, a = pixels[px, py]
                        else:
                            r, g, b, a = (0, 0, 0, 0)

                        # Specific RGB5A3 nonsense
                        if a >= 224:
                            # RGB555 (1 bit flag = 1, 5 bits each for RGB)
                            val = 0x8000 | ((r >> 3) << 10) | ((g >> 3) << 5) | (b >> 3)
                        else:
                            # RGB444A3 (1 bit flag = 0, 3 bits Alpha, 4 bits each for RGB)
                            val = ((a >> 5) << 12) | ((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4)

                        pixel_idx = (y * 4) + x
                        byte_offset = offset + (pixel_idx * 2)
                        encoded_data[byte_offset] = (val >> 8) & 0xFF
                        encoded_data[byte_offset + 1] = val & 0xFF

                offset += BLOCK_SIZE_BYTES
        self.image_data = bytes(encoded_data)

    def write_bti(self, filepath: str):
        """Writes the generated BTI file to specified path."""
        with open(filepath, "wb") as f:
            f.write(struct.pack(">B", self.image_format))
            f.write(struct.pack(">B", self.alpha_setting))
            f.write(struct.pack(">H", self.width))
            f.write(struct.pack(">H", self.height))
            f.write(struct.pack(">B", self.wrap_s))
            f.write(struct.pack(">B", self.wrap_t))
            f.write(struct.pack(">B", int(self.palettes_enabled)))
            f.write(struct.pack(">B", self.palette_format))
            f.write(struct.pack(">H", self.num_colors))
            f.write(struct.pack(">I", self.palette_offset))
            f.write(struct.pack(">B", int(self.mipmap_enable)))
            f.write(struct.pack(">B", 0x00)) # EnableEdgeLOD
            f.write(struct.pack(">B", 0x00)) # Clamp LOD Bias
            f.write(struct.pack(">B", 0x00)) # Max Anisotropy
            f.write(struct.pack(">B", self.min_filter))
            f.write(struct.pack(">B", self.mag_filter))
            f.write(struct.pack(">B", self.min_lod))
            f.write(struct.pack(">B", self.max_lod))
            f.write(struct.pack(">B", self.mipmap_count))
            f.write(struct.pack(">B", 0x00)) # Unknown
            f.write(struct.pack(">h", self.lod_bias))
            f.write(struct.pack(">I", self.data_offset))

            f.write(self.image_data)