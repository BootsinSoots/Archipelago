from typing import Self
from io import BytesIO
from enum import StrEnum
import gclib.fs_helpers as fs
from gclib.dol import DOL

from .extensions import DOLExtended, CustomDOLSection
from .bcsv import BCSV

from ..Constants.Names.region_names import FLIPSWAP
from ..regions import region_list

GATEWAY: str = region_list[FLIPSWAP].in_game_name

DOL_RELATIVE_PATH: str = "/DATA/sys/main.dol"

NAME_TO_CREATE_FUNCTION_START_ADDRESS = 0x80533980
NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT = 1183
NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE = 0xC

NAME_TO_ARCHIVE_START_ADDRESS = 0x805370f4
NAME_TO_ARCHIVE_ELEMENT_COUNT = 440
NAME_TO_ARCHIVE_ELEMENT_SIZE = 0x8

NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS = 0x80537eb4
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT = 91
NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE = 0x8

GALAXY_UNLOCK_TABLE_START_ADDRESS = 0x8053c800
GALAXY_UNLOCK_TABLE_END_ADDRESS = 0x8053d520

CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS = 0x8026a8cc
CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS = 0x8026a90c
STRING_ADDRESS_MINISURPRISEDGALAXY = 0x8059838c

ASTRO_DOME_ARRAY_ADDRESS = 0x8057a9e0
ASTRO_DOME_SKY_ARRAY_ADDRESS = 0x8057aa24
ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS = 0x8057aad4
ASTRO_STAR_PLATE_ARRAY_ADDRESS = 0x8057ab70

class Pointer:
    base_address: int
    pointing_address: int
    
    def __init__(self, dol: DOL, base_address: int):
        self.dol = dol
        
        self.base_address = base_address

        self.read_pointer()

    def read_pointer(self):
        self.pointing_address = self.dol.read_data(fs.read_u32, self.base_address)
    
    def write_pointer(self):
        self.dol.write_data(fs.write_u32, self.base_address, self.pointing_address)

    def swap_with_pointer(self, other: Self):
        self.pointing_address, other.pointing_address = other.pointing_address, self.pointing_address

        self.write_pointer()
        other.write_pointer()

class CharPointer(Pointer):
    string: str

    def read_pointer(self):
        super().read_pointer()

        if self.pointing_address != 0:
            self.string = self.dol.read_data(fs.read_str_until_null_character, self.pointing_address)
        else:
            self.string = None
    
    def write_string(self) -> None:
        self.dol.write_data(fs.write_str_with_null_byte, self.pointing_address, self.string)

    def replace_prefix(self, new_prefix: str) -> None:
        self.string = new_prefix + self.string[len(new_prefix):]
        self.write_string()

class FunctionPointer(Pointer):
    def write_function_address(self, new_function_address: int):
        self.pointing_address = new_function_address

        self.write_pointer()

class Name2CreateFuncElement:
    name_pointer: CharPointer
    create_function_pointer: FunctionPointer
    archive_name_pointer: CharPointer

    def __init__(self, name_pointer: CharPointer, create_function_pointer: FunctionPointer, archive_name_pointer: CharPointer):
        self.name_pointer = name_pointer
        self.create_function_pointer = create_function_pointer
        self.archive_name_pointer = archive_name_pointer

class Name2ArchiveElement:
    object_name_pointer: CharPointer
    archive_name_pointer: CharPointer

    def __init__(self, object_name_pointer: CharPointer, archive_name_pointer: CharPointer):
        self.object_name_pointer = object_name_pointer
        self.archive_name_pointer = archive_name_pointer

class Name2MakeArchiveListFuncElement:
    name_pointer: CharPointer
    archive_function: FunctionPointer

    def __init__(self, name_pointer: CharPointer, archive_function: FunctionPointer):
        self.name_pointer = name_pointer
        self.archive_function = archive_function

