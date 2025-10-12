from typing import Optional, Callable, TYPE_CHECKING

from . import Rules

if TYPE_CHECKING:
    from . import Rules, LMWorld

vanilla_door_state = {
        34: 0,
        38: 0,
        43: 1,
        41: 1,
        33: 0,
        32: 1,
        31: 0,
        27: 0,
        28: 0,
        3: 0,
        1: 1,
        4: 0,
        5: 1,
        7: 0,
        11: 1,
        14: 0,
        15: 0,
        10: 1,
        17: 0,
        18: 1,
        20: 0,
        16: 0,
        74: 0,
        75: 1,
        23: 1,
        21: 0,
        25: 0,
        24: 1,
        42: 0,
        29: 0,
        30: 1,
        44: 1,
        40: 1,
        45: 1,
        48: 1,
        49: 1,
        47: 1,
        51: 0,
        63: 0,
        52: 1,
        59: 0,
        62: 1,
        55: 1,
        53: 0,
        56: 0,
        50: 1,
        65: 0,
        9: 1,
        71: 0,
        68: 0,
        67: 1,
        69: 0,
        70: 1,
        72: 0
    }

GHOST_TO_ROOM = {
    "Wardrobe": "No Element",
    "Laundry Room": "No Element",
    "Hidden Room": "Ice",  # "Ice",
    "Storage Room": "No Element",
    "Kitchen": "Ice",  # "Ice",
    "1F Bathroom": "No Element",
    "Courtyard": "No Element",
    "Ballroom": "No Element",
    "Tea Room": "No Element",
    "2F Washroom": "Fire",  # "Fire",
    "Projection Room": "No Element",
    "Safari Room": "Water",  # "Water",
    "Cellar": "No Element",
    "Roof": "Ice",
    "Sealed Room": "No Element",
    "Telephone Room": "No Element",
    "Armory": "No Element",
    "Pipe Room": "No Element",
    "Artist's Studio": "No Element",
    "Mirror Room": "No Element",
    "Graveyard": "No Element",
    "Anteroom": "No Element",
    # "Sitting Room": "Fire"  # Fire
}

