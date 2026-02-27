from dataclasses import dataclass
from typing import Dict, Any

from Options import Toggle, Range, PerGameCommonOptions, Choice, StartInventoryPool, DeathLinkMixin, OptionSet, \
    DefaultOnToggle, OptionDict, OptionCounter, OptionGroup


#Example Options from Luigi's Mansion


class LuigiWalkSpeed(Choice):
    """Choose how fast Luigi moves. Speeds above normal may cause OoB issues"""
    display_name = "Walk Speed"
    internal_name = "walk_speed"
    option_normal_speed = 0
    option_kinda_fast = 1
    option_schmoovin = 2
    default = 0


class FillerWeights(OptionCounter):
    """
    Set filler weights for filler items.
    Each weight represents a number of balls in a lottery roller with that trap on it.
    So if you had Banana Trap set to 3, and Ice Trap set to 7, and the rest set to 0,
    you would have a 3/10 for a Banana Trap to be chosen when rolling for trap fillers
    Must be between 0 and 100
    """
    display_name = "Filler Weights"
    internal_name = "filler_weights"
    min = 0
    max = 100
    valid_keys = ["Bundles", "Coins", "Bills", "Bars", "Gems", "Dust", "Hearts"]
    default = {
        "Bundles": 10,
        "Coins": 15,
        "Bills": 10,
        "Bars": 10,
        "Gems": 5,
        "Dust": 40,
        "Hearts": 10
    }
    all_on_dict = {item: 100 for item in valid_keys}
    all_off_dict = {item: 0 for item in valid_keys}

class Option1(DefaultOnToggle):
    """
    If enabled, in-game hints will be sent out to the multiworld when discovered.

    This is automatically disabled if hint distribution is set to Junk, Disabled or Vague
    """
    display_name = "Send Hints"
    internal_name = "send_hints"

@dataclass
class GameOptions(DeathLinkMixin, PerGameCommonOptions):
    Option1: Option1
    start_inventory_from_pool: StartInventoryPool


trap_settings = {
    FillerWeights.internal_name:             FillerWeights.all_off_dict,
}

game_options_presets: Dict[str, Dict[str, Any]] = {
    "Raining Traps": trap_settings,

}

options_groups = [
        OptionGroup("Extra Locations", [
            Option1,
        ])
    ]