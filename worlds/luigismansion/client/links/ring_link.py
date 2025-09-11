""" Manages RingLink interactions between Luigi's Mansion Client and the Archipelago Server. """

import uuid
import logging
import time

from .network_engine import ArchipelagoNetworkEngine, RingNetworkRequest
from .link_base import LinkBase
from ..wallet_manager import WalletManager
from ..constants import AP_LOGGER_NAME

logger = logging.getLogger(AP_LOGGER_NAME)

class RingLinkConstants():
    FRIENDLY_NAME = "RingLink"
    SLOT_NAME = "ring_link"

class RingLink(LinkBase):
    wallet_manager: WalletManager
    ring_multiplier = 5
    timer_start: time = time.time()
    pending_rings: int = 0
    remote_pending_rings: int = 0

    def __init__(self, network_engine: ArchipelagoNetworkEngine, wallet_manager: WalletManager):
        super().__init__(friendly_name=RingLinkConstants.FRIENDLY_NAME, slot_name=RingLinkConstants.SLOT_NAME,
            network_engine=network_engine)
        self.wallet_manager = wallet_manager
        self.id = str(uuid.uuid4())

    def on_bounced(self, args):
        data = args["data"]
        source_name = data["source"]
        if self.is_enabled() and RingLinkConstants.FRIENDLY_NAME in args["tags"] and source_name != self.id:
            base_amount = data["amount"]
            amount = _calc_rings(self, base_amount)

            calculated_ring_worth = self.wallet_manager.wallet.get_calculated_amount_worth(1)
            if amount > 0:
                logger.info("%s: Somebody got %s coin(s)!",RingLinkConstants.FRIENDLY_NAME, amount)
                currencies = self.wallet_manager.add_currencies(int(amount * calculated_ring_worth))
                self.wallet_manager.wallet.add_to_wallet(currencies)
                self.remote_pending_rings += amount
            elif amount < 0:
                logger.info("%s: Somebody lost %s coin(s).", RingLinkConstants.FRIENDLY_NAME, amount)
                currencies = self.wallet_manager.remove_currencies(amount, calculated_ring_worth)
                self.wallet_manager.wallet.remove_from_wallet(currencies)
                self.remote_pending_rings -= amount

    async def handle_ring_link_async(self, delay: int = 5):
        timer_end = time.time()

        # this is the first time the function is run and shouldn't continue if true.
        initial_check: bool = self.wallet_manager.previous_amount == 0
        pending_rings: int = self.wallet_manager.calc_wallet_differences()

        if initial_check:
            return

        self.pending_rings += pending_rings

        if self.remote_pending_rings != 0:
            self.pending_rings -= self.remote_pending_rings
            self.remote_pending_rings = 0

        if timer_end - self.timer_start >= delay:
            amount_to_send, remainder = divmod(self.pending_rings, self.ring_multiplier)

            if amount_to_send == 0:
                return

            await self.send_rings_async(amount_to_send)
            self.pending_rings = remainder
            self.timer_start = time.time()

    async def send_rings_async(self, amount: int):
        if amount != 0:
            ring_link_req = RingNetworkRequest([ RingLinkConstants.FRIENDLY_NAME ], int(amount))
            ring_link_req.source = self.id

            logger.info("%s: You sent %s rings!", RingLinkConstants.FRIENDLY_NAME, int(amount))
            await self.network_engine.send_ring_link_request_async(ring_link_req)

def _calc_rings(ring_link: RingLink, amount: int) -> int:
    amount_to_update, remainder = divmod(amount + ring_link.remote_pending_rings, ring_link.ring_multiplier)
    ring_link.remote_pending_rings = remainder

    return amount_to_update
