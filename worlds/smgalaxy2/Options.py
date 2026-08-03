from dataclasses import dataclass
from typing import Dict, Any
from collections import Counter


from Options import Choice, Range, PerGameCommonOptions, OptionSet, Toggle, OptionCounter, OptionDict, OptionGroup

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

    Off: No Green Stars items or locations are added to the pool

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
    value: Counter
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
    default = 1

class ActiveCometsWorld(Range): # doesn't affect logic
    """
    How many comets are allowed to be active in a single world at a time.
    """
    display_name = "Active Comets per World"
    internal_name = "active_comets_world"
    range_start = 1
    range_end = 7
    default = 1

class PowerupRando(Toggle):
    """
    Requires you to receive an item before you can use the related power-up
    """
    display_name = "Power-Up Rando"
    internal_name = "powerup_rando"

class PowerUpFiller(Choice):
    """
    Add consumable Power-Ups as filler items to the itempool

    Ice Mario and the Flight Star from Super Mario Galaxy 1 are only included as consumables if chosen
    """
    display_name = "Power-Up Consumables"
    internal_name = ("powerup_consumables")
    option_Off = 0
    option_Exclude_Ice_and_Fly = 1
    option_All = 2

class MoveRando(Choice):
    """
    Lock Mario's movement abilities until they have been received. Basic Jump and Ground Spin are never removed.

    Progressive jumps: Unlock Double Jump then Triple Jump.

    Separate jumps: unlock Double and Triple jump separately
    """
    display_name = "Move Rando"
    internal_name = "move_rando"
    option_Off = 0
    option_Progressive_Jumps = 1
    option_Separate_Jumps = 2

class YoshiRando(Toggle):
    """
    Lock Yoshi and his fruits until you receive a related item.
    """
    display_name = "Yoshi Rando"
    internal_name = "yoshi_rando"

class ObjectRando(Toggle):
    """
    Lock various kinds of items until you receive a related item
    """
    display_name = "Object Rando"
    internal_name = "object_rando"

class StarbitLumaLocks(Choice):
    """
    Determine if Starbit lumas require extra items, in addition to starbits, to unlock

    Global: One key opens all Starbit Lumas

    Individual: Each Luma requires their own key to open.
    """
    display_name = "Starbit Luma Locks"
    internal_name = "starbit_luma_locks"
    option_Off = 0
    option_Global = 1
    option_Individual = 2


class StarbitLumaCounts(OptionCounter):
    """
    Determine how many starbits are required for each Starbit Luma

    Adding 'random: XXX' will roll ALL values somewhere between 0 and XXX
    """
    display_name = "Starbit Luma Counts"
    internal_name = "starbit_luma_counts"
    min = 0
    max = 9999
    valid_keys = ["World 1 Starbit Luma", "World 2 Starbit Luma", "World 3 Starbit Luma","World 4 Starbit Luma",
                  "World 5 Starbit Luma", "World 6 Starbit Luma", "World 7 Starbit Luma", "random"]
    default = {
        "World 1 Starbit Luma": 300,
        "World 2 Starbit Luma": 700,
        "World 3 Starbit Luma": 1000,
        "World 4 Starbit Luma": 1200,
        "World 5 Starbit Luma": 1500,
        "World 6 Starbit Luma": 1800,
        "World 7 Starbit Luma": 2000
    }

class CoinLumaLocks(Choice):
    """
    Determine if Coin Lumas require extra items, in addition to coins, to unlock

    Global: One key opens all Coin Lumas

    Individual: Each Luma requires their own key to open.
    """
    display_name = "Coin Luma Locks"
    internal_name = "coin_luma_locks"
    option_Off = 0
    option_Global = 1
    option_Individual = 2


