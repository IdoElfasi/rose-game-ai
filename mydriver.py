from rose.common import obstacles, actions  # NOQA

driver_name = "SmartDrive v0.2"
bad = [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]


def soumthing_infrount(world, pose, obstacle):
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    if obstacle == obstacles.CRACK:
        return actions.JUMP
    return pingwin(world, pose)


def chek_corner(world, pos, xAdjaster):
    if world.get(pos["f"]) == obstacles.PENGUIN:
        return actions.PICKUP
    elif world.get(pos["f"]) == obstacles.WATER:
        return actions.BRAKE
    elif world.get(pos["f"]) == obstacles.CRACK:
        return actions.JUMP
    elif world.get(pos["f" + xAdjaster]) in (obstacles.PENGUIN, obstacles.NONE) and world.get(
            pos["ff" + xAdjaster]) in (obstacles.PENGUIN, obstacles.CRACK, obstacles.WATER):
        return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    elif world.get(pos["f"]) == obstacles.NONE:
        return actions.NONE


def check_center(world, pos):
    if world.get(pos["f"]) == obstacles.PENGUIN: return actions.PICKUP
    elif world.get(pos["f"]) == obstacles.WATER: return actions.BRAKE
    elif world.get(pos["f"]) == obstacles.CRACK: return actions.JUMP
    elif world.get(pos["fl"]) in (obstacles.PENGUIN, obstacles.NONE) or (pos["s"][1] > 2 and world.get(pos["ffl"]) == obstacles.PENGUIN and world.get(pos["fl"]) not in bad):
        return actions.LEFT
    elif world.get(pos["fr"]) in (obstacles.PENGUIN, obstacles.NONE) and world.get(pos["ffr"] == obstacles.PENGUIN):
        return actions.RIGHT
    return actions.NONE


def pingwin(world, pos):
    if pos["s"][0] == 0 or pos["s"][0] == 3:
        return chek_corner(world, pos, "r")
    if pos["s"][0] == 2 or pos["s"][0] == 5:
        return chek_corner(world, pos, "l")
    return check_center(world, pos)


def drive(world):
    x, y = world.car.x, world.car.y
    poss = {"s": (x, y), "f": (x, y - 1), "fl": (x - 1, y - 1), "fr": (x + 1, y - 1), "ffl": (x - 1, y - 2),
            "ffr": (x + 1, y - 2), "ffll": (x - 2, y - 2), "ffrr": (x + 2, y - 2), "ff": (x, y - 2)}
    try:
        obstacle = world.get(poss["f"])
        if world.get(poss["f"]) == obstacles.NONE: return pingwin(world, poss)
        return soumthing_infrount(world, poss, obstacle)
    except IndexError:
        return actions.NONE
