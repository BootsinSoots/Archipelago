""" Module which adds client commands to a given Archipelago Client. """
import Utils

from CommonClient import logger
from .energy_link_processor import EnergyLinkProcessor, EnergyLinkConstants
from ....LMUniversalContext import LMUniversalCommandProcessor, LMUniversalContext, logger

class EnergyLinkCommandProcessor(LMUniversalCommandProcessor):
    """ EnergyLink client commands. """
    energy_link: EnergyLinkProcessor

    def __init__(self, ctx: LMUniversalContext, server_address: str = None):
        super().__init__(ctx, server_address)
        self.energy_link = EnergyLinkProcessor(ctx)

    def _cmd_send_energy(self, arg: str):
        """ Sends an amount of energy to the server, which is pulled from Luigi's wallet.
        Each point of energy is worth a single coin (rank worth 5000)"""
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.send_energy_async(arg))

    def _cmd_display_energy(self):
        """ Displays the current amount of energy available from the server. """
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.get_energy_async())

    def _cmd_request_energy(self, arg: str):
        """
        Requests energy from the server, which each point has the worth of a single coin (rank worth 5000).
        Will return up to the requested amount based upon the team's energy pool.
        """
        if not _validate_processor_context(self.ctx):
            return

        Utils.async_start(self.energy_link.request_energy_async(arg))

    def _cmd_energy_link(self):
        """Toggle EnergyLink from the client. Overrides default setting."""
        luigismansion_context: LMUniversalContext = self.ctx
        Utils.async_start(luigismansion_context.network_engine.update_tags_async(
            not EnergyLinkConstants.INTERNAL_NAME in self.ctx.tags,
            EnergyLinkConstants.FRIENDLY_NAME),
            name=f"Update {EnergyLinkConstants.FRIENDLY_NAME}")

def _validate_processor_context(ctx: LMUniversalContext):
    has_energy_link: bool = ctx.energy_link is not None
    is_connected_to_server: bool = ctx.server is not None
    if isinstance(ctx, LMUniversalContext) and has_energy_link and is_connected_to_server:
        return True
    logger.warning("Please connect the client to the AP server before continuing.")
    return False
