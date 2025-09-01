""" Base context for Luigi's Mansion's game tab in the client. """

from .universal_context import UniversalContext, UniversalCommandProcessor, logger
from ..ap_link.network_engine import ArchipelagoNetworkEngine
from ...client.constants import CLIENT_VERSION

class BaseCommandProcessor(UniversalCommandProcessor):
    pass

class BaseContext(UniversalContext):
    network_engine: ArchipelagoNetworkEngine

    def __init__(self, server_address, password):
        """
        Initialize the Luigi's Mansion Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        self.network_engine = ArchipelagoNetworkEngine(self)

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