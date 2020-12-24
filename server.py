import socket
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
SERVER_LISTEN_NUM = 5


class Server():
    def __init__(self):
        self.Ip = SERVER_IP
        self.Port = SERVER_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.Ip, self.Port)
        self.socket.listen(SERVER_LISTEN_NUM)

        self.socket_list = [self.socket]
        self.clients = {}
        #self.infomation = {}

        print(f"Listening for connections on {SERVER_IP}:{SERVER_PORT}...")

    def start(self):
        read_sockets, _, exception_sockets = select.select(
            self.socket_list, [], self.socket_list)
        for notified_socket in read_sockets:
            if notified_socket is self.socket:
                print('wait for connecting...')
                client_socket, client_address = self.socket.accept()

                # TODO:
                # receve infomation from client
                info = self.receive_info()
                if info is False:
                    print("error")
                    continue
                self.socket_list.append(client_socket)
                # TODO:
                self.process()
                # TODO:
                self.send_class_info()

                print(f"send successfully, client address is {client_address}")
            else:
                pass

            for notified_socket in exception_sockets:
                self.socket_list.remove(notified_socket)
                del self.clients[notified_socket]

    def receive_info(self):
        return True

    def process(self):
        pass

    def send_class_info(self):
        pass
