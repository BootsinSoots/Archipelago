""" Abstract class which manages common AP Link functionality. """
import Utils

from abc import ABC
from .network_engine import ArchipelagoNetworkEngine

class LinkBase(ABC):
    """ Generic class managing common function which each AP Link will utilize. """
    friendly_name: str
    slot_name: str
    network_engine: ArchipelagoNetworkEngine
    enable_logger: bool = True

    def __init__(self, friendly_name, slot_name, network_engine: ArchipelagoNetworkEngine):
        self.friendly_name = friendly_name
        self.slot_name = slot_name
        self.network_engine = network_engine

    def is_enabled(self) -> bool:
        """ Determines if the given link is enabled in the client. """
        return self.friendly_name in self.network_engine.get_tags()

    def set_logs(self, value: bool):
        """
        Sets the Link's client logger to the given value.
        
        :param value: If True, we enable client messages.
            Otherwise no link related messages will be sent to the client.
        """
        self.enable_logger = value
