from __future__ import annotations
import asyncio
from enum import Enum, StrEnum
import struct
import sys

import Utils

from typing import Callable, NamedTuple, Optional
from CommonClient import CommonContext, ClientCommandProcessor, logger, server_loop, gui_enabled, get_base_parser
from worlds.smgalaxy.Patch.Patch import SuperMarioGalaxyRandomiser

from .locations import SMG2LocationData, location_table
from .regions import SMG2RegionData, region_list
from .Constants.ram_constants import *
from .items import SMG2ItemData, item_table

import os
import copy
import dolphin_memory_engine as dme
clientname: str = "SMG Client"
# All the dolphin connection messages used in the client
CONNECTION_REFUSED_STATUS: str = "Detected a non-randomized ROM for SMG. Please close and load a different one. Retrying in 5 seconds..."
CONNECTION_LOST_STATUS: str = "Dolphin connection was lost. Please restart your emulator and make sure SMG is running."
NO_SLOT_NAME_STATUS: str = "No slot name was detected. Ensure a randomized ROM is loaded. Retrying in 5 seconds..."
CONNECTION_VERIFY_SERVER: str = "Dolphin was confirmed to be opened and ready, Connect to the server when ready..."
CONNECTION_INITIAL_STATUS: str = "Dolphin emulator was not detected to be running. Retrying in 5 seconds..."
DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY: str = "Dolphin did not load the ROM correctly. Close only the game / dolphin launcher and try again..."
CONNECTION_CONNECTED_STATUS: str = "Dolphin is connected, AP is connected, Ready to play SMG!"
AP_REFUSED_STATUS: str = "AP Refused to connect for one or more reasons, see above for more details."
EXPECTED_GAME_ID: str = "RMGE01"
WAIT_TIMER_LONG_TIMEOUT: int = 5
WAIT_TIMER_SHORT_TIMEOUT: float = 0.125

class TypeTuple(NamedTuple):
    format: str
    size: int

class ValueType(Enum):
    u8 = TypeTuple(">B", 1)
    u16 = TypeTuple(">H", 2)
    u32 = TypeTuple(">I", 4)
    s8 = TypeTuple(">b", 1)
    s16 = TypeTuple(">h", 2)
    s32 = TypeTuple(">i", 4)
    string32 = TypeTuple(">32s", 32)

class Pointer:
    address: int
    offsets: list[int]
    value_type: ValueType

    def __init__(self, offsets: list[int], value_type: ValueType):
        self.address = -1
        self.offsets = offsets
        self.value_type = value_type

    async def recalculate(self):
        """Recalculates the address of the offset chain."""
        if self.address == -1:
            raise ValueError("Address of pointer is not initialised")
        
        self.address = dme.follow_pointers(GAMESYSTEM, self.offsets)

    async def get_value(self) -> int | str:
        """Gets the value of the pointer at its address."""
        value = dme.read_bytes(self.address, self.value_type.value.size)
        return struct.unpack(self.value_type.value.format, value)[0]
    
    def write_value(self, value) -> None:
        """Write a value at the addresss of the pointer."""
        value = struct.pack(self.value_type.value.format, value)
        dme.write_bytes(self.address, value)

