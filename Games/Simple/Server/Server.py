import Server.IServer
import time
import socket
import threading
import queue
import logging


# {"message_type":"connect", "value":{"name":"value"}
# {"message_type":"action", "value":{"name":"value"}


def listener(is_run, socket, msg_size, action_queue):
    logging.info('Port Listener Started')
    while is_run:
        msg = socket.recvfrom(msg_size)
        action_queue.put(msg)
        time.sleep(0.01)


class Agent:
    def __init__(self):
        self.number = 0
        self.name = ''
        self.point = 0
        self.last_action = ''
        self.address = ''


class Server:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self.game_name = 'Simple'
        self.agent_number = 2
        self.agents = {}
        self.world = ''
        self.max_cycle = 100
        self.cycle = 1
        self.is_run = True
        self.ip = "127.0.0.1"
        self.port = 20002
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.action_queue = queue.Queue(0)
        self.msg_size = 1024
        self.listener = threading.Thread(target=listener, args=(self.is_run, self.socket, self.msg_size, self.action_queue,))
        self.listener.start()

    def connect(self):
        logging.info('Wait for agents')
        for i in range(100):
            try:
                msg_address = self.action_queue.get(block=True, timeout=1)
                message = eval(str(msg_address[0].decode("utf-8")))
                address = msg_address[1]
            except:
                logging.debug('Did not Receive msg')
                continue
            if message['message_type'] is not 'connect':
                logging.error('message_type is not connect')
                continue
            if address not in self.agents:
                agent = Agent()
                agent.name = message['value']['name']
                agent.address = address
                self.agents[address] = agent
                action_resp = str.encode('connected')
                self.socket.sendto(action_resp, address)
                logging.info('agent {} connected on port number {}'.format(agent.name, agent.address))
            if len(self.agents) == self.agent_number:
                break
            time.sleep(1)
        logging.info('{} agents connected'.format(len(self.agents)))

    def run(self):
        logging.info('Game Started')
        for s in range(self.max_cycle):
            for agent in self.agents:
                msg = self.world_to_string()
                self.socket.sendto(msg, agent)

            while self.action_queue.qsize() > 0:
                try:
                    msg = self.action_queue.get(block=True)
                except:
                    continue
                self.action_parse(msg)

            self.update()
            self.send_world()
            time.sleep(1)

    def action_parse(self, msg):
        action = msg[0]
        address = msg[1]
        if not action.startswith('action'):
            return False
        if address not in self.agents:
            return False
        self.agents[address].last_action = action
        return True

    def world_to_string(self):
        return ''.encode()

    def update(self):
        pass

    def send_world(self):
        pass
