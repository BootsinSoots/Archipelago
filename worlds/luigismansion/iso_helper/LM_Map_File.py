from gcbrickwork import JMP
from gclib.gcm import GCM
from gclib.rarc import RARC, RARCFileEntry
from gclib.yaz0_yay0 import Yay0

from ..Helper_Functions import get_arc, find_rarc_file_entry


class LMMapFile:
    _arc_data: RARC = None
    _arc_name: str = None
    jmp_files: dict[str, JMP] = {}

    def __init__(self, lm_gcm: GCM, name_of_rarc: str):
        """
        Creates an object representation of an LM Map file, which can contain several directories/files such as:
            JMP (JUMP) object tables, Path files (which describe literal paths characters take), and J3D effect/animation files.
        Automatically caches all JMP table RARCFileEntries to make it easier to query later.
        Automatically also decompresses from Yay0 format.
        """
        self._arc_name = name_of_rarc
        self._arc_data = get_arc(lm_gcm, name_of_rarc)

    def get_all_jmp_files(self):
        """
        Loads all JMP files found within the arc file into self.jmp_files object.
        """
        self.load_jmp_files(list(jmp.name for jmp in self._jmp_arc_files))

    def load_jmp_files(self, jmp_file_names: list[str]):
        """
        Loads one or more JMP files based on the provided list of JMP file names
        """
        for jmp_file_name in jmp_file_names:
            self.jmp_files[jmp_file_name] = self.get_jmp_file(jmp_file_name)

    def get_jmp_file(self, jmp_file_name: str) -> JMP:
        """
        Checks if a JMP file is already loaded in memory and returns that, otherwise searches the arc's jmp files.
        """
        if jmp_file_name in self.jmp_files:
            return self.jmp_files[jmp_file_name]

        jmp_file: RARCFileEntry = find_rarc_file_entry(self._arc_data, "jmp", jmp_file_name)
        if jmp_file is None:
            raise Exception(f"Unable to find the jmp file: '{jmp_file_name}'")

        jmp_file_data: JMP = JMP(jmp_file.data)
        jmp_file_data.load_file()
        return jmp_file_data

    def _update_all_jmp_files(self):
        """
        Updates all jmp files data back into their arc file
        """
        for jmp_name, jmp_file in self.jmp_files.items():
            arc_jmp: RARCFileEntry = find_rarc_file_entry(self._arc_data, "jmp", jmp_name)
            if jmp_file is None:
                raise Exception(f"Unable to find the jmp file: '{jmp_name}'")

            jmp_file.update_file()
            arc_jmp.data = jmp_file.data

    def update_and_save_map(self, lm_gcm: GCM):
        """
        Saves the map file and all related changes, then recompresses the map back into Yay0 format.
        """
        self._update_all_jmp_files()
        self._arc_data.save_changes()
        lm_gcm.changed_files[self._arc_name] = Yay0.compress(self._arc_data.data)