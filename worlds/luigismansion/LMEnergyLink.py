import uuid
import Utils
import dolphin_memory_engine as dme

from enum import Enum
from CommonClient import CommonContext, ClientCommandProcessor, logger

class EnergyLinkConstants:
    ENERGY_LINK = "EnergyLink"

    class ResponseArgs:
        ORIGINAL_VALUE = "original_value"
        VALUE = "value"
        TAG = "tag"
        KEY = "key"

# This address will start the point to Luigi's inventory to get his wallet to calculate rank.
WALLET_START_ADDR = 0x803D8B7C

class WalletNames:
    Coins = 0x324
    Bills = 0x328
    GoldBars = 0x32C

WALLET_OFFSETS: dict[int, int] = {
    WalletNames.Coins: 5000,
    WalletNames.Bills: 20000,
    WalletNames.GoldBars: 100000,
    0x330: 500000,
    0x334: 800000,
    0x338: 1000000,
    0x33C: 2000000,
    0x344: 20000000,
    0x348: 50000,
    0x34C: 100000,
    0x350: 1000000
}

class WalletManager:
    def add_coins(self, amount: int):
        """
        Adds an amount of coins to the player's wallet.
        :param amount: The amount of currency in coins to be added to the player's wallet.
        """
        self._add_currency_amount(WalletNames.Coins, amount)
    
    def remove_coins(self, amount: int):
        """
        Removes an amount of coins from the player's wallet.
        :param amount: The amount of currency in coins to be added to the player's wallet.
        """
        self._remove_currency_amount(WalletNames.Coins, amount)

    def get_coin_amount(self) -> int:
        """
        Returns the current amount of coins.
        """
        return self._get_currency_amount(WalletNames.Coins)
    
    def get_bill_amount(self) -> int:
        """
        Returns the current amount of bills.
        """
        return self._get_currency_amount(WalletNames.Bills)

    def get_wallet_value(self) -> int:
        """
        Returns the total value of all currency types in the player's wallet.
        This is used when determining the currency goal state.
        """
        total_wallet_value: int = 0
        for key in WALLET_OFFSETS.keys():
            wallet_key_amount = dme.read_word(dme.follow_pointers(WALLET_START_ADDR, [key]))
            total_wallet_value += wallet_key_amount * WALLET_OFFSETS[key]
        return total_wallet_value
    
    def _remove_currency_amount(self, currency_type: int, amount: int):
        """
        Removes an amount of currency based upon the currency_type.

        :param currency_type: The memory location for the currency type to be removed.
        :param amount: The amount of currency to be added based upon the currency_type.
        """
        current_currency = self._get_currency_amount(currency_type)
        dme.write_word(dme.follow_pointers(WALLET_START_ADDR, [currency_type]), (current_currency - amount))

    def _add_currency_amount(self, currency_type: int, amount: int):
        """
        Adds an amount of currency based upon the currency_type.

        :param currency_type: The memory location for the currency type to be added.
        :param amount: The amount of currency to be added based upon the currency_type.
        """
        current_currency = self._get_currency_amount(currency_type)
        dme.write_word(dme.follow_pointers(WALLET_START_ADDR, [currency_type]), (current_currency + amount))

    def _get_currency_amount(self, currency_type: int):
        """
        Gets the current currency value based upon the currency_type.

        :param currency_type: The memory location for the currency type to be retreived.
        """
        return dme.read_word(dme.follow_pointers(WALLET_START_ADDR, [currency_type]))

class RequestStatus(Enum):
    UNKNOWN = 0
    REQUESTED = 1
    COMPLETED = 2

class EnergyRequest:
    uuid: str
    request_amount: int
    received_amount: int
    status: RequestStatus

    def __init__(self, amount: int):
        self.uuid = str(uuid.uuid4())
        self.request_amount = amount
        self.status = RequestStatus.UNKNOWN
        self.received_amount: int = 0

    def __eq__(self, other):
        if isinstance(other, EnergyRequest):
            return self.uuid == other.uuid
        return False

