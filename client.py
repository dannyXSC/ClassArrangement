import socket


class Client():
    def __init__(self):
        self.sleepTime = 0.1
        self.serverIp = "127.0.0.1"
        # self.serverIp="192.168.1.122"
        self.serverPort = 8888

    def link(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.serverIp, self.serverPort))
        self.socket.setblocking(False)

    def send_info(self, info):
        head = {}
        name = info['name']
        mode = info['mode']
        if mode == 'get_Fachschaft':

    def receive_info(self, mode):
        pass
