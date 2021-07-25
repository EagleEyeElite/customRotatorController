import socket
import selectors
from logzero import logger
from .Configuration import Configuration, RotatorDir, State
import threading
import sys
import errno


class RotCtl(threading.Thread):
    """
    This class serves a rotctl API.
    """

    def __init__(self, rc: Configuration):
        super().__init__()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', 4533))
        server_socket.listen(5)
        server_socket.setblocking(False)

        self.selector = selectors.DefaultSelector()
        self.selector.register(server_socket, selectors.EVENT_READ)
        self.RC = rc

        self._stop_event = threading.Event()

        self._error = b'RPRT -1\n'
        self._confirm = b'RPRT 0\n'

    def stop(self):
        self._stop_event.set()

    def __del__(self):
        self.selector.close()

    def run(self):
        while True:
            if self._stop_event.is_set():
                return
            events = self.selector.select(timeout=0.1)
            for key, _ in events:
                if key.data is None:
                    self.accept_client(key.fileobj)
                    continue

                try:
                    request = key.fileobj.recv(4096).decode('utf-8')
                except socket.error as e:
                    err = e.args[0]
                    if err != errno.EAGAIN and err != errno.EWOULDBLOCK:
                        # a "real" error occurred
                        print("shit, exit")
                        sys.exit(1)
                    continue

                self.service_client(key.fileobj, key.data, request)

    def accept_client(self, socket: socket.socket):
        client_sock, addr = socket.accept()
        logger.info(f"Connection address: {addr}")
        client_sock.setblocking(False)
        self.selector.register(client_sock, selectors.EVENT_READ, data=addr)

    def service_client(self, sock: socket.socket, addr, request):
        listed_command = request.split(' ')

        if not request or request == 'q\n':
            logger.info(f"Closing connection to {addr}")
            self.selector.unregister(sock)
            sock.close()

        elif request == '\\dump_state\n':
            sock.sendall(f"{0}\n{2}\n{0}\n{360}\n{0}\n{360}\n".encode('utf-8'))

        elif listed_command[0] == 'P':
            az = listed_command[1]
            el = listed_command[2]
            self.set_pos(sock, az, el)
            logger.info(f"TPM request: AZ {az}, EL {el}")

        elif request == 'p\n':
            self.get_pos(sock)

        elif listed_command[0] == 'M':
            direc = listed_command[1]
            speed = listed_command[2]
            self.move(sock, direc, speed)
            logger.info(f"MOVE request: DIR {direc}, Speed {speed}")

        elif request == 'K\n':
            self.set_pos(sock, "0", "0")
            logger.info(f"PARK request: AZ {0}, EL {0}")

        elif request == 'S\n':
            self.RC.state = State.stop
            sock.sendall(self._confirm)
            logger.info(f"Stop request")

        elif listed_command[0] == 'R':
            reset_option = listed_command[1]

            if reset_option != '1\n':
                sock.sendall(self._error)
                return

            sock.sendall(self._confirm)

            self.set_pos(sock, "0", "0")

            if reset_option == '1\n':
                logger.info(f"RESET request: AZ {0}, EL {0}")
            else:
                logger.info(f"RESET request: Unknown option {reset_option}")

        elif request == '_\n':
            sock.sendall("Satcom custom Rotator\n".encode('utf-8'))

        else:
            sock.sendall(self._error)

    def get_pos(self, sock: socket.socket):
        pos = self.RC.actual_pos
        sock.sendall(f"{format(pos[0], '.6f')}\n{format(pos[1], '.6f')}\n".encode('utf-8'))

    def set_pos(self, sock: socket.socket, az_str: str, el_str: str):
        try:
            self.RC.desired_pos = [int(float(az_str)), int(float(el_str))]
            self.RC.state = State.move_to_pos
        except ValueError:
            sock.sendall(self._error)
        else:
            sock.sendall(self._confirm)

    def move(self, sock: socket.socket, dir: str, speed: str):
        try:
            self.RC.speed = int(speed)
        except ValueError:
            sock.sendall(self._error)
            self.RC.state = State.stop
            return

        sock.sendall(self._confirm)
        self.RC.state = State.move_to_dir

        if dir == '2':
            self.RC.desired_direc = RotatorDir.up
        elif dir == '4':
            self.RC.desired_direc = RotatorDir.down
        elif dir == '8':
            self.RC.desired_direc = RotatorDir.clockwise
        elif dir == '16':
            self.RC.desired_direc = RotatorDir.counterclockwise
        else:
            logger.warning("Wrong MOVE direction")
