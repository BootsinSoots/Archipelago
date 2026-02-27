from typing import NamedTuple, Optional

from BaseClasses import Item, ItemClassification as IC

from .Constants.Names import item_names as ItemName

class GameItemData(NamedTuple):
    item_groups: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None


class GameItem(Item):
    game: str = "Game"
    doorid: Optional[int] = None

    def __init__(self, name: str, classification: IC, code: Optional[int], player: int):
        super(GameItem, self).__init__(name, classification, code, player)
        data: GameItemData = item_table[name]

item_table: dict[str, GameItemData] = {

}

def get_items_name_to_id() -> dict[str, int]:
    dict_locs: dict[str, int] = {}
    for name, data in item_table.items():
        dict_locs.update({name: len(dict_locs) + 1})
    return dict_locs

def get_item_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in item_table.items():
        for category in data.item_groups:
            categories.setdefault(category, set()).add(name)

    return categories

ITEM_NAME_TO_ID: dict[str, int] = get_items_name_to_id()