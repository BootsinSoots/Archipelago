import json
from typing import Optional, NamedTuple, TYPE_CHECKING, Any

from BaseClasses import Location, Region
from rule_builder.rules import True_, Rule

from .Constants.Names import location_names as LocationName
from .Constants.Names import region_names as RegionName
from .Constants.world_constants import GAME_NAME
from .Helpers_Function import RamData

if TYPE_CHECKING:
    from .world import GameWorld

class GameOptionData(NamedTuple):
    option_list: dict[str, list[Any]]
    combine: bool = True

class GameLocationData(NamedTuple):
    region: str
    location_groups: list[str]  # one or more groups that this location belongs to
    access: Rule[Any] = None
    req_options: GameOptionData = None
    ram_data: RamData = None


class GameLocation(Location):
    game: str = GAME_NAME
    data: GameLocationData

    def __init__(self, player: int, name: str, address: Optional[int], parent: Optional[Region]):
        super(GameLocation, self).__init__(player, name, address, parent)
        self.data = all_location_table[name]
        self.code = LOCATION_NAME_TO_ID["item"] if "item" in LOCATION_NAME_TO_ID else None

base_locations: dict[str, GameLocationData] = {
    LocationName.LOCATION1: GameLocationData(RegionName.REGION1, ["Location Group"], True_())
}

all_location_table: dict[str, GameLocationData] = {

}

def get_location_name_to_id() -> dict[str, int]:
    dict_locs: dict[str, int] = {}
    for name, data in all_location_table.items():
        dict_locs.update({name: len(dict_locs) + 1})

    # We output location name to ID for anyone creating poptracker packs, so it's available if we update
    with open("locations.json", "w", encoding="utf-8") as file:
        json.dump(dict_locs, file, indent=4, sort_keys=True, ensure_ascii=False)
    return dict_locs

def get_location_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in all_location_table.items():
        for category in data.location_groups:
            categories.setdefault(category, set()).add(name)

    return categories

LOCATION_NAME_TO_ID: dict[str, int] = get_location_name_to_id()

def create_all_locations(world: "GameWorld"):
    for loc, data in all_location_table.items():
        if data.req_options:
            req_option_list: list = [getattr(world.options, x).value in y for (x,y) in data.req_options.option_list.items()]
            option_value: bool = all(req_option_list) if data.req_options.combine else any(req_option_list)
            if not option_value:
                continue

        reg = world.get_region(data.region)
        location = GameLocation(world.player, loc, list(all_location_table.keys()).index(loc), reg)
        if data.access is not None:
            world.set_rule(location, data.access)

        reg.locations += [location]
