""" Module providing LMClient with EnergyLink integration operations. """

from ...wallet import Wallet
from .energy_link import EnergyLink, RequestStatus, ArchipelagoNetworkEngine

class _ResponseArgs:
    ORIGINAL_VALUE = "original_value"
    VALUE = "value"
    TAG = "tag"
    KEY = "key"

class EnergyLinkClient:
    """
    Service which allows clients interact with energy link responses.
    """
    _energy_link: EnergyLink
    _wallet: Wallet

    _current_currency_amount: dict[str, int]

    def __init__(self, network_engine: ArchipelagoNetworkEngine, wallet: Wallet):
        self._energy_link = EnergyLink(network_engine)
        self._wallet = wallet
        self._current_currency_amount = {}

    def try_update_energy_request(self, args: dict[str, str]) -> bool:
        """
        Checks args for a matching EnergyLink key and a 'tag' attribute in the given. 
        If there's a match we iterate through the EnergyLink requests looking for a matching tag.
        If a matching tag is found we update the request object with the actual amount received from the server and setting the status to COMPLETED.

        :param args: Dict of parameters used to determine if a EnergyLink request was fufilled.
        """
        if args[_ResponseArgs.KEY] is not self._energy_link.get_ap_key() and _ResponseArgs.TAG not in args:
            return False

        request = self._energy_link.energy_requests.pop(args[_ResponseArgs.TAG], None)
        if request is None:
            return False

        if request.status != RequestStatus.REQUESTED:
            return False

        request.received_amount = args[_ResponseArgs.ORIGINAL_VALUE] - args[_ResponseArgs.VALUE]
        _get_currencies_to_be_added(self._wallet, request.received_amount)

        request.status = RequestStatus.COMPLETED
        return True

def _calc_currency_difference(previous_amount: int, amount: int, percentage: float = 0.25) -> int:
    temp_amount = amount - previous_amount
    return int(temp_amount * percentage)

def _get_currencies_to_be_added(wallet: Wallet, amount_to_add: int):
    currencies_to_add = _add_currencies(wallet, amount_to_add)
    wallet.add_to_wallet(currencies_to_add)

def _add_currencies(wallet: Wallet, amount_to_receive: int) -> dict[str, int]:
    new_amount = amount_to_receive
    currencies_to_add: dict[str, int] = {}

    for currency_name, currency_type in wallet.get_currencies().items():
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