class EnergyLink:
    _ctx: CommonContext
    wallet: WalletManager = WalletManager()

    energy_requests: list = list()
    current_energy: int = 0

    def __init__(self, ctx: CommonContext):
        self._ctx = ctx
    
    def request_energy(self, amount: int) -> EnergyRequest:
        """
        Requests energy for use from the Archipelago server.

        :param amount: The amount of energy requesting from the server. 
        The actual amount may vary due to the async nature of the call.
        """
        current_ctx = self._ctx
        if _validate_energy_request(current_ctx.tags, amount):
            request = EnergyRequest(amount)
            Utils.async_start(current_ctx.send_msgs([{
                "cmd": "Set",
                "key": self.get_ap_key(),
                "tag": request.uuid,
                "default": 0,
                "want_reply": True,
                "operations": [
                    { "operation": "add", "value": (request.request_amount * -1)},
                    { "operation": "max", "value": 0},
                ]
            }]))

            request.status = RequestStatus.REQUESTED
            self.energy_requests.append(request)
            return request

    async def send_energy_async(self, amount: int):
        """
        Sends energy to Archipelago server for other slots to consume.

        :param amount: The amount of energy to be sent to the server.
        """

        current_ctx = self._ctx
        if _validate_energy_request(current_ctx.tags, amount):
            coin_amount = self.wallet.get_coin_amount()
            if coin_amount < amount:
                return
            
            self.wallet.remove_coins(amount)
            await current_ctx.send_msgs([{"cmd": "Set", "key": self.get_ap_key(), "default": 0, "operations": [{ "operation": "add", "value": amount}]}])

    def get_ap_key(self) -> str:
        return f"{EnergyLinkConstants.ENERGY_LINK}{self._ctx.team}"

    def try_update_energy_request(self, args: dict) -> bool:
        """
        Checks args for a matching EnergyLink key and a 'tag' attribute in the given. If there's a match we iterate through the EnergyLink requests looking for a matching tag.
        If a matching tag is found we update the request object with the actual amount received from the server and setting the status to COMPLETED.

        :param args: Dict of parameters used to determine if a EnergyLink request was fufilled.
        """
        if args[EnergyLinkConstants.ResponseArgs.KEY] == self.get_ap_key() and EnergyLinkConstants.ResponseArgs.TAG in args:
            request = next(r for r in self.energy_requests if r.uuid == args[EnergyLinkConstants.ResponseArgs.TAG])
            if request is not None:
                request.received_amount += args[EnergyLinkConstants.ResponseArgs.ORIGINAL_VALUE] - args[EnergyLinkConstants.ResponseArgs.VALUE]
                request.status = RequestStatus.COMPLETED
                self.wallet.add_coins(request.received_amount)
                return True
        return False

    def tag_and_notify(self):
        """
        Adds the 'EnergyLink' tag to the given context and registers notifications from Archipelago when the team's EnergyLink is updated.
        """
        self._ctx.tags.add(EnergyLinkConstants.ENERGY_LINK)
        self._ctx.set_notify(self.get_ap_key())

class EnergyLinkProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_send_energy(self, arg: str):
        """Sends an amount of energy to the server.This amount is pulled from Luigi's money."""
        if not _validate_processor_context(self.ctx):
            return
        
        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return

        Utils.async_start(self.ctx.energy_link.send_energy_async(amount))
    
    def _cmd_display_energy(self):
        """Displays the current amount of energy available from the server."""
        if not _validate_processor_context(self.ctx):
            return

        energyAmount = self.ctx.stored_data[self.ctx.energy_link.get_ap_key()]
        logger.info(f"Team {self.ctx.team}'s energy: {energyAmount}.")

    def _cmd_request_energy(self, arg: str):
        """Requests energy from the server. Will return up to the requested amount based upon the team's energy pool."""
        if not _validate_processor_context(self.ctx):
            return

        is_valid, amount = _validate_processor_arg(arg)
        if not is_valid:
            return

        request = self.ctx.energy_link.request_energy(amount)
        logger.info(f"Requested {request.request_amount} energy.")

def _validate_processor_context(ctx: CommonContext):
    CONNECT_WARNING = "Please connect the client to the AP server before continuing."

    has_energy_link: bool = ctx.energy_link is not None
    is_connected_to_server: bool = ctx.server is not None
    if isinstance(ctx, CommonContext) and has_energy_link and is_connected_to_server:
        return True
    logger.warning(CONNECT_WARNING)
    return False

def _validate_processor_arg(amount: str):
    try:
        amount_as_int = int(amount)
    except ValueError:
        logger.info("The amount must be a number value.")
        return False, 0
    if amount_as_int <= 0:
        logger.info("The amount requested needs to be greater than zero.")
        return False, 0
    return True, amount_as_int

def _validate_energy_request(tags: set, amount: int) -> bool:
    """
    Determines if the request is valid before sending it to Archipelago.

    :param self: The client context making the request to the server.
    :param amount: The amount to be verified before sending the request.
    """
    try:
        amount_as_int = int(amount)
    except ValueError:
        return False
    if amount_as_int <= 0:
        return False
    if not EnergyLinkConstants.ENERGY_LINK in tags:
        return False
    return True