import Server.IServer
import time
import socket
import threading
import queue
import logging
import random
import Games.Simple.Server.Conf as Conf
from Games.Simple.Server.Message import *
from Games.Simple.Server.Math import *


is_run = True


def listener(socket, msg_size, action_queue):
    global is_run
    logging.info('Port Listener Started')
    while is_run:
        try:
            msg = socket.recvfrom(msg_size)
            action_queue.put(msg)
        except:
            continue


def monitor_listener(socket, msg_size, action_queue):
    global is_run
    logging.info('Port Listener Started')
    while is_run:
        try:
            msg = socket.recvfrom(msg_size)
            action_queue.put(msg)
        except:
            continue


class Agent:
    def __init__(self):
        self.number = 0
        self.name = ''
        self.score = 0
        self.last_action = Vector2D(0, 0)
        self.address = ''
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)

    def update_next_pos(self):
        self.next_pos.i = self.pos.i + self.last_action.i
        self.next_pos.j = self.pos.j + self.last_action.j
        logging.debug('pos {} action {} to {}'.format(self.pos, self.last_action, self.next_pos))


class Server:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
        self.game_name = Conf.game_name
        self.agent_numbers = Conf.agent_numbers
        self.agents = {}
        self.monitors = []
        self.world = []
        self.max_i = Conf.max_i
        self.max_j = Conf.max_j
        self.goal_number = self.agent_numbers + 1
        self.max_cycle = Conf.max_cycle
        self.think_time = Conf.think_time
        self.cycle = 1
        self.ip = Conf.ip
        self.player_port = Conf.player_port
        self.monitor_port = Conf.monitor_port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.settimeout(1)
        self.socket.bind((self.ip, self.player_port))
        self.monitor_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.monitor_socket.settimeout(1)
        self.monitor_socket.bind((self.ip, self.monitor_port))
        self.action_queue = queue.Queue(0)
        self.monitor_queue = queue.Queue(0)
        self.msg_size = 1024
        self.listener = threading.Thread(target=listener,
                                         args=(self.socket, self.msg_size, self.action_queue,))
        self.listener.start()
        self.monitor_listener = threading.Thread(target=monitor_listener,
                                                 args=(self.monitor_socket, self.msg_size, self.monitor_queue,))
        self.monitor_listener.start()

    def make_world(self):
        logging.info('make new world')
        self.world = [[0 for x in range(self.max_j)] for x in range(self.max_i)]
        positions = [(i, j) for i in range(self.max_i) for j in range(self.max_j)]
        random.shuffle(positions)
        a = 0
        self.world[positions[a][0]][positions[a][1]] = self.goal_number
        a += 1
        for key in self.agents:
            self.world[positions[a][0]][positions[a][1]] = a
            self.agents[key].pos = Vector2D(positions[a][0], positions[a][1])
            a += 1

    def connect(self):
        logging.info('Wait for Agents')
        for i in range(100):
            self.check_monitor_connected()
            try:
                msg_address = self.action_queue.get(block=True, timeout=1)
                message = parse(msg_address[0])
                address = msg_address[1]
            except Exception as c:
                logging.debug('Did not Receive msg:{}'.format(c))
                continue

            if not message.type == 'ClientConnectRequest':
                logging.error('message_type is not connect')
                continue

            if address not in self.agents:
                self.agents[address] = Agent()
                self.agents[address].name = message.client_name
                self.agents[address].address = address
                self.agents[address].number = len(self.agents)
                action_resp = MessageClientConnectResponse(self.agents[address].number).build()
                self.socket.sendto(action_resp, address)
                logging.info('agent {} connected on port number {}'
                             .format(self.agents[address].name, self.agents[address].address))
            else:
                logging.error('Client {} Want to Reconnect'.format(address))
            if len(self.agents) == self.agent_numbers:
                break
            time.sleep(1)
        logging.info('{} agents connected'.format(len(self.agents)))

    def run(self):
        global is_run
        logging.info('Game Started')
        self.make_world()
        self.print_world()
        for s in range(self.max_cycle):
            self.check_monitor_connected()
            self.send_world()
            self.send_visual_to_monitors()
            start_time = time.time()
            while time.time() - start_time < self.think_time:
                try:
                    msg = self.action_queue.get(block=True, timeout=0.001)
                    logging.debug('Receive {}'.format(msg))
                except:
                    continue
                self.action_parse(msg)
            while self.action_queue.qsize() > 0:
                self.action_queue.get()
            logging.debug('Receive Action Finished')
            self.update()

            self.print_world()
        self.send_disconnected()
        is_run = False

    def check_monitor_connected(self):
        if self.monitor_queue.qsize() > 0:
            try:
                msg_address = self.monitor_queue.get(block=True, timeout=0.001)
                message = parse(msg_address[0])
                if message.type == 'MessageMonitorConnectRequest':
                    self.monitors.append(msg_address[1])
                    self.socket.sendto(MessageMonitorConnectResponse().build(), msg_address[1])
            except:
                return

    def send_visual_to_monitors(self):
        score = dict([(self.agents[key].name, self.agents[key].score) for key in self.agents])
        message = MessageClientWorld(self.cycle, self.world, score).build()
        for key in self.monitors:
            self.socket.sendto(message, key)

    def action_parse(self, msg):
        message = parse(msg[0])
        address = msg[1]
        if message.type is not 'MessageClientAction':
            logging.error('message type is not action, client: {}'
                          .format(self.agents.get(address, Agent()).name))
            return False
        if address not in self.agents:
            logging.error('message from invalid address, address: {}'.format(address))
            return False
        action = message.vector_action
        if action is None:
            action = self.agents[address].last_action
        self.agents[address].last_action = action
        return True

    def normalize_pos(self, pos):
        if pos.i >= self.max_i:
            pos.i = self.max_i - 1
        if pos.i < 0:
            pos.i = 0
        if pos.j >= self.max_j:
            pos.j = self.max_j - 1
        if pos.j < 0:
            pos.j = 0
        return pos

    def update(self):
        logging.debug('Update World')
        for key in self.agents:
            self.world[self.agents[key].pos.i][self.agents[key].pos.j] = 0
            self.agents[key].update_next_pos()
            self.agents[key].next_pos = self.normalize_pos(self.agents[key].next_pos)
            logging.debug('agent {} : {} to {}'
                          .format(self.agents[key].number, self.agents[key].pos, self.agents[key].next_pos))

            if self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] == self.goal_number:
                self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = 0
                seted_goal = False
                while not seted_goal:
                    rand_position = Vector2D(random.randint(0, self.max_i - 1), random.randint(0, self.max_j - 1))
                    is_near = False
                    for k in self.agents:
                        if self.agents[k].pos.is_near(rand_position):
                            is_near = True
                    if not is_near:
                        seted_goal = True
                self.world[rand_position.i][rand_position.j] = self.goal_number
                self.agents[key].score += 1
            else:
                self.world[self.agents[key].pos.i][self.agents[key].pos.j] = 0
            self.agents[key].pos = self.agents[key].next_pos
            self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = self.agents[key].number
        self.cycle += 1

    def send_world(self):
        score = dict([(self.agents[key].name, self.agents[key].score) for key in self.agents])
        message = MessageClientWorld(self.cycle, self.world, score).build()
        for key in self.agents:
            self.socket.sendto(message, key)

    def send_disconnected(self):
        message = MessageClientDisconnect().build()
        for key in self.agents:
            self.socket.sendto(message, key)
        for key in self.monitors:
            self.socket.sendto(message, key)

    def print_world(self):
        logging.info('cycle:{}'.format(self.cycle))
        for key in self.agents:
            logging.info('score {} : {}'.format(self.agents[key].name, str(self.agents[key].score)))
        for c in self.world:
            logging.info(str(c))
