""" Module providing type representation of the Archipelago NetworkProtocol """

import uuid
import abc
import time

from typing import NamedTuple, Optional, Any, Set
from enum import Enum
from CommonClient import CommonContext

class RequestStatus(Enum):
    """ Archipelago client -> server request statuses. """
    UNKNOWN = 0
    """ Used during initialization. """
    REQUESTED = 1
    """ Indicates that a request was made to Archipelago. """
    RECEIVED = 2
    """ Indicates that a response from the initial response was received and ready for processing. """
    COMPLETED = 3
    """ Indicates that the request was processed to completion. """

class ArchipelagoRequest:
    """ Base level request object for clients to interact with the Archipelago DataStorage. """
    uuid: str
    status: RequestStatus

    def __init__(self):
        self.uuid = str(uuid.uuid4())
        self.status = RequestStatus.UNKNOWN

    def __eq__(self, other):
        if isinstance(other, ArchipelagoRequest):
            return self.uuid == other.uuid
        return False

class NetworkRequest(NamedTuple):
    """
    Object representation of Archipelago's NetworkProtocol Client--> Server DataStorage operations.

    more information can be found at: 
        https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/network%20protocol.md#client---server
    """
    command: str
    tag: str

    @abc.abstractmethod
    def create_request(self) -> dict[str, Any]:
        """ Creates a dict[str, Any] of the object to be used in 'CommonContext.send_msgs()'. """
        return

class SetNetworkRequest(NetworkRequest):
    """ Object representation of the 'Set'command in Archipelago's NetworkProtocol. """
    operations: dict[str, Any]
    key: str
    default: Optional[Any]
    want_reply: bool

    def __new__(cls, tag, key, want_reply, default, operations):
        instance = super().__new__(cls, "Set", tag)
        instance.operations = operations
        instance.key = key
        instance.default = default
        instance.want_reply = want_reply

        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tag": self.tag,
            "key": self.key,
            "operations": self.operations,
        }

        if self.want_reply is not None:
            request.update({ "want_reply": self.want_reply })

        if self.default is not None:
            request.update({ "default": self.default })

        return request

class GetNetworkRequest(NetworkRequest):
    """ Object representation of the 'Get' command in Archipelago's NetworkProtocol. """
    keys: list[str]

    def __new__(cls, tag, keys):
        instance = super().__new__(cls, "Get", tag)
        instance.keys = keys
        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tag": self.tag,
            "keys": self.keys,
        }

        return request

class ConnectUpdateRequest(NetworkRequest):
    """ Object representation of the 'ConnectUpdate' command in Archipelago's NetworkProtocol. """
    tags: Set[str]

    def __new__(cls, tags):
        instance = super().__new__(cls, "ConnectUpdate", tag=None)
        instance.tags = tags
        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tags": self.tags,
        }

        return request

class BounceNetworkRequest(NetworkRequest):
    tags: Set[str]
    source: str | int

    def __new__(cls, tags):
        instance = super().__new__(cls, "Bounce", tag=None)
        instance.tags = tags
        return instance

    def create_request(self) -> dict[str, Any]:
        request = {
            "cmd": self.command,
            "tags": self.tags,
            "data": {
                "time": time.time(),
                "source": self.source
            }
        }

        return request

class TrapNetworkRequest(BounceNetworkRequest):
    trap_name: str

    def __new__(cls, tags, trap_name):
        instance = super().__new__(cls, tags=tags)
        instance.trap_name = trap_name
        return instance

    def create_request(self) -> dict[str, Any]:
        if not isinstance(self.source, str):
            raise TypeError("Cannot create TrapLink request, source: '%s' isn't a string.", self.source)
        request = super().create_request()
        request["data"]["trap_name"] = self.trap_name
        return request

class RingNetworkRequest(BounceNetworkRequest):
    amount: int

    def __new__(cls, tags, amount: int):
        instance = super().__new__(cls, tags=tags)
        instance.amount = amount
        return instance

    def create_request(self):
        if not isinstance(self.source, int):
            raise TypeError("Cannot create RingLink request, source: '%s' isn't an int.", self.source)
        request = super().create_request()
        request["data"]["amount"] = self.amount
        return request

class ArchipelagoNetworkEngine:
    """
    Archipelago's Client to Server NetworkProtocol which utilizes
    typing instead of manual request construction.
    """
    _ctx: CommonContext

    def __init__(self, ctx: CommonContext):
        self._ctx = ctx

    async def send_set_request_async(self, network_request: SetNetworkRequest):
        """
        Sends a 'Set' command to the Archipelago server.
        
        :param network_request: The request information to be sent to the 'Set' command.
        """
        return await self._send_network_request_async(network_request)

    async def send_get_request_async(self, network_request: GetNetworkRequest):
        """
        Sends a 'Get' command to the Archipelago server.

        :param network_request: The request information to be sent to the 'Get' command.
        """
        return await self._send_network_request_async(network_request)

    async def send_connect_update_request_async(self, network_request: ConnectUpdateRequest):
        """
        Sends a 'ConnectUpdate' command to the Archipelago server.

        :param network_request: The request information to be sent to the 'ConnectUpdate' command.
        """
        return await self._send_network_request_async(network_request)

    async def send_trap_link_request_async(self, network_request: TrapNetworkRequest):
        network_request.source = self.get_player_name(self.get_slot())
        return await self._send_network_request_async(network_request)

    async def send_ring_link_request_async(self, network_request: RingNetworkRequest):
        return await self._send_network_request_async(network_request)

    def get_team(self) -> int:
        """Gets the team number of the given network context."""
        return self._ctx.team

    def get_tags(self) -> Set[str]:
        """ Gets the tags for the given network context. """
        return self._ctx.tags

    def get_slot(self) -> int:
        """ Gets the context's slot for the given network context."""
        return self._ctx.slot

    def get_player_name(self, slot: int) -> str:
        """
        Gets the friendly name of the Archipelago game's slot ID.
        
        :param slot: The ID of the Archipelago game.
        """
        return self._ctx.player_names[slot]

    async def update_tags_async(self, enable_tag: bool, tag_name:str):
        """Set tags on/off and update the connection if already connected."""
        old_tags = self.get_tags().copy()
        if enable_tag:
            self._ctx.tags.add(tag_name)
        else:
            self._ctx.tags -= { tag_name }
        if old_tags != self.get_tags() and self._ctx.server and not self._ctx.server.socket.closed:
            await self.send_connect_update_request_async(ConnectUpdateRequest(self.get_tags()))

    async def update_client_tags_async(self, tags: list[str]):
        """
        Adds client tags and sends them to Archipelago server.
        
        :param tags: The tags to be added to the client tag collection.
        """
        for tag in tags:
            self._ctx.tags.add(tag)
        await self.send_connect_update_request_async(ConnectUpdateRequest(self.get_tags()))

    async def _send_network_request_async(self, request: NetworkRequest):
        await self._ctx.send_msgs([ request.create_request() ])
