from dataclasses import dataclass
from typing import Dict, Any, Counter

import Options
from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle, OptionCounter, OptionDict

class Goal(Choice):
    """
    Determine goal for your world

    Galaxy Generator: Beating Bowser's Fortified Fortress in Bowser's Galaxy Generator

    Green Star Cutscene: Getting 120 stars and beating Bowser's Fortified Fortress a 2nd time

    Grandmaster: Collecting all the Green Stars and beating The Ultimate Test

    Perfect Run: Beating the Perfect Run in Grandmaster Galaxy
    """
    display_name = "Goal"
    internal_name = "goal"
    option_Galaxy_Generator = 0
    option_Green_Star_Cutscene = 1
    option_Grandmaster = 2
    option_Perfect_Run = 3
    option_All_Bowsers = 4

class GalaxyShuffle(OptionSet):
    """
    Determine what kinds of galaxies should be added to the shuffle pool. Leave empty to disable shuffling

    Goal galaxy will be left in its original position

    Full: Any galaxy in any galaxy position

    World Majors: Add Major (3 star) galaxies to shuffle pool

    World Minors: Add Minor (2 star) galaxies to shuffle pool

    Hungry Lumas: Add Hungry Luma galaxies to shuffle pool

    World S Specials: Add World S galaxies to shuffle pool, excluding Grandmaster and Boss Blitz

    Grandmaster: Allow Grandmaster Galaxy to be shuffled if it is not your goal, with other World S Galaxies

    Bosses: Add Boss galaxies to shuffle pool, including Boss Blitz Galaxy. Galaxy Generator will only be randomized if
    it is not the goal
    """
    display_name = "Galaxy Shuffle"
    internal_name = "galaxy_shuffle"
    valid_keys = {"Full", "World Majors", "World Minors", "Hungry Lumas", "World S Specials", "Bosses", "Grandmaster"}

class GalaxyShuffleType(Choice):
    """
    Choose how galaxies are shuffled between slots. Does nothing if no galaxies are randomized

    By Type - Galaxies will only be shuffled between slots of the same kind. Major galaxies on major galaxies,
    Boss galaxies on Boss galaxies, Luma Galaxies on Luma galaxies

    Major Separately - Major galaxies will only be shuffled among themselves, but all other galaxies can go anywhere

    Full - Any galaxy can go on any Galaxy slot
    """
    display_name = "Galaxy Shuffle Type"
    internal_name = "galaxy_shuffle_type"
    option_By_Type = 0
    option_Major_Separate = 1
    option_Full = 2

class WorldShuffle(Choice):
    """
    How World order is shuffled

    Progressive means each Grand Star will unlock the next world

    Keyed Grand Stars means each Grand Star unlocks a specific world map for you to access.
    You will receive one at random in your starting inventory

    Open means that all world maps are open from the start
    """
    display_name = "World Shuffle"
    internal_name = "world_shuffle"
    option_Progressive = 0
    option_Keyed_Grand_Stars = 1
    option_Open = 2

class EnableGreenStars(Choice):
    """
    Add Green Star locations and items. Items are not added if Green Star Behavior is set to Disabled

    Off: No Green Stars items of locations are added to the pool

    Unlocked: Green Star Locations are added to the multiworld with no extra logical requirements

    Require Galaxy Generator: Require beating Galaxy Generator with 120 other stars before Green Star locations are in logic

    Green Star Comet: Must receive the Green Star Comet Key before Green Star locations are unlocked

    Require World Green key: Each World has a Green Star key needed before the Green Star Locations in that world are available
    """
    display_name = "Enable Green Stars"
    internal_name = "enable_green_stars"
    option_Off = 0
    option_Unlocked = 1
    option_Require_Galaxy_Generator = 2
    option_Require_Green_Star_Comet = 3
    option_Require_World_Green_Key = 4

class StarstoFinish(Range):
    """
    This will set the number of stars required to reach your chosen goal galaxy

    This will be capped to a percentage if Green Star locations are not enabled and this option is set to over 120 stars.
    The same will happen if Green Stars are not set to count as Power Stars
    """
    display_name = "Stars to finish"
    internal_name = "stars_to_finish"
    range_start = 0
    range_end = 240
    default = 60

