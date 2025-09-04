""" Manages TrapLink interactions between Luigi's Mansion Client and the Archipelago Server. """

import dolphin_memory_engine as dme
import Utils

from ..network_engine import ArchipelagoNetworkEngine, TrapNetworkRequest
from ....Items import *
from enum import Flag

class TrapLinkConstants:
    """
    Constants for internal and public facing energy link names.
    """
    FRIENDLY_NAME = "TrapLink"
    SLOT_NAME = "trap_link"

class TrapLinkType(Flag):
    """ A flag collection of Trap types supported in Luigi's Mansion. """
    NONE = 0
    POISON = 1
    ICE = 2
    BANANA = 4
    POSSESSION = 8
    BONK = 16
    GHOST = 32
    FEAR = 64
    BOMB = 128
    SPOOKY = 256
    SQUASH = 512
    NOVAC = 1024

class TrapLink():
    """ Manages interactions between Luigi's Mansion Client, emulator, and Archipelago server. """
    network_engine: ArchipelagoNetworkEngine
    received_trap: bool = False

    # We want to ignore traps if the player set the trap weight to 0.
    disabled_trap_flags: TrapLinkType = TrapLinkType.NONE

    def __init__(self, network_engine: ArchipelagoNetworkEngine):
        self.network_engine = network_engine

    async def handle_traplink_async(self):
        """ Manages remote Traps being sent to Luigi's Mansion. """
        if self.received_trap:
            trap = self.received_trap
            lm_item = ALL_ITEMS_TABLE[trap]
            for addr_to_update in lm_item.update_ram_addr:
                byte_size = 1 if addr_to_update.ram_byte_size is None else addr_to_update.ram_byte_size
                curr_val = addr_to_update.item_count
                if not addr_to_update.pointer_offset is None:
                    dme.write_bytes(dme.follow_pointers(addr_to_update.ram_addr,
                        [addr_to_update.pointer_offset]), curr_val.to_bytes(byte_size, 'big'))
                else:
                    dme.write_bytes(addr_to_update.ram_addr, curr_val.to_bytes(byte_size, 'big'))
            self.received_trap = False

    async def send_trap_link_async(self, trap_name: str):
        """
        Sends a Trap to the Archipelago server.

        :param trap_name: Friendly name of the trap being set.
        """
        if self.is_enabled() or self.network_engine.get_slot() is None:
            return

        await self.network_engine.send_trap_link_request_async(
            TrapNetworkRequest(tags=[ TrapLinkConstants.FRIENDLY_NAME ],
            trap_name=trap_name))

    def on_bounced(self, args):
        """
        Performs traplink operations during the 'Bounced' command in `on_package`.
        
        :param args: The arguments to be passed into the 'Bounced' command.
        """
        data = args["data"]
        source_name = data["source"]
        # if the traplink tag is not present in the client's available tags, and if traplink isn't available in the args tags,
            # and lastly if the source of the trap was local (slot name matches current client's slot name) we don't want to send a trap
        if self.is_enabled() and TrapLinkConstants.FRIENDLY_NAME in args["tags"] and source_name != self.network_engine.get_player_name(self.network_engine.get_slot()):
            trap_name: str = data["trap_name"]
            if trap_name not in ACCEPTED_TRAPS:
                return

            if trap_name in ICE_TRAP_EQUIV and TrapLinkType.ICE not in self.disabled_trap_flags:
                self.received_trap = "Ice Trap"
            elif trap_name in BOMB_EQUIV and TrapLinkType.BOMB not in self.disabled_trap_flags:
                self.received_trap = "Bomb"
            elif trap_name in BANANA_TRAP_EQUIV and TrapLinkType.BANANA not in self.disabled_trap_flags:
                self.received_trap = "Banana Trap"
            elif trap_name in GHOST_EQUIV and TrapLinkType.GHOST not in self.disabled_trap_flags:
                self.received_trap = "Ghost"
            elif trap_name in POISON_MUSH_EQUIV and TrapLinkType.POISON not in self.disabled_trap_flags:
                self.received_trap = "Poison Mushroom"
            elif trap_name in BONK_EQUIV and TrapLinkType.BONK not in self.disabled_trap_flags:
                self.received_trap = "Bonk Trap"
            elif trap_name in POSSESION_EQUIV and TrapLinkType.POSSESSION not in self.disabled_trap_flags:
                self.received_trap = "Possession Trap"
            elif trap_name in FEAR_EQUIV and TrapLinkType.FEAR not in self.disabled_trap_flags:
                self.received_trap = "Fear Trap"
            elif trap_name in SPOOKY_EQUIV and TrapLinkType.SPOOKY not in self.disabled_trap_flags:
                self.received_trap = "Spooky Time"
            elif trap_name in SQUASH_EQUIV and TrapLinkType.SQUASH not in self.disabled_trap_flags:
                self.received_trap = "Squash Trap"
            elif trap_name in NOVAC_EQUIV and TrapLinkType.NOVAC not in self.disabled_trap_flags:
                self.received_trap = "No Vac Trap"

    def on_connected(self, args):
        """
        Performs traplink operations during the 'Connected' command in `on_package`.
        
        :param args: The arguments to be passed into the 'Connected' command.
        """
        slot_data = args["slot_data"]
        Utils.async_start(self.network_engine.update_tags_async(bool(slot_data[TrapLinkConstants.SLOT_NAME]),
            TrapLinkConstants.FRIENDLY_NAME), name=f"Update {TrapLinkConstants.FRIENDLY_NAME}")
        # The flags are cast to an int when sent to the server, so they need to be cast back to the enum.
        self.disabled_trap_flags = TrapLinkType(slot_data["disabled_traps"])

    def is_enabled(self) -> bool:
        """ Determines if traplink is enabled in the client. """
        return TrapLinkConstants.FRIENDLY_NAME in self.network_engine.get_tags()
