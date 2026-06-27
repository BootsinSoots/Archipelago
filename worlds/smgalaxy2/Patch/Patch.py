import hashlib, os, time, zipfile, json
from pathlib import Path
from typing import NamedTuple, Optional

from disc_riider_py import WiiIsoExtractor, rebuild_from_directory
import gclib.fs_helpers as fs

from worlds.Files import APAutoPatchInterface, APPlayerContainer, AutoPatchRegister
from NetUtils import convert_to_base_types

from .extensions import RARCExtended, DOLExtended
from .SMGDOL import SMGDOL
from .SMGObjects.Mario import Mario
from .SMGObjects.AstroDomeEntrances import AstroDomeEntrances
from .SMGStages.AstroDome import AstroDome
from .SMGStages.AstroDomeScenario import AstroDomeScenario
from .SMGStages.AstroGalaxy import AstroGalaxy
from ..regions import region_list
from ..Constants.Names.region_names import FLIPSWAP

class InvalidCleanISOError(Exception): pass

# Name of the game, which is used in various error messaging.
RANDOMIZER_NAME: str = "Super Mario Galaxy"

# Can pull this from dolphin or a cmd command / bash command
CLEAN_MD5: int = 0xf99a97f9ae4dccd1db45e9aaab9cebd8

# Expected Game ID of the GC/Wii game we expect here.
EXPECTED_GAME_ID: str = "RMGE01"


