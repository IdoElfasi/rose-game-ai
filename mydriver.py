from rose.common import obstacles, actions  # NOQA

driver_name = "SmartDrive v1.6.5"
bad = [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]


def check_corner(world, pos, xAdjaster):
    print("Checking corner")
    f = world.get(pos["f"])
    ff = world.get(pos["ff"])
    fx = world.get(pos["f" + xAdjaster])
    ffx = world.get(pos["ff" + xAdjaster])
    if f in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.NONE] and fx in [obstacles.NONE, obstacles.PENGUIN] and ff in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.NONE] and ffx in [obstacles.NONE, obstacles.WATER, obstacles.CRACK, obstacles.PENGUIN]: return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if f in bad:
        if fx in (obstacles.PENGUIN, obstacles.NONE):
            return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    else:
        if fx in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]:
            if f == obstacles.NONE: return actions.NONE
            if f == obstacles.WATER: return actions.BRAKE
            if f == obstacles.CRACK: return actions.JUMP
    print(f"ff: {ff}  ff{xAdjaster}: {ffx}")
    print(f"f: {f}  f{xAdjaster}: {fx}")
    if world.get(pos["ff"]) == obstacles.PENGUIN :
        if f == obstacles.NONE: return actions.NONE
        if f == obstacles.WATER: return actions.BRAKE
        if f == obstacles.CRACK: return actions.JUMP
    if ffx == obstacles.PENGUIN : return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if f == obstacles.WATER : return actions.BRAKE
    if f == obstacles.CRACK: return actions.JUMP
    if ff in (obstacles.CRACK, obstacles.WATER) : return actions.NONE
    if ffx in (obstacles.CRACK, obstacles.WATER) : return actions.RIGHT if xAdjaster == "r" else actions.LEFT
    if ff == obstacles.NONE : return actions.NONE
    if ffx == obstacles.NONE : return actions.RIGHT if xAdjaster == "r" else actions.LEFT


def check_center(world, pos):
    f = world.get(pos["f"])
    fl = world.get(pos["fl"])
    fr = world.get(pos["fr"])
    ff = world.get(pos["ff"])
    ffl = world.get(pos["ffl"])
    ffr = world.get(pos["ffr"])
    possible = [actions.NONE, actions.LEFT, actions.RIGHT]
    if f in bad: possible.remove(actions.NONE)
    if fl in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]: possible.remove(actions.LEFT)
    if fr in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER, obstacles.WATER, obstacles.CRACK]: possible.remove(actions.RIGHT)
    allSame = True if len(possible) == 0 or len(possible) == 3 else False
    if (allSame or actions.NONE in possible) and ff == obstacles.PENGUIN :
        if f == obstacles.NONE : return actions.NONE
        if f == obstacles.WATER: return actions.BRAKE
        if f == obstacles.CRACK: return actions.JUMP
    if (allSame or actions.LEFT in possible) and ffl == obstacles.PENGUIN: return actions.LEFT
    if (allSame or actions.RIGHT in possible) and ffr == obstacles.PENGUIN: return actions.RIGHT
    if f == obstacles.WATER : return actions.BRAKE
    if f == obstacles.CRACK: return actions.JUMP
    if (allSame or actions.NONE in possible) and ff in (obstacles.CRACK, obstacles.WATER) : return actions.NONE
    if (allSame or actions.LEFT in possible) and ffl in (obstacles.CRACK, obstacles.WATER): return actions.LEFT
    if (allSame or actions.RIGHT in possible) and ffr in (obstacles.CRACK, obstacles.WATER): return actions.RIGHT
    if (allSame or actions.NONE in possible) and ff == obstacles.NONE : return actions.NONE
    if (allSame or actions.LEFT in possible) and ffl == obstacles.NONE: return actions.LEFT
    if (allSame or actions.RIGHT in possible) and ffr == obstacles.NONE: return actions.RIGHT
    return actions.NONE


def directByLane(world, pos):
    if world.get(pos["f"]) == obstacles.PENGUIN: return actions.PICKUP
    # if world.get(pos["f"]) == obstacles.WATER: return actions.BRAKE
    # if world.get(pos["f"]) == obstacles.CRACK: return actions.JUMP
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