import copy
from typing import NamedTuple, Optional, Callable, TYPE_CHECKING
from BaseClasses import Region, Entrance, MultiWorld
from entrance_rando import disconnect_entrance_for_randomization
from rule_builder.rules import CanReachLocation

from .Constants.Names import region_names as regname
from .Constants.Names import location_names as locname
from .Constants.Names.region_names import SPACSTOR2GSTAR3
from .Options import SMG2Options
from .locations import SMG2Location, base_stars_locations, SMG2LocationData, green_star_locations

if TYPE_CHECKING:
    from . import SMG2World

class SMG2RegionData(NamedTuple):
    type: str  # type of randomization for GER
    entrance_regions: Optional[list[str]] # Regions with entrances to this one
    exit_regions: Optional[list[str]] # Regions with entrances from this one
    region_offset: Optional[int] = None
    in_game_name: Optional[str] = None

class SMGRegion(Region):
    game: str = "Super Mario Galaxy 2"
    region_data: SMG2RegionData

    def __init__(self, region_name: str, region_data: SMG2RegionData, player: int, multiworld: MultiWorld):
        super().__init__(region_name, player, multiworld)
        self.region_data = region_data

major_entr_list: list[str] = ["World 1 Slot 1 Galaxy", "World 1 Slot 2 Galaxy", "World 1 Slot 3 Galaxy",
                              "World 1 Slot 5 Galaxy", "World 2 Slot 1 Galaxy", "World 2 Slot 2 Galaxy",
                              "World 2 Slot 3 Galaxy", "World 2 Slot 3 Galaxy", "World 3 Slot 1 Galaxy",
                              "World 3 Slot 2 Galaxy", "World 3 Slot 3 Galaxy", "World 3 Slot 4 Galaxy",
                              "World 4 Slot 1 Galaxy", "World 4 Slot 3 Galaxy", "World 4 Slot 5 Galaxy",
                              "World 4 Slot 6 Galaxy", "World 5 Slot 1 Galaxy", "World 5 Slot 2 Galaxy",
                              "World 5 Slot 4 Galaxy", "World 5 Slot 6 Galaxy", "World 6 Slot 1 Galaxy",
                              "World 6 Slot 2 Galaxy", "World 6 Slot 4 Galaxy", "World 6 Slot 6 Galaxy"]

boss_entr_list: list[str] = ["World 1 Slot 7 Galaxy", "World 2 Slot 7 Galaxy", "World 3 Slot 7 Galaxy",
                             "World 4 Slot 7 Galaxy", "World 5 Slot 7 Galaxy"]

ggen_entr: list[str] = ["World 6 Slot 7 Galaxy"]

gal_minor_entr_list: list[str] = ["World 1 Slot 6 Galaxy", "World 2 Slot 4 Galaxy", "World 3 Slot 6 Galaxy",
                                  "World 4 Slot 4 Galaxy", "World 5 Slot 3 Galaxy", "World 6 Slot 5 Galaxy"]

luma_entr_list: list[str] = ["World 1 Slot 4 Galaxy", "World 2 Slot 6 Galaxy", "World 3 Slot 5 Galaxy",
                            "World 4 Slot 2 Galaxy", "World 5 Slot 5 Galaxy", "World 6 Slot 3 Galaxy", "World 7 Slot 6 Galaxy"]

special_entr_list: list[str] = ["World 7 Slot 1 Galaxy", "World 7 Slot 2 Galaxy", "World 7 Slot 3 Galaxy",
                                "World 7 Slot 4 Galaxy", "World 7 Slot 5 Galaxy"]

grand_entr: list[str] = ["World 7 Slot 7 Galaxy"]

all_galaxy_slots: list[str] = (major_entr_list + gal_minor_entr_list + luma_entr_list + boss_entr_list
                               + special_entr_list + ggen_entr + grand_entr)

