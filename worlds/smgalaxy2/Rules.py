from turtledemo.penrose import star
from typing import TYPE_CHECKING, Any

from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_, HasFromList, Rule, HasGroup, CanReachLocation
from .Options import GreenStarBehavior, GreenStarstoFinish, EnableGreenStars, PowerupRando, MoveRando, YoshiRando, \
    CoinLumaLocks, ObjectRando, CometMission, \
    CometItems, WorldShuffle, LogicDifficulty
from .Constants.Names import item_names as itemname
from .Constants.Names import location_names as locname

# Common Rules
NoGreenList: list[str] = [itemname.POWER, itemname.GRAND, itemname.GRAND1, itemname.GRAND2, itemname.GRAND3, itemname.GRAND4, itemname.GRAND5, itemname.GRAND6,itemname.GRAND7]
GreenSeparateGoal: Rule[Any] = ((Has(itemname.GREEN, FromOption(GreenStarstoFinish)) & OptionFilter(GreenStarBehavior, 1))
                     | OptionFilter(GreenStarBehavior, 2))

GreenStarLocationRule: Rule[Any] = ((True_() & OptionFilter(EnableGreenStars, 1))
                                    | (OptionFilter(EnableGreenStars, 2)&CanReachLocation(locname.GALAXYGENSTAR1)
                               &((HasFromList(*NoGreenList, count=120)&OptionFilter(GreenStarBehavior, 0, operator="ne"))
                                 |(HasGroup("Power Stars", count=120)&OptionFilter(GreenStarBehavior, 0))))
                                    | (OptionFilter(EnableGreenStars, 3)&Has(itemname.GREENCOMETKEY)))

GreenStarsSeparate: Rule[Any] = (True_() & OptionFilter(GreenStarBehavior, 0, operator="gt")
                                 |True_() & OptionFilter(EnableGreenStars, 0))
IncludeGreenStars: Rule[Any] = (True_() & OptionFilter(GreenStarBehavior, 0)
                                & OptionFilter(EnableGreenStars, 0, operator="gt"))

CometMissionOff: Rule[Any] = True_()&OptionFilter(CometMission, 0) # CanReach previous star/CanReach Comet Medal/Both/Neither
CometItemsOff: Rule[Any] = True_()&OptionFilter(CometItems, 0)
Comet1ItemAccess: Rule[Any] = CometItemsOff|(Has(itemname.ALLCOMETSKEY)&OptionFilter(CometItems, 1))# Has All Comet Key and option or unlocked

def PowerStarCount(star_count: int) -> Rule[Any]:
    return (GreenStarsSeparate & HasFromList(*NoGreenList, count = (min(star_count, 120))) |
            IncludeGreenStars & HasGroup("Power Stars", count = star_count))

OpenWorlds: Rule[Any] = True_()&OptionFilter(WorldShuffle, WorldShuffle.option_Open)

PowerUpOff: Rule[Any] = True_()&OptionFilter(PowerupRando,0)
BeeFlight: Rule[Any] = PowerUpOff|(Has(itemname.BEEMARIO)&OptionFilter(PowerupRando,1))
SUPAPOWA: Rule[Any] = PowerUpOff|(Has(itemname.SUPASTAR)&OptionFilter(PowerupRando,1))
FireMario: Rule[Any] = PowerUpOff|(Has(itemname.FIREFLOWER)&OptionFilter(PowerupRando,1))
SPRONGIN: Rule[Any] = PowerUpOff|(Has(itemname.SPRING)&OptionFilter(PowerupRando,1))
BooMario: Rule[Any] = PowerUpOff|(Has(itemname.BOOMARIO)&OptionFilter(PowerupRando,1))
CloudMario: Rule[Any] = PowerUpOff|(Has(itemname.CLOUD)&OptionFilter(PowerupRando,1))
ROCKNROLLIN: Rule[Any] = PowerUpOff|(Has(itemname.ROCK)&OptionFilter(PowerupRando,1))
DRILLMASTER: Rule[Any] = PowerUpOff|(Has(itemname.SPINDRILL)&OptionFilter(PowerupRando,1))

YoshiRandoOff: Rule[Any] = True_()&OptionFilter(YoshiRando, 0)
CanRideDino: Rule[Any] = YoshiRandoOff|(Has(itemname.YOSHI)&OptionFilter(YoshiRando, 1))
CanDinoBlimp: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIBLIMP)&OptionFilter(YoshiRando, 1))
CanDinoRun: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIPEPPER)&OptionFilter(YoshiRando, 1))
CanDinoGlow: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIBULB)&OptionFilter(YoshiRando, 1))
CanDinoSwing: Rule[Any] = YoshiRandoOff|(CanRideDino&Has(itemname.YOSHIFLOWER)&OptionFilter(YoshiRando, 1))

