from gclib.dol import DOL, DOLSection
from gclib.rarc import RARC
from gclib.yaz0_yay0 import Yaz0
import gclib.fs_helpers as fs
from io import BytesIO

from .bcsv import BCSV

NOP = b'\x60\x00\x00\x00'

class CustomDOLSection(DOLSection):
    pointer: int

    def __init__(self, offset: int, address: int, size: int, dol: DOL):
        super().__init__(offset, address, size)

        self.dol = dol

    def init2(self) -> None:
        self.pointer = 0x804A16C0
        self.write_instructions(b'\x38\x63\xef\x90')

        self.pointer = 0x804AAC98
        self.write_instructions(b'\x38\xa5\xef\x90')

        self.reset_pointer()
        self.write_instructions([NOP] * int(self.size/4))

        # Return
        instructions = b'\x39\x61\x01\x00\x4b\xe6\x85\xcd\x80\x01\x01\x04\x7c\x08\x03\xa6\x38\x21\x01\x00\x4e\x80\x00\x20'
        self.pointer -= len(instructions)
        self.write_instructions(instructions)

        # Setup
        self.reset_pointer()
        self.write_instructions(b'\x94\x21\xff\x00\x7c\x08\x02\xa6\x90\x01\x01\x04\x39\x61\x01\x00\x4b\xe6\x95\x5d\x4b\xce\xbb\x4d')
        

    def reset_pointer(self) -> None:
        self.pointer = self.address

    def write_instructions(self, instructions: bytes | list[bytes]) -> None:
        if isinstance(instructions, bytes):
            assert len(instructions) % 4 == 0
        elif isinstance(instructions, list):
            for instruction in instructions:
                assert len(instruction) == 4
            instructions = b''.join(instructions)

        self.dol.write_data(fs.write_bytes, self.pointer, instructions)

        self.pointer += len(instructions)
    
    def deathlink(self) -> None:
        # Set 0x8000 into higher bits of r3
        # Load byte from 0x80001af0 into r3
        # Compare 0x80001af0 with 0
        # Jump over if its not 0
        # Jump to forceKillPlayerByAbyss
        # Set 0 into r3
        # Store byte from r3 (0) into 0x80001af0 and reset it
        self.write_instructions(b'\x3f\xe0\x80\x00\x88\x7f\x1a\xf0\x2c\x03\x00\x00\x41\x82\x00\x10\x4b\xd4\x3e\xbd\x38\x60\x00\x00\x98\x7f\x1a\xf0')
        
class DOLExtended(DOL):
    """To read data, call self.read_data and use the corresponding fs_helper function as read_callback"""
    # Path to be set before calling classes that inherit from this class
    iso_base_path = ''

    # Path to be set in each class that inherits this class
    relative_path = ''

    def __init__(self):
        if self.iso_base_path == '' or self.relative_path == '':
            raise ValueError(f"ISO path and relative path must not be empty. \
                             \nISO path: {self.iso_base_path}\nRelative path: {self.relative_path}")
        
        self.absolute_file_path = self.iso_base_path + self.relative_path
        super().__init__()
        
        with open(self.absolute_file_path, 'rb') as file:
            data = BytesIO(file.read())
            self.read(data)
    
    def get_last_section_offset(self) -> int:
        max_offset: int = 0
        for section in self.sections:
            end_of_section = section.offset + section.size
            if end_of_section > max_offset:
                max_offset = end_of_section

        return max_offset

    def add_section(self, address_start: int, size: int) -> CustomDOLSection:
        for index, section in enumerate(self.sections[:self.TEXT_SECTION_COUNT]):
            if section.address != 0:
                continue

            new_section: CustomDOLSection = CustomDOLSection(self.get_last_section_offset(), address_start, size, self)
            self.sections[index] = new_section
            new_section.init2()

            return new_section

    def save(self) -> None:
        """Save the changes back to the file"""
        self.save_changes()

        with open(self.absolute_file_path, 'wb') as f:
            f.write(self.data.getvalue())

class RARCExtended(RARC):
    """
    Extends the functionality of the gclib RARC class. Is meant as a base class for other classes to inherit from.
    Assumes the file path is an absolute path to the .arc file and uses that to write it back when saving.
    Set iso_path before instantiating inheriting classes.
    Set relative_path before initialising inheriting class instance
    """
    # Path to be set before calling classes that inherit from this class
    iso_base_path = ''

    # Path to be set in each class that inherits this class
    relative_path = ''

    def __init__(self):
        if self.iso_base_path == '' or self.relative_path == '':
            raise ValueError(f"ISO path and relative path must not be empty. \
                             \nISO path: {self.iso_base_path}\nRelative path: {self.relative_path}")
        
        self.absolute_file_path = self.iso_base_path + self.relative_path
        super().__init__(self.absolute_file_path)

    def get_bcsv_file(self, relative_file_path: str, file_name: str) -> BCSV:
        """Get a BCSV file from the archive given its relative path and file name."""
        for file in self.get_node_by_path(relative_file_path).files:
            if file.name == file_name:
                return BCSV(file)
        raise FileNotFoundError(f"File {relative_file_path}/{file_name} not found in archive {self.absolute_file_path}")

    def save(self) -> None:
        """Save the changes back to the file."""
        self.save_changes()

        with open(self.absolute_file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
    
    def save_to_new_file(self, new_file_path: str) -> None:
        self.save_changes()

        with open(new_file_path, 'wb') as f:
            f.write(Yaz0.compress(self.data).getvalue())