# TODO Replace in game name for galaxies, or remove entirely
region_list: dict[str, SMG2RegionData] = {
    regname.SHIP: SMG2RegionData("Main", [], []),
    regname.WORLD1: SMG2RegionData("World", [regname.SHIP], []),
    regname.WORLD2: SMG2RegionData("World", [regname.SHIP], []),
    regname.WORLD5: SMG2RegionData("World", [regname.SHIP], []),
    regname.WORLD3: SMG2RegionData("World", [regname.SHIP], []),
    regname.WORLD4: SMG2RegionData("World", [regname.SHIP], []),
    regname.WORLD6: SMG2RegionData("World", [regname.SHIP], []),
    regname.SHIPINSIDE: SMG2RegionData("Main", [regname.SHIP], []),
    regname.WORLD7: SMG2RegionData("World", [regname.SHIP], []),
    # Hungry Luma Galaxies
    regname.FLIPSWAP: SMG2RegionData("Luma", [regname.WORLD1], [], 0x0, "HeavensDoorGalaxy"),
    regname.HONEYBLOOM: SMG2RegionData("Luma", [regname.WORLD2], [], 0x14, "BeltConveyerExGalaxy"),
    regname.BEATBLOCK: SMG2RegionData("Luma", [regname.WORLD3], [], 0x2C, "CocoonExGalaxy"),
    regname.SWEETMYS: SMG2RegionData("Luma", [regname.WORLD4], [], 0x44, "TearDropGalaxy"),
    regname.FLEETGLIDE: SMG2RegionData("Luma", [regname.WORLD5], [], 0x90, "FishTunnelGalaxy"),
    regname.FLASHBLACK: SMG2RegionData("Luma", [regname.WORLD6], [], 0x78, "TransformationExGalaxy"),
    regname.FLIPOUT: SMG2RegionData("Luma", [regname.WORLD7], [], 0x60, "SnowCapsuleGalaxy"),
    # Boss Galaxies
    regname.BOWJR1: SMG2RegionData("Boss", [regname.WORLD1], [], 0x18, "TriLegLv1Galaxy"),
    regname.BOWJR2: SMG2RegionData("Boss", [regname.WORLD3], [], 0x4C, "KoopaJrShipLv1Galaxy"),
    regname.BOWJR3: SMG2RegionData("Boss", [regname.WORLD5], [], 0x7C, "FloaterOtaKingGalaxy"), # Dome 5
    regname.BOWSER1: SMG2RegionData("Boss", [regname.WORLD2], [], 0x30, "KoopaBattleVs1Galaxy"),
    regname.BOWSER2: SMG2RegionData("Boss", [regname.WORLD4], [], 0x64, "KoopaBattleVs2Galaxy"),
    regname.BOWSER3: SMG2RegionData("Goal", [regname.WORLD6], [], 0x94, "KoopaBattleVs3Galaxy"),
    # Major Galaxies
    regname.SKYOBS: SMG2RegionData("Major", [regname.WORLD1], [], 0x4, "EggStarGalaxy"),
    regname.GOODEGG: SMG2RegionData("Major", [regname.WORLD1], [], 0x4, "EggStarGalaxy"),
    regname.SPINDIG: SMG2RegionData("Major", [regname.WORLD1], [], 0x8, "HoneyBeeKingdomGalaxy"),
    regname.FLUFFBLUFF: SMG2RegionData("Major", [regname.WORLD1], [], 0x1C, "StarDustGalaxy"),
    regname.PUZZPLAN: SMG2RegionData("Major", [regname.WORLD2], [], 0x24, "BattleShipGalaxy"),
    regname.HIGHTAIL: SMG2RegionData("Major", [regname.WORLD2], [], 0x34, "HeavenlyBeachGalaxy"),
    regname.BOULBOWL: SMG2RegionData("Major", [regname.WORLD2], [], 0x3C, "PhantomGalaxy"),
    regname.COSMICO: SMG2RegionData("Major", [regname.WORLD2], [],  0x50, "CosmosGardenGalaxy"),
    regname.TALLTRUNK: SMG2RegionData("Major", [regname.WORLD3], [], 0x54, "IceVolcanoGalaxy"),
    regname.CLOUCOUR: SMG2RegionData("Major", [regname.WORLD3], [], 0x5C, "SandClockGalaxy"),
    regname.HAUNHALL: SMG2RegionData("Major", [regname.WORLD3], [], 0x68, "ReverseKingdomGalaxy"),
    regname.FREEFLAKE: SMG2RegionData("Major", [regname.WORLD3], [], 0x6C, "OceanRingGalaxy"),
    regname.SUPMASS: SMG2RegionData("Major", [regname.WORLD4], [], 0x74, "FactoryGalaxy"),
    regname.FLIPVILL: SMG2RegionData("Major", [regname.WORLD4], [], 0x80, "OceanPhantomCaveGalaxy"),
    regname.STARBEACH: SMG2RegionData("Major", [regname.WORLD4], [], 0x84, "CannonFleetGalaxy"),
    regname.CHOMWORK: SMG2RegionData("Major", [regname.WORLD4], [], 0x8C, "HellProminenceGalaxy"),
    regname.SPACSTOR: SMG2RegionData("Major", [regname.WORLD5], [], 0x8C, "HellProminenceGalaxy"),
    regname.SLIPSAND: SMG2RegionData("Major", [regname.WORLD5], [], 0x8C, "HellProminenceGalaxy"),
    regname.SHIVBURN: SMG2RegionData("Major", [regname.WORLD5], [], 0x8C, "HellProminenceGalaxy"),
    regname.BOOMOON: SMG2RegionData("Major", [regname.WORLD5], [], 0x8C, "HellProminenceGalaxy"),
    regname.MELTY: SMG2RegionData("Major", [regname.WORLD6], [], 0x8C, "HellProminenceGalaxy"),
    regname.CLOCKWORK: SMG2RegionData("Major", [regname.WORLD6], [], 0x8C, "HellProminenceGalaxy"),
    regname.WHOMPFORT: SMG2RegionData("Major", [regname.WORLD6], [], 0x8C, "HellProminenceGalaxy"),
    regname.BATTLEBELT: SMG2RegionData("Major", [regname.WORLD6], [], 0x8C, "HellProminenceGalaxy"),
    # Minor Galaxies
    regname.RIGHTDOWN: SMG2RegionData("Minor", [regname.WORLD1], [], 0xC, "SurfingLv1Galaxy"),
    regname.WILDGLIDE: SMG2RegionData("Minor", [regname.WORLD2], [], 0x20, "TamakoroExLv1Galaxy"),
    regname.ROLLMAST: SMG2RegionData("Minor", [regname.WORLD3], [], 0x38, "CubeBubbleExLv1Galaxy"),
    regname.HONEYHOP: SMG2RegionData("Minor", [regname.WORLD4], [], 0x40, "OceanFloaterLandGalaxy"),
    regname.UPDOWN: SMG2RegionData("Minor", [regname.WORLD5], [], 0x58, "HoneyBeeExGalaxy"),
    regname.SLIMSPRI: SMG2RegionData("Minor", [regname.WORLD6], [], 0x58, "HoneyBeeExGalaxy"),
    # World S Galaxies
    regname.MARIO: SMG2RegionData("Special", [regname.WORLD7], [], 0x58, "HoneyBeeExGalaxy"),
    regname.ROLLCOAST: SMG2RegionData("Special", [regname.WORLD7], [], 0x58, "HoneyBeeExGalaxy"),
    regname.TWISTTRI: SMG2RegionData("Special", [regname.WORLD7], [], 0x58, "HoneyBeeExGalaxy"),
    regname.STONECYC: SMG2RegionData("Special", [regname.WORLD7], [], 0x58, "HoneyBeeExGalaxy"),
    regname.BOSSBLITZ: SMG2RegionData("Special", [regname.WORLD7], [], 0x94, "KoopaBattleVs3Galaxy"),
    regname.GRANDMASTER: SMG2RegionData("Goal", [regname.WORLD7], [], 0x58, "HoneyBeeExGalaxy"),
    # Planetoids
    regname. : SMG2RegionData("Planet", [], []),
    regname.SKYOBS1STARTTOPSIDE:        SMG2RegionData("Planet", [], []),
    regname.SKYOBS2STARTTOPSIDE:        SMG2RegionData("Planet", [], []),
    regname.SKYOBS1STARTBOTTOM:         SMG2RegionData("Planet", [], []),
    regname.SKYOBS2STARTBOTTOM:         SMG2RegionData("Planet", [], []),
    regname.SKYOBS1TOPOFHOUSE:          SMG2RegionData("Planet", [], []),
    regname.SKYOBS2TOPOFHOUSE:          SMG2RegionData("Planet", [], []),
    regname.SKYOBS1GREENHILL:           SMG2RegionData("Planet", [], []),
    regname.SKYOBS1OCTOBONUS:           SMG2RegionData("Planet", [], []),
    regname.SKYOBS2OCTOBONUS:           SMG2RegionData("Planet", [], []),
    regname.SKYOBS1MINIPLANETS:         SMG2RegionData("Planet", [], []),
    regname.SKYOBS1CYLINDER:            SMG2RegionData("Planet", [], []),
    regname.SKYOBS1BEFOREBOSS:          SMG2RegionData("Planet", [], []),
    regname.SKYOBS1BOSS:                SMG2RegionData("Planet", [], []),
    regname.SKYOBS2SKYFLEET:            SMG2RegionData("Planet", [], []),
    regname.SKYOBS2FLIPSWITCH:          SMG2RegionData("Planet", [], []),
    regname.SKYOBS2GRASSFLEET:          SMG2RegionData("Planet", [], []),
    regname.SKYOBS1GSTAR1:              SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK1BIGTREE:          SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK1PIRANHABONUS:     SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK1LOG:              SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK1DICEPIPE:         SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK1WOODCIRClE:       SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK2BIGTREE:          SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK2PIRANHABONUS:     SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK2SLIDE:            SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK2SLIDEND:          SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK3PCOINSLIDE:       SMG2RegionData("Planet", [], []),
    regname.TALLTRUNK3PCOINEND:         SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR1LANDING:           SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR1CYMBAL:            SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR1TOWERS:            SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR1PARAGOOMBONUS:     SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR3PCOINS:            SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR1CASTLE:            SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR2LANDING:           SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR2CASTLE1:           SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR2CASTLE2:           SMG2RegionData("Planet", [], []),
    regname.CLOUCOUR2FINAL:             SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1PULL:              SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1SATELLITE:         SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1REDCANOUT:         SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1REDCANIN:          SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1TOPMAN:            SMG2RegionData("Planet", [], []),
    regname.SPACSTOR1PULLPATH:          SMG2RegionData("Planet", [], []),
    regname.SPACSTOR2PULL:              SMG2RegionData("Planet", [], []),
    regname.SPACSTOR2TOPTOWERBASE:      SMG2RegionData("Planet", [], []),
    regname.SPACSTOR2TOPTOWER:          SMG2RegionData("Planet", [], []),
    regname.SPACSTOR2COINROOM:          SMG2RegionData("Planet", [], []),
    regname.SPACSTOR2GSTAR3:            SMG2RegionData("Planet", [], []),
    regname.SLIPSAND1LONG:              SMG2RegionData("Planet", [], []),
    regname.SLIPSAND1COINROOM:          SMG2RegionData("Planet", [], []),
    regname.SLIPSAND1CUBE:              SMG2RegionData("Planet", [], []),
    regname.SLIPSAND1SLIDE:             SMG2RegionData("Planet", [], []),
    regname.SLIPSAND1BOSS:              SMG2RegionData("Planet", [], []),
    regname.SLIPSAND2LONG1:             SMG2RegionData("Planet", [], []),
    regname.SLIPSAND2GRAV:              SMG2RegionData("Planet", [], []),
    regname.SLIPSAND2LONG2:             SMG2RegionData("Planet", [], []),
    regname.SLIPSAND2LONG3:             SMG2RegionData("Planet", [], []),
    regname.SLIPSAND2BIRD:              SMG2RegionData("Planet", [], []),
    regname.SLIPSAND3BOSS:              SMG2RegionData("Planet", [], []),
    regname.SHIVBURN1VOLCANO:           SMG2RegionData("Planet", [], []),
    regname.SHIVBURN3CHIMP:             SMG2RegionData("Planet", [], []),
    regname.SHIVBURN1LAVA:              SMG2RegionData("Planet", [], []),
    regname.SHIVBURN1FIREICE:           SMG2RegionData("Planet", [], []),
    regname.SHIVBURN1TOAD:              SMG2RegionData("Planet", [], []),
    regname.SHIVBURN1BOSS:              SMG2RegionData("Planet", [], []),
    regname.SHIVBURN2TOAD:              SMG2RegionData("Planet", [], []),
    regname.SHIVBURN2ROMP:              SMG2RegionData("Planet", [], []),
}

