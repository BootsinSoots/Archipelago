from typing import NamedTuple, Optional, List
from BaseClasses import Region

from .Constants.Names import region_names as RegionName

class GameRegionData(NamedTuple):
    region: str
    type: str  # type of randomization for GER



class GameRegion(Region):
    game: str = "Game"

    def __init__(self, player: int, name: str, parent: Region, data: GameRegionData):
        super(GameRegion, self).__init__(player, name)

        self.region = data.region
        self.type = data.type