class CoinLumaCounts(OptionCounter):
    """
    Determine how many coins are required for each Coin Luma

    Adding 'random: XXX' will roll ALL values somewhere between 0 and XXX
    """
    display_name = "Coin Luma Counts"
    internal_name = "Coin_luma_counts"
    min = 0
    max = 9999
    valid_keys = ["Fluffy Bluff Coin Luma", "Puzzle Plank Coin Luma", "Hightail Falls Coin Luma","Cosmic Cove Coin Luma",
                  "Cloudy Court Coin Luma", "Clockwork Ruins Coin Luma", "Battle Belt Coin Luma", "random"]
    default = {
        "Fluffy Bluff Coin Luma": 100,
        "Puzzle Plank Coin Luma": 70,
        "Hightail Falls Coin Luma": 30,
        "Cosmic Cove Coin Luma": 15,
        "Cloudy Court Coin Luma": 30,
        "Clockwork Ruins Coin Luma": 30,
        "Battle Belt Coin Luma": 20
    }

class CometItems(Choice):
    """
    Choose whether comet stars require an item to unlock them.

    Global: All comets unlock after receiving a single item

    Type: Comets unlock based on what kind of comet star they are
    """
    display_name = "Comet Items"
    internal_name = "comet_items"
    option_Off = 0
    option_Global = 1
    option_Type = 2

class CometMission(Choice):
    """
    Choose whether comets require the galaxy's Comet medal or the vanilla mission to be beaten first

    Off: Neither is required

    Medal: Requires you to get the Comet Medal for the galaxy before the Comet Star mission appears

    Mission: Requires the vanilla mission to be cleared before the comet version can be completed

    Both: Requires both the Comet Medal and vanilla mission to be completed before the Comet Star unlocks
    """
    display_name = "Comet Missions"
    internal_name = "comet_mission"
    option_Off = 0
    option_Medal = 1
    option_Mission = 2
    option_Both = 3

class LogicDifficulty(Choice):
    """
    Set required difficulty for logic. This makes a difference primarily with move randomizations on

    Vanilla: Only vanilla expected requirements for jumps and item usage

    Medium: Turns on some skips that could be found through repeated gameplay

    Hard: Turns on both medium skips and skips used in speedrunning communities

    Hell: Infinite Flutter could be required for some transitions
    """
    display_name = "Logic Difficulty"
    internal_name = "logic_difficulty"
    option_Vanilla = 0
    option_Medium = 1
    option_Hard = 2
    option_Hell = 3

class MailtoadLetters(Toggle):
    """
    Turns Mailtoad's letters into locations that will also give you an item when you receive them.
    """
    display_name = "Mailtoad Letters"
    internal_name = "mailtoad_letters"

class Passengers(Toggle):
    """
    Speak to each new passenger on Starship Mario for an item!
    """
    display_name = "Passengers"
    internal_name = "passengers"


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
    powerup_rando: PowerupRando
    powerup_consumables: PowerUpFiller
    move_rando: MoveRando
    yoshi_rando: YoshiRando
    object_rando: ObjectRando
    starbit_luma_locks: StarbitLumaLocks
    starbit_luma_counts: StarbitLumaCounts
    coin_luma_locks: CoinLumaLocks
    coin_luma_counts: CoinLumaCounts
    comet_items: CometItems
    comet_mission: CometMission
    logic_difficulty: LogicDifficulty
    mailtoad_letters: MailtoadLetters
    passengers: Passengers

option_groups = [
    OptionGroup("Map Options", [
        Goal,
        StarstoFinish,
        WorldShuffle,
        FinalStarBlocks,
        GalaxyShuffle,
        GalaxyShuffleType,
        GalaxyLock,
        StarbitLumaLocks,
        StarbitLumaCounts,
        ActiveCometsWorld,
        ActiveCometsGame,
    ]),
    OptionGroup("Green Stars", [
        EnableGreenStars,
        GreenStarBehavior,
        GreenStarstoFinish,
    ]),
    OptionGroup("Logic Options", [
        LogicDifficulty,
        PowerupRando,
        MoveRando,
        YoshiRando,
        ObjectRando,
        CoinLumaLocks,
        CoinLumaCounts,
        CometMission,
        CometItems,
    ]),
    OptionGroup("Extra Locations", [
        MailtoadLetters,
        Passengers,
    ]),
    OptionGroup("Itempool Changes", [
        PowerUpFiller
    ]),
    OptionGroup("Cosmetics", [
        MarioColors
    ]),
]


option_presets: dict[str, dict[str, Any]] = {

}
