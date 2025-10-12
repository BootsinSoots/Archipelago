""" Helper functions for wallet operations. """

import logging

from .wallet import Wallet, CURRENCY_NAME
from.constants import AP_LOGGER_NAME

logger = logging.getLogger(AP_LOGGER_NAME)

class WalletManager:
    wallet: Wallet
    previous_amount: int = 0
    initial_check: bool = True
    _difference: int = 0

    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    def add_currencies(self, amount_to_receive: int) -> dict[str, int]:
        new_amount = amount_to_receive
        currencies_to_add: dict[str, int] = {}

        for currency_name, currency_type in self.wallet.get_currencies().items():
            # If we added the entire amount we want to stop trying to add new currencies.
            if new_amount == 0:
                break

            currency_to_add, remainder = divmod(new_amount, currency_type.calc_value)
            new_amount = remainder

            # If we don't have any amount of a given currency to add we want to skip updating.
            if currency_to_add <= 0:
                continue

            currencies_to_add.update({ currency_name: int(currency_to_add) })

        return currencies_to_add

    def remove_currencies(self, amount_to_send: int, minimum_worth: int) -> dict[str, int]:
        new_amount = amount_to_send
        temp_currencies: dict[str, int]
        remaining: int

        while new_amount > 0:
            # Try to remove currency from energy link amount.
            temp_currencies, remaining  = _remove_currencies(self.wallet, new_amount)
            new_amount = remaining
            self.wallet.remove_from_wallet(temp_currencies)

            # If the remaining amount of energy is less than the minimum possible amount we break out of the loop.
            if remaining < minimum_worth:
                break

            # If the remaining amount isn't 0 and we run out of currency we will try to convert
            # some higher valued currencies to close the gap.
            if remaining > 0:
                for currency_name in self.wallet.get_currencies(has_amount=True):
                    if self.wallet.try_convert_currency(currency_name):
                        break

            if len(self.wallet.get_currencies(has_amount=True)) == 0:
                break

        return int(new_amount)

    def reset_wallet_watching(self):
        """ Resets wallet counting, used when a client disconnects/reconnects. """
        self.initial_check = True
        self.reset_difference()

    async def calc_wallet_differences_async(self):
        """ We want to asychnrously monitor the difference in currency for sending rings VIA ringlink. """
        ring_equiv = self.wallet.get_currency_amount(CURRENCY_NAME.COINS)

        if self.initial_check and ring_equiv > 0:
            self.initial_check = not self.initial_check
        else:
            self._difference += ring_equiv - self.previous_amount

        self.previous_amount = ring_equiv

    def reset_difference(self) -> int:
        """ Gets the current wallet differences and resets the counter. """
        current_difference = self._difference
        self._difference = 0
        return current_difference

def _remove_currencies(wallet: Wallet, amount_to_send: int) -> tuple[dict[str, int], int]:
    new_amount = amount_to_send
    currencies_to_remove: dict[str, int] = {}

    for currency_name, currency_type in wallet.get_currencies().items():
        if new_amount == 0:
            break

        # We don't want to convert gold diamonds because they are a hard requirement to complete the game.
        if currency_name == CURRENCY_NAME.GOLD_DIAMOND:
            continue

        currency_to_remove, remainder = divmod(new_amount, currency_type.calc_value)
        new_amount = remainder
        if currency_to_remove <= 0:
            continue

        remove_amount = currency_type.get() - currency_to_remove
        if remove_amount < 0:
            currency_to_remove += remove_amount
            new_amount += ((remove_amount * -1) * currency_type.calc_value)

        currencies_to_remove.update({ currency_name: int(currency_to_remove) })

    return currencies_to_remove, int(new_amount)