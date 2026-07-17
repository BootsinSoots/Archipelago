from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional, Dict, Set
from .Constants.Names import item_names as itemname


class SMG2ItemData(NamedTuple):
    type: list[str]
    code: Optional[int]
    classification: IC
    default_count: int = 1

class SMG2Item(Item):
    game: str = "Super Mario Galaxy 2"

    def __init__(self, name: str, player: int, data: SMG2ItemData):
        super(SMG2Item, self).__init__(name, data.classification, data.code, player)
        self.type = data.type
        self.code = data.code

# TODO Replace this item table
item_table: dict[str, SMG2ItemData] = {
  "Power Star": SMG2ItemData(["Power Stars"], 170000004, IC.progression_deprioritized_skip_balancing, 115),
  "Grand Star": SMG2ItemData(["Grand Stars", "Power Stars"], 170000005, IC.progression, 7),
  "Green Star": SMG2ItemData(["Power Stars", "Green Stars"], 170000006, IC.progression, 120),
  # Comet Medals
  "Progressive Comets": SMG2ItemData(["Comet"], 170000008, IC.progression),
}

filler_items: dict[str, SMG2ItemData] = {
    "1up Mushroom": SMG2ItemData(["Filler Items"], 170000007, IC.filler),
    # Life Up
    # Starbits
    # Coins
}

yoshi_moves: dict[str, SMG2ItemData] = {
    itemname.YOSHI: SMG2ItemData(["Yoshi Move"], 1, IC.progression),
    itemname.YOSHIBLIMP: SMG2ItemData(["Yoshi Move"], 1, IC.progression),
    itemname.YOSHIPEPPER: SMG2ItemData(["Yoshi Move"], 1, IC.progression),
    itemname.YOSHIBULB: SMG2ItemData(["Yoshi Move"], 1, IC.progression),
    itemname.YOSHIFLOWER: SMG2ItemData(["Yoshi Move"], 1, IC.progression),
}

separate_jump: dict[str, SMG2ItemData] = {
    itemname.MARIODOUBLE: SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOTRIPLE: SMG2ItemData(["Mario Move"], 1, IC.progression),
}

prog_jumps: dict[str, SMG2ItemData] = {
    itemname.MARIOPROGJUMP: SMG2ItemData(["Mario Move"], 1, IC.progression, 2),
}

move_rando: dict[str, SMG2ItemData] = {
    itemname.MARIOSWIM:      SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOLONG:      SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOBACK:      SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOSIDE:      SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOCLIMB:     SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOPOUND:     SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOWALL:      SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOLEDGE:     SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOSLIDE:     SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOSTARBALL:  SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOFLUZZ:     SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOSTARBIT:   SMG2ItemData(["Mario Move"], 1, IC.progression),
    itemname.MARIOAIRSPIN:   SMG2ItemData(["Mario Move"], 1, IC.progression),
}

move_rando_prog_jump: dict[str, SMG2ItemData] = {**move_rando, **prog_jumps}

move_rando_separate_jump: dict[str, SMG2ItemData] = {**move_rando, **separate_jump}

powerup_consumables: dict[str, SMG2ItemData] = {
    itemname.INVINCIBILITY: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.FIREBALLFLO: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.BEESHROOM: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.SPRINGSHROOM: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.BOOSHROOM: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.CLOUDFLOW: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.ROCKSHROOM: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.DRILLHAT: SMG2ItemData(["Consumable"], 2, IC.useful),
}

smg1_consumables: dict[str, SMG2ItemData] = {
    itemname.ICEFLOWER: SMG2ItemData(["Consumable"], 2, IC.useful),
    itemname.REDSTAR: SMG2ItemData(["Consumable"], 2, IC.useful),
}

powerup_unlocks: dict[str, SMG2ItemData] = {
    itemname.SUPASTAR: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.FIREFLOWER: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.BEEMARIO: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.SPRING: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.BOOMARIO: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.CLOUD: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.ROCK: SMG2ItemData(["Power-Up"], 3, IC.progression),
    itemname.SPINDRILL: SMG2ItemData(["Power-Up"], 3, IC.progression),
}

generic_event_items: dict[str, SMG2ItemData] = {
    "Peach": SMG2ItemData([], None, IC.progression),
    "Silver Star": SMG2ItemData([], None, IC.progression),
    "Purple Coin": SMG2ItemData([], None, IC.progression),
}

