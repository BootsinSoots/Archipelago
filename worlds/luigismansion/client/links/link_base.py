""" Abstract class which manages common AP Link functionality. """
import Utils

from abc import ABC
from .network_engine import ArchipelagoNetworkEngine

class LinkBase(ABC):
    """ Generic class managing common function which each AP Link will utilize. """
    friendly_name: str
    slot_name: str
    network_engine: ArchipelagoNetworkEngine

    def __init__(self, friendly_name, slot_name, network_engine: ArchipelagoNetworkEngine):
        self.friendly_name = friendly_name
        self.slot_name = slot_name
        self.network_engine = network_engine

    def update_tag(self, args):
        """
        Updates tag of the given link if they are present in the provided args.
        
        :param args: The argument collection used to determine if we should enable the given link.
        """
        slot_data = args["slot_data"]
        Utils.async_start(self.network_engine.update_tags_async(bool(slot_data[self.slot_name]),
            self.friendly_name), name=f"Update {self.friendly_name}")

    def is_enabled(self) -> bool:
        """ Determines if the given link is enabled in the client. """
        return self.friendly_name in self.network_engine.get_tags()

    def on_connected(self, args):
        self.update_tag(args)
