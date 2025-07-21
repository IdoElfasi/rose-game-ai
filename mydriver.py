from rose.common import obstacles, actions  # NOQA

driver_name = "Best driver"
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
    if world.get((pos[0], pos[1] - 1)) == obstacles.PENGUIN or world.get((pos[0] + xAdjaster, pos[1] - 1)) in bad:
        return 0
    if world.get((pos[0] + xAdjaster, pos[1] - 1)) == obstacles.PENGUIN or world.get(
            (pos[0] + 2 * xAdjaster, pos[1] - 2)) == obstacles.PENGUIN or world.get((pos[0], pos[1] - 1)) in bad:
        return xAdjaster
    return -xAdjaster


def check_center(world, pos):
    if world.get(pos[0], pos[1] - 1) == obstacles.PENGUIN:
        return actions.NONE
    if world.get(pos[0] - 1, pos[1] - 1) == obstacles.PENGUIN or( pos[1] > 2 and world.get(pos[0] - 1, pos[
                                                                                                        1] - 2) == obstacles.PENGUIN and world.get(
        pos[0] - 1, pos[1] - 1) not in bad):
        return actions.LEFT
    if world.get(pos[0] + 1, pos[1] - 1) not in bad :
        return actions.RIGHT
    return actions.NONE

def pingwin(world, pos):
    if pos[0] == 0 or pos[0] == 3:
        if chek_corner(world, pos, 1) == 1:
            return actions.RIGHT
        return actions.NONE
    if pos[0] == 2 or pos[0] == 5:
        if chek_corner(world, pos, -1) == -1:
            return actions.LEFT
        return actions.NONE
    return check_center(world, pos)


def drive(world):
    pos = [world.car.x, world.car.y]
    try:
        obstacle = world.get((pos[0], pos[1]))
    except IndexError:
        return actions.NONE
    else:
        if world.get(pos[0], pos[1] - 1) == obstacles.NONE: return pingwin(world, pos)
        return soumthing_infrount(world, pose, obstacle)
