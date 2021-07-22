import socket
import selectors
from logzero import logger
from configuration import Configuration
import threading


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
        self.rC = rc

    def __del__(self):
        self.selector.close()

    def run(self):
        while True:
            events = self.selector.select(timeout=None)
            for key, _ in events:
                if key.data is None:
                    self.accept_client(key.fileobj)
                else:
                    self.service_client(key.fileobj, key.data)

    def accept_client(self, socket: socket.socket):
        client_sock, addr = socket.accept()
        logger.info(f"Connection address: {addr}")
        client_sock.setblocking(False)
        self.selector.register(client_sock, selectors.EVENT_READ, data=addr)

    def service_client(self, sock: socket.socket, addr):
        request = sock.recv(4096).decode('utf-8')
        listed_command = request.split(' ')

        if not request or request == 'q\n':
            logger.info(f"Closing connection to {addr}")
            self.selector.unregister(sock)
            sock.close()

        elif request == '\\dump_state\n':
            sock.sendall(f"{0}\n{2}\n{0}\n{100000}\n{0}\n{100000}\n".encode('utf-8'))

        elif listed_command[0] == 'P':
            az = listed_command[1]
            el = listed_command[2]
            self.set_pos(sock, az, el)
            logger.info(f"TPM request: AZ {az}, EL {el}")

        elif request == 'p\n':
            self.get_pos(sock)
        else:
            sock.sendall(b'RPRT -1\n')

    def get_pos(self, sock: socket.socket):
        pos = self.rC.get_actual_pos()
        sock.sendall(f"{format(pos[0], '.6f')}\n{format(pos[1], '.6f')}\n".encode('utf-8'))

    def set_pos(self, sock: socket.socket, az_str: str, el_str: str):
        try:
            self.rC.set_desired_pos([int(float(az_str)), int(float(el_str))])
        except ValueError:
            sock.sendall(b'RPRT -1\n')
        else:
            sock.sendall(b'RPRT 0\n')
