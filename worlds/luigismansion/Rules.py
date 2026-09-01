import copy
import math
from typing import TYPE_CHECKING, Any
from BaseClasses import CollectionState, MultiWorld
from rule_builder.rules import Rule, True_, OptionFilter, CanReachRegion, Has, HasGroup, HasGroupUnique

from .Locations import LMLocation, PORTRAIT_LOCATION_TABLE
from .LuigiOptions import VacuumStart, Boosanity
from worlds.generic.Rules import add_rule

if TYPE_CHECKING:
    from . import LMWorld

FIRE_SPIRIT_SPOT = ("1F Hallway",
                    "Study",
                    "Butler's Room",
                    "Cold Storage",
                    "Mirror Room",
                    "Dining Room",
                    "2F Rear Hallway",
                    "Sitting Room",
                    "Graveyard",
                    "Roof")

WATER_SPIRIT_SPOT = ("Kitchen",
                     "Boneyard",
                     "Courtyard",
                     "1F Bathroom",
                     "2F Washroom",
                     "Sitting Room")

ICE_SPIRIT_SPOT = ("Kitchen",
                   "Pipe Room",
                   "Tea Room",
                   "Ceramics Studio")

grimmly_list = ["Uncle Grimmly, Hermit of the Darkness", "Catch Grimmly - Silver", "Catch Grimmly - Gold"]


def set_element_rules(world: "LMWorld", location: LMLocation, use_enemizer: bool):
    region = location.region
    rule: Rule = location.access

    if use_enemizer:
        if region in world.ghost_affected_regions.keys() and location not in grimmly_list:
            # if fire, require water
            if world.ghost_affected_regions[region] == "Fire":
                rule = rule & CanFstWater
            # if water, require ice
            elif world.ghost_affected_regions[region] == "Water":
                rule = rule & CanFstIce
            # if ice, require fire
            elif world.ghost_affected_regions[region] == "Ice":
                rule = rule & CanFstFire
            else:
                pass
    world.set_rule(location, rule)

HasVac: Rule[Any] = (True_() & OptionFilter(VacuumStart, 1))|(Has("Poltergust 3000") & OptionFilter(VacuumStart, 0))
VacnIce: Rule[Any] = HasVac & Has("Ice Element Medal")

def BooCount(boo_count: int) -> Rule[Any]:     
    return ((HasGroupUnique("Boo", boo_count) & OptionFilter(Boosanity, 1))
            |(Has("Boo", boo_count) & OptionFilter(Boosanity, 0)))  

CanFstFire: Rule[Any] = HasVac & Has("Fire Element Medal") & (
    CanReachRegion("1F Hallway")|
    CanReachRegion("Study")| 
    CanReachRegion("Butler's Room")| 
    CanReachRegion("Cold Storage")|
    CanReachRegion("Mirror Room")|
    CanReachRegion("Dining Room")|
    CanReachRegion("2F Rear Hallway")|
    CanReachRegion("Sitting Room")|
    CanReachRegion("Graveyard")|
    CanReachRegion("Roof")
)

CanFstWater: Rule[Any] = HasVac & Has("Water Element Medal") & (
    CanReachRegion("Kitchen")|
    CanReachRegion("Boneyard")|
    CanReachRegion("Courtyard")|
    CanReachRegion("1F Bathroom")|
    CanReachRegion("2F Washroom")|
    CanReachRegion("Sitting Room")
)

CanFstIce: Rule[Any] = VacnIce & (
    CanReachRegion("Kitchen")|
    CanReachRegion("Pipe Room")|
    CanReachRegion("Tea Room")|
    CanReachRegion("Ceramics Studio")
)

def can_fst_fire(state: CollectionState, player: int):
    return (state.has("Fire Element Medal", player) and state.has("Poltergust 3000", player)
                                                    and (state.can_reach_region("1F Hallway", player) or
                                                        state.can_reach_region("Study", player) or
                                                        state.can_reach_region("Butler's Room", player) or
                                                        state.can_reach_region("Cold Storage", player) or
                                                        state.can_reach_region("Mirror Room", player) or
                                                        state.can_reach_region("Dining Room", player) or
                                                        state.can_reach_region("2F Rear Hallway", player) or
                                                        state.can_reach_region("Sitting Room", player) or
                                                        state.can_reach_region("Graveyard", player) or
                                                        state.can_reach_region("Roof", player)))


def can_fst_water(state, player):
    return (state.has("Water Element Medal", player) and state.has("Poltergust 3000", player) and
                                                        (state.can_reach_region("Kitchen", player) or
                                                         state.can_reach_region("Boneyard", player) or
                                                         state.can_reach_region("Courtyard", player) or
                                                         state.can_reach_region("1F Bathroom", player) or
                                                         state.can_reach_region("2F Washroom", player) or
                                                         state.can_reach_region("Sitting Room", player)))


def can_fst_ice(state, player):
    return (state.has("Ice Element Medal", player) and state.has("Poltergust 3000", player)
                                                    and (state.can_reach_region("Kitchen", player) or
                                                       state.can_reach_region("Pipe Room", player) or
                                                       state.can_reach_region("Tea Room", player) or
                                                       state.can_reach_region("Ceramics Studio", player)))

def portrait_health_sphere_things(multiworld: MultiWorld, portrait_sphere_players: set[int]):
    exclude_bosses: list[str] = copy.deepcopy(list(PORTRAIT_LOCATION_TABLE.keys()))
    exclude_bosses.remove("Boolossus, the Jumbo Ghost")
    player_max_sphere: dict[int, int] = {}

    def check_portrait_players_done() -> None:
        done_players = set()
        for player in portrait_sphere_players:
            player_lm_world = multiworld.worlds[player]
            if len(player_lm_world.portrait_ghost_health.keys()) == len(exclude_bosses):
                done_players.add(player)
        portrait_sphere_players.difference_update(done_players)

    for player in portrait_sphere_players:
        max_sphere: int = max([sphere_num for sphere_num, sphere in enumerate(multiworld.get_spheres(), 1) if
            bool(set([sphere_loc.name for sphere_loc in sphere if sphere_loc.player == player]) & set(exclude_bosses))])
        player_max_sphere.update({player: max_sphere})
    for sphere_num, sphere in enumerate(multiworld.get_spheres(), 1):
        for loc in sphere:
            if loc.player in portrait_sphere_players and loc.name in exclude_bosses:
                player_world: "LMWorld" = multiworld.worlds[loc.player]
                health = min((math.floor(player_world.options.portrait_health_value.value/player_max_sphere[loc.player]))
                        * sphere_num, player_world.options.portrait_health_value.value)
                if player_world.options.silver_ghosts.value == 1 and loc.name not in ["Bogmire, the Cemetary Shadow", "Chauncey, the Spoiled Baby", "Boolossus, the Jumbo Ghost"]:
                    health = min(health, (player_world.silver_portrait_upgrades[loc.name]+1) * 200)
                if player_world.options.gold_ghosts.value == 1 and loc.name not in ["Bogmire, the Cemetary Shadow", "Chauncey, the Spoiled Baby", "Boolossus, the Jumbo Ghost"]:
                    health = min(health, (player_world.gold_portrait_upgrades[loc.name]+1) * 130)
                player_world.portrait_ghost_health.update({loc.name: health})
            check_portrait_players_done()