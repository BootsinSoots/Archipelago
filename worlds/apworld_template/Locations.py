from typing import Optional, NamedTuple

from BaseClasses import Location, Region

from .Constants.Names import location_names as LocationName

class GameLocationData(NamedTuple):
    region: str
    location_groups: list[str]  # one or more groups that this location belongs to
    access: list[str]
    other_variable: int = -1  # entry number on the jmp table it belongs to


class GameLocation(Location):
    game: str = "Game"
    data: GameLocationData

    def __init__(self, player: int, name: str, address: Optional[int], parent: Optional[Region]):
        super(GameLocation, self).__init__(player, name, address, parent)
        self.data = location_table[name]


location_table: dict[str, GameLocationData] = {

}

def get_location_name_to_id() -> dict[str, int]:
    dict_locs: dict[str, int] = {}
    for name, data in location_table.items():
        dict_locs.update({name: len(dict_locs) + 1})
    return dict_locs

def get_location_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories

LOCATION_NAME_TO_ID: dict[str, int] = get_location_name_to_id()