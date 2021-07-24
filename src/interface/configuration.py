from threading import Lock

from enum import IntEnum


class State(IntEnum):
    stop = 0
    move_to_pos = 1
    move_to_dir = 2


class RotatorDir(IntEnum):
    up = 1
    down = 2
    clockwise = 3
    counterclockwise = 4


class Configuration(object):
    def __init__(self):
        self._lock_desired = Lock()
        self._desired_pos: [int, int] = [0, 0]
        self._desired_direction: RotatorDir = RotatorDir.up
        self.speed = 20

        self._lock_actual = Lock()
        self._actualPos: [int, int] = [0, 0]

        self.state = State.stop

    def get_actual_pos(self) -> [int, int]:
        with self._lock_actual:
            return self._actualPos

    def set_actual_pos(self, pos: [int, int]):
        with self._lock_actual:
            self._actualPos = pos

    def get_desired_pos(self) -> [int, int]:
        with self._lock_desired:
            return self._desired_pos

    def set_desired_pos(self, pos: [int, int]):
        with self._lock_desired:
            self._desired_pos = pos

    def get_desired_direc(self) -> RotatorDir:
        with self._lock_desired:
            return self._desired_direction

    def set_desired_direc(self, pos: RotatorDir):
        with self._lock_desired:
            self._desired_direction = pos