class WiiISO:
    def __init__(self, patch_name: str):
        """Initialize a Patch object for Super Mario Galaxy ISO modification.
        Args:
            patch_name (str): Name of the patch file
        Attributes:
            clean_iso_path (str): Path of the unmodified ISO.
            dest_path (str): Output directory for the patched ISO.
            temp_dir (str): Temporary extraction directory.
            iso_name (str): Name of the new ISO file.
        """
        clean_iso_path: str = self.get_base_rom_path()
        dest_path: str = os.path.split(clean_iso_path)[0]
        temp_dir = os.path.join(dest_path, "temp")

        self.clean_iso_path = clean_iso_path
        self.dest_path = dest_path
        self.temp_dir = temp_dir
        self.iso_name = patch_name

        self.progress = None
        self.calling_function = None

    def verify_base_rom(self):
        """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
        of the file matches against the one we expect, and third, we had a game id in the file that matches the games
        official one"""
        # Verifies we have a valid installation of Super Mario Galaxy USA. There are some regional file differences.
        print(f"Verifying if the provided ISO is a valid copy of {RANDOMIZER_NAME}...")
        
        # Reads the file in chunks, as its too big as a file on its own and could lead to the python process slowing
        # down to process and read each byte. After reading each chunk, it updates and calculates the MD5
        base_md5 = hashlib.md5()
        with open(self.clean_iso_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read the file in chunks.
                base_md5.update(chunk)

            # Grab the Magic Code and Game_ID with the file still open
            f.seek(0)
            game_id = f.read(6).decode("shift_jis")
            magic = game_id[:4]
            print(f"Magic Code: {magic}; Game ID: {game_id}")

        # Verify that the file has the right has format first, as the wrong file could have been loaded.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != CLEAN_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {CLEAN_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                "only supports ISOs in ISO format.")
        if game_id != EXPECTED_GAME_ID:
            # Checks this starts with "RMG" at least, otherwise user provided an entirely different game.
            if game_id and game_id.startswith(EXPECTED_GAME_ID[:3]):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                    "Currently, only the North American / English version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError(f"Non-{RANDOMIZER_NAME} game detected. Please re-select the vanilla " +
                    f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return
    
    @staticmethod
    def get_base_rom_path() -> str:
        from settings import get_settings, Settings
        import Utils

        """Gets the base rom path from the host.yml settings."""
        options: Settings = get_settings()
        file_name = options["smgalaxy.world_options"]["iso_file"]
        if not os.path.exists(file_name):
            file_name = Utils.user_path(file_name)
        return file_name
    
    def extract(self):
        """Extracts the ISO into the output directory, preserving the orignal file/folder structure within the ISO.
        Once extracted, you can then read these files individually to change/edit, create new folders/files in the
        structure or delete old ones.
        """
        try:
            # Makes sure the file exists
            if not Path(self.clean_iso_path).exists():
                raise Exception(f"ISO file not found: {self.clean_iso_path}")
                
            # Extract the Wii file into memory and load all the disc partitions/disc structure.
            extractor: WiiIsoExtractor = WiiIsoExtractor(self.clean_iso_path)

            # Prepare the Data section of the disc by reading its file metadata into memory.
            extractor.prepare_extract_section("DATA")

            # Once prepared, we can export it to a directory of our choice.
            print("Initiating extracting ISO")
            self.calling_function = 'extract_iso'
            extractor.extract_to(self.temp_dir, self.progress_callback)

            print("Extacting ISO complete")

        except Exception as e:
            raise Exception(f"ISO extraction failed: {e}")

    def repack(self, delete: bool = True, verbose: bool = True):
        """Takes an extracted ISO directory and re-compiles it into a playable Wii ISO."""
        output_path = Path(self.dest_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("Initiating repacking ISO")
        self.calling_function = 'repack_iso'
        rebuild_from_directory(self.temp_dir, self.dest_path + self.iso_name + '.iso', callback=self.progress_callback)
        
        print("Repacking ISO complete")

        if delete:
            print("Deleting temporary directory...")

            # Delete the extracted ISO after its done repacking
            time.sleep(10)
            self._delete_temp_dir(self.temp_dir, verbose)
            
            print("Done deleting temporary directory!")
        
    def _delete_temp_dir(self, temp_dir, verbose: bool = True):
        """Remove the temporarily created directory for the extracted ISO"""
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            # Remove it if its a file otherwise recurse
            if os.path.isfile(file_path):
                os.remove(file_path)
                if verbose:
                    print(f"Deleting temp file: {file_path}")
            else:
                self._delete_temp_dir(file_path, verbose)
        
        if verbose:
            print(f"Deleting empty directory: {temp_dir}")
        os.rmdir(temp_dir)

    def progress_callback(self, progress):
        """Prints the progress as the callback is completing its steps."""
        out = ''
        if self.calling_function == 'repack_iso':
            out = "repacking ISO"
        elif self.calling_function == 'extract_iso':
            out = "extracting ISO"
        
        if progress % 10 == 0:
            if self.progress != progress:
                self.progress = progress
                print(f"Progress {out}: {self.progress}%")

class GalaxyDestination(NamedTuple):
    name: str
    type: str
    dome_index: int
    orbit_index: int
    old_luma_name: str

class GalaxyShuffle:
    converter = {"First" : 1,
                 "Second": 2,
                 "Third" : 3,
                 "Fourth": 4,
                 "Fifth" : 5}
    galaxy_destinations: list[GalaxyDestination]
    
    def __init__(self, galaxies: dict[str, str]):
        self.galaxies = galaxies
        self.galaxy_destinations = []

        # Generate a list of GalaxyDestinations from the galaxies dict
        for location, galaxy in self.galaxies.items():
            # Convert to its in-game name
            galaxy = region_list[galaxy].in_game_name

            if location.startswith("Dome"):
                # Extract the dome index and orbit index
                elements: list[str] = location.split(' ')
                dome_index: int = int(elements[1])
                orbit_index: int = self.converter[elements[2]] - 1
                
                new_galaxy = GalaxyDestination(galaxy, "dome", dome_index, orbit_index, None)

            elif location.startswith("Gateway"):
                new_galaxy = GalaxyDestination(galaxy, "gateway", None, None, None)

            else:
                luma_name: str = location.replace("Hungry Luma", "Galaxy").replace("Launch Star", "Galaxy")
                new_galaxy = GalaxyDestination(galaxy, "luma", None, None, region_list[luma_name].in_game_name)
            
            self.galaxy_destinations.append(new_galaxy)

class Patch:
    def __init__(self, patch_name: str, output: dict):
        self.iso: WiiISO = WiiISO(patch_name)

        RARCExtended.iso_base_path = self.iso.temp_dir
        DOLExtended.iso_base_path = self.iso.temp_dir

        self.counts: dict[str, int] = output['Galaxy Counts']
        self.galaxies: dict[str, str] = output['Galaxies']
        self.mario_colours: dict[str, str] = output['Options']['mario_colors']
        self.dome_shuffle: dict[str, str] = output['Options']['dome_shuffle']

        self.old_galaxies: str = self.galaxies.keys()
        self.new_galaxies: str = self.galaxies.values()

        self.unpack_iso()

        self.mario: Mario = Mario()
        self.astrogalaxy: AstroGalaxy = AstroGalaxy()
        self.astrodomescenario: AstroDomeScenario = AstroDomeScenario()
        self.astrodome: AstroDome = AstroDome()
        self.astrodomeentrances: AstroDomeEntrances = AstroDomeEntrances()
        self.dol: SMGDOL = SMGDOL()

    def unpack_iso(self) -> None:
        """Unpack the contents of the ISO file."""
        self.iso.extract()
    
    def repack_iso(self, delete: bool = True, verbose: bool = False) -> None:
        """Repack the contents of the ISO file."""
        self.iso.repack(delete, verbose)

    def update_mario(self) -> None:
        """
        Update mario. Currently only updates his outfit colours, but might do more stuff in the future.
        """
        # In the future possibly more functionality
        self.mario.update_colours(self.mario_colours)

    def update_astrogalaxy(self, luma_shuffle: list[GalaxyDestination]) -> None:
        """
        Shuffle the luma galaxies within the observatory.
        Luma shuffle is a list of GalaxyDestinations and if a luma name exists it expect the type to be "luma".
        """
        self.astrogalaxy.shuffle_lumas(luma_shuffle)

    def update_astrodomes(self, galaxy_shuffle: list[GalaxyDestination], dome_shuffle: dict[int, int]) -> None:
        """
        Shuffle the galaxies within a dome. Galaxy shuffle is a list of GalaxyDestinations and if a dome and orbit index exists,
        it expects the type to be "dome".
        """
        for index in range(1,7):
            self.astrodome.update_dome([galaxy for galaxy in galaxy_shuffle if galaxy.dome_index == index], index, dome_shuffle[index])

    def update_visual_astrodomes(self, dome_shuffle: dict[int, int]) -> None:
        """
        Update the Astro Dome arrays within the DOL.
        """
        #self.astrodomeentrances.rename_files(dome_shuffle)
        self.dol.astro_dome_models.shuffle(dome_shuffle)
        
    def update_gateway_location(self, gateway_galaxy: GalaxyDestination) -> None:
        galaxy_name = gateway_galaxy.name
        if galaxy_name == "HeavensDoorGalaxy":
            return
        
        mini_galaxy = self.dol.name_object_factory.get_name_to_create_function_elements_by_name("Mini" + galaxy_name)
        surp_galaxy = self.dol.name_object_factory.get_name_to_create_function_elements_by_name("Surp" + galaxy_name)

        if mini_galaxy:
            name_address = mini_galaxy[0].name_pointer.pointing_address
        elif surp_galaxy:
            name_address = surp_galaxy[0].name_pointer.pointing_address
        else:
            raise ValueError(f"{galaxy_name} cannot be found.")

        print(f"Loading zone gateway -> {galaxy_name}")

        # +4 to the name address to skip over the galaxy identifier tag (Mini/Surp)
        self.astrodome.gateway_galaxy.replace_loading(self.dol, name_address + 4)
        return

    def update_nameobjfactory(self, dome_galaxies: list[GalaxyDestination], luma_galaxies: list[GalaxyDestination]) -> None:
        dome_galaxy_names = [galaxy.name for galaxy in dome_galaxies]
        luma_galaxy_names = [galaxy.name for galaxy in luma_galaxies]
        
        self.dol.set_name_object_factory_galaxies(dome_galaxy_names, luma_galaxy_names)

    def update_galaxyunlocktable(self, dome_galaxies: list[GalaxyDestination], star_requirements: dict[str, int]) -> None:
        requirements: dict[int, dict[int, int]] = {i: {} for i in range(1,7)}
        
        for location, requirement in star_requirements.items():
            dome_index: int = int(location[1])
            orbit_index: int = int(location[3:])

            requirements[dome_index][orbit_index] = requirement
        
        for galaxy in dome_galaxies:
            star_requirement: int = requirements[galaxy.dome_index][galaxy.orbit_index + 1]

            entry = self.dol.get_galaxy_unlock_table_entry_by_name(galaxy.name)
            entry.power_star_requirement = star_requirement
            entry.return_dome = galaxy.dome_index
            self.dol.galaxy_unlock_table.set_entry(entry)

    def update_instructions(self) -> None:
        #######################################################
        # Skip opening cutscene and go immediately to gateway #
        #######################################################
        address = 0x803bb3cc
        new_instruction = b'\x38\x60\x00\x00'
        self.dol.write_data(fs.write_bytes, address, new_instruction)
        
        #######################################
        # Miniature galaxy orbit manipulation #
        #######################################
        # Get obj_arg0 from miniature galaxy
        address = 0x80200758
        new_instruction = b'\x80\x7f\x00\x8c'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Shift 16 bits to the right to get the upper bits where the custom index is stored
        address = 0x8020075c
        new_instruction = b'\x54\x63\x84\x3e'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        ################################
        # Scenario select star loading #
        ################################
        # Keep loading regular stars even if they're not available yet
        address = 0x8037d9ec
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Calculate all secret/comet stars, including possibly normally unavailable ones
        address = 0x8037da44
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Show secret/comet stars as calculated above
        address = 0x8037db54
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Set visibility to 1 (not collected) if appearing as collected has failed (ensuring it shows up even if not available)
        address = 0x8037db18
        new_instruction = b'\x38\xc0\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Always show up and appear correctly as collected/not collected
        address = 0x8037db74
        new_instruction = b'\x38\xc6\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)
        
        #######################################
        # Read star count from memory address #
        #######################################
        # Load upper 2 bytes of memory pointer (0x8000)
        address = 0x803b10fc
        new_instruction = b'\x3f\x80\x80\x00'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Load lower 2 bytes of memory pointer (0x1880), and load the byte at 0x80001880 into r3
        address = 0x803b1100
        new_instruction = b'\x88\x7c\x18\x80'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        # Skip the rest of the normal function
        address = 0x803b1104
        new_instruction = b'\x48\x00\x00\x38'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        ###################################
        # Custom powerstar colour loading #
        ###################################
        address = 0x8020f270
        new_instruction = b'\x7c\x7f\x1b\x78\x48\x1e\x68\x45\x7c\x64\x1b\x78\x48\x1a\x12\xc9\x80\x63\x00\x0c\x48\x1a\x21\x0d\x3c\x80\x80\x00\x60\x84\x18\xff\x1c\x63\x00\x08\x7c\x63\x22\x14\x7c\x63\xf8\xae'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        #########################
        # Skip wii strap screen #
        #########################
        address = 0x80340408
        new_instruction = b'\x38\x8d\xcf\x80'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        address = 0x803406ac
        new_instruction = b'\x38\x80\x00\x00'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        address = 0x803406d0
        new_instruction = b'\x38\x80\x00\x00'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        #################################################
        # Show the bros button to select Mario or Luigi #
        #################################################
        address = 0x8017cd70
        new_instruction = b'\x38\x60\x00\x01'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        ####################
        # Custom Functions #
        ####################
        # Jump to custom section
        address = 0x803995c0
        new_instruction = b'\x48\x31\x49\xd1'
        self.dol.write_data(fs.write_bytes, address, new_instruction)

        self.dol.custom_section.deathlink()
        

    def save_all(self) -> None:
        """
        Save all the changes made to the different files back to the ISO.
        Saves:
            Mario.arc
            AstroGalaxy.arc
            AstroDomeScenario.arc
            AstroDome.arc
            AstroDomeEntrance[name].arc
            main.dol
        """
        self.mario.save()
        self.astrogalaxy.save()
        self.astrodomescenario.save()
        self.astrodome.save()
        self.astrodomeentrances.save()
        self.dol.save()

        #self.save_copies()

    def save_copies(self):
        self.mario.save_to_new_file("MarioCopy.arc")
        self.astrogalaxy.save_to_new_file("AstroGalaxyCopy.arc")
        self.astrodomescenario.save_to_new_file("AstroDomeScenarioCopy.arc")
        self.astrodome.save_to_new_file("AstroDomeCopy.arc")

        for entrance in self.astrodomeentrances.entrances:
            entrance.save_to_new_file(f"AstroDomeEntrance{entrance.name}Copy.arc")
        
        with open("main.dol", 'wb') as f:
            f.write(self.dol.data.getvalue())

class SuperMarioGalaxyRandomiser(APAutoPatchInterface, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    patch_file_ending = ".apsmg"
    result_file_ending = ".iso"

    @staticmethod
    def patch(patch_path: str) -> None:
        # Get the data from the generated output to use for patching
        with zipfile.ZipFile(patch_path, "r") as zf:
            output = json.loads(zf.read("patch.json").decode('shift-jis'))

        patch_name: str = os.path.split(patch_path)[1].split('.')[0]
        patch = Patch(patch_name, output)

        galaxies: dict[str, str] = patch.galaxies
        galaxy_counts: dict[str, int] = patch.counts
        dome_shuffle = {i: int(patch.dome_shuffle[f"Dome {i}"].removeprefix("Dome ")) for i in range(1,7)}

        patch.update_mario()
        
        galaxy_shuffle: list[GalaxyDestination] = GalaxyShuffle(galaxies).galaxy_destinations
        
        dome_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "dome"]
        luma_galaxies = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "luma"]
        gateway_galaxy = [galaxy for galaxy in galaxy_shuffle if galaxy.type == "gateway"][0]

        patch.update_visual_astrodomes(dome_shuffle)

        patch.update_astrodomes(dome_galaxies, dome_shuffle)
        patch.update_astrogalaxy(luma_galaxies)
        patch.update_gateway_location(gateway_galaxy)

        patch.update_nameobjfactory(dome_galaxies, luma_galaxies)
        patch.update_galaxyunlocktable(dome_galaxies, galaxy_counts)
        patch.update_instructions()

        patch.save_all()
        patch.repack_iso()

        # REMOVE WHEN RELEASED
        import winsound
        winsound.MessageBeep(winsound.MB_OK)
        

class SMGPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsmg"

    def __init__(self, player_choices: dict, patch_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.json", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

if __name__ == "__main__":
    patch_path = r"C:/Users/sebas/Documents/GitHub/Archipelago/output/AP_91073106683428351458_P1_Player1.apsmg"
    
    SuperMarioGalaxyRandomiser.patch(patch_path)