spawn_locations = {
    "Hidden Room":           {"room_no": 1, "pos_x": -1998.314700, "pos_y": 0.000000, "pos_z": 225.000000,
                              "key": ["Butler's Room Key", "Laundry Room Key", "Heart Key"], "door_keys": [],
                              "door_ids": [], "in_game_room_id": 1}, # Hidden
    "Courtyard":             {"room_no": 23, "pos_x": 1613.042970, "pos_y": 9.000000, "pos_z": -5663.574710,
                              "key": ["Club Key", "North Rec Room Key", "Heart Key"], "door_keys":
                              ["Club Key", "North Rec Room Key"], "door_ids": [42, 25], "in_game_room_id": 24}, # Courtyard
    "Clockwork Room":        {"room_no": 56, "pos_x": 10.759588, "pos_y": 1100.000000, "pos_z": -1649.743900,
                              "key": ["Clockwork Key", "Telephone Room Key"],
                              "door_keys": ["Clockwork Key"], "door_ids": [53],
                              "in_game_room_id": 59}, # Clockwork
    "Foyer":                 {"room_no": 2, "pos_x": -7.640748, "pos_y": 0.000000, "pos_z": 145.174300,
                              "key": ["Heart Key", "Family Hallway Key", "Parlor Key"],
                              "door_keys": ["Heart Key", "Family Hallway Key", "Parlor Key"],
                              "door_ids": [3, 34, 33], "in_game_room_id": 2}, # Foyer
    "Rec Room":              {"room_no": 22, "pos_x": 3517.026860, "pos_y": 0.000000, "pos_z": -4646.33203,
                              "key": ["North Rec Room Key", "South Rec Room Key", "Lower 2F Stairwell Key", "Upper 2F Stairwell Key"],
                              "door_keys": ["North Rec Room Key", "South Rec Room Key"],
                              "door_ids": [24, 25], "in_game_room_id": 23}, # Rec Room
    # "Laundry Room":          {"room_no": 5, "pos_x": -3165.112550, "pos_y": 0, "pos_z": -804.770508,
    #                           "key": ["Laundry Key", "Butler's Rom Key", "Heart Key"], "door_keys": ["Laundry Key", "Butler's Rom Key"],
    #                           "door_ids": [1, 7]},  # Laundry removed due to new spawn toad triggering as you leave
    "Telephone Room":        {"room_no": 50, "pos_x": -9.812825, "pos_y": 1100, "pos_z": 118.738243,
                              "key": ["Telephone Room Key", "Clockwork Key"], "door_keys": ["Telephone Room Key", "Clockwork Key"],
                              "door_ids": [53, 52], "in_game_room_id": 53}, # Telephone
    "Butler's Room":         {"room_no": 0, "pos_x": -3800.646, "pos_y": 0, "pos_z": -327.291077,
                              "key": ["Butler's Room Key", "Laundry Room Key", "Heart Key"], "door_keys": [],
                              "door_ids": [1], "in_game_room_id": 0}, # Butler
    "Conservatory":          {"room_no": 21, "pos_x": 780.405884, "pos_y": 0, "pos_z": -4662.089840,
                              "key": ["Conservatory Key", "Lower 2F Stairwell Key","Heart Key"], "door_keys": ["Conservatory Key"],
                              "door_ids": [21], "in_game_room_id": 22}, # Conservatory
    "Billiards Room":        {"room_no": 12, "pos_x": -963.755737, "pos_y": 0, "pos_z": -3055.808110,
                              "key": ["Billiards Room Key", "Heart Key"], "door_keys": ["Billiards Room Key", "Projection Room Key"],
                              "door_ids": [17, 18], "in_game_room_id": 12}, # Billiards
    "Twins' Room":           {"room_no": 25, "pos_x": -1729.586790, "pos_y": 550, "pos_z": 116.055779,
                              "key": ["Twins Bedroom Key", "Family Hallway Key"], "door_keys": ["Twins Bedroom Key"],
                              "door_ids": [28], "in_game_room_id": 27}, # Twins
    "Nursery":               {"room_no": 24, "pos_x": -3331.658690, "pos_y": 550, "pos_z": -198.970337,
                              "key": ["Nursery Key", "Family Hallway Key"], "door_keys": ["Nursery Key"],
                              "door_ids": [27], "in_game_room_id": 26}, # Nursery
    "Master Bedroom":        {"room_no": 33, "pos_x": -3365.857670, "pos_y": 550, "pos_z": -1513.529660,
                              "key": ["Master Bedroom Key", "Family Hallway Key"], "door_keys": ["Master Bedroom Key"],
                              "door_ids": [31], "in_game_room_id": 34}, # Master bed
    #"Study":                 {"room_no": 34, "pos_x": -1696.352290, "pos_y": 550, "pos_z": -1605.182980,
    #                          "key": ["Study Key", "Family Hallway Key"], "door_keys": ["Study Key"]
    #                          "door_ids": [32]}, # Study Errors and neville's Chair doesn't spawn?
    "Parlor":                {"room_no": 35, "pos_x": -43.294357, "pos_y": 550, "pos_z": -1775.288450,
                             "key": ["Parlor Key", "Heart Key", "Anteroom Key"], "door_keys": ["Parlor Key", "Anteroom Key"],
                              "door_ids": [34, 38], "in_game_room_id": 36}, # Parlor
    "Nana's Room":           {"room_no": 46, "pos_x": -457.708374, "pos_y": 550, "pos_z": -4535.000000,
                              "key": ["Nana's Room Key", "Upper 2F Stairwell Key"], "door_keys": ["Nana's Room Key"],
                              "door_ids": [49], "in_game_room_id": 49}, # Nana
    "2F Bathroom":           {"room_no": 45, "pos_x": -1902.854130, "pos_y": 550, "pos_z": -4660.501950,
                              "key": ["2F Bathroom Key", "Upper 2F Stairwell Key"], "door_keys": ["2F Bathroom Key"],
                              "door_ids": [48], "in_game_room_id": 48}, # 2f bath
    "Astral Hall":           {"room_no": 40, "pos_x": 2023.579290, "pos_y": 550, "pos_z": -2915.000000,
                              "key": ["Astral Hall Key", "Upper 2F Stairwell Key"],
                              "door_keys": ["Astral Hall Key", "Observatory Key"], "door_ids": [44, 40], "in_game_room_id": 43}, # astral
    "Sitting Room":          {"room_no": 27, "pos_x": 2225.465090, "pos_y": 550, "pos_z": -98.163559,
                              "key": ["Sitting Room Key", "Guest Room Key"],
                              "door_keys": ["Sitting Room Key", "Guest Room Key"], "door_ids": [29, 30], "in_game_room_id": 28}, # sitting
    "Guest Room":            {"room_no": 28, "pos_x": 3637.69727, "pos_y": 550, "pos_z": 201.316391,
                              "key": ["Guest Room Key", "Sitting Room Key"], "door_keys": ["Guest Room Key"],
                              "door_ids": [30], "in_game_room_id": 29}, # guest
    "Safari Room":           {"room_no": 52, "pos_x": 3317.313480, "pos_y": 1100, "pos_z": 225,
                              "key": ["Safari Room Key", "East Attic Hallway Key", "Balcony Key"],
                              "door_keys": ["Safari Room Key", "East Attic Hallway Key"], "door_ids": [55, 56], "in_game_room_id": 55}, # safari
    "Ceramics Studio":       {"room_no": 55, "pos_x": -2397.3373540, "pos_y": 1100, "pos_z": -1579.717410,
                              "key": ["Armory Key", "Diamond Key", "Telephone Room Key"], "door_keys": ["Armory Key"],
                              "door_ids": [50], "in_game_room_id": 58}, # ceramics
    "Anteroom":              {"room_no": 39, "pos_x": -1.503195, "pos_y": 550, "pos_z": -3087.626950,
                              "key": ["Wardrobe Key", "Anteroom Key", "Parlor Key"],
                              "door_keys": ["Wardrobe Key", "Anteroom Key"], "door_ids": [43, 38], "in_game_room_id": 42}, # Anteroom
    "Wardrobe":              {"room_no": 38, "pos_x": -1789.859250, "pos_y": 550, "pos_z": -3303.123780,
                              "key": ["Wardrobe Key","Anteroom Key", "Parlor Key", "Heart Key"],
                              "door_keys": ["Wardrobe Key", "Wardrobe Balcony Key"], "door_ids": [43, 41], "in_game_room_id": 40}, # Wardrobe
    "Projection Room":       {"room_no": 13, "pos_x": 281.914215, "pos_y": 0, "pos_z": -3137.967530,
                              "key": ["Projection Room Key", "Billiards Room Key"], "door_keys": ["Projection Room Key"],
                              "door_ids": [18], "in_game_room_id": 13}, # Projection
    "Fortune-Teller's Room": {"room_no": 3, "pos_x": 1807.135740, "pos_y": 0, "pos_z": 214.838852,
                              "key": ["Fortune Teller Key", "Mirror Room Key"],
                              "door_keys": ["Fortune Teller Key", "Mirror Room Key"], "door_ids": [4, 5], "in_game_room_id": 3}, # Fortune Teller
    "1F Bathroom":           {"room_no": 17, "pos_x": -2160.237550, "pos_y": 0, "pos_z": -4671.114750,
                              "key": ["1F Bathroom Key", "Heart Key"], "door_keys": ["1F Bathroom Key"],
                              "door_ids": [23], "in_game_room_id": 21}, # 1f bath
    "Mirror Room":           {"room_no": 4, "pos_x": 3821.63525, "pos_y": 0, "pos_z": 215.000000,
                              "key": ["Mirror Room Key", "Fortune Teller Key"], "door_keys": ["Mirror Room Key"],
                              "door_ids": [5], "in_game_room_id": 4}, # Mirror
    "Ballroom":              {"room_no": 10, "pos_x": 2854.236820, "pos_y": 0, "pos_z": -1565.909060,
                              "key": ["Ballroom Key", "Storage Room Key"], "door_keys": ["Ballroom Key", "Storage Room Key"],
                              "door_ids": [15, 16], "in_game_room_id": 9}, # BaLLROOM
    "Storage Room":          {"room_no": 14, "pos_x": 3412.177250, "pos_y": 0, "pos_z": -3009.698000,
                              "key": ["Storage Room Key", "Ballroom Key"], "door_keys": ["Storage Room Key"],
                              "door_ids": [16], "in_game_room_id": 14}, # Storage
    "Breaker Room":          {"room_no": 67, "pos_x": 3127.567140, "pos_y": -550, "pos_z": -1437.766600,
                              "key": ["Breaker Room Key", "Basement Stairwell Key"], "door_keys": ["Breaker Room Key"],
                              "door_ids": [71], "in_game_room_id": 69}, # Breaker
    "Dining Room":           {"room_no": 9, "pos_x": -393.851349, "pos_y": 0, "pos_z": -1416.557500,
                              "key": ["Dining Room Key", "Kitchen Key"], "door_keys": ["Dining Room Key", "Kitchen Key"],
                              "door_ids": [11, 14], "in_game_room_id": 8}, # Dining
    "Armory":                {"room_no": 48, "pos_x": -2541.662600, "pos_y": 1100.000000, "pos_z": -40.361595,
                              "key": ["Armory Key", "Balcony Key", "Telephone Room Key"],
                              "door_keys": ["Armory Key", "Ceramics Studio Key"], "door_ids": [50, 51], "in_game_room_id": 51}, # Armory
    "Pipe Room":             {"room_no": 66, "pos_x": 1235, "pos_y": -480.000000, "pos_z": -1433.000000,
                             "key": ["Pipe Room Key", "Cellar Key"],
                             "door_keys": ["Pipe Room Key"],
                             "door_ids": [69], "in_game_room_id": 68},  # Foyer
    "Cold Storage":          {"room_no": 61, "pos_x": 1405, "pos_y": -550.000000, "pos_z": -25.000000,
                             "key": ["Cold Storage Key", "Cellar Key"],
                             "door_keys": ["Cold Storage Key"],
                             "door_ids": [65], "in_game_room_id": 64},  # Foyer
    # "Secret Altar":          {"room_no": 70, "pos_x": 2293, "pos_y": -550.000000, "pos_z": -5805.000000,
    #                          "key": ["Spade Key", "Altar Hallway Key"],
    #                          "door_keys": ["Spade Key"],
    #                          "door_ids": [72], "in_game_room_id": 73},  # Foyer
}

