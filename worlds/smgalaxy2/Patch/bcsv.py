from gclib.gclib_file import GCLibFile
import gclib.fs_helpers as fs
from io import BytesIO
from .hashtable import hash_to_name
import struct, copy

class BCSVField:
    def __init__(self, data: BytesIO):
        self.data = data

        self.hash = None
        self.bitmask = None
        self.offset = None
        self.shift = None
        self.type = None

        self.read()
    
    def read(self):
        self.hash = fs.read_u32(self.data, 0x0)
        self.bitmask = fs.read_u32(self.data, 0x4)
        self.offset = fs.read_u16(self.data, 0x8)
        self.shift = fs.read_u8(self.data, 0xA)
        self.type = fs.read_u8(self.data, 0xB)

        self.name = hash_to_name[fs.read_bytes(self.data, 0x0, 4)]

    def get_value(self, entry_data: BytesIO):
        if self.type == 0: # LONG
            return fs.read_s32(entry_data, self.offset)
        elif self.type == 1: # STRING
            return fs.try_read_str(entry_data, self.offset, 32)
        elif self.type == 2: # FLOAT
            return fs.read_float(entry_data, self.offset)
        elif self.type == 3: # LONG_2
            return fs.read_s32(entry_data, self.offset)
        elif self.type == 4: # SHORT
            return fs.read_s16(entry_data, self.offset)
        elif self.type == 5: # BYTE
            return fs.read_s8(entry_data, self.offset)
        elif self.type == 6: # STRING_OFFSET
            return fs.read_u32(entry_data, self.offset)
        return None

    def get_bytes(self, value):
        if self.type == 0: # LONG
            return struct.pack('>i', value)
        elif self.type == 1: # STRING
            return struct.pack('>32s', value)
        elif self.type == 2: # FLOAT
            return struct.pack('>f', value)
        elif self.type == 3: # LONG_2
            return struct.pack('>i', value)
        elif self.type == 4: # SHORT
            return struct.pack('>h', value)
        elif self.type == 5: # BYTE
            return struct.pack('>b', value)
        elif self.type == 6: # STRING_OFFSET
            return struct.pack('>I', value)
        return None

    def write_bytes(self, entry_data: BytesIO, value):
        if self.type == 0: # LONG
            fs.write_s32(entry_data, self.offset, value)
        elif self.type == 1: # STRING
            fs.write_str(entry_data, self.offset, value, 32)
        elif self.type == 2: # FLOAT
            fs.write_float(entry_data, self.offset, value)
        elif self.type == 3: # LONG_2
            fs.write_s32(entry_data, self.offset, value)
        elif self.type == 4: # SHORT
            fs.write_s16(entry_data, self.offset, value)
        elif self.type == 5: # BYTE
            fs.write_s8(entry_data, self.offset, value)
        elif self.type == 6: # STRING_OFFSET
            fs.write_u32(entry_data, self.offset, value)
        return None

    def save_changes(self):
        self.data.truncate(0)
        fs.write_u32(self.data, 0x0, self.hash)
        fs.write_u32(self.data, 0x4, self.bitmask)
        fs.write_u16(self.data, 0x8, self.offset)
        fs.write_u8(self.data, 0xA, self.shift)
        fs.write_u8(self.data, 0xB, self.type)

