from typing import Any, Dict

import Options as APOptions
from . import LuigiOptions as LMOptions

all_random_settings = {
    "progression_balancing":                          "random",
    "accessibility":                                  "random",
    LMOptions.RankRequirement.internal_name:           "random",
    LMOptions.LuigiWalkSpeed.internal_name:            "random",
    LMOptions.LuigiFearAnim.internal_name:             "random",
    LMOptions.BetterVacuum.internal_name:              "random",
    LMOptions.StartWithBooRadar.internal_name:         "random",
    LMOptions.StartHiddenMansion.internal_name:        "random",
    LMOptions.PickupAnim.internal_name:                "random",
    LMOptions.RandomMusic.internal_name:               "random",
    LMOptions.DoorRando.internal_name:                 "random",
    LMOptions.PortraitHints.internal_name:             "random",
    LMOptions.HintDistribution.internal_name:          "random",
    LMOptions.Toadsanity.internal_name:                "random",
    LMOptions.Plants.internal_name:                    "random",
    LMOptions.Boosanity.internal_name:                 "random",
    LMOptions.Portrification.internal_name:            "random",
    LMOptions.Lightsanity.internal_name:               "random",
    LMOptions.Walksanity.internal_name:                "random",
    LMOptions.SpeedySpirits.internal_name:             "random",
    LMOptions.BooGates.internal_name:                  "random",
    LMOptions.KingBooHealth.internal_name:             "random",
    LMOptions.MarioItems.internal_name:                "random",
    LMOptions.WashroomBooCount.internal_name:          "random",
    LMOptions.BalconyBooCount.internal_name:           "random",
    LMOptions.FinalBooCount.internal_name:             "random",
    LMOptions.BundleWeight.internal_name:              "random",
    LMOptions.CoinWeight.internal_name:                "random",
    LMOptions.BillWeight.internal_name:                "random",
    LMOptions.BarsWeight.internal_name:                "random",
    LMOptions.GemsWeight.internal_name:                "random",
    LMOptions.PoisonTrapWeight.internal_name:          "random",
    LMOptions.BombWeight.internal_name:                "random",
    LMOptions.IceTrapWeight.internal_name:             "random",
    LMOptions.BananaTrapWeight.internal_name:          "random",
    LMOptions.HeartWeight.internal_name:               "random",
    LMOptions.NothingWeight.internal_name:             "random",
    LMOptions.ChestTypes.internal_name:                "random",
    LMOptions.TrapChestType.internal_name:             "random",
    LMOptions.BooHealthOption.internal_name:           "random",
    LMOptions.BooHealthValue.internal_name:            "random",
    LMOptions.BooSpeed.internal_name:                  "random",
    LMOptions.BooEscapeTime.internal_name:             "random",
    LMOptions.BooAnger.internal_name:                  'random',
    LMOptions.Enemizer.internal_name:                  "random",
    LMOptions.RandomSpawn.internal_name:               "random",
    "death_link":                                      "random",
}

allsanity_settings = {
    LMOptions.Toadsanity.internal_name:                "true",
    LMOptions.Plants.internal_name:                    "true",
    LMOptions.Furnisanity.internal_name:               ["Full"],
    LMOptions.Boosanity.internal_name:                 "true",
    LMOptions.Portrification.internal_name:            "true",
    LMOptions.Lightsanity.internal_name:               "true",
    LMOptions.Walksanity.internal_name:                "true",
    LMOptions.SpeedySpirits.internal_name:             "true",
}

money_settings = {
    LMOptions.BundleWeight.internal_name:              100,
    LMOptions.CoinWeight.internal_name:                100,
    LMOptions.BillWeight.internal_name:                100,
    LMOptions.BarsWeight.internal_name:                100,
    LMOptions.GemsWeight.internal_name:                100,
    LMOptions.PoisonTrapWeight.internal_name:          0,
    LMOptions.BombWeight.internal_name:                0,
    LMOptions.IceTrapWeight.internal_name:             0,
    LMOptions.BananaTrapWeight.internal_name:          0,
}

trap_settings = {
    LMOptions.BundleWeight.internal_name:              0,
    LMOptions.CoinWeight.internal_name:                0,
    LMOptions.BillWeight.internal_name:                0,
    LMOptions.BarsWeight.internal_name:                0,
    LMOptions.GemsWeight.internal_name:                0,
    LMOptions.PoisonTrapWeight.internal_name:          100,
    LMOptions.BombWeight.internal_name:                100,
    LMOptions.IceTrapWeight.internal_name:             100,
    LMOptions.BananaTrapWeight.internal_name:          100,
}

lm_options_presets: Dict[str, Dict[str, Any]] = {
    "All random": all_random_settings,
    "I Love Money": money_settings,
    "Raining Traps": trap_settings,
    "Allsanity": allsanity_settings,
}