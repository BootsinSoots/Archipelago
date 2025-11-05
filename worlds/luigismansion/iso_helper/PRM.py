from dataclasses import dataclass
from enum import IntEnum
from io import BytesIO
import struct


@dataclass
class PRMColor:
    """C/C++ Clr (color) object representation"""
    red_value: int
    green_value: int
    blue_value: int
    opacity: int

    def __init__(self, red: int, green: int, blue: int, opacity: int):
        self.red_value = red
        self.green_value = green
        self.blue_value = blue
        self.opacity = opacity

    @staticmethod
    def unpack_color(color_data: bytes) -> "PRMColor":
        return PRMColor(*struct.unpack(">4I", color_data))

    def __str__(self):
        return (f"Red Val: {str(self.red_value)}; Green Val: {str(self.green_value)}; " +
                f"Blue Val: {str(self.blue_value)}; Opacity Val: {str(self.green_value)}")

    def __len__(self):
        return 16

    def __bytes__(self):
        return struct.pack(">4I", self.red_value, self.green_value, self.blue_value, self.green_value)


@dataclass
class PRMVector:
    """C/C++ Vector3 object equivalent. Float representation of things like positions, scale, directions, etc."""
    float_one: float
    float_two: float
    float_three: float

    def __init__(self, first_float: float, second_float: float, third_float: float):
        self.float_one = first_float
        self.float_two = second_float
        self.float_three = third_float

    @staticmethod
    def unpack_vector(vector_data: bytes) -> "PRMVector":
        return PRMVector(*struct.unpack(">3f", vector_data))

    def __str__(self):
        return (f"First Float: {str(self.float_one)}; Second Float: {str(self.float_two)}; " +
                f"Third Float: {str(self.float_three)}")

    def __len__(self):
        return 12

    def __bytes__(self):
        return struct.pack(">3f", self.float_one, self.float_two, self.float_three)


@dataclass
class PRMFileEntry:
    field_idx: int
    field_hash: int
    field_name: str
    field_value: bytes | str | PRMColor | PRMVector
    field_value_offset: int

    def __init__(self, idx: int, entry_hash: int, entry_name: str,
        entry_value: bytes | int | float | PRMColor | PRMVector, entry_offset: int):
        self.field_idx = idx
        self.field_hash = entry_hash
        self.field_name = entry_name
        self.field_value = entry_value
        self.field_value_offset = entry_offset

    def __str__(self):
        return f"Field Hash: {str(self.field_hash)}\nField Name: {self.field_name}\nField Value: {str(self.field_value)}"


class PRMType(IntEnum):
    Byte = 1
    Short = 2
    Hex = 4
    Vector = 12 # Ties out to PRMVector
    Color = 16 # Ties out to PRMColor


class PRM:
    data: BytesIO = None
    data_entries: list[PRMFileEntry] = []

    def __init__(self, prm_data: BytesIO):
        self.data = prm_data

    def load_file(self) -> None:
        self.data.seek(0)
        num_of_entries = struct.unpack(">I", self.data.read(4))[0]

        for entry_num in range(num_of_entries):
            entry_hash: int = int(struct.unpack(">H", self.data.read(2))[0])
            entry_name_length: int = int(struct.unpack(">H", self.data.read(2))[0])
            entry_name: str = struct.unpack(f">{entry_name_length}s", self.data.read(entry_name_length))[0].decode("shift_jis")

            entry_size: int = int(struct.unpack(">I", self.data.read(4))[0])
            entry_bytes: bytes = self.data.read(entry_size)
            match entry_size:
                case PRMType.Byte:
                    entry_value: bytes = entry_bytes[:1]
                case PRMType.Short:
                    entry_value: int = int.from_bytes(entry_bytes, "big")
                case PRMType.Hex:
                    entry_value: str = entry_bytes.hex()
                case PRMType.Vector:
                    entry_value: PRMVector = PRMVector.unpack_vector(entry_bytes)
                case PRMType.Color:
                    entry_value: PRMColor = PRMColor.unpack_color(entry_bytes)
                case _:
                    raise ValueError("Unimplemented PRM type detected: " + str(entry_size))

            # 4 for initial data entry count, the other numbers listed here are the hash, length, etc.
            data_offset: int = 4 + ((2 + 2 + entry_name_length + 4 + entry_size) * (entry_num + 1))
            self.data_entries.append(PRMFileEntry(entry_num, entry_hash, entry_name, entry_value, data_offset))

    def update_file(self) -> None:
        self.data.seek(0)
        self.data.write(len(self.data_entries).to_bytes(4, "big"))

        self.data_entries.sort(key=lambda entry: entry.field_idx)
        for prm_entry in self.data_entries:
            self.data.seek(prm_entry.field_value_offset)
            match prm_entry.field_value:
                case bytes():
                    self.data.write(prm_entry.field_value)
                case str():
                    self.data.write(prm_entry.field_value.encode("shift_jis"))
                case _:
                    self.data.write(bytes(prm_entry.field_value))

    def get_entry(self, field_name: str) -> PRMFileEntry:
        return next(entry for entry in self.data_entries if entry.field_name == field_name)

    def print_entries(self):
        for _ in self.data_entries:
            print(str(_))