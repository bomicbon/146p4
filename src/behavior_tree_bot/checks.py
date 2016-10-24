

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
        + sum(fleet.num_ships for fleet in state.my_fleets()) \
        > sum(planet.num_ships for planet in state.enemy_planets()) \
        + sum(fleet.num_ships for fleet in state.enemy_fleets())


def if_attacked(state):
    return len(state.enemy_fleets()) > 0


def neutral_lost(state):
    for t in state.enemy_fleets():
        if t.destination_planet in state.neutral_planets():
            # Is enemy fleet big enough to take over?
            target = t.destination_planet
            if t.num_ships > target.num_ships:
                return True
            else:
                pass
    return False
