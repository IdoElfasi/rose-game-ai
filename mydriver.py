from rose.common import obstacles, actions  # NOQA

driver_name = "SmartDrive v1.6.2"
bad = [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]


def check_corner(world, pos, xAdjaster):
    if world.get(pos["f"]) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.NONE] and world.get(pos["f" + xAdjaster]) in [obstacles.NONE, obstacles.PENGUIN] and world.get(pos["ff"]) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.NONE] and world.get(pos["ff" + xAdjaster]) in [obstacles.NONE, obstacles.WATER, obstacles.CRACK, obstacles.PENGUIN]: return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if world.get(pos["f"]) in bad:
        if world.get(pos["f" + xAdjaster]) in (obstacles.PENGUIN, obstacles.NONE):
            return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    else:
        if world.get(pos["f" + xAdjaster]) in bad:
            return actions.NONE
    if world.get(pos["ff"]) == obstacles.PENGUIN : return actions.NONE
    if world.get(pos["ff" + xAdjaster]) == obstacles.PENGUIN : return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if world.get(pos["ff"]) in (obstacles.CRACK, obstacles.WATER) : return actions.NONE
    if world.get(pos["ff" + xAdjaster]) in (obstacles.CRACK, obstacles.WATER) : return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if world.get(pos["ff"]) == obstacles.NONE : return actions.NONE
    if world.get(pos["ff" + xAdjaster]) == obstacles.NONE : return actions.RIGHT if xAdjaster == "r" else actions.LEFT


def check_center(world, pos):
    possible = [actions.NONE, actions.LEFT, actions.RIGHT]
    if world.get(pos["f"]) in bad: possible.remove(actions.NONE)
    if world.get(pos["fl"]) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]: possible.remove(actions.LEFT)
    if world.get(pos["fr"]) in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]: possible.remove(actions.RIGHT)
    allSame = True if len(possible) == 0 or len(possible) == 3 else False
    print(f"possible: {possible} | allSame {allSame}")
    print("ff: "+ world.get(pos["ff"]) + " | ffl: " + world.get(pos["ffl"]) + " | ffr: " + world.get(pos["ffr"]) + "")
    if (allSame or actions.NONE in possible) and world.get(pos["ff"]) == obstacles.PENGUIN : return actions.NONE
    if (allSame or actions.LEFT in possible) and world.get(pos["ffl"]) == obstacles.PENGUIN: return actions.LEFT
    if (allSame or actions.RIGHT in possible) and world.get(pos["ffr"]) == obstacles.PENGUIN: return actions.RIGHT
    if (allSame or actions.NONE in possible) and world.get(pos["ff"]) in (obstacles.CRACK, obstacles.WATER) : return actions.NONE
    if (allSame or actions.LEFT in possible) and world.get(pos["ffl"]) in (obstacles.CRACK, obstacles.WATER): return actions.LEFT
    if (allSame or actions.RIGHT in possible) and world.get(pos["ffr"]) in (obstacles.CRACK, obstacles.WATER): return actions.RIGHT
    if (allSame or actions.NONE in possible) and world.get(pos["ff"]) == obstacles.NONE : return actions.NONE
    if (allSame or actions.LEFT in possible) and world.get(pos["ffl"]) == obstacles.NONE: return actions.LEFT
    if (allSame or actions.RIGHT in possible) and world.get(pos["ffr"]) == obstacles.NONE: return actions.RIGHT
    return actions.NONE


def directByLane(world, pos):
    if world.get(pos["f"]) == obstacles.PENGUIN: return actions.PICKUP
    if world.get(pos["f"]) == obstacles.WATER: return actions.BRAKE
    if world.get(pos["f"]) == obstacles.CRACK: return actions.JUMP
    if pos["s"][0] == 0 or pos["s"][0] == 3:
        return check_corner(world, pos, "r")
    if pos["s"][0] == 2 or pos["s"][0] == 5:
        return check_corner(world, pos, "l")
    return check_center(world, pos)


def drive(world):
    x, y = world.car.x, world.car.y
    poss = {"s": (x, y), "f": (x, y - 1), "fl": (x - 1, y - 1), "fr": (x + 1, y - 1), "ffl": (x - 1, y - 2),
            "ffr": (x + 1, y - 2), "ffll": (x - 2, y - 2), "ffrr": (x + 2, y - 2), "ff": (x, y - 2)}
    try:
        return directByLane(world, poss)
    except IndexError:
        return actions.NONE
