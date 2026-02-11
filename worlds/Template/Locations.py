from typing import Optional, NamedTuple, List, Dict, Set

from BaseClasses import Location, Region

from .Constants.Names import location_names as LocationName

class GameLocationData(NamedTuple):
    region: str
    code: Optional[int]  # used to create ap_id, None for events
    location_groups: str  # type of randomization option/jmp table and group [Chest, Furniture, Furniture, Plant, Boo, GSpeedy (Gold Mouse), BSpeedy (Blue Ghost), Portrait, Toad]
    other_variable: int = -1  # entry number on the jmp table it belongs to


class GameLocation(Location):
    game: str = "Game"
    access: list[str]
    rule_def: str = ""
    locked_item: Optional[str]

    def __init__(self, player: int, name: str, parent: Region, data: GameLocationData):
        address = None if data.code is None else GameLocation.get_apid(data.code)
        super(GameLocation, self).__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.region = data.region
        self.type = data.type
        self.address = self.address

    @staticmethod
    def get_apid(code: int):
        base_id: int = 9200
        return base_id + code


location_table: dict[str, GameLocationData] = {

}

LOCATION_NAME_TO_ID: dict[str, int] =  {
    name: data.code for name, data in location_table.items() if data.code is not None}

def get_location_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories