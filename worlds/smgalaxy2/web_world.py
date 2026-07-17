from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld


from .Options import option_groups, option_presets


# For our game to display correctly on the website, we need to define a WebWorld subclass.
class SMG2WebWorld(WebWorld):
    game = "Super Mario Galaxy 2"
    theme = "ice"

    options_presets = option_presets
    option_groups = option_groups

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Super Mario Galaxy 2 for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["CosmicCarbon"],
        # This is mostly placeholder till someone writes the full guide
    )
    tutorials = [setup_en]
    #option_groups = option_groups