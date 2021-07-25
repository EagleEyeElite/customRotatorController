import time
import threading
import interface

from .rotator import Rotator


class Controller(threading.Thread):
    def __init__(self, RC: interface.Configuration):
        super().__init__()
        self.Rotator = Rotator()

        self.RC = RC
        self.m_encoder_offset = [-self.Rotator.shaft[0].get_magnetic_encoder_angle(),
                                 -self.Rotator.shaft[1].get_magnetic_encoder_angle()]

        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while True:
            if self._stop_event.is_set():
                return

            self.RC.actual_pos = self.Rotator.get_pos()

            if self.RC.state == interface.State.stop:
                self.Rotator.stop()
            elif self.RC.state == interface.State.move_to_dir:
                speed = self.RC.speed
                self.Rotator.move_dir(self.RC.desired_direc, speed)
            elif self.RC.state == interface.State.move_to_pos:
                self.Rotator.move_pos(self.RC.desired_pos)

            time.sleep(0.1)

