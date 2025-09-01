from BaseClasses import ItemClassification
from test.bases import WorldTestBase

from .. import LMWorld, ITEM_TABLE

class LMTestBase(WorldTestBase):
    game = "Luigi's Mansion"
    world = LMWorld

class LocationFail(LMTestBase):
    options = {
        "enemizer": 1
    }

    def test_enemizer_locations_requires_element(self):
        prog_items = []
        for name, data in ITEM_TABLE.items():
            if data.classification == ItemClassification.progression and not data.type == "Medal":
                prog_items.append(name)

        self.collect_by_name(prog_items)
        print(self.multiworld.state.prog_items)
        print(self.multiworld.seed)
        self.assertFalse(self.multiworld.state.can_reach_location("1F Bathroom Shelf Key", self.player))