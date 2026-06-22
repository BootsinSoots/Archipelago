from dataclasses import dataclass
from typing import Dict, Any

import Options
from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle, OptionCounter, OptionDict

class GalaxyShuffle(OptionSet):
    """
    Determine what kinds of galaxies should be added to the shuffle pool. Leave empty to disable shuffling

    Full: Any galaxy in any galaxy position

    Dome Majors: Add Major galaxies to shuffle pool

    Dome Minors: Add Minor galaxies to shuffle pool

    Observatory Specials: Add Direct from Observatory galaxies to shuffle pool, such as Trials or Hungry Luma galaxies

    Bosses: Add Boss galaxies to shuffle pool
    """
    display_name = "Galaxy Shuffle"
    internal_name = "galaxy_shuffle"
    valid_keys = {"Full", "Dome Majors", "Dome Minors", "Observatory Specials", "Bosses"}

class GalaxyShuffleType(Choice):
    """
    Choose how galaxies are shuffled between slots. Does nothing if no galaxies are randomized

    By Type - Galaxies will only be shuffled between slots of the same kind. Major galaxies on major galaxies,
    Boss galaxies on Boss galaxies, Observatory Galaxies on observatory galaxies

    Major Separately - Major galaxies will only be shuffled among themselves, but all other galaxies can go anywhere

    Full - Any galaxy can go on any Galaxy slot
    """
    display_name = "Galaxy Shuffle Type"
    internal_name = "galaxy_shuffle_type"
    option_By_Type = 0
    option_Major_Separate = 1
    option_Full = 2

class ShuffleDomes(Toggle):
    """
    Shuffle Dome entrances
    """
    display_name = "Dome Shuffle"
    internal_name = "dome_shuffle"

# this defines the enable_purple_coin_stars setting 
class EnablePurpleCoinStars(Toggle):
    """
    Add Purple Coin star location. Only one of these is normally available outside of post game
    """
    display_name = "Enable Purple Coin Stars"
    internal_name = "enable_purple_coin_stars"

# this allows players to pick their own star count to finish the game. 
class StarstoFinish(Range):
    """
    This will set the number of stars required to reach the center of the universe.
    This will be capped at 104 stars if extra locations are not enabled in a single world multiworld.
    """
    display_name = "Stars to finish"
    internal_name = "stars_to_finish"
    range_start = 25
    range_end = 119
    default = 60

class Dome1Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 1, which is the Terrace in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit. In Dome 1, some of these numbers
    will be capped to ensure generation if necessary, and will never be allowed to go above 9 total stars

    These are based on each orbit in the dome, in case levels are shuffled. First Orbit is excluded, to ensure you have
    at least one world to start.
    """
    display_name = "Dome 1 Access"
    internal_name = "dome_one_counts"
    min = 0
    max = 8
    valid_keys = ["Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }


class Dome2Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 2, which is the Fountain in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 10

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 2 Access"
    internal_name = "dome_two_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome3Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 3, which is the Kitchen in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 10

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 3 Access"
    internal_name = "dome_three_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome4Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 4, which is the Bedroom in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 10

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 4 Access"
    internal_name = "dome_four_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome5Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 5, which is the Engine Room in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 10

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 5 Access"
    internal_name = "dome_five_counts"
    min = 0
    max = 10
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0,
        "Fifth Orbit": 0
    }

class Dome6Offsets(OptionCounter):
    """
    Set the star requirements for each galaxy in the Dome 6, which is the Garden in vanilla.
    Each number corresponds to how many more stars are needed than the last orbit,
    and willed be capped if it goes above 20

    These are based on each orbit in the dome, in case levels are shuffled.
    """
    display_name = "Dome 6 Access"
    internal_name = "dome_six_counts"
    min = 0
    max = 20
    valid_keys = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit"]
    default = {
        "First Orbit": 0,
        "Second Orbit": 0,
        "Third Orbit": 0,
        "Fourth Orbit": 0
    }


class  MarioColors(OptionDict):
    """
    Choose new colors for part of Mario's Outfit! (These will also be applied to Luigi)
    4 pieces are changeable: 'Hat & Shirt' , 'Overalls', 'Shoes', 'Gloves'

    The following predetermined colors are available:
    "Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black", "Brown", "White", "Pink", "Gray"
    """
    display_name = "Mario Colors"
    internal_name = "mario_colors"
    valid_keys = ["Hat & Shirt", "Overalls", "Shoes", "Gloves"]
    valid_values = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Black", "Brown", "White", "Pink", "Gray"]
    default = {
        "Hat & Shirt": "Red",
        "Overalls": "Blue",
        "Shoes": "Brown",
        "Gloves": "White"
    }


# this defines all the options.
@dataclass
class SMG2Options(PerGameCommonOptions):
    enable_purple_coin_stars: EnablePurpleCoinStars
    stars_to_finish: StarstoFinish
    mario_colors: MarioColors
    dome_one_counts: Dome1Offsets
    dome_two_counts: Dome2Offsets
    dome_three_counts: Dome3Offsets
    dome_four_counts: Dome4Offsets
    dome_five_counts: Dome5Offsets
    dome_six_counts: Dome6Offsets
    dome_shuffle: ShuffleDomes
    galaxy_shuffle: GalaxyShuffle
    galaxy_shuffle_type: GalaxyShuffleType

option_groups = [
    Options.OptionGroup("Extra Locations", [
        EnablePurpleCoinStars,
    ]),
    Options.OptionGroup("Access Options", [
        StarstoFinish,
        ShuffleDomes,
        GalaxyShuffle,
        GalaxyShuffleType
    ]),
    Options.OptionGroup("Dome Offsets", [
       Dome1Offsets,
       Dome2Offsets,
       Dome3Offsets,
       Dome4Offsets,
       Dome5Offsets,
       Dome6Offsets
    ]),
    Options.OptionGroup("Cosmetics", [
        MarioColors
    ]),
]


option_presets: dict[str, dict[str, Any]] = {

}
