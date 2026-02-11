from typing import NamedTuple, Optional, Dict, Set

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

from .Constants.Names import item_names as ItemName

class GameItemData(NamedTuple):
    type: list[str]
    code: Optional[int]
    classification: IC
    other_variable: Optional[int] = None


class GameItem(Item):
    game: str = "Game"
    doorid: Optional[int] = None

    def __init__(self, name: str, player: int, data: GameItemData):
        super(GameItem, self).__init__(name, data.classification, GameItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.code

    @staticmethod
    def get_apid(code: int):
        base_id: int = 9200
        return base_id + code if code is not None else None

item_table: dict[str, GameItemData] = {

}

ITEM_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in item_table.items() if data.code is not None}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        for category in data.type:
            categories.setdefault(category, set()).add(name)

    return categories