class NameObjFactory:
    name_to_create_function_elements: list[Name2CreateFuncElement]
    name_to_archive_elements: list[Name2ArchiveElement]
    name_to_make_archive_list_function_elements: list[Name2MakeArchiveListFuncElement]

    def __init__(self, dol: DOL):
        self.dol = dol

        self.miniature_function_address = CREATE_NAME_OBJECT_MINIATURE_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_function_address = CREATE_NAME_OBJECT_SURPRISED_GALAXY_FUNCTION_START_ADDRESS
        self.surprised_galaxy_string_address = STRING_ADDRESS_MINISURPRISEDGALAXY

        # Initialise the Name2CreateFunction list
        start_address = NAME_TO_CREATE_FUNCTION_START_ADDRESS
        element_count = NAME_TO_CREATE_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_CREATE_FUNCTION_ELEMENT_SIZE

        self.name_to_create_function_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_address = offset + 0x0
            create_function_address = offset + 0x4
            archive_name_address = offset + 0x8

            name_pointer: CharPointer = CharPointer(self.dol, name_address)
            create_function_pointer: FunctionPointer = FunctionPointer(self.dol, create_function_address)
            archive_name_pointer: CharPointer = CharPointer(self.dol, archive_name_address)

            element: Name2CreateFuncElement = Name2CreateFuncElement(name_pointer, create_function_pointer, archive_name_pointer)

            self.name_to_create_function_elements.append(element)

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_create_element: Name2CreateFuncElement = element

        # Initialise the Name2Archive list    
        start_address = NAME_TO_ARCHIVE_START_ADDRESS
        element_count = NAME_TO_ARCHIVE_ELEMENT_COUNT
        element_size = NAME_TO_ARCHIVE_ELEMENT_SIZE

        self.name_to_archive_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            object_name_address = offset + 0x0
            archive_name_address = offset + 0x4

            object_name_pointer: CharPointer = CharPointer(self.dol, object_name_address)
            archive_name_pointer: CharPointer = CharPointer(self.dol, archive_name_address)

            element: Name2ArchiveElement = Name2ArchiveElement(object_name_pointer, archive_name_pointer)

            self.name_to_archive_elements.append(element)

        # Initialise the Name2MakeArchiveList list
        start_address = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_START_ADDRESS
        element_count = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_COUNT
        element_size = NAME_TO_MAKE_ARCHIVE_LIST_FUNCTION_ELEMENT_SIZE

        self.name_to_make_archive_list_function_elements = []

        for element_index in range(element_count):
            offset = start_address + element_size * element_index
            name_address = offset + 0x0
            archive_function_address = offset + 0x4

            name_pointer: CharPointer = CharPointer(self.dol, name_address)
            archive_function_pointer: FunctionPointer = FunctionPointer(self.dol, archive_function_address)

            element: Name2MakeArchiveListFuncElement = Name2MakeArchiveListFuncElement(name_pointer, archive_function_pointer)

            self.name_to_make_archive_list_function_elements.append(element)

            if name_pointer.string == "MiniKoopaBattleVs3Galaxy":
                self.extra_archive_element: Name2MakeArchiveListFuncElement = element

    def get_name_to_create_function_elements_by_name(self, name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.name_pointer.string == name]

    def get_name_to_create_function_elements_by_create_function(self, create_function_address: int) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.create_function_pointer.pointing_address == create_function_address]
    
    def get_name_to_create_function_elements_by_archive_name(self, archive_name: str) -> list[Name2CreateFuncElement]:
        return [element for element in self.name_to_create_function_elements
                if element.archive_name_pointer.string == archive_name]

    def get_miniature_galaxy_name_to_make_archive_list_function_elements(self) -> list[Name2MakeArchiveListFuncElement]:
        return [element for element in self.name_to_make_archive_list_function_elements
                if element.name_pointer.string.startswith("Mini")][:-1]

    def set_miniature_galaxy_name_to_make_archive_list_function_elements(self, new_miniature_name_pointers: list[CharPointer]) -> None:
        archive_miniature_elements = self.get_miniature_galaxy_name_to_make_archive_list_function_elements()
        
        for archive_miniature_element, new_miniature_name_pointer in zip(archive_miniature_elements, new_miniature_name_pointers):
            archive_miniature_element.name_pointer.pointing_address = new_miniature_name_pointer.pointing_address
            archive_miniature_element.name_pointer.write_pointer()

    def set_miniature_galaxy_name_to_create_function_element(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Mini"
        element.name_pointer.replace_prefix("Mini")

        # Set the create function as the create miniature galaxy function
        element.create_function_pointer.write_function_address(self.miniature_function_address)
        
        # Empty the archive name
        element.archive_name_pointer.pointing_address = 0
        element.archive_name_pointer.write_pointer()

    def set_as_miniature_galaxies(self, miniature_elements: list[Name2CreateFuncElement]) -> None:
        self.set_miniature_galaxy_name_to_make_archive_list_function_elements([element.name_pointer for element in miniature_elements])

        for element in miniature_elements:
            self.set_miniature_galaxy_name_to_create_function_element(element)

    def set_name_to_create_function_element_as_surprised(self, element: Name2CreateFuncElement) -> None:
        # Replace the first 4 characters of the name with "Surp"
        element.name_pointer.replace_prefix("Surp")

        # Set the create function as the create surprised galaxy function
        element.create_function_pointer.write_function_address(self.surprised_function_address)

        # Set the archive name to "MiniSurprisedGalaxy"
        element.archive_name_pointer.pointing_address = self.surprised_galaxy_string_address
        element.archive_name_pointer.write_pointer()

    def set_as_surprised_galaxies(self, surprised_elements: list[Name2CreateFuncElement]) -> None:
        for element in surprised_elements:
            self.set_name_to_create_function_element_as_surprised(element)

    def set_galaxies(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str]) -> None:
        # Get the elements in the array that should be converted to dome and luma galaxies
        to_miniature_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in miniature_galaxy_names]
        to_surprised_elements: list[Name2CreateFuncElement] = [element for element in self.name_to_create_function_elements
                                                               if element.name_pointer.string[4:] in surprised_galaxy_names]

        if FLIPSWAP in miniature_galaxy_names:
            self.extra_create_element.name_pointer.string = "Mini" + FLIPSWAP
            self.extra_create_element.name_pointer.write_string()
            to_miniature_elements.append(self.extra_create_element)
        
        self.set_as_miniature_galaxies(to_miniature_elements)
        self.set_as_surprised_galaxies(to_surprised_elements)

    def swap_pointers(self, pointer1: Pointer, pointer2: Pointer) -> None:
        pointer1.swap_with_pointer(pointer2)

