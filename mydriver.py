from rose.common import obstacles, actions  # NOQA

driver_name = "Best drhaer"
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
    if world.get(pos["f"]) == obstacles.PENGUIN or world.get(pos["f"+xAdjaster]) in bad:
        return 0
    if world.get(pos["f"+xAdjaster]) == obstacles.PENGUIN or world.get(pos["ff"+xAdjaster+xAdjaster]) == obstacles.PENGUIN or world.get(pos["f"]) in bad:
        return xAdjaster
    return "r" if xAdjaster == "l" else "l"


def check_center(world, pos):
    if world.get(pos["f"]) == obstacles.PENGUIN:
        return actions.NONE
    if world.get(pos["fl"]) == obstacles.PENGUIN or( pos["s"][1] > 2 and world.get(pos["ffl"]) == obstacles.PENGUIN and world.get(pos["fl"]) not in bad):
        return actions.LEFT
    if world.get(pos["fr"]) not in bad and world.get(pos["ffr"]==obstacles.PENGUIN):
        return actions.RIGHT
    return actions.NONE

def pingwin(world, pos):
    if pos["s"][0] == 0 or pos["s"][0] == 3:
        if chek_corner(world, pos, "r") == "r":
            return actions.RIGHT
        return actions.NONE
    if pos["s"][0] == 2 or pos["s"][0] == 5:
        if chek_corner(world, pos, "l") == "l":
            return actions.LEFT
        return actions.NONE
    return check_center(world, pos)


def drive(world):
    poss = {"s":(world.car.x, world.car.y),"f":(pos[0],pos[1]-1),"fl":(pos[0]-1,pos[1]-1),"fr":(pos[0]+1,pos[1]-1),"ffl":(pos[0]-1,pos[1]-2),"ffr":(pos[0]+1,pos[1]-2),"ffll":(pos[0]-2,pos[1]-2),"ffrr":(pos[0]+2,pos[1]-2),"ff":(pos[0],pos[1]-2)}
    try:
        obstacle = world.get(poss["f"])
        if world.get(poss["f"]) == obstacles.NONE: return pingwin(world, poss)
        return soumthing_infrount(world, poss, obstacle)
    except IndexError:
        return actions.NONE

