from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional, Dict, Set
from .Constants.Names import item_names as itemname


class SMG2ItemData(NamedTuple):
    type: list[str]
    classification: IC
    default_count: int = 1
    default_weight: int = 0

class SMG2Item(Item):
    game: str = "Super Mario Galaxy 2"

    def __init__(self, name: str, classification: IC, code: Optional[int], player: int):
        super(SMG2Item, self).__init__(name, classification,
                                       list(all_items_table.keys()).index(name)
                                       if name in all_items_table.keys() else None
                                       , player)
        self.data = all_items_table[name] if name in all_items_table.keys() else None

# TODO Replace this item table
item_table: dict[str, SMG2ItemData] = {
  "Power Star": SMG2ItemData(["Power Stars"], IC.progression_deprioritized_skip_balancing, 115),
  "Grand Star": SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression, 7),
  "Green Star": SMG2ItemData(["Power Stars", "Green Stars"], IC.progression, 120),
  # Comet Medals
}

filler_items: dict[str, SMG2ItemData] = {
    itemname.ONEUP: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.LIFEUP: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.STARBIT10: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.STARBIT25: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.STARBIT50: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.STARBI100: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.COINS1: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.COINS5: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.COIN10: SMG2ItemData(["Filler Items"], IC.filler),
    itemname.COIN20: SMG2ItemData(["Filler Items"], IC.filler),
}

yoshi_moves: dict[str, SMG2ItemData] = {
    itemname.YOSHI: SMG2ItemData(["Yoshi Move"], IC.progression),
    itemname.YOSHIBLIMP: SMG2ItemData(["Yoshi Move"], IC.progression),
    itemname.YOSHIPEPPER: SMG2ItemData(["Yoshi Move"], IC.progression),
    itemname.YOSHIBULB: SMG2ItemData(["Yoshi Move"], IC.progression),
    itemname.YOSHIFLOWER: SMG2ItemData(["Yoshi Move"], IC.progression),
}

separate_jump: dict[str, SMG2ItemData] = {
    itemname.MARIODOUBLE: SMG2ItemData(["Mario Move"], (IC.progression | IC.trap)),
    itemname.MARIOTRIPLE: SMG2ItemData(["Mario Move"], IC.progression),
}

prog_jumps: dict[str, SMG2ItemData] = {
    itemname.MARIOPROGJUMP: SMG2ItemData(["Mario Move"], IC.progression, 2),
}

move_rando: dict[str, SMG2ItemData] = {
    itemname.MARIOSWIM:      SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOLONG:      SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOBACK:      SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOSIDE:      SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOCLIMB:     SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOPOUND:     SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOWALL:      SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOLEDGE:     SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOSLIDE:     SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOSTARBALL:  SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOFLUZZ:     SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOSTARBIT:   SMG2ItemData(["Mario Move"], IC.progression),
    itemname.MARIOAIRSPIN:   SMG2ItemData(["Mario Move"], IC.progression),
}

move_rando_prog_jump: dict[str, SMG2ItemData] = {**move_rando, **prog_jumps}

move_rando_separate_jump: dict[str, SMG2ItemData] = {**move_rando, **separate_jump}

powerup_consumables: dict[str, SMG2ItemData] = {
    itemname.INVINCIBILITY: SMG2ItemData(["Consumable"], IC.useful),
    itemname.FIREBALLFLO: SMG2ItemData(["Consumable"], IC.useful),
    itemname.BEESHROOM: SMG2ItemData(["Consumable"], IC.useful),
    itemname.SPRINGSHROOM: SMG2ItemData(["Consumable"], IC.useful),
    itemname.BOOSHROOM: SMG2ItemData(["Consumable"], IC.useful),
    itemname.CLOUDFLOW: SMG2ItemData(["Consumable"], IC.useful),
    itemname.ROCKSHROOM: SMG2ItemData(["Consumable"], IC.useful),
    itemname.DRILLHAT: SMG2ItemData(["Consumable"], IC.useful),
}

smg1_consumables: dict[str, SMG2ItemData] = {
    itemname.ICEFLOWER: SMG2ItemData(["Consumable"], IC.useful),
    itemname.REDSTAR: SMG2ItemData(["Consumable"], IC.useful),
}

powerup_unlocks: dict[str, SMG2ItemData] = {
    itemname.SUPASTAR: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.FIREFLOWER: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.BEEMARIO: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.SPRING: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.BOOMARIO: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.CLOUD: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.ROCK: SMG2ItemData(["Power-Up"], IC.progression),
    itemname.SPINDRILL: SMG2ItemData(["Power-Up"], IC.progression),
}

object_unlocks: dict[str, SMG2ItemData] = {
    itemname.MARIOCANNON:       SMG2ItemData(["Objects"], IC.progression),
    itemname.MARIOSHELL:        SMG2ItemData(["Objects"], IC.progression),
    itemname.MARIOSWING:        SMG2ItemData(["Objects"], IC.progression),
    itemname.MARIOSTARCHIPS:    SMG2ItemData(["Objects"], IC.progression),
}

generic_event_items: dict[str, SMG2ItemData] = {
    "Peach": SMG2ItemData([], IC.progression),
    "Silver Star": SMG2ItemData([], IC.progression),
    "Purple Coin": SMG2ItemData([], IC.progression),
    "Can Farm Coins": SMG2ItemData([], IC.progression),
    "Can Farm Starbits": SMG2ItemData([], IC.progression),
}

keyed_grand_stars: dict[str, SMG2ItemData] = {
    itemname.GRAND1: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND2: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND3: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND4: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND5: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND6: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
    itemname.GRAND7: SMG2ItemData(["Grand Stars", "Power Stars"], IC.progression),
}

green_comet_key: dict[str, SMG2ItemData] = {
    itemname.GREENCOMETKEY: SMG2ItemData(["Green Comet Key"], IC.progression)
}

starbit_luma_key: dict[str, SMG2ItemData] = {
    itemname.STARBITLUMAKEY: SMG2ItemData(["All Starbit Luma Key"], IC.progression)
}

comet_all_key: dict[str, SMG2ItemData] = {
    itemname.ALLCOMETSKEY: SMG2ItemData(["All Comets Key"], IC.progression)
}

comet_type_keys: dict[str, SMG2ItemData] = {
    itemname.SPEEDYCOMET: SMG2ItemData(["Comet Key"], IC.progression),
    itemname.DAREDEVILCOMET: SMG2ItemData(["Comet Key"], IC.progression),
    itemname.PURPLECOMET: SMG2ItemData(["Comet Key"], IC.progression),
    itemname.COSMICCLONE: SMG2ItemData(["Comet Key"], IC.progression),
    itemname.ROMPCOMET: SMG2ItemData(["Comet Key"], IC.progression),
    itemname.DOUBLETIME: SMG2ItemData(["Comet Key"], IC.progression),
}

starbit_world_keys: dict[str, SMG2ItemData] ={
    itemname.STARBITHL1: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL2: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL3: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL4: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL5: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL6: SMG2ItemData(["Starbit Luma Key"], IC.progression),
    itemname.STARBITHL7: SMG2ItemData(["Starbit Luma Key"], IC.progression),
}

coin_luma_key: dict[str, SMG2ItemData] = {
    itemname.COINLUMAKEY: SMG2ItemData(["All Coin Luma Key"], IC.progression)
}

coin_world_keys: dict[str, SMG2ItemData] = {
    itemname.COINHL1: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL2: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL3: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL4: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL5: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL6: SMG2ItemData(["Coin Luma Key"], IC.progression),
    itemname.COINHL7: SMG2ItemData(["Coin Luma Key"], IC.progression),
}

green_star_all_key: dict[str, SMG2ItemData] = {
    itemname.GREENCOMETKEY: SMG2ItemData(["All Green Star Key"], IC.progression),
}

world_green_keys: dict[str, SMG2ItemData] = {
    itemname.GREENCOMETW1: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW2: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW3: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW4: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW5: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW6: SMG2ItemData(["World Green Star Key"], IC.progression),
    itemname.GREENCOMETW7: SMG2ItemData(["World Green Star Key"], IC.progression),
}

galaxy_keys: dict[str, SMG2ItemData] = {
   itemname.SKYPOBSKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLIPSWAPKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.HONEYBLOOMKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SWEETMYSKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLEETGLIDEKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLASHBLACKKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLIPOUTKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.GOODEGGKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SPINDIGKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLUFFBLUFFKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.PUZZPLANKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BEATBLOCKKEY: SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.HIGHTAILKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOULBOWLKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.COSMICOKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.TALLTRUNKKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.CLOUCOURKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.HAUNHALLKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FREEFLAKEKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SUPMASSKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.FLIPVILLKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.STARBEACHKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.CHOMWORKKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SPACSTORKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SLIPSANDKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SHIVBURNKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOOMOONKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.MELTYKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.CLOCKWORKKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.WHOMPFORTKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BATTLEBELTKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.MARIOKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.ROLLCOASTKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.TWISTTRIKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.STONECYCKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.GRANDMASTERKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWJR1KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWJR2KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWJR3KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWSER1KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWSER2KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOWSER3KEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.BOSSBLITZKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.RIGHTDOWNKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.WILDGLIDEKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.ROLLMASTKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.HONEYHOPKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.UPDOWNKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
   itemname.SLIMSPRIKEY : SMG2ItemData(["Galaxy Key"], IC.progression),
}

trap_filler_items: dict[str, SMG2ItemData] = {
    itemname.DARETRAP: SMG2ItemData(["Trap"], IC.trap, default_weight=5),
    itemname.JOYTRAP: SMG2ItemData(["Trap"], IC.trap, default_weight=5),
}

launch_star_all: dict[str, SMG2ItemData] = {
    itemname.LAUNCHSTARALL: SMG2ItemData(["Launch Star All Key"], IC.progression)
}

pipe_all: dict[str, SMG2ItemData] = {
    itemname.PIPEALL: SMG2ItemData(["All Pipes Key"], IC.progression)
}

expanded_filler: dict[str, SMG2ItemData] = {**filler_items, **powerup_consumables}

all_filler: dict[str, SMG2ItemData] = {**expanded_filler, **smg1_consumables}

all_items_table: dict[str, SMG2ItemData] = {**keyed_grand_stars, **item_table, **galaxy_keys,
                                            **world_green_keys, **all_filler, **powerup_consumables, **powerup_unlocks,
                                            **starbit_luma_key, **starbit_world_keys, **move_rando_separate_jump,
                                            **prog_jumps, **yoshi_moves, **object_unlocks, **coin_world_keys,
                                            **coin_luma_key, **comet_type_keys, **comet_all_key, **green_star_all_key,
                                            **trap_filler_items, **pipe_all, **launch_star_all}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: list(all_items_table.keys()).index(name) for name in list(all_items_table.keys()) }

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories

music_map: dict[str, str] = {
    "Starship Mario 1": "MBGM_SMG2_MARIO_SHIP01",
    "Starship Mario 2": "MBGM_SMG2_MARIO_SHIP02",
    "Starship Mario 3": "MBGM_SMG2_MARIO_SHIP03",
}

all_music_list: set[str] = {
    "BGM_CLEAR",
    "MBGM_SMG2_GALAXY_06",
    "MBGM_SMG2_GALAXY_05",
    "MBGM_SMG2_GALAXY_32",
    "MBGM_SMG2_GALAXY_09",
    "MBGM_SMG2_GALAXY_07",
    "MBGM_SMG2_GALAXY_03",
    "MBGM_SMG2_GALAXY_04",
    "MBGM_SMG2_GALAXY_31",
    "MBGM_SMG2_GALAXY_29",
    "BGM_DASH_YOSHI",
    "MBGM_SMG2_GALAXY_02",
    "MBGM_GLIDER",
    "MBGM_SMG2_GALAXY_13",
    "MBGM_SMG2_GALAXY_15",
    "BGM_SLIDER",
    "MBGM_SMG2_GALAXY_11",
    "MBGM_SMG2_GALAXY_19",
    "BGM_REPEAT_TIMER",
    "MBGM_SMG2_GALAXY_23",
    "MBGM_SMG2_GALAXY_14",
    "MBGM_SMG2_GALAXY_27",
    "MBGM_SMG2_GALAXY_10",
    "MBGM_SMG2_GALAXY_12",
    "MBGM_SMG2_GALAXY_17",
    "MBGM_SMG2_GALAXY_01",
    "MBGM_SMG2_GALAXY_16",
    "MBGM_SMG2_GALAXY_28",
    "MBGM_SMG2_GALAXY_30",
    "MBGM_SMG2_GALAXY_21",
    "MBGM_SMG2_GALAXY_24",
    "MBGM_SMG2_GALAXY_24B",
    "MBGM_SMG2_GALAXY_20",
    "MBGM_SMG2_GALAXY_22",
    "BGM_EV_BOSSRUSH",
    "BGM_EV_BOSSRUSH02",
    "MBGM_SMG_GALAXY_01",
    "MBGM_SMG_GALAXY_14",
    "MBGM_SMG_GALAXY_28",
    "MBGM_SMG2_GALAXY_INTER",
    "MBGM_SMG2_GALAXY_HURRY",
    "MBGM_SMG2_GALAXY_DANGER",
    "MBGM_SMG2_GALAXY_26",
    "MBGM_SMG2_GALAXY_18",
    "BGM_GAMBLE",
    "BGM_SMG2_EV_PORTER",
    "MBGM_MINI_GAME",
    "BGM_TAMAKORO",
    "BGM_TAMAKORO_2",
    "BGM_DREAM01",
    "MBGM_EV_KINOTAN",
    "MBGM_EV_RABBIT",
    "MBGM_SMG2_EV_MOKKU",
    "STM_SMG2_EV_KUPPABT01",
    "MBGM_STAR_CHANCE",
    "MBGM_STAR_CHANCE_2",
    "STM_STAR_CHANCE_3",
    "MBGM_SMG2_BOSS_05A",
    "STM_SMG2_BOSS_05B",
    "BGM_PINCH_01",
    "BGM_PINCH_02",
    "MBGM_SMG2_BOSS_08A",
    "MBGM_SMG2_BOSS_01A",
    "MBGM_SMG2_BOSS_07",
    "MBGM_SMG2_BOSS_07B",
    "MBGM_SMG2_BOSS_03A",
    "MBGM_SMG2_BOSS_02A",
    "BGM_SMG2_BOSS_04A",
    "MBGM_SMG2_BOSS_06A",
    "MBGM_SMG2_BOSS_06B",
    "MBGM_SMG2_BOSS_10",
    "MBGM_SMG_BOSS_03A",
    "MBGM_SMG_BOSS_03B",
    "MBGM_SMG_BOSS_01A",
    "MBGM_SMG_BOSS_01B",
    "MBGM_SMG_BOSS_05A",
    "MBGM_SMG_BOSS_05B",
    "MBGM_SMG_BOSS_09A",
    "MBGM_SMG_BOSS_09B",
    "MBGM_SMG2_WORLDMAP_06",
    "MBGM_SMG2_WORLDMAP_00",
    "MBGM_SMG2_WORLDMAP_04",
    "MBGM_SMG2_WORLDMAP_08",
    "MBGM_SMG2_WORLDMAP_07",
    "MBGM_SMG2_WORLDMAP_03",
    "MBGM_SMG2_WORLDMAP_05",
    "MBGM_SMG2_MARIO_SHIP01",
    "MBGM_SMG2_MARIO_SHIP02",
    "MBGM_SMG2_MARIO_SHIP03",
    "STM_SMG_ASTROOUT03",
    "BGM_MUTEKI_A",
    "BGM_MUTEKI_B",
    "BGM_FIRE_A",
    "BGM_FIRE_B",
    "BGM_FIRST_MORPH_A",
    "BGM_FIRST_MORPH_B",
    "STM_SMG2_EV_PROLOGUE_02",
    "BGM_SMG2_EV_PROLO_03",
    "STM_SMG2_EV_PROLOGUE_05",
    "BGM_SMG2_EV_DEPART01",
    "BGM_SMG2_COURSESELECT02",
    "BGM_JG_START_CAMERA_DEMO",
    "BGM_KOOPA_JR_APPEAR",
    "STM_SMG2_FIRST_ASTRO",
    "STM_SMG2_FIRST_ASTRO2",
    "STM_SMG2_SECOND_ASTRO",
    "STM_SMG2_EV_EPILOGUE_01",
    "STM_SMG2_EV_ENDING01",
    "MBGM_SMG2_STAFFROLL",
    "MBGM_TITLE",
    "BGM_ICE_A",
    "BGM_ICE_B",
    "BGM_FLYING_A",
    "BGM_FLYING_B",
    "MBGM_SMG2_GALAXY_08",
    "MBGM_SMG2_GALAXY_25",
    "STM_SMG2_BOSS08B",
    "STM_SMG2_BOSS_01B",
    "STM_SMG2_BOSS_03B",
    "STM_SMG2_BOSS_02B",
    "STM_SMG2_BOSS10",
    "STM_SMG_ASTROOUT02",
    "BGM_JG_GRAND_STAR_GET",
    "BGM_IN_BUBBLE",
}