class GalaxyUnlockTableFieldNames(StrEnum):
    NAME: str = "name"
    MAP_PANE_NAME: str = "MapPaneName"
    OPEN_CONDITION0: str = "OpenCondition0"
    OPEN_CONDITION1: str = "OpenCondition1"
    OPEN_CONDITION2: str = "OpenCondition2"
    POWER_STAR_REQUIREMENT: str = "PowerStarNum"
    RETURN_DOME: str = "GrandGalaxyNo"

class GalaxyUnlockTableEntry:
    def __init__(self, entry_index: int, name: str, open_condition0: str, open_condition1: str,
                 power_star_requirement: int, return_dome: int):
        self.entry_index: int = entry_index
        self.name: str = name
        self.open_condition0: str = open_condition0
        self.open_condition1: str = open_condition1
        self.power_star_requirement: int = power_star_requirement
        self.return_dome: int = return_dome

    def __str__(self):
        return ' '.join([str(self.entry_index),
                        str(self.name),
                        str(self.open_condition0),
                        str(self.open_condition1),
                        str(self.power_star_requirement),
                        str(self.return_dome)])

class GalaxyUnlockTable:
    table: BCSV

    start_address: int
    end_address: int
    size: int

    entries: list[GalaxyUnlockTableEntry]

    def __init__(self, dol: DOL):
        self.start_address = GALAXY_UNLOCK_TABLE_START_ADDRESS
        self.end_address = GALAXY_UNLOCK_TABLE_END_ADDRESS
        self.size = self.end_address - self.start_address

        self.entries = []

        table_bytes: bytes = dol.read_data(fs.read_bytes, self.start_address, self.size)
        self.table = BCSV(BytesIO(table_bytes))

        self.name_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.NAME)
        self.open_condition0_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.OPEN_CONDITION0)
        self.open_condition1_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.OPEN_CONDITION1)
        self.power_star_requirement_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.POWER_STAR_REQUIREMENT)
        self.return_dome_index = self.table.get_field_index(GalaxyUnlockTableFieldNames.RETURN_DOME)
        
        for entry_index in range(self.table.entry_count):
            entry = self.get_entry(entry_index)

            # Set empty by default, to be overridden later
            entry.open_condition0 = ''
            entry.open_condition1 = ''
            entry.power_star_requirement = 0
            entry.return_dome = 0
            self.set_entry(entry)
            
            self.entries.append(entry)

    def get_entry(self, entry_index: int) -> GalaxyUnlockTableEntry:
        name = self.table.get_value_by_index(entry_index, self.name_index)
        open_condition0 = self.table.get_value_by_index(entry_index, self.open_condition0_index)
        open_condition1 = self.table.get_value_by_index(entry_index, self.open_condition1_index)
        power_star_requirement = self.table.get_value_by_index(entry_index, self.power_star_requirement_index)
        return_dome = self.table.get_value_by_index(entry_index, self.return_dome_index)

        return GalaxyUnlockTableEntry(entry_index, name, open_condition0, open_condition1,
                                      power_star_requirement, return_dome)
    
    def set_entry(self, entry: GalaxyUnlockTableEntry) -> None:
        self.table.set_value_by_index(entry.entry_index, self.name_index, entry.name)
        self.table.set_value_by_index(entry.entry_index, self.open_condition0_index, entry.open_condition0)
        self.table.set_value_by_index(entry.entry_index, self.open_condition1_index, entry.open_condition1)
        self.table.set_value_by_index(entry.entry_index, self.power_star_requirement_index, entry.power_star_requirement)
        self.table.set_value_by_index(entry.entry_index, self.return_dome_index, entry.return_dome)

    def save_to_dol(self, dol: DOL, address: int) -> None:
        self.table.save_changes()
        dol.write_data(fs.write_bytes, address, self.table.data.getvalue())

