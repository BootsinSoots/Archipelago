from enum import StrEnum
from typing import NamedTuple, Optional


class RamEndianness(StrEnum):
    little = "little",
    big = "big"


class RamData(NamedTuple):
    address: int
    endianness: RamEndianness
    size: int
    bit_position: int = None
    pointers_list: list[int] = None