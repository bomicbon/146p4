

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
        + sum(fleet.num_ships for fleet in state.my_fleets()) \
        > sum(planet.num_ships for planet in state.enemy_planets()) \
        + sum(fleet.num_ships for fleet in state.enemy_fleets())


def starter(state):
    startingPlanet = state.my_planets()
    return len(startingPlanet) < 2


def myFleets(state):
    f = [fleet for fleet in state.my_fleets()]
    if not f:
        return True
    else:
        return False


def above100(state):
    temp = [p for p in state.my_planets() if p.num_ships >= 100]
    return len(temp) > 0


def if_attacked(state):
    e_size = len(state.enemy_fleets())
    if e_size > 0:
        return True
    else:
        return False