class GalaxyCommand(ClientCommandProcessor):
    # command to print dolphin status
    def _cmd_dolphin(self):
        """Prints the current Dolphin status to the client."""
        if isinstance(self.ctx, GalaxyContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")
        
    # command to print deathlink status
    # commented out till we implement deathlink
#    def _cmd_deathlink(self):
#        """Toggle deathlink from client. Overrides default setting."""
#        if isinstance(self.ctx, GalaxyContext):
#            Utils.async_start(self.ctx.update_death_link(not "DeathLink" in self.ctx.tags))

class GalaxyContext(CommonContext):
    password_required: bool = False
    rom_loaded: bool = False
    command_processor = GalaxyCommand
    game: str = "Super Mario Galaxy"
    items_handling = 0b111
    runloop: Optional[asyncio.Task[None]] = None
    dolphin_status: str = CONNECTION_INITIAL_STATUS
    last_galaxy: str = ""
    needs_recalculating: bool = True
    pointers: dict[str, Pointer] = {}

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for SMG Client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = f"Archipelago | {clientname}"
        return ui
    
    def __init__(self, server_address, password):
        """
        Initialize the SMG context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)

        # Create pointer dictionary for all the galaxy star flags
        star_count_flag_pointers = {value.in_game_name: Pointer(GALAXY_DATA_POINTER_LIST + [value.region_offset, STAR_BIT_FLAG_OFFSET], ValueType.u16) for value in region_list.values() if value.region_offset is not None}

        self.pointers = {**star_count_flag_pointers,
                         "Scene Name": Pointer(CURRENT_SCENE_POINTER_LIST, ValueType.string32),
                         "Galaxy Name": Pointer(CURRENT_GALAXY_POINTER_LIST, ValueType.string32),
                         "Lives": Pointer(ONEUP_POINTER_LIST, ValueType.u16)}

    async def wait_for_next_loop(self, time_to_wait: float):
        await asyncio.sleep(time_to_wait)

    async def check_ingame(self) -> bool:
        """Checks to see if Mario/Luigi is in game and not at file select."""
        game_status: str = await self.pointers["Scene Name"].get_value()
        curr_galaxy: str = await self.current_galaxy()
        
        return game_status == "Game" and curr_galaxy != "FileSelect"

    async def current_galaxy(self):
        """Updates what Galaxy the user is currently on, but for some weird reason also tracks if you are in FileSelect.
        Everything else including Domes, the Observatory Ship and even the intro planet has a galaxy name."""
        return await self.pointers["Galaxy Name"].get_value()
    
    async def last_visited_galaxy(self):
        """Updates the last Galaxy Mario/Luigi was on."""
        if not await self.check_ingame():
            return

        curr_galaxy: str = await self.current_galaxy()

        if curr_galaxy != self.last_galaxy:
            self.needs_recalculating = True

        if curr_galaxy in ["AstroDome", "AstroGalaxy"]:
            return

        self.last_galaxy = curr_galaxy
    
    async def smg_location_checker(self):
        """Checks the various location within SMG to see if the player has completed any appropriate actions"""
        if not await self.check_ingame():
            return
        
        local_missing_locs = copy.deepcopy(self.missing_locations)
        star_bit_flag: int | None = None

        for loc_id in local_missing_locs:
            local_loc: SMG2LocationData = location_table[self.location_names.lookup_in_game(loc_id)]
            region_data: SMG2RegionData = region_list[local_loc.region]

            if region_data.in_game_name != self.last_galaxy:
                continue

            if local_loc.game_address is None:
                continue

            if star_bit_flag is None:
                star_bit_flag: int = self.pointers[region_data.in_game_name].get_value()

            if (star_bit_flag & (1 << local_loc.game_address)) > 0:
                self.locations_checked.add(loc_id)
                logger.info(loc_id)

        await self.check_locations(self.locations_checked)
    
    async def writeitems(self):
        """Modify the items we have received to change things in game"""
        if not await self.check_ingame():
            return
        
        #note will resend items upon reconnection
        for item_id in self.items_received[self.highest_processed_item_index :]:
            self.highest_processed_item_index += 1
            logger.info(item_id.item)

            match item_id.item:
                case 170000007:
                    logger.info("1up Received")
                    lives = self.pointers["Lives"].get_value()
                    self.pointers["Lives"].write_value(lives + 1)

            #note currently adding these in breaks lives adding(might fix once changing that value does something?)
            #   case 170000004:
            #     logger.debug("Power Star Received")
            #     stars = int.from_bytes(dme.read_bytes(0x80001880, 4))
            #     dme.write_bytes(0x80F63CF0, (stars + 1).to_bytes(4))

            #   case 170000005:
            #     logger.debug("Grand Star Received")
            #     stars = int.from_bytes(dme.read_bytes(0x80001880, 4))
            #     dme.write_bytes(0x80F63CF0, (stars + 1).to_bytes(4))

            #   case 170000006:
            #     logger.debug("Green Star Received")
            #     stars = int.from_bytes(dme.read_bytes(0x80001880, 4))
            #     dme.write_bytes(0x80F63CF0, (stars + 1).to_bytes(4))

            self.items_received.remove(item_id)
    
    async def recalculate_pointers(self):
        if self.needs_recalculating:
            for pointer in self.pointers.values():
                await pointer.recalculate()
        
        self.needs_recalculating = False

    async def dolphinloop(self):
        logger.info("Starting Dolphin connector. Use /dolphin for status information.")
        try:
            while(not self.exit_event.is_set()):
                try:
                    # If DME is not already hooked or connected in any way
                    if not dme.is_hooked():
                        dme.hook()
                        if dme.get_status() == dme.get_status().noEmu or dme.get_status() == dme.get_status().notRunning:
                            dme.un_hook()

                            self.dolphin_status = CONNECTION_INITIAL_STATUS
                            logger.info(self.dolphin_status)

                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                    if not self.dolphin_status == CONNECTION_CONNECTED_STATUS:
                        #checks the id of the game as a string
                        romgameid: str = dme.read_bytes(0x80000000,6)
                        if romgameid.decode() != EXPECTED_GAME_ID:
                            dme.un_hook()

                            self.dolphin_status = DOLPHIN_DIDNT_LOAD_ROM_CORRECTLY
                            logger.info(self.dolphin_status)

                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                        if not self.auth:
                            await self.get_username()
                            
                        # Inform the player we are ready and waiting for them to connect.
                        if not self.rom_loaded:
                            self.dolphin_status = CONNECTION_VERIFY_SERVER
                            logger.info(self.dolphin_status)

                            self.rom_loaded = True
                            await self.server_auth(self.password_required)

                        if not self.slot:
                            await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                            continue

                    await self.recalculate_pointers()

                    # Currently verified connected to AP and dolphin is properly loaded
                    await self.last_visited_galaxy()
                    await self.smg_location_checker()
                    await self.writeitems()
                    await self.wait_for_next_loop(WAIT_TIMER_SHORT_TIMEOUT)

                except Exception as dmeEx:
                    await self.disconnect()

                    logger.error("Something went wrong when connection to Dolphin Memory Engine details: " + str(dmeEx))

                    dme.un_hook()

                    self.dolphin_status = CONNECTION_LOST_STATUS
                    logger.info(self.dolphin_status)
                    
                    self.rom_loaded = False
                    self.needs_recalculating = True
                    
                    await self.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)
                    continue

        except Exception as dolphinEx:
            logger.error("Something went wrong when connection to dolphin details:" + str(dolphinEx))

    def on_package(self, cmd, args):
        super().on_package(cmd, args)
        
        match cmd:
            case "RoomInfo":
                self.password_required = bool(args["password"])
            
            case "Connected":
                self.highest_processed_item_index = 0
                #TODO: UNCOMMENT WHEN STAR RECEIVING WORKS PROPERLY
                # dme.write_bytes(0x80F63CF0, 0.to_bytes(4))
                pass

            case "Connection Refused":
                pass

    def on_deathlink(self, data: dict[str, Any]):
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)

        self.is_dead = True
        
        dme.write_byte(0x80001af0, 1)
        return

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server. This function will be called as part of the init RoomInfo call
        in CommonClient, however we will exit if the rom is not loaded yet.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if not self.rom_loaded:
            logger.info("ROM is not loaded yet, waiting for dolphin to be connected before trying again.")
            return

        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()

        await self.send_connect()

# launches/starts everything we need
def launch(*launch_args: str):
    import colorama
    Utils.init_logging(clientname)
    logger.info("Starting SMG Client")
    
    parser = get_base_parser()
    parser.add_argument("apsmg_file", default="", type=str, nargs="?", help="Path to an AP SMG file")
    args = parser.parse_args(launch_args)

    if args.apsmg_file:
        SuperMarioGalaxyRandomiser().patch(args.apsmg_file)

    async def _main(connect, password):
        try:
            ctx = GalaxyContext(connect, password)
            ctx.server_task = asyncio.create_task(server_loop(ctx), name="SMG - ServerLoop")

            if gui_enabled:
                ctx.run_gui()
            ctx.run_cli()
            await ctx.wait_for_next_loop(WAIT_TIMER_LONG_TIMEOUT)

            ctx.runloop = asyncio.create_task(ctx.dolphinloop(), name="SMG - DolphinSync")

            await ctx.exit_event.wait()
            await ctx.shutdown()

            if ctx.runloop:
                await ctx.runloop

        except Exception as clientEx:
            client_msg: str = (f"An unknown error occurred while running {clientname}.\n" +
                f"Additional details:\n{str(clientEx)}")
            logger.error(client_msg)
            Utils.messagebox(f"Main Client Issue {clientname}", client_msg, True)
            raise clientEx
        
    colorama.just_fix_windows_console()
    asyncio.run(_main(args.connect, args.password))
    colorama.deinit()

if __name__ == "__main__":
    launch(*sys.argv[1:])
