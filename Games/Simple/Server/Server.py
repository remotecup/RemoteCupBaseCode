import Server.IServer
import time
import socket


class Agent:
    def __init__(self):
        self.number = 0
        self.name = ''
        self.point = 0
        self.last_action = ''
        self.address = ''


class Server(Server):
    def __init__(self):
        self.game_name = 'Simple'
        self.agent_number = 2
        self.agents = {}
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
                agent = Agent()
                agent.name = action[1]
                agent.address = address
                self.agents[address] = agent
                print('agent {} connected'.format(agent.name))
            if len(self.agents) == self.agent_number:
                break
            time.sleep(1)

    def run_game(self):
        for s in range(self.max_step):
            for c in range(len(self.agents)):
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
        if address not in self.agents:
            return False
        self.agents[address].last_action = action
        return True

    def update(self):
        pass

    def send_world(self):
        pass
