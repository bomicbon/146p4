import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import math


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

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
    if len(state.my_fleets()) >= 1:
        return False

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


def closestFour(state):
    enemyDestIDs = [f.destination_planet for f in state.enemy_fleets()]
    test = [(p, state.distance(state.my_planets()[0].ID, p.ID) + p.num_ships)
            for p in state.neutral_planets() if p.ID not in enemyDestIDs]
    test = sorted(test, key=lambda x: x[1])
    test = test[:4]

    for d in test:
        issue_order(state, state.my_planets()[0].ID, d[
                    0].ID, (d[0].num_ships + 1) * d[0].growth_rate)
    return True


def attack100(state):
    myP = max([p for p in state.my_planets() if p.num_ships >= 100],
              key=lambda x: x.num_ships)
    if not myP:
        return False

    distances = []
    for planet in state.not_my_planets():
        distances.append((planet, state.distance(
            myP.ID, planet.ID) + planet.num_ships))

    distances = sorted(distances, key=lambda x: x[1])
    distances = distances[:3]
    for d in distances:
        issue_order(state, myP.ID, d[0].ID,
                    (d[0].num_ships + 1) * d[0].growth_rate)

'''
# Neutralize colonizing enemy units with closest competent planet
def defend_planet(state):
    min_dist = math.inf
    second_min_dist = math.inf
    # Find where enemy is going
    for t in state.enemy_fleets():
        tp = t.destination_planet
        for p in state.my_planets():
            if p is not t.destination_planet:
                if min_dist > state.distance(p, tp.ID):
                    min_dist = state.distance(p, tp.ID)
                    support_planet = p
                else:
                    if second_min_dist > state.distance(p, tp):
                        second_min_dist = state.distance(p, tp)
                        backup_planet = p
            else:
                support_planet = max(
                    state.my_planets(), key=lambda t: t.num_ships, default=None)
                for p in state.my_planets():
                    if p is not support_planet:
                        backup_planet = p
                        break
        # if enough troops and enemy is about to arrive - deploy steal fleet
        if support_planet.num_ships > t.num_ships - tp.num_ships:
            if t.turns_remaining <= 2:
                deployment = int((t.num_ships - tp.num_ships) * 1.5)
                issue_order(state, support_planet.ID, tp.ID, deployment)
            else:
                pass
        # if not enough, replenish with neighboring planet
        else:
            deployment = int(backup_planet.num_ships / 2)
            issue_order(state, backup_planet.ID, support_planet.ID, deployment)
    return True
'''
