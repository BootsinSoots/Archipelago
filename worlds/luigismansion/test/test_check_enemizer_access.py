from BaseClasses import ItemClassification
from test.bases import WorldTestBase

from .. import LMWorld, ITEM_TABLE
from ..Locations import *

class LMTestBase(WorldTestBase):
    game = "Luigi's Mansion"
    world = LMWorld
    run_default_tests = False

class LocationFail(LMTestBase):
    options = {
        "enemizer": 1,
        "portrification": 1,
        "toadsanity": 1,
        "boosanity": 1,
        "lightsanity": 1,
    }

    def test_enemizer_locations_requires_element(self):
        import logging
        logger = logging.getLogger(__name__)

        if not any([_ for _ in self.world.ghost_affected_regions.keys() if self.world.ghost_affected_regions[_] == "No Element"]):
            logger.info("All regions did not require any elements. Multiworld Seed was: " + str(self.multiworld.seed))
            return

        prog_items = []
        for name, data in ITEM_TABLE.items():
            if data.classification == ItemClassification.progression and not data.type == "Medal":
                prog_items.append(name)
        self.collect_by_name(prog_items)
        logger.info("Currently all of the multiworld's progressive items required are: " + str(self.multiworld.state.prog_items))
        logger.info("Multiworld Seed was: " + str(self.multiworld.seed))

        all_enemizer_locs: dict[str, LMLocationData] = {**CLEAR_GHOST_LOCATION_TABLE, **ENEMIZER_LOCATION_TABLE,
            **ROOM_BOO_LOCATION_TABLE, **LIGHT_LOCATION_TABLE, **PORTRAIT_LOCATION_TABLE, **TOAD_LOCATION_TABLE}

        for affected_region in self.world.ghost_affected_regions.keys():
            if self.world.ghost_affected_regions[affected_region] == "No Element":
                continue

            region_enemizer_locs: list[str] = [loc for (loc, loc_data) in all_enemizer_locs.items() if loc_data.region == affected_region]
            for region_loc in region_enemizer_locs:
                self.assertFalse(self.multiworld.state.can_reach_location(region_loc, self.player))