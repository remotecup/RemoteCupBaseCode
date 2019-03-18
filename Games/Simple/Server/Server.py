import Server.IServer
import time
import socket


class Client:
    def __init__(self):
        self.number = 0
        self.name = ''
        self.point = 0
        self.last_action = ''
        self.address = ''

class Server(Server):
    def __init__(self):
        self.game_name = 'Simple'
        self.client_number = 2
        self.clients = {}
        self.world = ''
        self.max_step = 100
        self.ip = "127.0.0.1"
        self.port = "20002"
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.msg_size = 1024
        self.connect()
        self.run_game()

    def connect(self):
        for i in range(100):
            msg = self.socket.recvfrom(self.msg_size)
            action = msg[0]
            address = msg[1]
            if action.startswith('connect'):
                action = action.split(',')
                client = Client()
                client.name = action[1]
                client.address = address
                self.clients[address] = client
                print('client {} connected'.format(client.name))
            if len(self.clients) == self.client_number:
                break
            time.sleep(1)

    def run_game(self):
        for s in range(self.max_step):
            for c in range(len(self.clients)):
                msg = self.socket.recvfrom(self.msg_size)
                action = msg[0]
                address = msg[1]
                if not self.parse(msg):
                    c -= 1
            self.update()
            self.send_world()

    def parse(self, msg):
        action = msg[0]
        address = msg[1]
        if not action.startswith('action'):
            return False
        if address not in self.clients:
            return False
        self.clients[address].last_action = action
        return True

    def update(self):
        pass

    def send_world(self):
        pass
