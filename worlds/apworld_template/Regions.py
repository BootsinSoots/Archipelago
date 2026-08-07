from typing import NamedTuple, Optional, List, TYPE_CHECKING
from BaseClasses import Region, MultiWorld

from .Constants.Names import region_names as RegionName

if TYPE_CHECKING:
    from .world import GameWorld

class GameRegionData(NamedTuple):
    type: str  # type of randomization for GER
    entrance_regions: Optional[list[str]] # Regions with entrances to this one
    exit_regions: Optional[list[str]] # Regions with entrances from this one



class GameRegion(Region):
    game: str = "Game"
    region_data: GameRegionData

    def __init__(self, region_name: str, region_data: GameRegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

def create_regions(world: "GameWorld"):
    pass