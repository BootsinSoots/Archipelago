import copy
import dataclasses
import math
from typing import TYPE_CHECKING, Any, override
from BaseClasses import MultiWorld
from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Rule, True_, OptionFilter, CanReachRegion, Has, HasGroup, HasGroupUnique

from .Locations import LMLocation, PORTRAIT_LOCATION_TABLE
from .Items import ALL_ITEMS_TABLE
from .LuigiOptions import VacuumStart, Boosanity, MarioItems
from .client.constants import RANDOMIZER_NAME

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

grimmly_list = ["Uncle Grimmly, Hermit of the Darkness", "Catch Grimmly - Silver", "Catch Grimmly - Gold", "Wardrobe Clear Chest"]


def set_element_rules(world: "LMWorld", location: LMLocation, use_enemizer: bool):
    region = location.region
    rule = None
    if location.access is not None:
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
    if rule is not None and rule is not True_():
        world.set_rule(location, rule)

HasVac: Rule[Any] = (True_() & OptionFilter(VacuumStart, 1))|(Has("Poltergust 3000") & OptionFilter(VacuumStart, 0))
VacnIce: Rule[Any] = HasVac & Has("Ice Element Medal")
HasMarioItems: Rule[Any] = HasGroupUnique("Mario Item", count=FromOption(MarioItems))

# Require correct key for the provided door number
@dataclasses.dataclass()
class HasKey(Rule["LMWorld"], game_name=RANDOMIZER_NAME):
    door_id: int
    @override
    def _instantiate(self, world: "LMWorld") -> Rule.Resolved:
        if world.open_doors.get(self.door_id) == 1:
            return True_().resolve(world)
        else:
            key: str = next((k for k, v in ALL_ITEMS_TABLE.items() if v.door_id == self.door_id), None)
            if key is None:
                raise ValueError(f"Luigi's Mansion Rules Line 79 HasKey: Provided door ID:{self.door_id} has no matching Key")
            return Has(key).resolve(world)

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