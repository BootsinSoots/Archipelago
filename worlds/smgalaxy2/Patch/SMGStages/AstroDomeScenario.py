from enum import StrEnum

from ..extensions import RARCExtended

ASTRO_DOME_SCENARIO_RELATIVE_PATH = "/DATA/files/StageData/AstroDome/AstroDomeScenario.arc"
SCENARIO_DATA_FILE_NAME = "scenariodata.bcsv"

class ScenarioDataFieldName(StrEnum):
    SCENARIO_NUMBER: str = "ScenarioNo"
    SCENARIO_NAME: str = "ScenarioName"
    POWER_STAR_ID: str = "PowerStarId"
    APPEAR_POWER_STAR_OBJect: str = "AppearPowerStarObj"
    COMET: str = "Comet"
    LUIGI_MODE_TIMER: str = "LuigiModeTimer"
    ASTRO_DOME: str = "AstroDome"
    IS_HIDDEN: str = "IsHidden"
    ERROR_CHECK: str = "ErrorCheck"


class AstroDomeScenario(RARCExtended):
    def __init__(self):
        self.relative_path = ASTRO_DOME_SCENARIO_RELATIVE_PATH
        super().__init__()

        # Get the scenariodata bcsv
        self.scenariodata = self.get_bcsv_file('', SCENARIO_DATA_FILE_NAME)
        
        # Get the indices of the fields
        self.scenariono_index = self.scenariodata.get_field_index(ScenarioDataFieldName.SCENARIO_NUMBER)
        self.astrodome_index = self.scenariodata.get_field_index(ScenarioDataFieldName.ASTRO_DOME)

    def is_valid_shuffle(self, dome_shuffle: dict[int, int]) -> bool:
        """Validate that the dome shuffle mapping contains all indices 1-6 as both keys and values."""
        for index in range(1,7):
            if index not in dome_shuffle.keys() or index not in dome_shuffle.values():
                return False
        return True

    def shuffle_loading_zones(self, shuffle: dict[int, int]) -> None:
        """
        Shuffle the loading zones for the domes within the observatory. The shuffle maps the old dome index to the new dome index (from 1 to 6).
        The shuffle dict must contain all indices from 1 to 6 as both keys and values. The information to load the dome is contained in scenariodata.
        Field "AstroDome" determines which loading zone it should load and gets set according to the shuffle dict. The value of "AstroDome"
        is equal to 1 bitshifted left by dome index minus 1.
        shuffle:
            key: old dome index (1-6)
            value: new dome index (1-6)
        """
        # Make sure its a valid shuffle
        if not self.is_valid_shuffle(shuffle):
            raise ValueError(f"Invalid shuffle: {shuffle}")

        print("Updating dome loading zones...")
        
        for entry_index in range(self.scenariodata.entry_count):
            scenariono = self.scenariodata.get_value_by_index(entry_index, self.scenariono_index)
            new_value = 1 << (shuffle[scenariono] - 1)

            print(f"Loading zone dome {scenariono} -> dome {shuffle[scenariono]}")

            self.scenariodata.set_value_by_index(entry_index, self.astrodome_index, new_value)

        self.scenariodata.save_changes()
