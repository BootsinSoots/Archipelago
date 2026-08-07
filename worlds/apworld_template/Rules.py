from typing import TYPE_CHECKING, Any
from rule_builder import rules, options
from rule_builder.options import OptionFilter

from . import GameOptions

if TYPE_CHECKING:
    from .world import GameWorld

def connect_entrances(world: "GameWorld"):
    pass

OptionRule: rules.Rule[Any] = rules.True_()&OptionFilter(GameOptions.Option1, 1)