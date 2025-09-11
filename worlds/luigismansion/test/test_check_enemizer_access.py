from BaseClasses import ItemClassification
from test.bases import WorldTestBase

from .. import LMWorld, ITEM_TABLE

class LMTestBase(WorldTestBase):
    game = "Luigi's Mansion"
    world = LMWorld
    run_default_tests = False

class LocationFail(LMTestBase):
    options = {
        "enemizer": 1
    }

    def test_enemizer_locations_requires_element(self):
        if self.world.ghost_affected_regions["1F Bathroom"] == "No Element":
            print("1F Bathroom did not require an element, exiting...")
            return

        prog_items = []
        for name, data in ITEM_TABLE.items():
            if data.classification == ItemClassification.progression and not data.type == "Medal":
                prog_items.append(name)

        self.collect_by_name(prog_items)
        print("Currently all of the multiworld's progressive items required are: " + str(self.multiworld.state.prog_items))
        print("Multiworld Seed was: " + self.multiworld.seed)
        self.assertFalse(self.multiworld.state.can_reach_location("1F Bathroom Shelf Key", self.player))