class BCSV(GCLibFile):
    def __init__(self, flexible_data = None):
        super().__init__(flexible_data)
        
        self.entry_count = None
        self.field_count = None
        self.entry_offset = None
        self.entry_size = None

        self.field_offset = 0x10
        self.fields: list[BCSVField] = []
        self.entries: list[list] = []
        self.strings: list[str] = []
        self.string_offsets: list[int] = []

        self.hidden_strings: list[str] = []

        if flexible_data is not None:
            self.read()
    
    def read(self):
        # Read header
        self.entry_count = fs.read_u32(self.data, 0x0)
        self.field_count = fs.read_u32(self.data, 0x4)
        self.entry_offset = fs.read_u32(self.data, 0x8)
        self.entry_size = fs.read_u32(self.data, 0xC)
        
        strings_offset = self.entry_offset + self.entry_count*self.entry_size
        strings_data = fs.read_bytes(self.data, strings_offset, -1)
        strings = strings_data.split(b'\x00')
        self.strings = [string.decode('shift-jis') for string in strings[:-1]]

        self.calculate_string_offsets()

        for field_index in range(self.field_count):
            field_offset = self.field_offset + field_index*0xC
            field_data = BytesIO(fs.read_bytes(self.data, field_offset, 0xC))
            
            field = BCSVField(field_data)
            self.fields.append(field)
            
        for entry_index in range(self.entry_count):
            entry_offset = self.entry_offset + entry_index*self.entry_size
            entry_data = BytesIO(fs.read_bytes(self.data, entry_offset, self.entry_size))

            self.entries.append([])
            for field in self.fields:
                entry_value = field.get_value(entry_data)
                self.entries[-1].append(entry_value)

                # Replace string offset with string
                if field.type == 6:
                    string_index = self.string_offsets.index(self.entries[-1][-1])
                    self.entries[-1][-1] = self.strings[string_index]
    
        # Apparently there are hidden strings
        # They exist in the string pool BUT ARE NEVER USED BUT ARE SOMETIMES NECESSARY
        actual_strings: list[str] = []

        for entry_index, entry in enumerate(self.entries):
            for field_index, field in enumerate(self.fields):
                if field.type != 6:
                    continue

                string = self.entries[entry_index][field_index]
                if string not in actual_strings:
                    actual_strings.append(string)
        
        for string in self.strings:
            if string not in actual_strings:
                self.hidden_strings.append(string)

    def get_value_by_index(self, entry_index: int, field_index: int):
        if entry_index < 0 or entry_index >= len(self.entries):
            raise IndexError(f"Entry index out of range. Entries: {len(self.entries)}, index: {entry_index}.")
        if field_index < 0 or field_index >= len(self.fields):
            raise IndexError(f"Field index out of range. Fields: {len(self.fields)}, index: {field_index}.")
        return self.entries[entry_index][field_index]
        
    def set_value_by_index(self, entry_index: int, field_index: int, new_value):
        if entry_index < 0 or entry_index >= len(self.entries):
            raise IndexError(f"Entry index out of range. Entries: {len(self.entries)}, index: {entry_index}.")
        if field_index < 0 or field_index >= len(self.fields):
            raise IndexError(f"Field index out of range. Fields: {len(self.fields)}, index: {field_index}.")

        field = self.fields[field_index]

        if field.type != 1:
            self.entries[entry_index][field_index] = new_value
        
        self.get_strings()

    def replace_single_entry_name(self, old_name: str, new_name: str):
        for entry_index, entry in enumerate(self.entries):
            if entry[0] == old_name:
                self.replace_entry_name_by_index(entry_index, new_name)
                return
        return

    def replace_entry_name_by_index(self, entry_index: int, new_name: str):
        if entry_index < 0 or entry_index >= len(self.entries):
            raise IndexError(f"Entry index out of range. Entries: {len(self.entries)}, index: {entry_index}.")
        
        self.entries[entry_index][0] = new_name
        self.get_strings()

    def get_strings(self):
        self.strings = copy.deepcopy(self.hidden_strings)
        for entry_index, entry in enumerate(self.entries):
            for field_index, field in enumerate(self.fields):
                if field.type == 6:
                    string = self.entries[entry_index][field_index]
                    if string not in self.strings:
                        self.strings.append(string)
        
        self.calculate_string_offsets()

    def calculate_string_offsets(self):
        self.string_offsets = [0]
        for string in self.strings:
            # Encode to shift-jis before getting the length since japanese characters
            # have a different length decoded vs encoded
            self.string_offsets.append(self.string_offsets[-1] + len(string.encode('shift-jis')) + 1)
        
        # Remove the last entry since it will never get used
        self.string_offsets.pop()

    def get_field_index(self, field_name: str) -> int:
        for i, field in enumerate(self.fields):
            if field.name == field_name:
                return i

    def get_entry_index_by_name(self, entry_name: str) -> int:
        for i, entry in enumerate(self.entries):
            if entry[0] == entry_name:
                return i

    def save_changes(self):
        # Repacks the bcsv

        # Cut off all the data since we're replacing it entirely
        self.field_offset = 0x10
        self.data.truncate(0)
        fs.write_u32(self.data, 0x0, self.entry_count)
        fs.write_u32(self.data, 0x4, self.field_count)
        fs.write_u32(self.data, 0x8, self.entry_offset)
        fs.write_u32(self.data, 0xC, self.entry_size)

        for field_index, field in enumerate(self.fields):
            field.save_changes()
            field_offset = self.field_offset + field_index*0xC
            fs.write_bytes(self.data, field_offset, field.data.getvalue())

        for entry_index in range(self.entry_count):
            entry_offset = self.entry_offset + entry_index*self.entry_size
            entry_data = BytesIO(b'\x00'*self.entry_size)

            for field_index, field in enumerate(self.fields):
                # Replace string with string offset
                if field.type == 6:
                    string_offset_index = self.strings.index(self.entries[entry_index][field_index])
                    self.entries[entry_index][field_index] = self.string_offsets[string_offset_index]

                field.write_bytes(entry_data, self.entries[entry_index][field_index])

                # Replace string offset with string again
                if field.type == 6:
                    string_index = self.string_offsets.index(self.entries[entry_index][field_index])
                    self.entries[entry_index][field_index] = self.strings[string_index]
            
            fs.write_bytes(self.data, entry_offset, entry_data.getvalue())
        
        strings_offset = self.entry_offset + self.entry_count*self.entry_size
        
        self.calculate_string_offsets()

        for string, offset in zip(self.strings, self.string_offsets):
            string_offset = strings_offset + offset
            fs.write_str_with_null_byte(self.data, string_offset, string)
        
        data_length = self.data.seek(0, 2)
        if data_length % 0x20 != 0:
            padding = 0x20 - data_length % 0x20
            fs.write_bytes(self.data, data_length, b'@'*padding)
