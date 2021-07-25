#!/usr/bin/python3
import threading
import sys

import time
import interface
import controller

if __name__ == "__main__":
    """
    Software entry point
    """

    rC = interface.Configuration()
    controller = controller.Controller(rC)
    rotCtl = interface.RotCtl(rC)

    t0 = threading.Thread(target=rotCtl.run)
    t1 = threading.Thread(target=controller.run)

    try:
        t0.start()
        t1.start()
        while True:
            controller.sRec.print_debug()
            time.sleep(1)
            pass

    except KeyboardInterrupt:
        pass

    # quit
    rotCtl.stop()
    controller.stop()
    t0.join(timeout=0.2)
    t1.join(timeout=0.8)
    print("\nexit")
    time.sleep(0.05)  # wait for stdout
    sys.exit(0)