class GreenStarBehavior(Choice):
    """
    Choose how Green Stars are applied in logic

    Power Stars: Count as Power Stars for goal

    Green Stars: Changes goal to require both Green and Power stars seperately

    Disabled: Don't count towards any logical requirements or be in item pool
    """
    display_name = "Green Star Behavior"
    internal_name = "green_star_behavior"
    option_Power_Stars = 0
    option_Green_Stars = 1
    option_Disabled = 2

class GreenStarstoFinish(Range):
    """
    If Green Star Behavior is set to Green Stars, choose the amount required for goal.
    """
    display_name = "Green Stars to Finish"
    internal_name = "green_stars_to_finish"
    range_start = 0
    range_end = 120
    default = 60

class FinalStarBlocks(OptionCounter):
    """
    Set the star requirements for the final Star Block in each world.

    If the world has multiple blocks, the others will be set based on your choice for the final block.

    Counts may be reduced if it is determined not enough levels would be available.
    """
    display_name = "Final Star Blocks"
    internal_name = "final_star_blocks"
    min = 0
    max = 236
    valid_keys = ["Final Star Block 1", "Final Star Block 2", "Final Star Block 3", "Final Star Block 4",
                  "Final Star Block 5", "Final Star Block 6", "Final Star Block 7"]
    default = {
        "Final Star Block 1": 7, # -4 for other block
        "Final Star Block 2": 16,
        "Final Star Block 3": 28,
        "Final Star Block 4": 40,
        "Final Star Block 5": 55,
        "Final Star Block 6": 70, # -5 and -10 for other blocks
        "Final Star Block 7": 110 # -10, -20, -30, -35 for other blocks
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

class GalaxyLock(Toggle):
    """
    Apply an extra requirement that each galaxy requires a specific item to open.
    """
    display_name = "Galaxy Locks"
    internal_name = "galaxy_lock"

class ActiveCometsGame(Range): # doesn't affect logic
    """
    How many comets are allowed to be active at a time across all worlds
    """
    display_name = "Active Comets in Game"
    internal_name = "active_comets_game"
    range_start = 1
    range_end = 39

class ActiveCometsWorld(Range): # doesn't affect logic
    """
    How many comets are allowed to be active in a single world at a time.
    """
    display_name = "Active Comets per World"
    internal_name = "active_comets_world"
    range_start = 1
    range_end = 7

# Comet medals in pool, provide galaxy "order", 1 comet to one level


# this defines all the options.
@dataclass
class SMG2Options(PerGameCommonOptions):
    goal: Goal
    enable_green_stars: EnableGreenStars
    green_star_behavior: GreenStarBehavior
    stars_to_finish: StarstoFinish
    green_stars_to_finish: GreenStarstoFinish
    mario_colors: MarioColors
    final_star_blocks: FinalStarBlocks
    world_shuffle: WorldShuffle
    galaxy_shuffle: GalaxyShuffle
    galaxy_shuffle_type: GalaxyShuffleType
    galaxy_lock: GalaxyLock
    active_comets_world: ActiveCometsWorld
    active_comets_game: ActiveCometsGame

option_groups = [
    Options.OptionGroup("Map Options", [
        Goal,
        StarstoFinish,
        WorldShuffle,
        FinalStarBlocks,
        GalaxyShuffle,
        GalaxyShuffleType,
        GalaxyLock,
        ActiveCometsWorld.
        ActiveCometsGame,
    ]),
    Options.OptionGroup("Green Stars", [
        EnableGreenStars,
        GreenStarstoFinish,
        GreenStarBehavior,
    ]),
    Options.OptionGroup("Logic Options", [

    ]),
    Options.OptionGroup("Extra Locations", [

    ]),
    Options.OptionGroup("Cosmetics", [
        MarioColors
    ]),
]


option_presets: dict[str, dict[str, Any]] = {

}
