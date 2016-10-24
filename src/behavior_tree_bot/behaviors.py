import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import math


def attack_weakest_enemy_planet(state):
     #(1) If we currently have a fleet in flight, abort plan.
    # if len(state.my_fleets()) >= 1:
    #    return False

    # (2) Find my strongest planet.
    strongest_planet = max(
        state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(),
                         key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    # if len(state.my_fleets()) >= 1:
    #    return False

    # (2) Find my strongest planet.
    strongest_planet = max(
        state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(),
                         key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


# Neutralize colonizing enemy units with closest competent planet
def defend_planet(state):
    # Find which enemy is attacking my planets
    for t in state.enemy_fleets():
        if t.destination_planet in state.my_planets():
            tango = t
            planet_attacked = t.destination_planet
        else:
            return False
    # Find closest planet to the planet being attacked
    min_dist = math.inf
    second_min_dist = math.inf
    for p in state.my_planets():
        if p is not planet_attacked:
            if min_dist >= state.distance(p, planet_attacked):
                min_dist = state.distance(p, planet_attacked)
                support_planet = p
            elif second_min_dist > state.distance(p, planet_attacked):
                second_min_dist = state.distance(p, planet_attacked)
                backup_planet = p
    # Does support_planet have enough planets to support?
    # if not, supply support_planet from next closest planet
    if support_planet.num_ships > tango.num_ships:
        deployment = int(tango.num_ships / 2)
        return issue_order(state, support_planet.ID, planet_attacked.ID, deployment)
    else:
        deployment = int(backup_planet.num_ships / 2)
        return issue_order(state, backup_planet.ID, support_planet.ID, deployment)
    return False


def steal_colony(state):
    # Find enemy fleets attacking neutrals
    hit_list = []
    for t in state.enemy_fleets():
        if t.destination_planet in state.neutral_planets():
            # Is enemy going to take over?
            target = t.destination_planet
            if t.num_ships > target.num_ships:
                strongest_planet = max(
                    state.my_planets(), key=lambda p: p.num_ships, default=None)
                deployment = int(strongest_planet.num_ships / 2)
                return issue_order(state, strongest_planet.ID, target.ID, deployment)
            else:
                pass
    return False

# Spread to all close & weak neutrals


def take_candy(state):
    max_planet = max(state.my_planets(),
                     key=lambda p: p.num_ships, default=None)
    for n in state.neutral_planets():
        if n.num_ships < int(max_planet.num_ships / 3):
            deploy = int(max_planet.num_ships / 3)
            return issue_order(state, max_planet.ID, n.ID, deploy)
    return False