class AstroDomeModels:
    astro_dome: list[CharPointer]
    astro_dome_sky: list[CharPointer]
    astro_dome_entrance: list[CharPointer]
    astro_star_plate: list[CharPointer]

    def __init__(self, dol: DOL):
        self.astro_dome_address: int = ASTRO_DOME_ARRAY_ADDRESS
        self.astro_dome_sky_address: int = ASTRO_DOME_SKY_ARRAY_ADDRESS
        self.astro_dome_entrance_address: int = ASTRO_DOME_ENTRANCE_ARRAY_ADDRESS
        self.astro_star_plate_address: int = ASTRO_STAR_PLATE_ARRAY_ADDRESS

        self.astro_dome = []
        self.astro_dome_sky = []
        self.astro_dome_entrance = []
        self.astro_star_plate = []
        
        for index in range(6):
            astro_dome_pointer = CharPointer(dol, self.astro_dome_address + index * 0x4)
            astro_dome_sky_pointer = CharPointer(dol, self.astro_dome_sky_address + index * 0x4)
            astro_dome_entrance_pointer = CharPointer(dol, self.astro_dome_entrance_address + index * 0x4)
            astro_star_plate_pointer = CharPointer(dol, self.astro_star_plate_address + index * 0x4)

            self.astro_dome.append(astro_dome_pointer)
            self.astro_dome_sky.append(astro_dome_sky_pointer)
            self.astro_dome_entrance.append(astro_dome_entrance_pointer)
            self.astro_star_plate.append(astro_star_plate_pointer)
    
    def shuffle_list(self, pointer_list: list[CharPointer], shuffle: dict[int, int]):
        assert len(pointer_list) == 6
        
        reverse_shuffle: dict[int, int] = {value: key for key, value in shuffle.items()}
        addresses: list[int] = [pointer_list[i].pointing_address for i in range(6)]
        for index, address in enumerate(addresses):
            new_index = reverse_shuffle[index + 1] - 1
            pointer_list[new_index].pointing_address = address
            pointer_list[new_index].write_pointer()
    
    def shuffle(self, shuffle: dict[int, int]):
        #self.shuffle_list(self.astro_dome, shuffle)
        #self.shuffle_list(self.astro_dome_sky, shuffle)
        self.shuffle_list(self.astro_dome_entrance, shuffle)
        #self.shuffle_list(self.astro_dome, shuffle)

class SMGDOL(DOLExtended):
    """Extends the gclib DOL class to be easily useable for Super Mario Galaxy."""
    name_object_factory: NameObjFactory
    galaxy_unlock_table: GalaxyUnlockTable
    custom_section: CustomDOLSection

    def __init__(self):
        self.relative_path = DOL_RELATIVE_PATH
        super().__init__()
        
        self.name_object_factory = NameObjFactory(self)
        self.galaxy_unlock_table = GalaxyUnlockTable(self)
        self.astro_dome_models = AstroDomeModels(self)

        self.custom_section = self.add_section(0x806ADF90, 0x1000)

    def set_name_object_factory_galaxies(self, miniature_galaxy_names: list[str], surprised_galaxy_names: list[str]) -> None:
        self.name_object_factory.set_galaxies(miniature_galaxy_names, surprised_galaxy_names)

    def get_galaxy_unlock_table_entry_by_name(self, name: str) -> GalaxyUnlockTableEntry:
        for entry in self.galaxy_unlock_table.entries:
            if entry.name == name:
                return entry

    def save(self):
        self.save_changes()
        self.write_data(fs.write_bytes, self.galaxy_unlock_table.start_address, b'\x00' * self.galaxy_unlock_table.size)
        self.galaxy_unlock_table.save_to_dol(self, self.galaxy_unlock_table.start_address)

        with open(self.absolute_file_path, 'wb') as f:
            f.write(self.data.getvalue())
