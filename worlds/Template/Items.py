from typing import NamedTuple, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

from .Constants.Names import item_names as ItemName

class GameItemData(NamedTuple):
    type: str
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