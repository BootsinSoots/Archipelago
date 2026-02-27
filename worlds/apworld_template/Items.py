from typing import NamedTuple, Optional, Dict, Set

from BaseClasses import Item, ItemClassification
from BaseClasses import ItemClassification as IC

from .Constants.Names import item_names as ItemName

class GameItemData(NamedTuple):
    item_groups: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None


class GameItem(Item):
    game: str = "Game"
    doorid: Optional[int] = None

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super(GameItem, self).__init__(name, classification, code, player)
        data: GameItemData = item_table[name]
        self.item_groups = data.item_groups

item_table: dict[str, GameItemData] = {

}

def get_location_name_to_id():
    dict_locs: dict[str, int] = {}
    for name, data in item_table.items():
        dict_locs.update({name: len(dict_locs) + 1})
    return dict_locs

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.item_groups:
            categories.setdefault(category, set()).add(name)

    return categories

ITEM_NAME_TO_ID: dict[str, int] = get_location_name_to_id()