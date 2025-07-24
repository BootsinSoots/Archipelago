import copy
from pkgutil import get_data
from typing import Dict, Any, List, TYPE_CHECKING

from BaseClasses import Location,  MultiWorld
if TYPE_CHECKING:
    from . import LMWorld

ALWAYS_HINT: dict[str, int] = {"Madame Clairvoya": 3, "Foyer Toad": 2, "Wardrobe Balcony Toad": 40, "1F Washroom Toad": 16,
                               "Courtyard Toad": 24,"Left Telephone": 53, "Center Telephone": 53, "Right Telephone": 53}

PORTRAIT_HINTS: dict[str, int] = {"<father>": 35, "<mother>": 34, "<baby>": 26, "<dancer>": 9, "<situji>": 18,
                                  "<pianist>": 22, "<eater>": 8, "<dog01>": 11, "<builder>": 23, "<hustler>": 12,
                                  "<fat>": 48, "<obaasan>": 49, "<girl>": 29, "<dboy>":27, "<denwa>": 41,
                                  "<gaka>": 60, "<snowman>": 64, "<doll1>": 59, "<doll2>": 59, "<doll3>": 59}


def get_progression_only_items(multiworld: MultiWorld, player: int, loc, hinted_loc, prog_items_no_skip) -> Location:
    while loc is None:
        item = multiworld.worlds[player].random.choice(prog_items_no_skip)
        if item.location not in hinted_loc and item.code is not None and (item.player == player or item.location.player == player):
            loc: Location = item.location
    return loc


def get_other_items(multiworld: MultiWorld, player: int, loc, hinted_loc, other_items) -> Location:
    while loc is None:
        item = multiworld.worlds[player].random.choice(other_items)
        if item.location not in hinted_loc and item.code is not None and (item.player == player or item.location.player == player):
            loc: Location = item.location
    return loc


def get_hints_by_option(multiworld: MultiWorld, player_hints: set[int]) -> None:
    all_items = multiworld.get_items()
    prog_items = [item for item in multiworld.get_items() if item.advancement]
    prog_no_skip = [items for items in prog_items if not items.skip_in_prog_balancing]
    other_items = [item for item in multiworld.get_items() if not item.advancement]
    for player_int in player_hints:
        world: "LMWorld" = multiworld.worlds[player_int]
        already_hinted_locations: List[Location] = []
        hint_list: dict[str, int] = copy.copy(ALWAYS_HINT)
        if world.options.portrait_hints == 1:
            hint_list.update(PORTRAIT_HINTS)
        for name in hint_list.keys():
            if name == "Madame Clairvoya":
                if world.open_doors[72] == 0:
                    loc: Location = multiworld.find_item("Spade Key", player_int)
                else:
                    iname: str = world.random.choice(["Mario's Glove", "Mario's Letter", "Mario's Hat", "Mario's Star",
                                                     "Mario's Shoe"])
                    loc: Location = multiworld.find_item(iname, player_int)
                hint = {name: {"Item": loc.item.name,
                               "Location": loc.name,
                               "Location ID": str(loc.address),
                               "Rec Player": multiworld.player_name[loc.item.player],
                               "Send Player": multiworld.player_name[loc.player],
                               "Send Player ID": str(loc.player),
                               "Game": loc.game,
                               "Class": "Prog"}}
                already_hinted_locations.append(loc)
                world.hints.update(hint)
            else:
                loc: Any = None
                if world.options.hint_distribution.value == 0 or world.options.hint_distribution.value == 4:
                    hint_type = world.random.choices(["Prog", "Other"], [60, 40], k=1)[0]
                    if hint_type == "Prog":
                        loc = get_progression_only_items(multiworld, player_int, loc, already_hinted_locations, prog_no_skip)
                    else:
                        loc = get_other_items(multiworld, player_int, loc, already_hinted_locations, other_items)
                elif world.options.hint_distribution.value == 3 or world.options.hint_distribution.value == 1:
                    hint_type = world.random.choices(["Prog", "Other"], [90, 10], k=1)[0]
                    if hint_type == "Prog":
                        loc = get_progression_only_items(multiworld, player_int, loc, already_hinted_locations, prog_no_skip)
                    else:
                        loc = get_other_items(multiworld, player_int, loc, already_hinted_locations, other_items)
                elif world.options.hint_distribution.value == 2 or world.options.hint_distribution.value == 5:
                    while loc is None:
                        item = multiworld.worlds[player_int].random.choice(all_items)
                        if item.location not in already_hinted_locations:
                            loc: Location = item.location
                if loc.item.advancement:
                    icolor = "Prog"
                elif loc.item.trap:
                    icolor = "Trap"
                else:
                    icolor = "Other"
                hint = {name: {"Item": loc.item.name,
                               "Location": loc.name,
                               "Location ID": str(loc.address),
                               "Rec Player": multiworld.player_name[loc.item.player],
                               "Send Player": multiworld.player_name[loc.player],
                               "Send Player ID": str(loc.player),
                               "Game": loc.game,
                               "Class": icolor}}
                already_hinted_locations.append(loc)
                world.hints.update(hint)
        world.finished_hints.set()

