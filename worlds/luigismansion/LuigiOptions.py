from dataclasses import dataclass

from Options import Toggle, Range, PerGameCommonOptions, Choice, StartInventoryPool, DeathLinkMixin


class LuigiWalkSpeed(Choice):
    """Choose how fast Luigi moves"""
    display_name = "Walk Speed"
    internal_name = "walk_speed"
    option_normal_speed = 0
    option_kinda_fast = 1
    option_schmoovin = 2
    default = 0


class RandomMusic(Toggle):
    """Randomize Music"""
    display_name = "Music Randomization"
    internal_name = "random_music"


class BundleWeight(Range):
    """Set the weight for how often coin & bill bundles get chosen as filler."""
    display_name = "Money Bundle Weight"
    internal_name = "bundle_weight"
    range_start = 0
    range_end = 100
    default = 10


class CoinWeight(Range):
    """Set the weight for how often coins get chosen as filler."""
    display_name = "Coin Weight"
    internal_name = "coin_weight"
    range_start = 0
    range_end = 100
    default = 15


class BillWeight(Range):
    """Set the weight for how often bills get chosen as filler."""
    display_name = "Bill Weight"
    internal_name = "bill_weight"
    range_start = 0
    range_end = 100
    default = 10


class BarsWeight(Range):
    """Set the weight for how often gold bars get chosen as filler."""
    display_name = "Gold Bars Weight"
    internal_name = "bars_weight"
    range_start = 0
    range_end = 100
    default = 10


class GemsWeight(Range):
    """Set the weight for how often gemstones get chosen as filler."""
    display_name = "Gems Weight"
    internal_name = "gems_weight"
    range_start = 0
    range_end = 100
    default = 5


class PoisonTrapWeight(Range):
    """Set the weight for how often poison mushrooms get chosen as traps."""
    display_name = "Poison Trap Weight"
    internal_name = "poison_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class BombWeight(Range):
    """Set the weight for how often bombs get chosen as traps."""
    display_name = "Bomb Weight"
    internal_name = "bomb_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class IceTrapWeight(Range):
    """Set the weight for how often ice traps get chosen as traps."""
    display_name = "Ice Trap Weight"
    internal_name = "ice_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class BananaTrapWeight(Range):
    """Set the weight for how often bananas get chosen as traps."""
    display_name = "Banana Trap Weight"
    internal_name = "banana_trap_weight"
    range_start = 0
    range_end = 100
    default = 15


class NothingWeight(Range):
    """Set the weight for how often nothing is chosen as filler."""
    display_name = "'Nothing' Weight"
    internal_name = "mothing_weight"
    range_start = 0
    range_end = 100
    default = 40


class HeartWeight(Range):
    """Set the weight for how often hearts get chosen as filler."""
    display_name = "Heart Weight"
    internal_name = "heart_weight"
    range_start = 0
    range_end = 100
    default = 10


class BetterVacuum(Choice):
    """Choose whether to include the Poltergust 4000"""
    display_name = "Poltergust 4000"
    internal_name = "good_vacuum"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


# These might end up being the same
class StartHiddenMansion(Toggle):
    """Begin in the Hidden Mansion"""
    display_name = "Hidden Mansion"
    internal_name = "hidden_mansion"


class SpeedySpirits(Toggle):
    """Adds Blue Ghosts to location pool"""
    display_name = "Speedy Spirits"
    internal_name = "speedy_spirits"


class StartWithBooRadar(Choice):
    """
    Start with Boo Radar

    start_with: Start with Boo Radar

    include: Boo Radar in pool

    exclude: No Boo Radar - Boo Gates and Boosanity will be disabled if excluded
    """
    display_name = "Boo Radar"
    internal_name = "boo_radar"
    option_start_with = 0
    option_include = 1
    option_exclude = 2
    default = 1


class PortraitHints(Toggle):
    """Choose to add hints to the scans of the Portrait Ghosts' Hearts in the mansions"""
    display_name = "Portrait Ghost Hints"
    internal_name = "portrait_hints"


class HintDistribution(Choice):
    """Choose the level of hint from in-game hints. Will affect Portrait Ghost hints if the option is on."""
    display_name = "Hint Distribution"
    internal_name = "hint_distribution"
    option_balanced = 0
    option_junk = 1
    option_chaos = 2
    option_strong = 3
    option_vague = 4
    option_disabled = 5
    default = 0


