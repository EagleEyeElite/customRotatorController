from threading import Lock


class Configuration(object):
    def __init__(self):

        self._lock_desired = Lock()
        self._desired_pos: [int, int] = [0, 0]

        self._lock_actual = Lock()
        self._actualPos: [int, int] = [0, 0]

        self.magnetic_encoder_angle = [0, 0]

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

    def print_debug(self):
        print(str(self._actualPos[0]) + "\t" +
              str(self.magnetic_encoder_angle[0]) + "\t" +
              str(self._actualPos[1]) + "\t" +
              str(self.magnetic_encoder_angle[1]))
