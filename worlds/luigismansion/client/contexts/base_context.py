""" Base context for Luigi's Mansion's game tab in the client. """

import Utils

from .universal_context import UniversalContext, UniversalCommandProcessor, logger
from ..links.network_engine import ArchipelagoNetworkEngine
from ..links.energy_link.energy_link_client import EnergyLinkClient
from ..links.trap_link import TrapLink
from ..links.ring_link import RingLink
from ..links.link_base import LinkBase
from ..wallet import Wallet
from ..wallet_manager import WalletManager
from ...client.constants import CLIENT_VERSION

class BaseCommandProcessor(UniversalCommandProcessor):
    pass

class BaseContext(UniversalContext):
    network_engine: ArchipelagoNetworkEngine
    wallet: Wallet
    energy_link: EnergyLinkClient
    trap_link: TrapLink
    ring_link: RingLink

    def __init__(self, server_address, password):
        """
        Initialize the Luigi's Mansion Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        self.network_engine = ArchipelagoNetworkEngine(self)
        self.wallet = Wallet()
        self.trap_link = TrapLink(self.network_engine)
        self.ring_link = RingLink(self.network_engine, WalletManager(self.wallet))
    
    def on_connected(self, args):
        tags: list[str] = []
        if _check_tag(self.trap_link, self.network_engine, args):
            tags.append(self.trap_link.friendly_name)
        if _check_tag(self.ring_link, self.network_engine, args):
            tags.append(self.ring_link.friendly_name)
        if len(tags) > 0:
            Utils.async_start(self.network_engine.update_client_tags_async(tags), name="UpdateClientTags")

        self.trap_link.on_connected(args)

    def make_gui(self):
        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from .lm_tab import build_gui, GameManager, MDLabel, MDLinearProgressIndicator

        ui: GameManager = super().make_gui()
        class LMGuiWrapper(ui):
            wallet_ui: MDLabel
            boo_count: MDLabel
            wallet_progress_bar: MDLinearProgressIndicator
            base_title = f"Luigi's Mansion {CLIENT_VERSION}"

            def build(self):
                container = super().build()

                self.base_title += " |  Archipelago"
                build_gui(self)

                return container

            def get_wallet_value(self):
                current_worth = 0
                total_worth = self.ctx.wallet.get_rank_requirement()

                if self.ctx.check_ingame():
                    current_worth = self.ctx.wallet.get_wallet_worth()

                self.wallet_ui.text = f"{format(current_worth, ',d')}/{format(total_worth, ',d')}"
                if total_worth != 0:
                    self.wallet_progress_bar.value = current_worth/total_worth
                else:
                    self.wallet_progress_bar.value = 100

            def update_boo_count_label(self, item_count: int):
                boo_total = 50
                self.boo_count.text = f"{item_count}/{boo_total}"
                self.boo_progress_bar.value = item_count/boo_total

            def update_flower_label(self, count: int):
                self.flower_label.text = f"{count}"

            def update_vacuum_label(self, item_count: int):
                self.vacuum_label.text = f"{item_count}"

        return LMGuiWrapper

def _check_tag(link: LinkBase, network_engine: ArchipelagoNetworkEngine, args) -> bool:
    return link.slot_name in args["slot_data"] and link.friendly_name not in network_engine.get_tags()