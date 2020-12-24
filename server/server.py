import socket
import select
import sys

from package import Package

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
SERVER_LISTEN_NUM = 5


class Server():
    def __init__(self):
        self.package = Package()

        self.Ip = SERVER_IP
        self.Port = SERVER_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.Ip, self.Port))
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

                # receve infomation from client
                header, message = self.receive_info(client_socket)
                if header is False:
                    print("error")
                    continue
                if header['mode'] != 'sendMajor':
                    print('mode error!')
                    continue
                header['address'] = client_address
                self.socket_list.append(client_socket)
                self.clients[client_socket] = header

                self.send_info(client_socket, header, message)

                print(
                    f'connect successfully, client\'s add is {client_address}, \
                        Major is {header["Major"]}')

            else:
                header, message = self.receive_info(notified_socket)

                if header is False:
                    print('Closed connection from {}, major in {}'.format(
                        self.clients[notified_socket]['address'],
                        self.clients[notified_socket]['Major']))
                    sys.stdout.flush()
                    self.socket_list.remove(notified_socket)
                    del self.clients[notified_socket]
                    continue

                self.send_info(notified_socket, header, message)

            for notified_socket in exception_sockets:
                self.socket_list.remove(notified_socket)
                del self.clients[notified_socket]

    def receive_info(self, client_socket):
        try:
            header_len_struct = client_socket.recv(4)
            if not len(header_len_struct):
                print('message miss')
                return False, ''
            header_len = self.package.unpack_header_size(header_len_struct)
            header_byte = client_socket.recv(header_len)
            header = self.package.unpack_header(header_byte)
            if header['mode'] == 'getFachschaft' or header[
                    'mode'] == 'sendMajor':
                return header, ''
            # elif header['mode'] == 'classArrange':
            #     message = b''
            #     message_len = header['message_length']
            #     current_len = 0
            #     while current_len < message_len:
            #         one_package = client_socket.recv(1024)
            #         current_len += len(one_package)
            #         message += one_package
            #     message = self.package.unpack_message(message)
            #     return header, messag
            else:
                message = b''
                message_len = header['message_length']
                current_len = 0
                while current_len < message_len:
                    one_package = client_socket.recv(1024)
                    current_len += len(one_package)
                    message += one_package
                message = self.package.unpack_message(message)
                return header, message
        except Exception as e:
            print(f'mystery error : {str(e)}')
            return False, ''

    def process(self, message):
        return True

    def send_info(self, client_socket, header, message):
        if header['mode'] == 'getFachschaft':
            client_socket.send(self.package.pack_message(header, message))
        elif header['mode'] == 'classArrange':
            client_socket.send(self.package.pack_message(header, message))
        elif header['mode'] == 'sendMajor':
            client_socket.send(self.package.pack_header(header))
        else:
            pass
