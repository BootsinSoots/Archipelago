""" Manages RingLink interactions between Luigi's Mansion Client and the Archipelago Server. """

import uuid
import logging
import time

from .network_engine import ArchipelagoNetworkEngine, RingNetworkRequest
from .link_base import LinkBase
from ..wallet_manager import WalletManager, _remove_currencies
from ..constants import AP_LOGGER_NAME
from ...game.Currency import CURRENCY_NAME

logger = logging.getLogger(AP_LOGGER_NAME)

class RingLinkConstants:
    FRIENDLY_NAME = "RingLink"
    SLOT_NAME = "ring_link"

class SlotDataConstants:
    ENABLE_LOGGER = "enable_ring_client_msg"
    SLOT_DATA = "slot_data"

class RingLink(LinkBase):
    wallet_manager: WalletManager
    ring_multiplier = 5
    timer_start: float = time.time()
    pending_rings: int = 0
    remote_pending_rings: int = 0
    remote_rings_sent: int = 0
    enable_logger: bool = True

    def __init__(self, network_engine: ArchipelagoNetworkEngine, wallet_manager: WalletManager):
        super().__init__(friendly_name=RingLinkConstants.FRIENDLY_NAME, slot_name=RingLinkConstants.SLOT_NAME,
            network_engine=network_engine)
        self.wallet_manager = wallet_manager
        self.id = _get_uuid()

    def on_connected(self, args):
        slot_data = args[SlotDataConstants.SLOT_DATA]
        self.enable_logger = bool(slot_data[SlotDataConstants.ENABLE_LOGGER])

    def on_bounced(self, args):
        if not self.is_enabled():
            return

        data = args["data"]
        source_name = data["source"]
        if RingLinkConstants.FRIENDLY_NAME in args["tags"] and source_name != self.id:
            base_amount = data["amount"]
            amount = _calc_rings(self, base_amount)

            calculated_ring_worth = self.wallet_manager.wallet.get_calculated_amount_worth(1)
            coins_current_amt: int = self.wallet_manager.wallet.get_currency_amount(CURRENCY_NAME.COINS)
            amount_difference: int = amount * calculated_ring_worth
            if amount > 0:
                if self.enable_logger:
                    logger.info("%s: You received %s coin(s)!",RingLinkConstants.FRIENDLY_NAME, amount)
                currencies = self.wallet_manager.add_currencies(amount_difference)
                self.wallet_manager.wallet.add_to_wallet(currencies)
                self.remote_rings_sent += amount
            elif amount < 0:
                if self.enable_logger:
                    logger.info("%s: You lost %s coin(s).", RingLinkConstants.FRIENDLY_NAME, amount)
                self.wallet_manager.wallet.set_specific_currency(CURRENCY_NAME.COINS, max(coins_current_amt - amount_difference, 0))
                self.remote_rings_sent -= amount

    async def handle_ring_link_async(self, delay: int = 5):
        if not self.is_enabled():
            return

        timer_end: float = time.time()

        # There may be instances where currency gained/lost may not equate to having a different final value
        # and/or ringlink requests may come in and cancel currency differences.
        if timer_end - self.timer_start >= delay:
            difference = self.wallet_manager._difference
            self.wallet_manager._difference = 0

            if difference == 0:
                return

            difference -= self.remote_rings_sent
            self.remote_rings_sent = 0

            await self.send_rings_async(difference * self.ring_multiplier)
            self.timer_start = time.time()

    async def send_rings_async(self, amount: int):
        if amount != 0:
            ring_link_req = RingNetworkRequest([ RingLinkConstants.FRIENDLY_NAME ], int(amount))
            ring_link_req.source = self.id

            if self.enable_logger:
                logger.info("%s: You sent %s rings!", RingLinkConstants.FRIENDLY_NAME, int(amount))
            await self.network_engine.send_ring_link_request_async(ring_link_req)

def _calc_rings(ring_link: RingLink, amount: int) -> int:
    amount_to_update, remainder = divmod(amount + ring_link.remote_pending_rings, ring_link.ring_multiplier)
    ring_link.remote_pending_rings = remainder

    return amount_to_update

def _get_uuid() -> int:
    string_id = str(uuid.uuid4())
    uid: int = 0
    for char in string_id:
        uid += ord(char)
    return uid
