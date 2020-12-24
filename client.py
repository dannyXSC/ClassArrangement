import socket

from package import Package


class Client():
    def __init__(self, Ip="127.0.0.1", Port=8888, st=0.1):
        self.sleepTime = st
        self.serverIp = Ip
        # self.serverIp="192.168.1.122"
        self.serverPort = Port
        self.package = Package()

    def link(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.serverIp, self.serverPort))
        self.socket.setblocking(False)

    def send_info(self, info):
        if info['mode'] == 'getFachschaft':
            header = {}
            #header['name'] = info['name']
            header['mode'] = info['mode']
            self.socket.send(self.package.pack_header(header))
        elif info['mode'] == 'classArrange':
            header = {}
            header['mode'] = info['mode']
            message = info['message']
            self.socket.send(self.package.pack_message(header, message))
        else:
            pass

    def receive_info(self):
        try:
            header_len_struct = self.socket.recv(4)
            if not len(header_len_struct):
                print('message miss')
                return False, ''
            header_len = self.package.unpack_header_size(header_len_struct)
            header_byte = self.socket.recv(header_len)
            header = self.package.unpack_header(header_byte)
            if header['mode'] == 'getFachschaft':
                message = b''
                message_len = header['message_length']
                current_len = 0
                while current_len < message_len:
                    one_package = self.socket.recv(1024)
                    current_len += len(one_package)
                    message += one_package
                message = self.package.unpack_message(message)
                return header['mode'], message
            elif header['mode'] == 'classArrange':
                message = b''
                message_len = header['message_length']
                current_len = 0
                while current_len < message_len:
                    one_package = self.socket.recv(1024)
                    current_len += len(one_package)
                    message += one_package
                message = self.package.unpack_message(message)
                return header['mode'], message
            else:
                return False, ''
        except Exception as e:
            print(f'mystery error : {str(e)}')
            return False, ''
