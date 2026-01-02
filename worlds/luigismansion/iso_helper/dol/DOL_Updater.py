import struct
from typing import TYPE_CHECKING

from gclib.dol import DOL, DOLSection
from gclib.fs_helpers import write_magic_str

from ...Regions import REGION_LIST, LMRegionInfo
from ...Helper_Functions import PROJECT_ROOT

if TYPE_CHECKING:
    from ..LM_Randomize_ISO import LuigisMansionRandomizer

CUSTOM_CODE_OFFSET_START = 0x39FA20
LM_PLAYER_NAME_BYTE_LENGTH = 64


def update_dol_offsets(lm_gen: "LuigisMansionRandomizer"):
    """ Updates the main DOL file, which is the main file used for GC and Wii games. This section includes some
    custom code inside the DOL file itself."""
    # Define all variables from the output data
    start_inv: list[str] = list(lm_gen.output_data["Options"]["start_inventory"])
    walk_speed: int = int(lm_gen.output_data["Options"]["walk_speed"])
    slot_name: str = str(lm_gen.output_data["Name"])
    random_spawn: str = str(lm_gen.output_data["Options"]["spawn"])
    king_boo_health: int = int(lm_gen.output_data["Options"]["king_boo_health"])
    fear_anim_enabled: bool = bool(lm_gen.output_data["Options"]["enable_fear_animation"])
    pickup_anim_enabled: bool = bool(lm_gen.output_data["Options"]["enable_pickup_animation"])
    boo_rando_enabled: bool = bool(lm_gen.output_data["Options"]["boosanity"])
    door_model_enabled: bool = bool(lm_gen.output_data["Options"]["door_model_rando"])

    # Find the main DOL file and read it.
    lm_dol = DOL()
    dol_data = lm_gen.lm_gcm.read_file_data("sys/main.dol")
    lm_dol.read(dol_data)

    # Walk Speed
    speed_to_use = 16784 if walk_speed == 0 else (16850 if walk_speed == 1 else 16950)
    lm_dol.data.seek(0x396538)
    lm_dol.data.write(struct.pack(">H", speed_to_use))

    # Update Vanilla Vac Speed based on if at least one upgrade is available in start inventory
    vac_count = len(list("Vacuum Upgrade" in key for key in start_inv))
    vac_speed = "3800000F" if vac_count >= 1 else "800D0160"
    lm_dol.data.seek(0x7EA28)
    lm_dol.data.write(bytes.fromhex(vac_speed))

    # Fix Boos to properly spawn
    lm_dol.data.seek(0x12DCC9)
    boo_data = "000005"
    lm_dol.data.write(bytes.fromhex(boo_data))

    # Turn on custom code handler for boo display counter only if Boo Rando is on. These are static changes from vanilla.
    if boo_rando_enabled:
        # Shift for y offset using custom boo counter display
        lm_dol.data.seek(0x04DB50)
        lm_dol.data.write(bytes.fromhex("93C1FFF0"))

        # Custom boo display counters.
        lm_dol.data.seek(0x04DBB0)
        lm_dol.data.write(bytes.fromhex("4848D469"))
        lm_dol.data.seek(0x04DC10)
        lm_dol.data.write(bytes.fromhex("4848D409"))

    # Turn on/off pickup animations
    if pickup_anim_enabled:
        keys_and_others_val = "02"
        gem_val = "06"
        hat_val = "06"
        elem_val = "16"
    else:
        keys_and_others_val = "01"
        gem_val = "05"
        hat_val = "05"
        elem_val = "15"

    # Keys and important animations
    lm_dol.data.seek(0xCD39B)
    lm_dol.data.write(bytes.fromhex(keys_and_others_val))

    # Diamonds and other treasure animations
    lm_dol.data.seek(0xCE8D3)
    lm_dol.data.write(bytes.fromhex(gem_val))

    # Disable Mario Item pickup animations
    lm_dol.data.seek(0x0CD707)
    lm_dol.data.write(bytes.fromhex(hat_val))

    # Disable Elemental Medal pickup animations
    lm_dol.data.seek(0x0CF4A3)
    lm_dol.data.write(bytes.fromhex(elem_val))

    # Turn on/off luigi scare animations
    if fear_anim_enabled:
        scare_val = [0x44]
    else:
        scare_val = [0x00]
    lm_dol.data.seek(0x396578)
    lm_dol.data.write(struct.pack(">B", *scare_val))

    # Store Player name
    lm_player_name = str(slot_name).strip()
    write_magic_str(lm_dol.data, 0x324740, lm_player_name, LM_PLAYER_NAME_BYTE_LENGTH)

    # Change King Boo's Health
    lm_dol.data.seek(0x399228)
    lm_dol.data.write(struct.pack(">H", king_boo_health))

    # Replace section two with our own custom section, which is about 1000 hex bytes long.
    new_dol_size = 0x1000
    new_dol_sect = DOLSection(CUSTOM_CODE_OFFSET_START, 0x804DD940, new_dol_size)
    lm_dol.sections[2] = new_dol_sect

    # Append the extra bytes we expect, to ensure we can write to them in memory.
    lm_dol.data.seek(len(lm_dol.data.getvalue()))
    blank_data = b"\x00" * new_dol_size
    lm_dol.data.write(blank_data)

    vanilla_game_changes(lm_dol)

    # Read in all the other custom DOL changes and update their values to the new value as expected.
    custom_dol_code = PROJECT_ROOT.joinpath("iso_helper").joinpath("dol").joinpath("LM_custom_code.lmco").read_bytes()
    lm_dol.data.seek(CUSTOM_CODE_OFFSET_START)
    lm_dol.data.write(custom_dol_code)

    read_and_update_hooks(lm_dol)

    if not random_spawn == "Foyer": # TODO Need to change this dynamically
        spawn_info: LMRegionInfo = REGION_LIST[random_spawn]
        lm_dol.data.seek(0x3A05E0)
        lm_dol.data.write(struct.pack(">f", spawn_info.pos_x))
        lm_dol.data.seek(0x3A05E4)
        lm_dol.data.write(struct.pack(">f", spawn_info.pos_y))
        lm_dol.data.seek(0x3A05E8)
        lm_dol.data.write(struct.pack(">f", spawn_info.pos_z))

    if door_model_enabled:
        # Each is 6 bytes off from the start door offset.
        # List of all doors we want to change on map2 (Main Mansion)
        door_model_offsets: list[int] = [0x2FFFBE, 0x2FFFDA, 0x2FFFF6, 0x300012, 0x30004A, 0x300066, 0x300082,
            0x30009E, 0x3000BA, 0x3000D6, 0x300146, 0x300162, 0x30017E, 0x30019A, 0x3001B6, 0x3001D2, 0x3001EE,
            0x30020A, 0x300242, 0x30025E, 0x30027A, 0x3002B2, 0x3002CE, 0x3002EA, 0x300306, 0x30035A, 0x3003AE,
            0x3003CA, 0x3003E6, 0x300402, 0x30043A, 0x300456, 0x300472, 0x30048E, 0x3004C6, 0x3004E2, 0x3004FE,
            0x30051A, 0x30056E, 0x30058A, 0x3005A6, 0x3005DE, 0x3005FA, 0x300616, 0x300632, 0x30064E, 0x300686,
            0x3006A2, 0x3006BE, 0x3006DA, 0x3006F6, 0x300712, 0x30072E, 0x30074A]
        # List of all doors we want to change on map6 (Gallery)
        door_model_offsets += [0x300C56, 0x300C72]
        for map_two_doors in door_model_offsets:
            lm_dol.data.seek(map_two_doors)
            door_model_id = lm_gen.random.randint(1,14)
            lm_dol.data.write(door_model_id.to_bytes())

    # Save all changes to the DOL itself.
    lm_dol.save_changes()
    lm_gen.lm_gcm.changed_files["sys/main.dol"] = lm_dol.data


