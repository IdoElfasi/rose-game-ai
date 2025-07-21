from rose.common import obstacles, actions  # NOQA

driver_name = "pathDrive v2.0"
points = {"": (0, 0), "crack": (5, -10), "trash": (-10, -10), "penguin": (10, 0), "bike": (-10, -10), "water": (4, -10),
          "barrier": (-10, -10)}


def check_corner(world, pos, p, xAdjaster, counter):
    fpos = mouve_pos(pos, 0, -1)
    fpoints = directByLane(world, fpos, p + points[world.get(fpos["s"])][0], counter - 1)
    if xAdjaster == "l":
        mpos = mouve_pos(fpos, -1, 0)
    else:
        mpos = mouve_pos(fpos, 1, 0)
    mpoints = directByLane(world, mpos, p + points[world.get(mpos["s"])][1], counter - 1)
    if fpoints > mpoints:
        if counter == 4:
            return "f"
        return fpoints
    if counter == 4:
        return xAdjaster
    return mpoints


def biger(f, l, r):
    if f > l:
        if f > r:
            return "f"
        else:
            return "r"
    if r > l: return "r"
    return "l"


def check_center(world, pos, p, counter):
    fpos = mouve_pos(pos, 0, -1)
    fpoints = directByLane(world, fpos, p + points[world.get(pos["f"])][0], counter - 1)
    rpos = mouve_pos(fpos, 1, 0)
    rpoints = directByLane(world, rpos, p + points[world.get(pos["fr"])][1], counter - 1)
    lpos = mouve_pos(fpos, -1, 0)
    lpoints = directByLane(world, lpos, p + points[world.get(pos["fl"])][1], counter - 1)
    big = biger(fpoints, lpoints, rpoints)
    if big == "f":
        if counter == 4:
            return "f"
        return fpoints
    if big == "r":
        if counter == 4:
            return "r"
        return rpoints
    if counter == 4:
        return "l"
    return lpoints


def mouve_pos(pos, mx, my):
    list_pos = pos.copy()
    fpos = pos.copy()
    for i in pos:
        list_pos[i] = list(list_pos[i])
        list_pos[i][0] = pos[i][0] + mx
        list_pos[i][1] = pos[i][1] + my
        fpos[i] = tuple(list_pos[i])
    return fpos


def directByLane(world, pos, p, counter):
    if counter == 0 or pos["s"][1] < 1: return p + points[world.get(pos["s"])][0]
    if pos["s"][0] == 0 or pos["s"][0] == 3:
        if counter == 4:
            return check_corner(world, pos, p, "r", counter)
        pos = mouve_pos(pos, 1, -1)
        return directByLane(world, pos, p + check_corner(world, pos, p, "r", counter), counter - 1)
    if pos["s"][0] == 2 or pos["s"][0] == 5:
        if counter == 4:
            return check_corner(world, pos, p, "l", counter)
        pos = mouve_pos(pos, -1, -1)
        return directByLane(world, pos, p + check_corner(world, pos, p, "l", counter), counter - 1)
    if counter == 4:
        return check_center(world, pos, p, counter)
    return directByLane(world, pos, p + check_center(world, pos, p, counter), counter - 1)


def picc_actions(obstacle):
    if obstacle == obstacles.PENGUIN:
        return actions.PICKUP
    if obstacle == obstacles.WATER:
        return actions.BRAKE
    if obstacle == obstacles.CRACK:
        return actions.JUMP
    return actions.NONE


def drive(world):
    x = world.car.x
    y = world.car.y
    poss = {"s": (x, y), "f": (x, y - 1), "fl": (x - 1, y - 1), "fr": (x + 1, y - 1)}
    try:
        d = directByLane(world, poss, 0, 4)
        if d == "r": return actions.RIGHT
        if d == "l": return actions.LEFT
        return picc_actions(world.get(poss["f"]))
    except IndexError:
        return actions.NONE


