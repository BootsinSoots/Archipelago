from enum import StrEnum
from typing import NamedTuple, Optional


class RamEndianness(StrEnum):
    little = "little",
    big = "big"


class RamData(NamedTuple):
    ram_addr: int
    endianness: RamEndianness
    ram_byte_size: int
    bit_position: Optional[int] = None
    pointers_list: Optional[list[int]] = None