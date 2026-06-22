from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional, Dict, Set


class SMG2ItemData(NamedTuple):
    type: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None

# this lets us use these items by using SMGItem.
class SMG2Item(Item):
    game: str = "Super Mario Galaxy"

    def __init__(self, name: str, player: int, data: SMG2ItemData):
        super(SMG2Item, self).__init__(name, data.classification, data.code, player)
        self.type = data.type
        self.code = data.code


# This is all the items that are used by the game we define them here so they can be used.
item_table: dict[str, SMG2ItemData] = {
  "Power Star": SMG2ItemData(["Power Star"], 170000004, IC.progression_deprioritized_skip_balancing),# rom address  0x007ACCA0F2FF8760 don't remeber how i found this or if it's acurate so could use double check.
  "Grand Star": SMG2ItemData(["Grand Star", "Power Star"], 170000005, IC.progression),
  "Green Star": SMG2ItemData(["Green Star", "Power Star"], 170000006, IC.progression),
  "1up Mushroom": SMG2ItemData(["Filler Items"], 170000007, IC.filler),
  
  "Progressive Comets": SMG2ItemData(["Comet"], 170000008, IC.progression),
  "Peach": SMG2ItemData(["Victory"], None, IC.progression)

}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in item_table.items() if data.code is not None}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories
