import copy
from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld
from entrance_rando import disconnect_entrance_for_randomization

from .Constants.Names import region_names as regname
from .Options import SMG2Options
from .locations import SMG2Location, locPC_table, base_stars_locations, SMG2LocationData
from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import SMG2World

class SMG2RegionData(NamedTuple):
    type: str  # type of randomization for GER
    entrance_regions: Optional[list[str]] # Regions with entrances to this one
    exit_regions: Optional[list[str]] # Regions with entrances from this one
    ger_exits: Optional[list[str]] # connected exit regions that can be swapped during Entrance Rando
    default_access: Optional[dict[str, int]]
    region_offset: Optional[int] = None
    in_game_name: Optional[str] = None

class SMGRegion(Region):
    game: str = "Super Mario Galaxy"
    region_data: SMG2RegionData

    def __init__(self, region_name: str, region_data: SMG2RegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

major_entr_list: list[str] = ["Dome 1 First Orbit Galaxy", "Dome 2 First Orbit Galaxy", "Dome 3 First Orbit Galaxy",
                              "Dome 4 First Orbit Galaxy", "Dome 5 First Orbit Galaxy", "Dome 6 First Orbit Galaxy",
                              "Dome 1 Second Orbit Galaxy", "Dome 2 Third Orbit Galaxy", "Dome 3 Third Orbit Galaxy",
                              "Dome 4 Second Orbit Galaxy", "Dome 5 Second Orbit Galaxy", "Dome 6 Second Orbit Galaxy",
                              "Dome 4 Third Orbit Galaxy", "Dome 5 Third Orbit Galaxy", "Dome 6 Fourth Orbit Galaxy"]

boss_entr_list: list[str] = ["Dome 1 Fifth Orbit Galaxy", "Dome 2 Fifth Orbit Galaxy", "Dome 3 Fifth Orbit Galaxy",
                             "Dome 4 Fifth Orbit Galaxy", "Dome 5 Fifth Orbit Galaxy"]

gal_minor_entr_list: list[str] = ["Dome 1 Third Orbit Galaxy", "Dome 2 Second Orbit Galaxy",
                                  "Dome 3 Second Orbit Galaxy", "Dome 4 Fourth Orbit Galaxy",
                                  "Dome 5 Fourth Orbit Galaxy", "Dome 6 Third Orbit Galaxy",
                                  "Dome 1 Fourth Orbit Galaxy", "Dome 2 Fourth Orbit Galaxy",
                                  "Dome 3 Fourth Orbit Galaxy"]

obs_entr_list: list[str] = ["Sweet Sweet Hungry Luma", "Sling Pod Hungry Luma", "Drip Drop Hungry Luma",
                            "Bigmouth Hungry Luma", "Sand Spiral Hungry Luma", "Snow Cap Hungry Luma", "Gateway Dome",
                            "Boo's Boneyard Hungry Luma", "Rolling Gizmo Launch Star", "Loopdeeswoop Launch Star",
                            "Bubble Blast Launch Star"]

all_galaxy_slots: list[str] = major_entr_list + gal_minor_entr_list + obs_entr_list + boss_entr_list

region_list: dict[str, SMG2RegionData] = {
    regname.SHIP: SMG2RegionData("Main", [],
                                 [],
                                 [regname.WORLD1, regname.LIBRARY, regname.WORLD3, regname.WORLD6, regname.GATEWAY,
                                  regname.WORLD5, regname.WORLD4, regname.WORLD2, regname.COTU, regname.SWEETSWEET,
                                  regname.SLINGPOD, regname.DRIPDROP, regname.BIGMOUTH, regname.SANDSPIRAL,
                                  regname.SNOWCAP, regname.BOOBONE, regname.ROLLINGGIZ, regname.BUBBLEBLAST,
                                  regname.LOOPDEESWOOP, regname.FINALE], {}),
    regname.WORLD1: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.GOODEGG, regname.HONEYHIVE, regname.LOOPDEELOOP, regname.FLIPSWITCH,
                                    regname.BOWJR1],
                                   {}),
    regname.WORLD2: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.SPACEJUNK, regname.ROLLINGGREEN, regname.BATTLEROCK, regname.HURRYSCUR,
                                     regname.BOWSER1],
                                   {"Grand Star": 1}),
    regname.WORLD5: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.GOLDLEAF, regname.SEASLIDE, regname.TOYTIME, regname.BONEFIN,
                                   regname.BOWJR3],
                                   {"Grand Star": 4}),
    regname.WORLD3: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.BEACHBOWL, regname.BUBBLEBREEZE, regname.GHOSTLY, regname.BUOY,
                                    regname.BOWJR2],
                                   {"Grand Star": 2}),
    regname.WORLD4: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.GUSTY, regname.FREEZEFLAME, regname.DUSTY, regname.HONEYCLIMB,
                                    regname.BOWSER2],
                                   {"Grand Star": 3}),
    regname.WORLD6: SMG2RegionData("Dome", [regname.SHIP], [],
                                   [regname.DEEPDARK, regname.DREADNOUGHT, regname.MATTER, regname.MELTY],
                                   {"Grand Star": 5}),
    regname.LIBRARY: SMG2RegionData("Dome", [regname.SHIP], [], [], {}),
    regname.COTU: SMG2RegionData("Dome", [regname.SHIP], [], [regname.BOWSER3], {"Grand Star": 5, "Power Star": 60}),
    regname.GATEWAY: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x0, "HeavensDoorGalaxy"),
    regname.SWEETSWEET: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x14, "BeltConveyerExGalaxy"),
    regname.SLINGPOD: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x2C, "CocoonExGalaxy"),
    regname.DRIPDROP: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x44, "TearDropGalaxy"),
    regname.BIGMOUTH: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x90, "FishTunnelGalaxy"),
    regname.SANDSPIRAL: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x78, "TransformationExGalaxy"),
    regname.SNOWCAP: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x60, "SnowCapsuleGalaxy"),
    regname.BOOBONE: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0x48, "TeresaMario2DGalaxy"),
    regname.ROLLINGGIZ: SMG2RegionData("Special", [regname.TRIALS], [], [], {}, 0x98, "TamakoroExLv2Galaxy"),
    regname.LOOPDEESWOOP: SMG2RegionData("Special", [regname.TRIALS], [], [], {}, 0x9C, "SurfingLv2Galaxy"),
    regname.BUBBLEBLAST: SMG2RegionData("Special", [regname.TRIALS], [], [], {}, 0xA0, "CubeBubbleExLv2Galaxy"),
    #regname.FINALE: SMG2RegionData("Special", [regname.SHIP], [], [], {}, 0xA4, "PeachCastleFinalGalaxy"),
    regname.BOWJR1: SMG2RegionData("Boss", [regname.WORLD1], [], [], {}, 0x18, "TriLegLv1Galaxy"),
    regname.BOWJR2: SMG2RegionData("Boss", [regname.WORLD3], [], [], {}, 0x4C, "KoopaJrShipLv1Galaxy"),
    regname.BOWJR3: SMG2RegionData("Boss", [regname.WORLD5], [], [], {}, 0x7C, "FloaterOtaKingGalaxy"), # Dome 5
    regname.BOWSER1: SMG2RegionData("Boss", [regname.WORLD2], [], [], {}, 0x30, "KoopaBattleVs1Galaxy"),
    regname.BOWSER2: SMG2RegionData("Boss", [regname.WORLD4], [], [], {}, 0x64, "KoopaBattleVs2Galaxy"),
    regname.BOWSER3: SMG2RegionData("Goal", [regname.COTU], [], [], {}, 0x94, "KoopaBattleVs3Galaxy"),
    regname.GOODEGG: SMG2RegionData("Major", [regname.WORLD1], [], [], {}, 0x4, "EggStarGalaxy"),
    regname.HONEYHIVE: SMG2RegionData("Major", [regname.WORLD1], [], [], {}, 0x8, "HoneyBeeKingdomGalaxy"),
    regname.SPACEJUNK: SMG2RegionData("Major", [regname.WORLD2], [], [], {}, 0x1C, "StarDustGalaxy"),
    regname.BATTLEROCK: SMG2RegionData("Major", [regname.WORLD2], [], [], {}, 0x24, "BattleShipGalaxy"),
    regname.BEACHBOWL: SMG2RegionData("Major", [regname.WORLD3], [], [], {}, 0x34, "HeavenlyBeachGalaxy"),
    regname.GHOSTLY: SMG2RegionData("Major", [regname.WORLD3], [], [], {}, 0x3C, "PhantomGalaxy"),
    regname.GUSTY: SMG2RegionData("Major", [regname.WORLD4], [], [], {}, 0x50, "CosmosGardenGalaxy"),
    regname.FREEZEFLAME: SMG2RegionData("Major", [regname.WORLD4], [], [], {}, 0x54, "IceVolcanoGalaxy"),
    regname.DUSTY: SMG2RegionData("Major", [regname.WORLD4], [], [], {}, 0x5C, "SandClockGalaxy"),
    regname.GOLDLEAF: SMG2RegionData("Major", [regname.WORLD5], [], [], {}, 0x68, "ReverseKingdomGalaxy"),
    regname.SEASLIDE: SMG2RegionData("Major", [regname.WORLD5], [], [], {}, 0x6C, "OceanRingGalaxy"),
    regname.TOYTIME: SMG2RegionData("Major", [regname.WORLD5], [], [], {}, 0x74, "FactoryGalaxy"),
    regname.DEEPDARK: SMG2RegionData("Major", [regname.WORLD6], [], [], {}, 0x80, "OceanPhantomCaveGalaxy"),
    regname.DREADNOUGHT: SMG2RegionData("Major", [regname.WORLD6], [], [], {}, 0x84, "CannonFleetGalaxy"),
    regname.MELTY: SMG2RegionData("Major", [regname.WORLD6], [], [], {}, 0x8C, "HellProminenceGalaxy"),
    regname.LOOPDEELOOP: SMG2RegionData("Minor", [regname.WORLD1], [], [], {}, 0xC, "SurfingLv1Galaxy"),
    regname.FLIPSWITCH: SMG2RegionData("Minor", [regname.WORLD1], [], [], {}, 0x10, "FlipPanelExGalaxy"),
    regname.ROLLINGGREEN: SMG2RegionData("Minor", [regname.WORLD2], [], [], {}, 0x20, "TamakoroExLv1Galaxy"),
    regname.HURRYSCUR: SMG2RegionData("Minor", [regname.WORLD2], [], [], {}, 0x28, "BreakDownPlanetGalaxy"),
    regname.BUBBLEBREEZE: SMG2RegionData("Minor", [regname.WORLD3], [], [], {}, 0x38, "CubeBubbleExLv1Galaxy"),
    regname.BUOY: SMG2RegionData("Minor", [regname.WORLD3], [], [], {}, 0x40, "OceanFloaterLandGalaxy"),
    regname.HONEYCLIMB: SMG2RegionData("Minor", [regname.WORLD4], [], [], {}, 0x58, "HoneyBeeExGalaxy"),
    regname.BONEFIN: SMG2RegionData("Minor", [regname.WORLD5], [], [], {}, 0x70, "SkullSharkGalaxy"),
    regname.MATTER: SMG2RegionData("Minor", [regname.WORLD6], [], [], {}, 0x88, "DarkRoomGalaxy"),
    regname.TRIALS: SMG2RegionData("Hub", [], [regname.SHIP], [regname.LOOPDEESWOOP, regname.BUBBLEBLAST, regname.ROLLINGGIZ], {"Green Star": 1}),
}

major_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Major"]

minor_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Minor"]

boss_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Boss"]

specials_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Special"]

def by_type_shuffle(world: "SMG2World", entrances: list, galaxies: list[str]):
    for entrance in entrances:
        slot = world.get_entrance(entrance)
        galaxy = world.get_region(world.random.choice(sorted(galaxies)))
        galaxies.remove(galaxy.name)
        er_target: Entrance = {e.name: e for e in galaxy.entrances}[galaxy.name]
        galaxy.entrances.remove(er_target)
        slot.connect(galaxy)

def create_regions(world: "SMG2World"):
    for region_name in region_list.keys():
        world.multiworld.regions.append(SMGRegion(region_name, region_list[region_name], world.player, world.multiworld))

    create_locations(base_stars_locations, world)

    if world.options.enable_purple_coin_stars.value == 1:
        create_locations(locPC_table, world)

    if world.options.stars_to_finish.value > 103 >= len(list(world.get_locations()))-1:
        world.options.stars_to_finish.value = len(list(world.get_locations()))-1

def connect_regions(world: "SMG2World", player: int, source: str, target: str, name: str, rule=None):
    sourceRegion = world.get_region(source)
    targetRegion = world.get_region(target)

    connection = Entrance(player, name, sourceRegion)
    if rule:
        add_rule(connection, rule, "and")

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_region(name: str, world: "SMG2World") -> Region:
    return Region(name, world.player, world.multiworld, name)

def create_locations(locs: dict[str, SMG2LocationData], world: "SMG2World"):
    for name, data in locs.items():
        reg = world.get_region(data.region)
        location = SMG2Location(world.player, name, reg)
        if data.default_access:
            for item, count in data.default_access:
                rule = lambda state,i=item, c=count: state.has(i, world.player, count)
                add_rule(location, rule, "and")

        reg.locations += [location]

def disconnect_from_option(world: "SMG2World") -> str:
    Dome1Slot1 = "Good Egg Galaxy"
    if "Bosses" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Fifth Orbit Galaxy"), 0, regname.BOWJR1)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Fifth Orbit Galaxy"), 0, regname.BOWSER1)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Fifth Orbit Galaxy"), 0, regname.BOWJR2)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Fifth Orbit Galaxy"), 0, regname.BOWSER2)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Fifth Orbit Galaxy"), 0, regname.BOWJR3)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, boss_entr_list, copy.deepcopy(boss_galaxy_list))
    if "Dome Majors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 First Orbit Galaxy"), 0, regname.GOODEGG)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 First Orbit Galaxy"), 0, regname.SPACEJUNK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 First Orbit Galaxy"), 0, regname.BEACHBOWL)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 First Orbit Galaxy"), 0, regname.GUSTY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 First Orbit Galaxy"), 0, regname.GOLDLEAF)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 First Orbit Galaxy"), 0, regname.DEEPDARK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Second Orbit Galaxy"), 0, regname.HONEYHIVE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Third Orbit Galaxy"), 0, regname.BATTLEROCK)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Third Orbit Galaxy"), 0, regname.GHOSTLY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Second Orbit Galaxy"), 0, regname.FREEZEFLAME)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Second Orbit Galaxy"), 0, regname.SEASLIDE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Second Orbit Galaxy"), 0, regname.DREADNOUGHT)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Third Orbit Galaxy"), 0, regname.DUSTY)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Third Orbit Galaxy"), 0, regname.TOYTIME)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Fourth Orbit Galaxy"), 0, regname.MELTY)

        # Ensure the first galaxy is a major one
        Dome1Galaxy1Slot = world.get_entrance("Dome 1 First Orbit Galaxy")
        major_list_copy = copy.deepcopy(major_galaxy_list)
        starting_galaxy = world.get_region(world.random.choice(sorted(major_list_copy)))
        major_list_copy.remove(starting_galaxy.name)
        er_target: Entrance = {e.name: e for e in starting_galaxy.entrances}[starting_galaxy.name] # couldn't figure out how to index by the entrance name but this should only ever have one of these entrances anyway
        starting_galaxy.entrances.remove(er_target)
        Dome1Galaxy1Slot.connect(starting_galaxy)
        Dome1Slot1 = starting_galaxy.name
        major_entr_list_copy = copy.deepcopy(major_entr_list)
        major_entr_list_copy.remove("Dome 1 First Orbit Galaxy")
        if world.options.galaxy_shuffle_type.value != 2:
            by_type_shuffle(world, major_entr_list_copy, major_list_copy)

    if "Dome Minors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Third Orbit Galaxy"), 0, regname.LOOPDEELOOP)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Second Orbit Galaxy"), 0, regname.ROLLINGGREEN)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Second Orbit Galaxy"), 0, regname.BUBBLEBREEZE)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 4 Fourth Orbit Galaxy"), 0, regname.HONEYCLIMB)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 5 Fourth Orbit Galaxy"), 0, regname.BONEFIN)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 6 Third Orbit Galaxy"), 0, regname.MATTER)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 1 Fourth Orbit Galaxy"), 0, regname.FLIPSWITCH)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 2 Fourth Orbit Galaxy"), 0, regname.HURRYSCUR)
        disconnect_entrance_for_randomization(world.get_entrance("Dome 3 Fourth Orbit Galaxy"), 0, regname.BUOY)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, gal_minor_entr_list, copy.deepcopy(minor_galaxy_list))
    if "Observatory Specials" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("Sweet Sweet Hungry Luma"), 0, regname.SWEETSWEET)
        disconnect_entrance_for_randomization(world.get_entrance("Sling Pod Hungry Luma"), 0, regname.SLINGPOD)
        disconnect_entrance_for_randomization(world.get_entrance("Drip Drop Hungry Luma"), 0, regname.DRIPDROP)
        disconnect_entrance_for_randomization(world.get_entrance("Bigmouth Hungry Luma"), 0, regname.BIGMOUTH)
        disconnect_entrance_for_randomization(world.get_entrance("Sand Spiral Hungry Luma"), 0, regname.SANDSPIRAL)
        disconnect_entrance_for_randomization(world.get_entrance("Snow Cap Hungry Luma"), 0, regname.SNOWCAP)
        disconnect_entrance_for_randomization(world.get_entrance("Gateway Dome"), 0, regname.GATEWAY)
        disconnect_entrance_for_randomization(world.get_entrance("Boo's Boneyard Hungry Luma"), 0, regname.BOOBONE)
        disconnect_entrance_for_randomization(world.get_entrance("Rolling Gizmo Launch Star"), 0, regname.ROLLINGGIZ)
        disconnect_entrance_for_randomization(world.get_entrance("Loopdeeswoop Launch Star"), 0, regname.LOOPDEESWOOP)
        disconnect_entrance_for_randomization(world.get_entrance("Bubble Blast Launch Star"), 0, regname.BUBBLEBLAST)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, obs_entr_list, copy.deepcopy(specials_galaxy_list))

    #if world.options.shuffle_option.value == 3:


    return Dome1Slot1