def vanilla_game_changes(dol_data: DOL):
    # Updates LM to allow the GC debug screen to be shown/used.
    dol_data.data.seek(0x00277C)
    dol_data.data.write(bytes.fromhex("60000000"))

    # Disables the 1F Washroom door from auto-unlocking
    dol_data.data.seek(0x019040)
    dol_data.data.write(bytes.fromhex("60000000"))

    # Disable Van-Gogh Easel/Chest Zoom
    dol_data.data.seek(0x0339CC)
    dol_data.data.write(bytes.fromhex("60000000"))

    # Force Storage Room Wall to stay open
    dol_data.data.seek(0x03458C)
    dol_data.data.write(bytes.fromhex("38600001"))

    # Force Skip the opening cutscene
    dol_data.data.seek(0x047500)
    dol_data.data.write(bytes.fromhex("38600002"))

    # Disables several flags from automatically turning on in-game
    dol_data.data.seek(0x072428) # Flag 15
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0AC83C) # Flag 56
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0ACE7C) # Flag 39
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0ACE88) # Flag 80
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0ACE94) # Flag 12
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0ACEA0) # Flag 68
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0ACEAC) # Flag 82
    dol_data.data.write(bytes.fromhex("60000000"))

    # Disables some default behaviour for crawl trap
    dol_data.data.seek(0x079E64)
    dol_data.data.write(bytes.fromhex("60000000"))
    dol_data.data.seek(0x0AC304)
    dol_data.data.write(bytes.fromhex("807F07E8"))


def read_and_update_hooks(dol_data: DOL):
    """Reads and updates all the necessary custom code hooks used for the custom features like mirror warp, traps, etc.
    Since these hooks typically start with "04", as they are AR codes, update them to start with "80" instead.
    Once formatted, need to convert the RAM address to a DOL offset instead to update it properly in the DOL file."""

    custom_hooks: list[str] = (PROJECT_ROOT.joinpath("iso_helper").joinpath("dol").joinpath("Code_Hooks.txt")
        .read_text(encoding="utf-8").splitlines())
    for hook_line in custom_hooks:
        ram_addr, dol_val = hook_line.split(" ")
        ram_addr = "80" + ram_addr[2:]
        dol_offset = dol_data.convert_address_to_offset(ram_addr)
        dol_data.data.seek(int(dol_offset, 16))
        dol_data.data.write(bytes.fromhex(dol_val))