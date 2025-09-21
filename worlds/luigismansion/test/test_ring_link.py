import unittest

from ..client.links.ring_link import RingLink, _should_send_rings
from ..client.links.network_engine import ArchipelagoNetworkEngine
from ..client.wallet_manager import WalletManager

class _MockNetworkEngine(ArchipelagoNetworkEngine):
    def __init__(self, tags = [ "TrapLink" ], player_name = "rando-player"):
        self.tags = tags
        self.player_name = player_name

    def update_tags_async(self, enable_tag: bool, tag_name:str):
        pass

    def get_tags(self):
        return self.tags

    def get_player_name(self, slot: int) -> str:
        return self.player_name

    def get_slot(self) -> int:
        return 0

class _MockWalletManager(WalletManager):
    def __init__(self):
        self._difference = 0

class TestRingLink(unittest.TestCase):
    def test_should_send_rings_true(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet_manager = _MockWalletManager()

        ring_link = RingLink(mock_network_engine, mock_wallet_manager)

        result: bool = _should_send_rings(ring_link, 100)
        self.assertTrue(result)

    def test_should_send_rings_false_difference_too_high_positive_value(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet_manager = _MockWalletManager()
        mock_wallet_manager._difference = 1

        ring_link = RingLink(mock_network_engine, mock_wallet_manager)

        result: bool = _should_send_rings(ring_link, 1100)

        self.assertFalse(result)
        self.assertTrue(mock_wallet_manager._difference == 0)
        self.assertFalse(ring_link.remote_rings_received)
    
    def test_should_send_rings_false_difference_too_high_negatvie_value(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet_manager = _MockWalletManager()
        mock_wallet_manager._difference = 1

        ring_link = RingLink(mock_network_engine, mock_wallet_manager)

        result: bool = _should_send_rings(ring_link, -1100)

        self.assertFalse(result)
        self.assertTrue(mock_wallet_manager._difference == 0)
        self.assertFalse(ring_link.remote_rings_received)

    def test_should_send_rings_false_remote_rings_present(self):
        mock_network_engine = _MockNetworkEngine()
        mock_wallet_manager = _MockWalletManager()
        mock_wallet_manager._difference = 1

        ring_link = RingLink(mock_network_engine, mock_wallet_manager)
        ring_link.remote_rings_received = True

        result: bool = _should_send_rings(ring_link, 100)

        self.assertFalse(result)
        self.assertTrue(mock_wallet_manager._difference == 0)
        self.assertFalse(ring_link.remote_rings_received)
