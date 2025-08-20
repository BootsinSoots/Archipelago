""" Luigi's Mansion GUI Module. Subclasses CommonContext and TrackerGameContext."""
import Utils
from .Items import BOO_AP_ID_LIST
from .LMGui import build_gui, GameManager, MDLabel

# Load Universal Tracker modules with aliases
_tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext, UT_VERSION, logger
    _tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, logger

CLIENT_VERSION = "V0.5.4"

class LMUniversalContext(CommonContext):
    tracker_enabled: bool = False

    def __init__(self, server_address, password):
        """
        Initialize the Luigi's Mansion Universal Context.

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication.
        """
        super().__init__(server_address, password)
        self.tracker_enabled = _tracker_loaded

    def make_gui(self):
        ui: GameManager = super().make_gui()
        class LMGuiWrapper(ui):
            wallet_ui: MDLabel
            boo_count: MDLabel
            base_title = f"Luigi's Mansion {CLIENT_VERSION}"

            def build(self):
                container = super().build()
                if _tracker_loaded:
                    if not _check_universal_tracker_version():
                        Utils.messagebox("Universal Tracker needs updated", "The minimum version of Universal Tracker required for LM is v0.2.11", error=True)
                        raise ImportError("Need to update universal tracker version to at least v0.2.11.")
                    self.base_title += f" | Universal Tracker {UT_VERSION}"
                self.base_title += " |  Archipelago"

                build_gui(self)
                return container

            async def get_wallet_value_async(self):
                current_worth = 0
                if self.ctx.check_ingame():
                    current_worth = self.ctx.wallet.get_wallet_worth()

                self.wallet_ui.text = f"Wallet:{current_worth}/{self.ctx.wallet.get_rank_requirement()}"

            async def update_boo_count_label_async(self):
                curr_boo_count = len(set(([item.item for item in self.ctx.items_received if item.item in BOO_AP_ID_LIST])))
                self.boo_count.text = f"Boo Count: {curr_boo_count}/50"

        return LMGuiWrapper

    def ut_generate(self):
        if self.tracker_enabled:
            self.run_generator()
            self.tags.remove("Tracker")
        else:
            logger.warning("Could not find Universal Tracker.")

def _check_universal_tracker_version() -> bool:
    import re
    if not _tracker_loaded:
        return False

    # We are checking for a string that starts with v contains any amount of digits followed by a period
    # repeating three times (e.x. v0.2.11)
    match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
    if len(match.groups()) < 2:
        return False
    if int(match.groups()[0]) < 2:
        return False
    if int(match.groups()[1]) < 11:
        return False

    return True