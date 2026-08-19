import json
import math
from typing import NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification as IC

from .Constants.Names import item_names as ItemName
from .Constants.world_constants import GAME_NAME
from .Locations import GameOptionData
from .Helpers_Function import RamData

if TYPE_CHECKING:
    from .world import GameWorld

class GameItemData(NamedTuple):
    item_groups: list[str]
    classification: IC
    count: int = 1
    req_options: GameOptionData = None
    default_weight: int = 1
    ram_data: RamData = None


class GameItem(Item):
    game: str = GAME_NAME
    data: GameItemData

    def __init__(self, name: str, classification: IC, code: Optional[int], player: int):
        super(GameItem, self).__init__(name, classification, code, player)
        self.data = all_item_table[name]
        self.code = ITEM_NAME_TO_ID["item"] if "item" in ITEM_NAME_TO_ID else None

# We make a table with all the items we are adding every time
base_items_table: dict[str, GameItemData] = {
    ItemName.ITEM1: GameItemData(["Item Group"], IC.progression)
}

filler_items: dict[str, GameItemData] = {

}

# We have a separate table for traps so we don't add them unless we need to.
trap_filler_items: dict[str, GameItemData] = {

}

all_item_table: dict[str, GameItemData] = {**base_items_table, **trap_filler_items}

def get_items_name_to_id() -> dict[str, int]:
    dict_locs: dict[str, int] = {}
    for name, data in all_item_table.items():
        dict_locs.update({name: len(dict_locs) + 1})

    # We output item name to ID for anyone creating poptracker packs, so it's available if we update
    with open("items.json", "w", encoding="utf-8") as file:
        json.dump(dict_locs, file, indent=4, sort_keys=True, ensure_ascii=False)
    return dict_locs

def get_item_names_per_category() -> dict[str, set[str]]:
    categories: dict[str, set[str]] = {}

    for name, data in all_item_table.items():
        for category in data.item_groups:
            categories.setdefault(category, set()).add(name)

    return categories

ITEM_NAME_TO_ID: dict[str, int] = get_items_name_to_id()

def create_all_items(world: "GameWorld"):
    #  We use this exclude here to force Start Inventory from Pool - if you do not want this functionality,
    #  simply remove it.
    exclude = [item.name for item in world.multiworld.precollected_items[world.player]]

    # We use this to temporarily keep track of what items we have made to determine filler count later
    local_pool: list[GameItem] = []

    # Add basic items, here and if statements for any optional items
    local_pool += create_items_from_dict(base_items_table, world, exclude)


    # Calculate the number of additional filler items to create to fill all locations
    n_locations = len(world.multiworld.get_unfilled_locations(world.player)) # How many locations in our world
    n_filler_items = n_locations - len(local_pool) # How many filler items we need to create
    n_trap_items = math.ceil(n_filler_items * (world.options.trap_percentage.value / 100)) # Percentage of traps to make
    n_other_filler = n_filler_items - n_trap_items # How many other filler items to make

    if sum(world.trap_filler_dict.values()) > 0:  # Add filler items to the item pool. Add traps if they are on.
        for _ in range(n_trap_items):
            local_pool.append(world.create_item(get_trap_item_name(world)))

        for _ in range(n_other_filler):
            local_pool.append(world.create_item((world.get_filler_item_name())))
    else:
        for _ in range(n_filler_items):
            local_pool.append(world.create_item((world.get_filler_item_name())))

    world.multiworld.itempool += local_pool

# Replace return "Nothing" with an actual filler determination. This function is required in case Archipelago needs to
# replace an item
def get_random_filler_item_name(world: "GameWorld"):
    return world.random.choice(list(filler_items.keys()))

# A generic function for pick
def  get_trap_item_name(world: "GameWorld"):
    filler_traps = dict(sorted(world.trap_filler_dict.items()))
    return world.random.choices(list(filler_traps.keys()), weights=list(filler_traps.values()), k=1)[0]


def create_items_from_dict(item_dict: dict[str, GameItemData],
                           world: "GameWorld", excluded:list[str]) -> list[GameItem]:
    new_items = []
    for item, data in item_dict.items():
        if data.req_options:
            req_option_list: list = [getattr(world.options, x).value in y for (x,y) in data.req_options.option_list.items()]
            option_value: bool = all(req_option_list) if data.req_options.combine else any(req_option_list)
            if not option_value:
                continue

        copies = max(0, all_item_table[item].count - excluded.count(item))
        new_items = [world.create_item(item) for _ in range(copies)]

    return new_items