major_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Major"]

minor_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Minor"]

boss_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Boss"]

luma_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Luma"]

specials_galaxy_list: list[str] = [key for key, data in region_list.items() if data.type == "Special"]

def by_type_shuffle(world: "SMG2World", entrances: list, galaxies: list[str]):
    for entrance in entrances:
        slot = world.get_entrance(entrance)
        galaxy = world.get_region(world.random.choice(sorted(galaxies)))
        galaxies.remove(galaxy.name)
        er_target: Entrance = {e.name: e for e in galaxy.entrances}[galaxy.name]
        galaxy.entrances.remove(er_target)
        slot.connect(galaxy)

def create_regions(world: "SMG2World"): #TODO Correctly add locations
    for region_name in region_list.keys():
        world.multiworld.regions.append(SMGRegion(region_name, region_list[region_name], world.player, world.multiworld))

    create_locations(base_stars_locations, world)

    # match case Goal to place item on correct location. Case 4 is placed ealier
    match world.options.goal.value:
        case 0 | 1:
            world.multiworld.get_location(locname.GALAXYGENSTAR1, world.player).place_locked_item(
                world.create_item("Peach"))
        case 2:
            world.multiworld.get_location(locname.GRANDMASTSTAR1, world.player).place_locked_item(
                world.create_item("Peach"))
        case 3:
            world.multiworld.get_location(locname.GRANDMASTSTAR2, world.player).place_locked_item(
                world.create_item("Peach"))
        case 4:
            world.get_region(regname.SHIP).add_event("Boss Rush Goal", "Peach",
                                                     (CanReachLocation(locname.FIREFLOTSTAR1)
                                                      & CanReachLocation(locname.LAVALAIRSTAR1)
                                                      & CanReachLocation(locname.FEARFLETSTAR1)
                                                      & CanReachLocation(locname.BOOMBUNKSTAR1)
                                                      & CanReachLocation(locname.GRAVGAUNSTAR1)
                                                      & CanReachLocation(locname.GALAXYGENSTAR1)))

    if world.options.enable_green_stars.value > 0: # Fix for Green star locations
        create_locations(green_star_locations, world, True)


