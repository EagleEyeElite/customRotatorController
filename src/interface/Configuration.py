from enum import IntEnum


class State(IntEnum):
    """
    different modes of the satellite receiver
    """
    stop = 0
    move_to_pos = 1
    move_to_dir = 2


class RotatorDir(IntEnum):
    up = 1
    down = 2
    clockwise = 3
    counterclockwise = 4


class Configuration(object):
    """
    middle class for rotctl and the controller to communicate.
    The communication is async. One thread sets a value, the other reads it.
    This is used in a thread safe manner, since every entry is only ever written by one thread,
    the other thread just reads the value
    """
    def __init__(self):
        self.desired_pos: [int, int] = [0, 0]
        self.desired_direction: RotatorDir = RotatorDir.up
        self.speed = 20

        self.actualPos: [int, int] = [0, 0]
        self.error = False
        self.state = State.stop
