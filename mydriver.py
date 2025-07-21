from rose.common import obstacles, actions  # NOQA

driver_name = "SmartDrive v0.5"
bad = [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]


def check_corner(world, pos, xAdjaster):
    if world.get(pos["f" + xAdjaster]) in (obstacles.PENGUIN, obstacles.NONE) and world.get(
            pos["ff" + xAdjaster]) in (obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER,actions.NONE):
        return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if world.get(pos["f"]) == obstacles.NONE:
        return actions.NONE
    return actions.RIGHT if xAdjaster == "r" else actions.LEFT


def check_center(world, pos):
    if world.get(pos["fl"]) in (obstacles.PENGUIN, obstacles.NONE) and pos["s"][1] > 2 and world.get(pos["ffl"]) in (obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER): return actions.LEFT
    if world.get(pos["fr"]) in (obstacles.PENGUIN, obstacles.NONE) and pos["s"][1] > 2 and world.get(pos["ffr"]) in (obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER): return actions.RIGHT
    if world.get(pos["f"]) in bad:
        if world.get(pos["fl"]) in (obstacles.PENGUIN, obstacles.NONE): return actions.LEFT
        if world.get(pos["fr"]) in (obstacles.PENGUIN, obstacles.NONE): return actions.RIGHT
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