keyed_grand_stars: dict[str, SMG2ItemData] = {
    itemname.GRAND1: SMG2ItemData(["Grand Stars", "Power Stars"], 170000010, IC.progression),
    itemname.GRAND2: SMG2ItemData(["Grand Stars", "Power Stars"], 170000011, IC.progression),
    itemname.GRAND3: SMG2ItemData(["Grand Stars", "Power Stars"], 170000012, IC.progression),
    itemname.GRAND4: SMG2ItemData(["Grand Stars", "Power Stars"], 170000013, IC.progression),
    itemname.GRAND5: SMG2ItemData(["Grand Stars", "Power Stars"], 170000014, IC.progression),
    itemname.GRAND6: SMG2ItemData(["Grand Stars", "Power Stars"], 170000015, IC.progression),
    itemname.GRAND7: SMG2ItemData(["Grand Stars", "Power Stars"], 170000016, IC.progression),
}

green_comet_key: dict[str, SMG2ItemData] = {
    itemname.GREENCOMETKEY: SMG2ItemData(["Green Comet Key"], 1, IC.progression)
}

starbit_luma_key: dict[str, SMG2ItemData] = {
    itemname.STARBITLUMAKEY: SMG2ItemData(["All Starbit Luma Key"], 1, IC.progression)
}

starbit_world_keys: dict[str, SMG2ItemData] ={
    itemname.STARBITHL1: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL2: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL3: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL4: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL5: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL6: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
    itemname.STARBITHL7: SMG2ItemData(["Starbit Luma Key"], 1, IC.progression),
}

coin_luma_key: dict[str, SMG2ItemData] = {
    itemname.COINLUMAKEY: SMG2ItemData(["All Coin Luma Key"], 1, IC.progression)
}

coin_world_keys: dict[str, SMG2ItemData] ={
    itemname.COINHL1: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL2: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL3: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL4: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL5: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL6: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
    itemname.COINHL7: SMG2ItemData(["Coin Luma Key"], 1, IC.progression),
}

world_green_keys: dict[str, SMG2ItemData] = {
    itemname.GREENCOMETW1: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW2: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW3: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW4: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW5: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW6: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
    itemname.GREENCOMETW7: SMG2ItemData(["World Green Star Key"], 1, IC.progression),
}

galaxy_keys: dict[str, SMG2ItemData] = {
   itemname.SKYPOBSKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLIPSWAPKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.HONEYBLOOMKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SWEETMYSKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLEETGLIDEKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLASHBLACKKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLIPOUTKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.GOODEGGKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SPINDIGKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLUFFBLUFFKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.PUZZPLANKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.HIGHTAILKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOULBOWLKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.COSMICOKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.TALLTRUNKKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.CLOUCOURKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.HAUNHALLKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FREEFLAKEKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SUPMASSKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.FLIPVILLKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.STARBEACHKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.CHOMWORKKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SPACSTORKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SLIPSANDKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SHIVBURNKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOOMOONKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.MELTYKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.CLOCKWORKKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.WHOMPFORTKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BATTLEBELTKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.MARIOKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.ROLLCOASTKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.TWISTTRIKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.STONECYCKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.GRANDMASTERKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWJR1KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWJR2KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWJR3KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWSER1KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWSER2KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOWSER3KEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.BOSSBLITZKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.RIGHTDOWNKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.WILDGLIDEKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.ROLLMASTKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.HONEYHOPKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.UPDOWNKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
   itemname.SLIMSPRIKEY : SMG2ItemData(["Galaxy Key"], 45, IC.progression),
}

expanded_filler: dict[str, SMG2ItemData] = {**filler_items, **powerup_consumables}

all_filler: dict[str, SMG2ItemData] = {**expanded_filler, **smg1_consumables}

all_items_table: dict[str, SMG2ItemData] = {**keyed_grand_stars, **item_table, **generic_event_items, **galaxy_keys,
                                            **world_green_keys, **all_filler, **powerup_consumables, **powerup_unlocks,
                                            **starbit_luma_key, **starbit_world_keys, **move_rando_separate_jump,
                                            **prog_jumps, **yoshi_moves}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in all_items_table.items() if data.code is not None}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories
