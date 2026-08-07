from typing import NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification as IC

from .Constants.Names import item_names as ItemName
from .Constants.world_constants import GAME_NAME

if TYPE_CHECKING:
    from .world import GameWorld

class GameItemData(NamedTuple):
    item_groups: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None
    default_weight: int = 1


class GameItem(Item):
    game: str = GAME_NAME
    data: GameItemData

    def __init__(self, name: str, classification: IC, code: Optional[int], player: int):
        super(GameItem, self).__init__(name, classification, code, player)
        self.data = item_table[name]

trap_filler_items: dict[str, GameItemData] = {

}

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

def create_all_items(world: "GameWorld"):
    pass