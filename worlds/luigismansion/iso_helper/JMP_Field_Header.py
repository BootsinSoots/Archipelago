import struct
from io import BytesIO

IMPORTANT_HEADER_BYTE_LENGTH = 12

class JMPFieldHeader:
    _field_name = ""
    _field_hash = 0
    _field_bitmask = 0
    _field_shift_bit = 0
    _field_data_type = ""

    # First 4 bytes represent the field's hash.
    # The second 4 bytes represent the field bitmask, which is used for modifying byte data. It can help
    #   with read/write optimization, compression, and efficiency, while also potentially helping in graphics.
    # The next 2 bytes represent the starting bit for the field within a given data line.
    # The second to last byte represents the shift bits, which is required when reading certain field data.
    # The last byte represents the data type, which for this project's purposes include:
    #   Integer, String, and Float.
    def __init__(self, name: str, header_bytes: BytesIO):
        self._field_name = name
        self._field_hash, self._field_bitmask, self._field_start_bit, self._field_shift_bit, data_type = (
            struct.unpack(">I I H B B", header_bytes.read(IMPORTANT_HEADER_BYTE_LENGTH)))
        match data_type:
            case 0:
                self._field_data_type="Int"
            case 1:
                self._field_data_type="Str"
            case 2:
                self._field_data_type = "Flt"
            case _:
                raise Exception("Unknown Data Type provided: " + str(data_type))

    @property
    def get_field_type(self):
        return self._field_data_type

    @property
    def get_field_name(self):
        return self._field_name

    @property
    def get_field_hash(self):
        return self._field_hash

    @property
    def get_field_bitmask(self):
        return self._field_bitmask

    @property
    def get_field_start_bit(self):
        return self._field_start_bit

    @property
    def get_field_shift_bit(self):
        return self._field_shift_bit