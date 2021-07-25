import time
import threading
import interface
from .SatelliteReceiver import SatelliteReceiver


class Controller(threading.Thread):
    def __init__(self, RC: interface.Configuration):
        super().__init__()
        self.sRec = SatelliteReceiver()
        self.RC = RC
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while True:
            if self._stop_event.is_set():
                self.sRec.exit()
                return

            if self.RC.error:
                print("error occurred")
                self.sRec.exit()
                return

            self.RC.actual_pos = self.sRec.get_rec_pos()

            if self.RC.state == interface.State.stop:
                self.sRec.stop()
            elif self.RC.state == interface.State.move_to_dir:
                speed = self.RC.speed
                self.sRec.move_dir(self.RC.desired_direction, speed)
            elif self.RC.state == interface.State.move_to_pos:
                self.sRec.move_pos(self.RC.desired_pos)

            time.sleep(0.1)
