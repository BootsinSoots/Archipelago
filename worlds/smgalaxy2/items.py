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
  "Power Star": SMG2ItemData(["Power Star"], 170000004, IC.progression_deprioritized_skip_balancing, 122),
  "Grand Star": SMG2ItemData(["Grand Star", "Power Star"], 170000005, IC.progression, 7),
  "Green Star": SMG2ItemData(["Green Star"], 170000006, IC.progression, 120),
  "Progressive Comets": SMG2ItemData(["Comet"], 170000008, IC.progression),
}

filler_items: dict[str, SMG2ItemData] = {
    "1up Mushroom": SMG2ItemData(["Filler Items"], 170000007, IC.filler),
}


generic_event_items: dict[str, SMG2ItemData] = {
    "Peach": SMG2ItemData([], None, IC.progression)
}

keyed_grand_stars: dict[str, SMG2ItemData] = {
    itemname.GRAND1: SMG2ItemData(["Grand Star", "Power Star"], 170000010, IC.progression),
    itemname.GRAND2: SMG2ItemData(["Grand Star", "Power Star"], 170000011, IC.progression),
    itemname.GRAND3: SMG2ItemData(["Grand Star", "Power Star"], 170000012, IC.progression),
    itemname.GRAND4: SMG2ItemData(["Grand Star", "Power Star"], 170000013, IC.progression),
    itemname.GRAND5: SMG2ItemData(["Grand Star", "Power Star"], 170000014, IC.progression),
    itemname.GRAND6: SMG2ItemData(["Grand Star", "Power Star"], 170000015, IC.progression),
    itemname.GRAND7: SMG2ItemData(["Grand Star", "Power Star"], 170000016, IC.progression),
}

all_items_table: dict[str, SMG2ItemData] = {**keyed_grand_stars, **item_table, **generic_event_items}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in all_items_table.items() if data.code is not None}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories
