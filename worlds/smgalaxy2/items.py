from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional, Dict, Set
from .Constants.Names import item_names as itemname
from .locations import all_location_table


class SMG2ItemData(NamedTuple):
    type: list[str]
    classification: IC
    default_count: int = 1

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

expanded_filler: dict[str, SMG2ItemData] = {**filler_items, **powerup_consumables}

all_filler: dict[str, SMG2ItemData] = {**expanded_filler, **smg1_consumables}

all_items_table: dict[str, SMG2ItemData] = {**keyed_grand_stars, **item_table, **galaxy_keys,
                                            **world_green_keys, **all_filler, **powerup_consumables, **powerup_unlocks,
                                            **starbit_luma_key, **starbit_world_keys, **move_rando_separate_jump,
                                            **prog_jumps, **yoshi_moves, **object_unlocks, **coin_world_keys,
                                            **coin_luma_key, **comet_type_keys, **comet_all_key, **green_star_all_key,}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: list(all_items_table.keys()).index(name) for name in list(all_items_table.keys()) }

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories
