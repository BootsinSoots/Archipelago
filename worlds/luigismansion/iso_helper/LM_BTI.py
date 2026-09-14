import struct
from io import BytesIO

from PIL import Image

BTI_FRMT = 0x05 # RGB5A3
BLOCK_WIDTH = 4
BLOCK_HEIGHT = 4
BLOCK_SIZE_BYTES = 32
MAX_TEXT_SIZE = 1024

# TODO Maybe use gclib's fs helpers here? Rather than me parsing this bytesio
#   But not using their BTI class because its not able to reasy change/modify or load in from PNG files.

class LMBTI:
    """ Creates a BTI of type RGB5A3 for LM HUD elements. """
    def __init__(self):
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
        self.resample: Image.Resampling = Image.Resampling.LANCZOS
        self._source_data: bytes = b""

    @property
    def image_data(self) -> bytes:
        """ Encoded image data that is rebuilt from the source. """
        if not self._source_data:
            return b""

        return self._encode(self._build_image())

    def load_bti(self, file_data: BytesIO):
        """
        Loads an existing RGB5A3 BTI. Pixels are decoded to a lossless in-memory PNG and header is copied.
        Only first image is used and mipmaps are dropped.
        """
        file_data.seek(0)
        bti_bytes: bytes = file_data.getvalue()
        if len(bti_bytes) < 0x20:
            raise ValueError(f"BTI file provided does not have proper header bytes expected.")

        img_fmt = file_data.read(1)[0]
        self.alpha_setting = file_data.read(1)[0]
        self.width = struct.unpack(">H", file_data.read(2))[0]
        self.height = struct.unpack(">H", file_data.read(2))[0]
        self.wrap_s = file_data.read(1)[0]
        self.wrap_t = file_data.read(1)[0]
        self.palettes_enabled = file_data.read(1)[0]
        self.palette_format = file_data.read(1)[0]
        self.num_colors = struct.unpack(">H", file_data.read(2))[0]
        self.palette_offset = struct.unpack(">I", file_data.read(4))[0]
        self.mipmap_enable = file_data.read(1)[0]
        # 3 Bytes that don't matter, see to_bytes() for more details on what they are.
        file_data.read(3)
        self.min_filter = file_data.read(1)[0]
        self.mag_filter = file_data.read(1)[0]
        self.min_lod = file_data.read(1)[0]
        self.max_lod = file_data.read(1)[0]
        self.mipmap_count = file_data.read(1)[0]
        # Unknown byte here we don't care about.
        file_data.read(1)
        self.lod_bias = struct.unpack(">h", file_data.read(2))[0]
        self.data_offset = struct.unpack(">I", file_data.read(4))[0]

        if img_fmt != BTI_FRMT:
            raise ValueError(f"Unsupported BTI image format of 0x{img_fmt:02X}. Only 0x{BTI_FRMT:02X} is supported.")

        self.image_format = BTI_FRMT
        img = self._decode(bti_bytes)
        png_buffer = BytesIO()
        img.save(png_buffer, "PNG")
        self._source_data = png_buffer.getvalue()

    def _decode(self, bti_bytes: bytes) -> Image.Image:
        """ Decodes RGB5A3 Block data into an RGBA Pillow Image. """
        blocks_x = (self.width + BLOCK_WIDTH - 1) // BLOCK_WIDTH
        blocks_y = (self.height + BLOCK_HEIGHT - 1) // BLOCK_HEIGHT
        expected_size = self.data_offset + blocks_x * blocks_y * BLOCK_SIZE_BYTES
        if expected_size > len(bti_bytes):
            raise ValueError(f"BTI image does not match the header size. Expected Size: {expected_size} vs Len: {len(bti_bytes)}")

        img = Image.new("RGBA", (self.width, self.height))
        pixels  = img.load()
        offset = self.data_offset

        for by in range(blocks_y):
            for bx in range(blocks_x):

                # Iterate over a given block, then convert to pixels from original img
                for y in range(BLOCK_HEIGHT):
                    for x in range(BLOCK_WIDTH):
                        px = bx * BLOCK_WIDTH + x
                        py = by * BLOCK_HEIGHT + y
                        byte_offset = offset + ((y * 4) + x) * 2
                        val = (bti_bytes[byte_offset] << 8) | bti_bytes[byte_offset + 1]

                        if px >= self.width or py >= self.height:
                            continue

                        # This is awful and I hate this and took me forever between 3 websites to figure this out
                        # I need to find a better way ._.
                        if val & 0x8000:
                            # RGB555
                            r, g, b = (val >> 10) & 0x1F, (val >> 5) & 0x1F, val & 0x1F
                            pixels[px, py] = ((r << 3) | (r >>2), (g << 3) | (g >> 2), (b << 3) | (b >> 2), 255)
                        else:
                            # RGB444A3
                            a = (val >> 12) & 0x7
                            r, g, b = (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF
                            pixels[px, py] = (r * 17, g * 17, b * 17, (a << 5) | (a << 2) | (a >> 1))
                offset += BLOCK_SIZE_BYTES
        return img

    def load_png(self, file_data: BytesIO | str):
        """ Loads a file (or reads the bytes directly) using Pillow and update relevant BTI header bytes. """
        img = Image.open(file_data).convert("RGBA")
        self.width, self.height = img.size
        png_buffer = BytesIO()
        img.save(png_buffer, "PNG")
        self._source_data = png_buffer.getvalue()

    @staticmethod
    def _validate_size(width: int, height: int):
        if not (1 <= width <= MAX_TEXT_SIZE and 1 <= height <= MAX_TEXT_SIZE):
            raise ValueError(f"Image of size {width}x{height} must be at least 1x1 and smaller then {MAX_TEXT_SIZE}x{MAX_TEXT_SIZE}")

    def _build_image(self) -> Image.Image:
        """ Decodes the source image and resize it to width/heigh values. """
        self._validate_size(self.width, self.height)
        img = Image.open(BytesIO(self._source_data)).convert("RGBA")
        if img.size != (self.width, self.height):
            img = img.resize((self.width, self.height), self.resample)
        return img

    @staticmethod
    def _encode(img: Image.Image) -> bytes:
        img_width, img_height = img.size
        # Calculate block dimensions. GC reads in tiles/blocks rather than line by line
        blocks_x = (img_width + BLOCK_WIDTH - 1) // BLOCK_WIDTH
        blocks_y = (img_height + BLOCK_HEIGHT - 1) // BLOCK_HEIGHT

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

                        if px < img_width and py < img_height:
                            r, g, b, a = pixels[px, py]
                        else:
                            r, g, b, a = (0, 0, 0, 0)

                        # Specific RGB5A3 nonsense
                        # This is awful and I hate this and took me forever between 3 websites to figure this out
                        # I need to find a better way ._.
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
        return bytes(encoded_data)

    def to_bytes(self) -> BytesIO:
        """ Writes the generated BTI file as a BytesIO object. """
        image_data = self.image_data

        out_bytes: bytes = bytes()
        out_bytes += struct.pack(">B", self.image_format)
        out_bytes += struct.pack(">B", self.alpha_setting)
        out_bytes += struct.pack(">H", self.width)
        out_bytes += struct.pack(">H", self.height)
        out_bytes += struct.pack(">B", self.wrap_s)
        out_bytes += struct.pack(">B", self.wrap_t)
        out_bytes += struct.pack(">B", int(self.palettes_enabled))
        out_bytes += struct.pack(">B", self.palette_format)
        out_bytes += struct.pack(">H", self.num_colors)
        out_bytes += struct.pack(">I", self.palette_offset)
        out_bytes += struct.pack(">B", int(self.mipmap_enable))
        out_bytes += struct.pack(">B", 0x00) # EnableEdgeLOD
        out_bytes += struct.pack(">B", 0x00) # Clamp LOD Bias
        out_bytes += struct.pack(">B", 0x00) # Max Anisotropy
        out_bytes += struct.pack(">B", self.min_filter)
        out_bytes += struct.pack(">B", self.mag_filter)
        out_bytes += struct.pack(">B", self.min_lod)
        out_bytes += struct.pack(">B", self.max_lod)
        out_bytes += struct.pack(">B", self.mipmap_count)
        out_bytes += struct.pack(">B", 0x00) # Unknown
        out_bytes += struct.pack(">h", self.lod_bias)
        out_bytes += struct.pack(">I", self.data_offset)
        out_bytes += image_data

        return BytesIO(out_bytes)