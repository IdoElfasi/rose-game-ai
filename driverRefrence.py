from rose.common import obstacles, actions  # NOQA

driver_name = "Old Driver (Ref)"


def drive(world):
    print("Started")
    x = world.car.x
    y = world.car.y
    try:
        obstacle = world.get((x, y - 1))
    except IndexError:
        return actions.NONE
    else:
        if obstacle == obstacles.PENGUIN: return actions.PICKUP
        elif obstacle == obstacles.WATER: return actions.BRAKE
        elif obstacle == obstacles.CRACK: return actions.JUMP
        elif obstacle in [obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER]:
            if x == 0 or x == 3: return actions.RIGHT
            elif x == 2 or x == 5: return actions.LEFT
            elif world.get((x - 1, y - 1)) in [obstacles.NONE, obstacles.PENGUIN] : return actions.LEFT
            else: return actions.RIGHT

    return actions.NONE
