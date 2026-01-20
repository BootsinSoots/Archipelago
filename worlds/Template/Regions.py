from typing import NamedTuple, Optional, List
from BaseClasses import Region, MultiWorld

from .Constants.Names import region_names as RegionName

class GameRegionData(NamedTuple):
    region: str
    type: str  # type of randomization for GER
    parent_region: Optional[str]



class GameRegion(Region):
    game: str = "Game"
    region_data: GameRegionData

    def __init__(self, region_name: str, region_data: GameRegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data