exp_spawns: dict[str,dict[str, int]] = {
}


def set_ghost_type(world: "LMWorld", ghost_list: dict):
    for region_name in ghost_list:
        types = ["Fire", "Water", "Ice", "No Element"]
        weights = [2, 2, 2, 8]
        ghost_type = world.random.choices(types, weights, k=1)[0]
        ghost_list.update({region_name: ghost_type})


def lmconnect(world: "LMWorld", source: str, target: str, key: Optional[str] = None,
            doorid: Optional[int] = None, rule: Optional[Callable] = None, one_way: bool = False, required_element: Optional[str] = ""):
    player = world.player

    if world.open_doors.get(doorid) == 0:
        extra_rule = lambda state: state.has(key, player)
        if rule is not None:
            rule = lambda state, orig_rule=rule: orig_rule(state) and extra_rule(state)
        else:
            rule = extra_rule

    source_region = world.get_region(source)
    target_region = world.get_region(target)
    source_region.connect(target_region, rule=rule)
    if not one_way:
        target_region.connect(source_region, rule=rule)

    if required_element == "Fire":
        for fregion in Rules.FIRE_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(fregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(fregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))
    elif required_element == "Ice":
        for iregion in Rules.ICE_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(iregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(iregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))
    elif required_element == "Water":
        for wregion in Rules.WATER_SPIRIT_SPOT:
            world.multiworld.register_indirect_condition(world.get_region(wregion),
                                                         world.multiworld.get_entrance(f"{source_region.name} -> {target_region.name}", world.player))
            if not one_way:
                world.multiworld.register_indirect_condition(world.get_region(wregion),
                                                             world.multiworld.get_entrance(
                                                                 f"{target_region.name} -> {source_region.name}", world.player))