def create_region(name: str, world: "SMG2World") -> Region:
    return Region(name, world.player, world.multiworld, name)

def create_locations(locs: dict[str, SMG2LocationData], world: "SMG2World", skip_rules: bool=False):
    for name, data in locs.items():
        reg = world.get_region(data.region)
        location = SMG2Location(world.player, name, reg)
        if data.default_access and skip_rules == False:
            world.set_rule(location, data.default_access)

        reg.locations += [location]

def disconnect_from_option(world: "SMG2World"):
    if "Bosses" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 7 Galaxy"), 0, regname.BOWJR1)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 7 Galaxy"), 0, regname.BOWSER1)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 7 Galaxy"), 0, regname.BOWJR2)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 7 Galaxy"), 0, regname.BOWSER2)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 7 Galaxy"), 0, regname.BOWJR3)
        if world.options.goal.value > 1:
            disconnect_entrance_for_randomization(world.get_entrance(ggen_entr[0]), 0, regname.BOWSER3)
        if world.options.galaxy_shuffle_type.value == 0:
            bg_list: list[str] = copy.deepcopy(boss_galaxy_list)
            bg_entr_list: list[str] = copy.deepcopy(boss_entr_list)
            if world.options.goal.value > 1:
                bg_list += [regname.BOWSER3]
                bg_entr_list += ggen_entr
            by_type_shuffle(world, bg_entr_list, bg_list)
    if "World Majors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 1 Galaxy"), 0, regname.SKYOBS)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 1 Galaxy"), 0, regname.PUZZPLAN)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 1 Galaxy"), 0, regname.TALLTRUNK)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 1 Galaxy"), 0, regname.SUPMASS)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 1 Galaxy"), 0, regname.SPACSTOR)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 1 Galaxy"), 0, regname.MELTY)
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 2 Galaxy"), 0, regname.GOODEGG)
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 3 Galaxy"), 0, regname.SPINDIG)
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 5 Galaxy"), 0, regname.FLUFFBLUFF)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 2 Galaxy"), 0, regname.BOULBOWL)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 3 Galaxy"), 0, regname.HIGHTAIL)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 5 Galaxy"), 0, regname.COSMICO)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 2 Galaxy"), 0, regname.CLOUCOUR)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 3 Galaxy"), 0, regname.HAUNHALL)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 4 Galaxy"), 0, regname.FREEFLAKE)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 3 Galaxy"), 0, regname.FLIPVILL)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 5 Galaxy"), 0, regname.STARBEACH)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 6 Galaxy"), 0, regname.CHOMWORK)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 2 Galaxy"), 0, regname.BOOMOON)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 4 Galaxy"), 0, regname.SLIPSAND)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 6 Galaxy"), 0, regname.SHIVBURN)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 2 Galaxy"), 0, regname.CLOCKWORK)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 4 Galaxy"), 0, regname.WHOMPFORT)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 6 Galaxy"), 0, regname.BATTLEBELT)

        major_list_copy = copy.deepcopy(major_galaxy_list)
        major_entr_list_copy = copy.deepcopy(major_entr_list)
        if world.options.galaxy_shuffle_type.value != 2:
            by_type_shuffle(world, major_entr_list_copy, major_list_copy)

    if "World Minors" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 6 Galaxy"), 0, regname.RIGHTDOWN)
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 4 Galaxy"), 0, regname.WILDGLIDE)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 6 Galaxy"), 0, regname.ROLLMAST)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 3 Galaxy"), 0, regname.UPDOWN)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 5 Galaxy"), 0, regname.SLIMSPRI)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 4 Galaxy"), 0, regname.HONEYHOP)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, copy.deepcopy(gal_minor_entr_list), copy.deepcopy(minor_galaxy_list))
    if "Hungry Lumas" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("World 2 Slot 6 Galaxy"), 0, regname.HONEYBLOOM)
        disconnect_entrance_for_randomization(world.get_entrance("World 3 Slot 5 Galaxy"), 0, regname.BEATBLOCK)
        disconnect_entrance_for_randomization(world.get_entrance("World 4 Slot 2 Galaxy"), 0, regname.SWEETMYS)
        disconnect_entrance_for_randomization(world.get_entrance("World 5 Slot 5 Galaxy"), 0, regname.FLEETGLIDE)
        disconnect_entrance_for_randomization(world.get_entrance("World 6 Slot 3 Galaxy"), 0, regname.FLASHBLACK)
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 6 Galaxy"), 0, regname.FLIPOUT)
        disconnect_entrance_for_randomization(world.get_entrance("World 1 Slot 3 Galaxy"), 0, regname.FLIPSWAP)
        if world.options.galaxy_shuffle_type.value == 0:
            by_type_shuffle(world, copy.deepcopy(luma_entr_list), copy.deepcopy(specials_galaxy_list))
    if "World S Specials" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value:
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 1 Galaxy"), 0, regname.MARIO)
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 2 Galaxy"), 0, regname.ROLLCOAST)
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 3 Galaxy"), 0, regname.TWISTTRI)
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 4 Galaxy"), 0, regname.STONECYC)
        disconnect_entrance_for_randomization(world.get_entrance("World 7 Slot 5 Galaxy"), 0, regname.BOSSBLITZ)
        if ((world.options.goal.value < 2 or world.options.goal.value == 4)
                and ("Grandmaster" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value)):
            disconnect_entrance_for_randomization(world.get_entrance(grand_entr[0]), 0, regname.GRANDMASTER)
        if world.options.galaxy_shuffle_type.value == 0:
            spec_list: list[str] = copy.deepcopy(specials_galaxy_list)
            spec_entr_list: list[str] = copy.deepcopy(special_entr_list)
            if ((world.options.goal.value < 2 or world.options.goal.value == 4)
                    and ("Grandmaster" in world.options.galaxy_shuffle.value or "Full" in world.options.galaxy_shuffle.value)):
                spec_list += [regname.GRANDMASTER]
                spec_entr_list += grand_entr
            by_type_shuffle(world, spec_entr_list, spec_list)



    return