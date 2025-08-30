""" Luigi's Mansion GUI Module. Subclasses CommonContext and TrackerGameContext."""
import Utils

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
        # Performing local import to prevent additional UIs to appear during the patching process.
        # This appears to be occurring if a spawned process does not have a UI element when importing kvui/kivymd.
        from .LMGui import build_gui, GameManager, MDLabel, MDLinearProgressIndicator

        ui: GameManager = super().make_gui()
        class LMGuiWrapper(ui):
            wallet_ui: MDLabel
            boo_count: MDLabel
            wallet_progress_bar: MDLinearProgressIndicator
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

    def _main(self):
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
