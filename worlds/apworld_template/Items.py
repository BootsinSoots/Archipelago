import json
import math
from typing import NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification as IC

from .Constants.Names import item_names as ItemName
from .Constants.world_constants import GAME_NAME

if TYPE_CHECKING:
    from .world import GameWorld

class GameItemData(NamedTuple):
    item_groups: list[str]
    classification: IC
    count: int = 1
    default_weight: int = 1
    other_variable: Optional[int] = None


class GameItem(Item):
    game: str = GAME_NAME
    data: GameItemData

    def __init__(self, name: str, classification: IC, code: Optional[int], player: int):
        super(GameItem, self).__init__(name, classification, code, player)
        self.data = all_item_table[name]
        self.code = ITEM_NAME_TO_ID["item"] if "item" in ITEM_NAME_TO_ID else None

base_items_table: dict[str, GameItemData] = {
    ItemName.ITEM1: GameItemData(["Item Group"], IC.progression)
}

trap_filler_items: dict[str, GameItemData] = {

}

all_item_table: dict[str, GameItemData] = {**trap_filler_items}

def get_items_name_to_id() -> dict[str, int]:
    dict_locs: dict[str, int] = {}
    for name, data in all_item_table.items():
        dict_locs.update({name: len(dict_locs) + 1})
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

    # Calculate the number of additional filler items to create to fill all locations
    n_locations = len(world.multiworld.get_unfilled_locations(world.player)) # How many locations in our world
    n_filler_items = n_locations - len(local_pool) # How many filler items we need to create
    n_trap_items = math.ceil(n_filler_items * (world.options.trap_percentage.value / 100)) # Percentage of traps to make
    n_other_filler = n_filler_items - n_trap_items # How many other filler items to make

    if sum(world.trap_filler_dict.values()) > 0:  # Add filler items to the item pool. Add traps if they are on.
        for _ in range(n_trap_items):
            local_pool.append(world.create_item(world.get_trap_item_name()))

        for _ in range(n_other_filler):
            local_pool.append(world.create_item((world.get_filler_item_name())))
    else:
        for _ in range(n_filler_items):
            local_pool.append(world.create_item((world.get_filler_item_name())))

    world.multiworld.itempool += local_pool

# Replace return "Nothing" with an actual filler determination. This function is required in case Archipelago needs to
# replace an item
def get_random_filler_item_name(world: "GameWorld"):
    return "Nothing"