class Plants(Toggle):
    """Adds all plants to location pool"""
    display_name = "Plantsanity"
    internal_name = "plantsanity"


class PickupAnim(Toggle):
    """Disable Luigi's pickup animations"""
    display_name = "Pickup Animation"
    internal_name = "pickup_animation"


class Toadsanity(Toggle):
    """Add Toads as locations to be checked."""
    display_name = "Toadsanity"
    internal_name = "toadsanity"


class Lightsanity(Toggle):
    """Adds the act of lighting up rooms as locations."""
    display_name = "Lightsanity"
    internal_name = "lightsanity"


class Walksanity(Toggle):
    """Adds the act of visiting rooms as locations."""
    display_name = "Walksanity"
    internal_name = "walksanity"


class Furnisanity(Toggle):
    """
    Adds interactable objects, such a dressers, paintings, candles, and light fixtures, to the location pool
    """
    display_name = "Furnisanity"
    internal_name = "furnisanity"


class BooGates(Toggle):
    """
    Toggle the events that prevent progress unless a certain number of boos have been caught

    Default to on. If this is turned off, the Boo Count options are ignored.
    """
    display_name = "Boo Gates"
    internal_name = "boo_gates"
    default = 1


class MarioItems(Range):
    """How many Mario Items it takes to capture the Fortune-Teller. 0 = Starts Capturable"""
    display_name = "Fortune-Teller Requirements"
    internal_name = "mario_items"
    range_start = 0
    range_end = 5
    default = 5


class WashroomBooCount(Range):
    """Set the number of Boos required to reach the 1F Washroom. 0 = Starts Open"""
    display_name = "Washroom Boo Count"
    internal_name = "washroom_boo_count"
    range_start = 0
    range_end = 50
    default = 5


class BalconyBooCount(Range):
    """Set the number of Boos required to reach the Balcony. 0 = Starts Open"""
    display_name = "Balcony Boo Count"
    internal_name = "balcony_boo_count"
    range_start = 0
    range_end = 36
    default = 20


class KingBooHealth(Range):
    """Set King Boo's health in the final fight."""
    display_name = "King Boo's Health"
    internal_name = "king_boo_health"
    range_start = 1
    range_end = 1000
    default = 500


class FinalBooCount(Range):
    """Set the number of Boos required to reach the Secret Altar. 0 = Starts Open"""
    display_name = "Altar Boo Count"
    internal_name = "final_boo_count"
    range_start = 0
    range_end = 50
    default = 40


class Boosanity(Toggle):
    """Turns Boos into Items and Locations."""
    display_name = "Boosanity"
    internal_name = "boosanity"


class Portrification(Toggle):
    """Turn Portrait Ghosts into checks in addition to their clear chests."""
    display_name = "Portrification"
    internal_name = "portrification"


class Enemizer(Choice):
    """
    Choose if and how ghosts are randomized.

    Vanilla: No ghost randomization

    Randomized Elements: Randomized ghost elements and waves

    No Elements: Remove ghost elements, randomize waves
    """
    display_name = "Enemizer"
    internal_name = "enemizer"
    option_vanilla = 0
    option_randomized_elements = 1
    option_no_elements = 2
    default = 0


class DoorRando(Toggle):
    """Randomize which doors are locked or unlocked in the mansion."""
    display_name = "Door Randomization"
    internal_name = "door_rando"


class LuigiFearAnim(Toggle):
    """Turn off Luigi being scared by ghosts if they spawn close to him"""
    display_name = "Courageous Luigi"
    internal_name = "fear_animation"


class ChestTypes(Choice):
    """
    Determines how chest colors and size are chosen,

    default: Size and color are determined by attempting to match the item type to a representative color similar to the vanilla game

    full_random: Size and color are chosen completely at random.

    color: Chest color represents the AP item classification

    size_and_color: Both size and color are determined by AP item classification

    no_fuzzy_matching: Same as default but uses item classification for other players' items
    """
    display_name = "Chest Cosmetics"
    internal_name = "chest_types"
    option_default = 0
    option_full_random = 1
    option_color = 2
    option_size_and_color = 3
    option_no_fuzzy_matching = 4
    default = 0


class TrapChestType(Choice):
    """
    Determines if chests containing traps can look like progression items

    filler: Trap chests only appear as traps

    progression: Trap chests only appear as progression

    anything: Trap chests can appear as anything
    """
    display_name = "Trap Appearance"
    internal_name = "trap_chests"
    option_filler = 0
    option_progression = 1
    option_anything = 2
    default = 0


class RankRequirement(Choice):
    """
    Choose the required rank (H to A) to complete the game, with A being the highest.

    Rank H requires any amount of money to finish the game, including 0

    Rank A requires 5 Gold Diamonds (or equivalent money) to finish the game
    """
    display_name = "Rank Requirement"
    internal_name = "rank_requirement"
    option_rank_h = 0
    option_rank_g = 1
    option_rank_f = 2
    option_rank_e = 3
    option_rank_d = 4
    option_rank_c = 5
    option_rank_b = 6
    option_rank_a = 7


class RandomSpawn(Choice):
    """
    Allows Luigi to randomly spawn somewhere in the mansion.

    Random Spawn: Randomly spawn in one of the rooms with enough locations to successfully generate

    Expanded Spawns: Only viable if Walksanity, or <furniture options here>. Larger amount of viable random spawn locations
    """
    display_name = "Random Spawn Location"
    internal_name = "random_spawn"
    option_vanilla = 0
    option_random_spawn = 1
    option_expanded_spawns = 2
    default = 0


class BooHealthOption(Choice):
    """
    Choose how Boo Health is determined

    Choice: Use Boo Health Value to set all boos to the specified value

    Random Values: Every boo has a different, randomly chosen health value between 1 and 999
    """
    display_name = "Boo Health Option"
    internal_name = "boo_health_option"
    option_choice = 0
    option_random_values = 1
    default = 0

class BooHealthValue(Range):
    """
    Choose the health value all Boos will have it the Boo Health Option is Choice. Range between 1 and 999

    Values over 150 may not be catchable within the current room and logic cannot account for where they move
    """
    display_name = "Boo Health Value"
    internal_name = "boo_health_value"
    range_start = 1
    range_end = 999
    default = 30

class BooSpeed(Range):
    """
    Choose how fast boos move. Range from 1 to 36
    """
    display_name = "Boo Speed"
    internal_name = "boo_speed"
    range_start = 1
    range_end = 36
    default = 15


class BooEscapeTime(Range):
    """
    Choose how long before Boos leave the current room. Range between 1 and 300.

    Values below 90 may not be catchable within the current room and logic cannot account for where they move
    """
    display_name = "Boo Escape Time"
    internal_name = "boo_escape_time"
    range_start = 1
    range_end = 300
    default = 120

class BooAnger(Toggle):
    """
    Choose whether boos can damage Luigi.
    """
    display_name = "Angry Boos"
    internal_name = "boo_anger"
    default = 0


@dataclass
class LMOptions(DeathLinkMixin, PerGameCommonOptions):
    rank_requirement: RankRequirement
    walk_speed: LuigiWalkSpeed
    good_vacuum: BetterVacuum
    boo_radar: StartWithBooRadar
    hidden_mansion: StartHiddenMansion
    fear_animation: LuigiFearAnim
    pickup_animation: PickupAnim
    random_music: RandomMusic
    door_rando: DoorRando
    enemizer: Enemizer
    random_spawn: RandomSpawn
    portrait_hints: PortraitHints
    hint_distribution: HintDistribution
    toadsanity: Toadsanity
    plantsanity: Plants
    furnisanity: Furnisanity
    boosanity: Boosanity
    portrification: Portrification
    lightsanity: Lightsanity
    walksanity: Walksanity
    speedy_spirits: SpeedySpirits
    boo_gates: BooGates
    mario_items: MarioItems
    washroom_boo_count: WashroomBooCount
    balcony_boo_count: BalconyBooCount
    final_boo_count: FinalBooCount
    king_boo_health: KingBooHealth
    bundle_weight: BundleWeight
    coin_weight: CoinWeight
    bill_weight: BillWeight
    bars_weight: BarsWeight
    gems_weight: GemsWeight
    poison_trap_weight: PoisonTrapWeight
    bomb_trap_weight: BombWeight
    ice_trap_weight: IceTrapWeight
    banana_trap_weight: BananaTrapWeight
    nothing_weight: NothingWeight
    heart_weight: HeartWeight
    boo_health_option: BooHealthOption
    boo_health_value: BooHealthValue
    boo_speed: BooSpeed
    boo_escape_time: BooEscapeTime
    boo_anger: BooAnger
    chest_types: ChestTypes
    trap_chests: TrapChestType
    start_inventory_from_pool: StartInventoryPool