MoveRandoOff: Rule[Any] = True_()&OptionFilter(MoveRando,0)
CanStarbitShoot: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSTARBIT)&OptionFilter(MoveRando, 0, operator="gt"))
CanBackflip: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOBACK)&OptionFilter(MoveRando, 0, operator="gt"))
CanSideflip: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSIDE)&OptionFilter(MoveRando, 0, operator="gt"))
CanAirSpin: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOAIRSPIN)&OptionFilter(MoveRando, 0, operator="gt"))
CanLongJump: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOLONG)&OptionFilter(MoveRando, 0, operator="gt"))
CanSwim: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSWIM)&OptionFilter(MoveRando, 0, operator="gt"))
CanWallJump: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOWALL)&OptionFilter(MoveRando, 0, operator="gt"))
CanPound: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOPOUND)&OptionFilter(MoveRando, 0, operator="gt"))
CanClimbPole: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOCLIMB)&OptionFilter(MoveRando, 0, operator="gt"))
CanSlide: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSLIDE)&OptionFilter(MoveRando, 0, operator="gt"))
CanGrabLedge: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOLEDGE)&OptionFilter(MoveRando, 0, operator="gt"))
CanBalance: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOSTARBALL)&OptionFilter(MoveRando, 0, operator="gt"))
CanRideBird: Rule[Any] = MoveRandoOff| (Has(itemname.MARIOFLUZZ)&OptionFilter(MoveRando, 0, operator="gt"))
CanTriple: Rule[Any] = (MoveRandoOff
                        |(Has(itemname.MARIOPROGJUMP, 2)&OptionFilter(MoveRando, 1))
                        |(Has(itemname.MARIOTRIPLE)&OptionFilter(MoveRando,2)))
CanDouble: Rule[Any] = (MoveRandoOff
                        |(Has(itemname.MARIOPROGJUMP)&OptionFilter(MoveRando, 1))
                        |(Has(itemname.MARIODOUBLE)&OptionFilter(MoveRando,2))
                        |CanTriple)
JumpHeight6: Rule[Any] = (CanTriple&CanAirSpin)
JumpHeight5: Rule[Any] = (CanTriple|(CanSideflip&CanAirSpin)|(CanBackflip&CanAirSpin)|JumpHeight6)
JumpHeight4: Rule[Any] = (CanDouble&CanAirSpin|JumpHeight5)
JumpHeight3: Rule[Any] = (CanAirSpin|CanSideflip|CanBackflip|JumpHeight4)
JumpHeight2: Rule[Any] = (CanDouble|JumpHeight3)
JumpHeight1: Rule[Any] = True_()

CanMakeCloud: Rule[Any] = CloudMario&CanAirSpin
CanWallSpin: Rule[Any] = CanWallJump&CanAirSpin
CanLongSpin: Rule[Any] = CanLongJump&CanAirSpin
CanBackOrSideflip: Rule[Any] = CanBackflip|CanSideflip

ObjectRandoOff: Rule[Any] = True_()&OptionFilter(ObjectRando, 0)
CanSwing: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSWING)&OptionFilter(ObjectRando,1))
CanCannon: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOCANNON)&OptionFilter(ObjectRando,1))
CanShell: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSHELL)&OptionFilter(ObjectRando,1))
CanCollectStarChips: Rule[Any] = ObjectRandoOff|(Has(itemname.MARIOSTARCHIPS)&OptionFilter(ObjectRando,1))

CoinLumaBase: Rule[Any] = ((True_()&OptionFilter(CoinLumaLocks, 0))
                           |(Has(itemname.COINLUMAKEY)&OptionFilter(CoinLumaLocks,1)))

HellLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 3)
HardLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 2)
MediumLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 1)
EasyLogic: Rule[Any] = True_()&OptionFilter(LogicDifficulty, 0)
CanInfiniteFlutter: Rule[Any] = HellLogic&CanRideDino

MailtoadOpen: Rule[Any] = PowerStarCount(13) # May need additional rules here in the future

def CoinLumaRule(coin_count: int) -> Rule[Any]:
    return (True_() if coin_count < 100 else Has("Can Farm Coins"))

