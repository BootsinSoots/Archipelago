from typing import TYPE_CHECKING

from BaseClasses import Entrance
from .regions import connect_regions, region_list, all_galaxy_slots
from.Constants.Names import region_names as regname
from ..generic.Rules import add_rule

if TYPE_CHECKING:
    from . import SMG2World

# Cap the incoming offsets to the maximum of that area.

# main stage logic
def set_rules(world: "SMG2World", player: int):
    # Dome 1
    connect_regions(world, player, regname.SHIP, regname.WORLD1, "Dome 1 Entry")
    connect_regions(world, player, regname.WORLD1, regname.GOODEGG, "Dome 1 First Orbit Galaxy")
    connect_regions(world, player, regname.WORLD1, regname.HONEYHIVE, "Dome 1 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Second Orbit"], 4)))
    connect_regions(world, player, regname.WORLD1, regname.LOOPDEELOOP, "Dome 1 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Third Orbit"], 5)))
    connect_regions(world, player, regname.WORLD1, regname.FLIPSWITCH, "Dome 1 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,
                                                  min(world.options.dome_one_counts["Fourth Orbit"], 6)))
    connect_regions(world, player, regname.WORLD1, regname.BOWJR1, "Dome 1 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player,7))
    # Dome 2
    connect_regions(world, player, regname.SHIP, regname.WORLD2, "Dome 2 Entry",
                    lambda state: state.has("Grand Star", player))
    connect_regions(world, player, regname.WORLD2, regname.SPACEJUNK, "Dome 2 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 8))
    connect_regions(world, player, regname.WORLD2, regname.ROLLINGGREEN, "Dome 2 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 9))
    connect_regions(world, player, regname.WORLD2, regname.BATTLEROCK, "Dome 2 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 10))
    connect_regions(world, player, regname.WORLD2, regname.HURRYSCUR, "Dome 2 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 11))
    connect_regions(world, player, regname.WORLD2, regname.BOWSER1, "Dome 2 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 12))
    # Dome 3
    connect_regions(world, player, regname.SHIP, regname.WORLD3, "Dome 3 Entry",
                    lambda state: state.has("Grand Star", player, 2))
    connect_regions(world, player, regname.WORLD3, regname.BEACHBOWL, "Dome 3 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 13))
    connect_regions(world, player, regname.WORLD3, regname.BUBBLEBREEZE, "Dome 3 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 14))
    connect_regions(world, player, regname.WORLD3, regname.GHOSTLY, "Dome 3 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 15))
    connect_regions(world, player, regname.WORLD3, regname.BUOY, "Dome 3 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 16))
    connect_regions(world, player, regname.WORLD3, regname.BOWJR2, "Dome 3 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 17))
    # Dome 4
    connect_regions(world, player, regname.SHIP, regname.WORLD4, "Dome 4 Entry",
                    lambda state: state.has("Grand Star", player, 3))
    connect_regions(world, player, regname.WORLD4, regname.GUSTY, "Dome 4 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 18))
    connect_regions(world, player, regname.WORLD4, regname.FREEZEFLAME, "Dome 4 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 19))
    connect_regions(world, player, regname.WORLD4, regname.DUSTY, "Dome 4 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 20))
    connect_regions(world, player, regname.WORLD4, regname.HONEYCLIMB, "Dome 4 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 21))
    connect_regions(world, player, regname.WORLD4, regname.BOWSER2, "Dome 4 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 22))
    # Dome 5
    connect_regions(world, player, regname.SHIP, regname.WORLD5, "Dome 5 Entry",
                    lambda state: state.has("Grand Star", player, 4))
    connect_regions(world, player, regname.WORLD5, regname.GOLDLEAF, "Dome 5 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 23))
    connect_regions(world, player, regname.WORLD5, regname.SEASLIDE, "Dome 5 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 24))
    connect_regions(world, player, regname.WORLD5, regname.TOYTIME, "Dome 5 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 25))
    connect_regions(world, player, regname.WORLD5, regname.BONEFIN, "Dome 5 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 26))
    connect_regions(world, player, regname.WORLD5, regname.BOWJR3, "Dome 5 Fifth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 27))
    # Dome 6
    connect_regions(world, player, regname.SHIP, regname.WORLD6, "Dome 6 Entry",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.WORLD6, regname.DEEPDARK, "Dome 6 First Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 28))
    connect_regions(world, player, regname.WORLD6, regname.DREADNOUGHT, "Dome 6 Second Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 29))
    connect_regions(world, player, regname.WORLD6, regname.MATTER, "Dome 6 Third Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 30))
    connect_regions(world, player, regname.WORLD6, regname.MELTY, "Dome 6 Fourth Orbit Galaxy",
                    lambda state: state.has_group("Power Star", player, 31))
    #Remaining Ship Connections
    connect_regions(world, player, regname.SHIP, regname.LIBRARY, "Library Entrance")
    connect_regions(world, player, regname.SHIP, regname.COTU, "Center Of the Universe Entry",
                    lambda state: state.has("Grand Star", player, 5) and state.has_group("Power Star", player, world.options.stars_to_finish.value))
    connect_regions(world, player, regname.COTU, regname.BOWSER3, "Galaxy's Center")
    connect_regions(world, player, regname.SHIP, regname.SWEETSWEET, "Sweet Sweet Hungry Luma")
    connect_regions(world, player, regname.SHIP, regname.SLINGPOD, "Sling Pod Hungry Luma",
                    lambda state: state.has("Grand Star", player))
    connect_regions(world, player, regname.SHIP, regname.DRIPDROP, "Drip Drop Hungry Luma",
                    lambda state: state.has("Grand Star", player, 2))
    connect_regions(world, player, regname.SHIP, regname.BIGMOUTH, "Bigmouth Hungry Luma",
                    lambda state: state.has("Grand Star", player, 3))
    connect_regions(world, player, regname.SHIP, regname.SANDSPIRAL, "Sand Spiral Hungry Luma",
                    lambda state: state.has("Grand Star", player, 4))
    connect_regions(world, player, regname.SHIP, regname.SNOWCAP, "Snow Cap Hungry Luma",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.GATEWAY, "Gateway Dome",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.BOOBONE, "Boo's Boneyard Hungry Luma",
                    lambda state: state.has("Grand Star", player, 5))
    connect_regions(world, player, regname.SHIP, regname.TRIALS, "Planet of Trials Launch Star",
                    lambda state: state.has("Green Star", player))
    connect_regions(world, player, regname.TRIALS, regname.ROLLINGGIZ, "Rolling Gizmo Launch Star")
    connect_regions(world, player, regname.TRIALS, regname.LOOPDEESWOOP, "Loopdeeswoop Launch Star")
    connect_regions(world, player, regname.TRIALS, regname.BUBBLEBLAST, "Bubble Blast Launch Star")
    # connect_regions(world, player, regname.SHIP, regname.FINALE, "Grand Finale Launch Star",
    #                 lambda state: state.has("Green Star", player) and state.has("Power Star", player, 120))
    world.multiworld.completion_condition[player] = lambda state: state.has("Peach", player)

def rules_from_er_placements(world: "SMG2World"):
    available_locations = 4
    dome_orbits: list[str] = ["First Orbit", "Second Orbit", "Third Orbit", "Fourth Orbit", "Fifth Orbit"]
    for dome_num in [1, 2, 3, 4, 5, 6]:
        dome_galaxy_dict: dict = dict(sorted(dict([(d_key, d_val) for d_key, d_val in world.galaxy_counts.items()
                                                   if f"D{dome_num}" in d_key]).items(), key=lambda item: item[1]))
        for galaxy, star_count in dome_galaxy_dict.items():
            gal_num: int = int(galaxy[3:])
            orbit_name:str = dome_orbits[(gal_num-1)]

            galaxy_entr: Entrance = world.get_entrance(f"Dome {dome_num} {orbit_name} Galaxy")
            galaxy_type: str = region_list[galaxy_entr.connected_region.name].type

            if star_count <= available_locations:
                add_rule(galaxy_entr, lambda state, count=star_count: state.has("Power Star", world.player, count))
            else:
                add_rule(galaxy_entr, lambda state, count=available_locations: state.has("Power Star", world.player, count))
                world.galaxy_counts[galaxy] = available_locations

            available_locations += 4 if galaxy_type == "Major" else 1

    for galaxy_slot in all_galaxy_slots:
        world.shuffled_levels[world.get_entrance(galaxy_slot).name] = world.get_entrance(galaxy_slot).connected_region.name


    # # special stages logic Left here for reference later on default values
    # add_rule(world.get_location("LDL: Surfing 101"), lambda state: state.has("Power Star", player, 5))
    # add_rule(world.get_location("FS: Painting the Planet Yellow"), lambda state: state.has("Power Star", player, 7))
    # add_rule(world.get_location("RG: Rolling in the Clouds"), lambda state: state.has("Power Star", player, 11) and state.has("Progressive Grand Star"))
    # add_rule(world.get_location("HS: Shrinking Satellite"), lambda state: state.has ("Power Star", player, 18) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BUB: Through the Poison Swamp"), lambda state: state.has ("Power Star", player, 19) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BB: The Secret of Buoy Base"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BB: The Floating Fortress"), lambda state: state.has ("Power Star", player, 30) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BF: Kingfin's Fearsome Waters"), lambda state: state.has("Power Star", player, 55) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("MS: Watch Your Step"), lambda state: state.has("Power Star", player, 50) and state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("DDR: Giant Eel Breakout"), lambda state: state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("RGT: Gizmos, Gears, and Gadgets"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("LDT: The Galaxy's Greatest Wave"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("BBT: The Electric Labyrinth"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player) and state.has("Progressive Grand Star", player, 2) and state.has("Green Star", player, 3))
    # add_rule(world.get_location("SS: Rocky Road"), lambda state: state.has("Power Star", player, 7))
    # add_rule(world.get_location("SP: A Very Sticky Situation"), lambda state: state.has("Progressive Grand Star", player) and state.has("Power Star", player, 9))
    # add_rule(world.get_location("BM: Bigmouth's Gold Bait"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 29))
    # add_rule(world.get_location("Sandy Spiral: Choosing a Favorite Snack"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 36) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("Bone's Boneyard: Racing the Spooky Speedster"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("SC: Star Bunnies in the Snow"), lambda state: state.has("Progressive Grand Star", player, 2) and state.has("Power Star", player, 52))
    # # comet logic
    # add_rule(world.get_location("GE: Dino Piranha Speed Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("HH: Honeyhive Cosmic Mario Race"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("SJ: Pull Star Path Speed Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("BR: Topmanic's Dardevil Run"), lambda state: state.has("Power Star", player, 13))
    # add_rule(world.get_location("BB: Fast Foes on the Cyclone Stone"), lambda state: state.has("Power Star", player, 13))
    # # boss stage logic
    # add_rule(world.get_location("BJ: Megaleg's Moon"), lambda state: state.has("Power Star", player, 8))
    # add_rule(world.get_location("B: The Firery Stronghold"), lambda state: state.has("Power Star", player, 15) and state.has("Progressive Grand Star", player))
    # add_rule(world.get_location("BJ: Sinking the Airships"), lambda state: state.has("Power Star", player, 23) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("BJ: King Kaliente's Spicy Return"), lambda state: state.has("Power Star", player, 45) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B:  Darkness on the Horizon"), lambda state: state.has("Power Star", player, 33) and state.has("Progressive Grand Star", player, 2))
    # add_rule(world.get_location("B: Bowser's Galaxy Reactor"), lambda state: state.has("Power Star", player, world.options.stars_to_finish.value) and state.has("Progressive Grand Star", player, 2))
    #
    #
    # # purple coin star logic
    # if world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_all:
    #     add_rule(world.get_location("DN: Battlestation's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("MM: Red-Hot Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("TT: Luigi's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DD: Plunder the Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GL: Purple Coins in the Woods"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("FF: Purple Coins on the Summit"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SS: Purple Coins by the Seaside"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Purple Coins on the Puzzle Cube"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("G: Purple Coins in the Bone Pen"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("DDune: Purple Coin in the Desert"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("BR: Purple Coins on the Battlerock"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GE: Purple Coin Omelet"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("HH: The Honeyhive's Purple Coins"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("SJ: Purple Coin Spacewalk"), lambda state: state.has("Peach", player))
    #     add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Peach", player))
    # elif world.options.enable_purple_coin_stars == world.options.enable_purple_coin_stars.option_main_game_only:
    #       add_rule(world.get_location("GG: Gateway's Purple coins"), lambda state: state.has("Grand Star Engine", player))
    # else:
    #     return


