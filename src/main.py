#!/usr/bin/python3
import threading
import sys
from logzero import logger

import time
import interface
import controller

if __name__ == "__main__":
    """
    Software entry point
    loads thread to service client and to control the satellite receiver itself
    """

    rC = interface.Configuration()
    Controller = controller.Controller(rC)
    rotCtl = interface.RotCtl(rC)

    t0 = threading.Thread(target=rotCtl.run)
    t1 = threading.Thread(target=Controller.run)

    try:
        t0.start()
        t1.start()
        while True:
            Controller.sRec.print_debug()
            time.sleep(1)
            pass

    except KeyboardInterrupt:
        pass

    # quit
    rotCtl.stop()
    Controller.stop()
    t0.join(timeout=0.2)
    t1.join(timeout=0.8)
    logger.info("exit")
    time.sleep(0.05)  # wait for stdout
    sys.exit(0)