def connect_regions(world: "LMWorld"):
    lmconnect(world, "Foyer", "Parlor", "Parlor Key", 34)
    lmconnect(world, "Parlor", "Anteroom", "Anteroom Key", 38)
    lmconnect(world, "Anteroom", "Wardrobe", "Wardrobe Key", 43)
    lmconnect(world, "Wardrobe", "Wardrobe Balcony", "Wardrobe Balcony Key", 41)
    lmconnect(world, "Foyer", "Family Hallway", "Family Hallway Key", 33)
    lmconnect(world, "Foyer", "1F Hallway", "Heart Key", 3)
    lmconnect(world, "Family Hallway", "Study", "Study Key", 32)
    lmconnect(world, "Family Hallway", "Master Bedroom", "Master Bedroom Key", 31)
    lmconnect(world, "Family Hallway", "Nursery", "Nursery Key", 27)
    lmconnect(world, "Family Hallway", "Twins' Room", "Twins Bedroom Key", 28)
    lmconnect(world, "1F Hallway", "Basement Stairwell", "Basement Stairwell Key", 9)
    lmconnect(world, "1F Hallway", "2F Stairwell", "Lower 2F Stairwell Key", 74)
    lmconnect(world, "1F Hallway", "Courtyard", "Club Key", 42)
    lmconnect(world, "1F Hallway", "1F Bathroom", "1F Bathroom Key", 23)
    lmconnect(world, "1F Hallway", "Conservatory", "Conservatory Key", 21)
    lmconnect(world, "1F Hallway", "Billiards Room", "Billiards Room Key", 17)
    lmconnect(world, "1F Hallway", "1F Washroom", "1F Washroom Key", 20)
            # lambda state, wash_boo_count=world.options.washroom_boo_count.value: state.has_group("Boo", world.player, wash_boo_count)
            #               or state.has("Boo", world.player, wash_boo_count))
    lmconnect(world, "1F Hallway", "Ballroom", "Ballroom Key", 15)
    lmconnect(world, "1F Hallway", "Dining Room", "Dining Room Key", 14)
    lmconnect(world, "1F Hallway", "Laundry Room", "Laundry Room Key", 7)
    lmconnect(world, "1F Hallway", "Fortune-Teller's Room", "Fortune Teller Key", 4)
    lmconnect(world, "Courtyard", "Rec Room", "North Rec Room Key", 25)
    lmconnect(world, "Ballroom", "Storage Room", "Storage Room Key", 16)
    lmconnect(world, "Dining Room", "Kitchen", "Kitchen Key", 11)
    lmconnect(world, "Kitchen", "Boneyard", "Boneyard Key", 10,
            lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "Boneyard", "Graveyard",
            rule=lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "Billiards Room", "Projection Room", "Projection Room Key", 18)
    lmconnect(world, "Fortune-Teller's Room", "Mirror Room", "Mirror Room Key", 5)
    lmconnect(world, "Laundry Room", "Butler's Room", "Butler's Room Key", 1)
    lmconnect(world, "Butler's Room", "Hidden Room", rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Courtyard", "The Well")
    lmconnect(world, "Rec Room", "2F Stairwell", "South Rec Room Key", 24)
    lmconnect(world, "2F Stairwell", "Tea Room", "Tea Room Key", 47,
            lambda state: Rules.can_fst_water(state, world.player), required_element="Water")
    lmconnect(world, "2F Stairwell", "2F Rear Hallway", "Upper 2F Stairwell Key", 75)
    lmconnect(world, "2F Rear Hallway", "2F Bathroom", "2F Bathroom Key", 48)
    lmconnect(world, "2F Rear Hallway", "2F Washroom", "2F Washroom Key", 45)
    lmconnect(world, "2F Rear Hallway", "Nana's Room", "Nana's Room Key", 49)
    lmconnect(world, "2F Rear Hallway", "Astral Hall", "Astral Hall Key", 44)
    lmconnect(world, "2F Rear Hallway", "Sitting Room", "Sitting Room Key", 29)
    lmconnect(world, "2F Rear Hallway", "Safari Room", "Safari Room Key", 56)
    lmconnect(world, "Astral Hall", "Observatory", "Observatory Key", 40,
            lambda state: Rules.can_fst_fire(state, world.player), required_element="Fire")
    lmconnect(world, "Sitting Room", "Guest Room", "Guest Room Key", 30)
    lmconnect(world, "Safari Room", "East Attic Hallway", "East Attic Hallway Key", 55)
    lmconnect(world, "East Attic Hallway", "Artist's Studio", "Artist's Studio Key", 63)
    lmconnect(world, "East Attic Hallway", "Balcony", "Balcony Key", 62,
            lambda state, balc_boo_count=world.options.balcony_boo_count.value: state.has_group("Boo", world.player, balc_boo_count)
                          or state.has("Boo", world.player, balc_boo_count))
    lmconnect(world, "Balcony", "West Attic Hallway", "Diamond Key", 59)
    lmconnect(world, "West Attic Hallway", "Armory", "Armory Key", 51)
    lmconnect(world, "West Attic Hallway", "Telephone Room", "Telephone Room Key", 52)
    lmconnect(world, "Telephone Room", "Clockwork Room", "Clockwork Key", 53)
    lmconnect(world, "Armory", "Ceramics Studio", "Ceramics Studio Key", 50)
    lmconnect(world, "Clockwork Room", "Roof", rule=lambda state: state.has("Defeat Clockwork", world.player))
    lmconnect(world, "Roof", "Sealed Room", one_way=True),
    lmconnect(world, "Basement Stairwell", "Breaker Room", "Breaker Room Key", 71)
    lmconnect(world, "Basement Stairwell", "Cellar", "Cellar Key", 68,
              rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Cellar", "Basement Hallway", "Basement Hallway Key", 67,
              rule=lambda state: state.has("Poltergust 3000", world.player))
    lmconnect(world, "Basement Hallway", "Cold Storage", "Cold Storage Key", 65)
    lmconnect(world, "Basement Hallway", "Pipe Room", "Pipe Room Key", 69)
    lmconnect(world, "Basement Hallway", "Altar Hallway", "Altar Hallway Key", 70)
    lmconnect(world, "Altar Hallway", "Secret Altar", "Spade Key", 72,
            lambda state, final_boo_count=world.options.final_boo_count.value: state.has_group("Boo", world.player, final_boo_count)
                          or state.has("Boo", world.player, final_boo_count))


REGION_LIST = {
    "Parlor": 35,
    "Foyer": 2,
    "Family Hallway": 29,
    "1F Hallway": 6,
    "Anteroom": 39,
    "The Well": 69,
    "Wardrobe": 38,
    "Wardrobe Balcony": 37,
    "Study": 34,
    "Master Bedroom": 33,
    "Nursery": 24,
    "Twins' Room": 25,
    "Laundry Room": 5,
    "Butler's Room": 0,
    "Fortune-Teller's Room": 3,
    "Ballroom": 10,
    "Dining Room": 9,
    "1F Washroom": 17,
    "1F Bathroom": 20,
    "Conservatory": 21,
    "Billiards Room": 12,
    "Basement Stairwell": 65,
    "Projection Room": 13,
    "Kitchen": 8,
    "Boneyard": 11,
    "Graveyard": 16,
    "Hidden Room": 1,
    "Storage Room": 14,
    "Mirror Room": 4,
    "Rec Room": 22,
    "Courtyard": 23,
    "2F Stairwell": 19,
    "Cellar": 63,
    "Breaker Room": 67,
    "Basement Hallway": 62,
    "Cold Storage": 61,
    "Pipe Room": 66,
    "Secret Altar": 70,
    "Tea Room": 47,
    "Nana's Room": 46,
    "2F Rear Hallway": 26,
    "2F Washroom": 42,
    "2F Bathroom": 45,
    "Astral Hall": 40,
    "Observatory": 41,
    "Sealed Room": 36,
    "Sitting Room": 27,
    "Guest Room": 28,
    "Safari Room": 52,
    "East Attic Hallway": 51,
    "West Attic Hallway": 49,
    "Artist's Studio": 57,
    "Balcony": 59,
    "Armory": 48,
    "Ceramics Studio": 55,
    "Telephone Room": 50,
    "Clockwork Room": 56,
    "Roof": 60,
    "Altar Hallway": 68
}

# ROOM_EXITS = []

# THis dict maps exits to entrances located in that exit
# ENTRANCE_ACCESSIBILITY: dict[str, list[str]] = {
#    "Foyer": [
#        "Dungeon Entrance on Dragon Roost Island",
#        ],
