import Server.IServer
import time
import socket
import threading
import queue
import logging
import random


# {"message_type":"connect", "value":{"name":"value"}
# {"message_type":"action", "value":{"name":"value"}


def listener(is_run, socket, msg_size, action_queue):
    logging.info('Port Listener Started')
    while is_run:
        msg = socket.recvfrom(msg_size)
        action_queue.put(msg)
        time.sleep(0.01)


class Vector2D:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return '(' + str(self.i) + ',' + str(self.j) + ')'


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
        self.game_name = 'Simple'
        self.agent_number = 2
        self.agents = {}
        self.world = []
        self.max_i = 5
        self.max_j = 8
        self.make_world()
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

    def make_world(self):
        logging.info('make new world')
        self.world = [[0 for x in range(self.max_j)] for x in range(self.max_i)]
        self.world[0][0] = 1  # agent 1
        self.world[3][2] = 2  # agent 2
        for agent in self.agents:
            if self.agents[agent].number == 1:
                self.agents[agent].pos = Vector2D(0, 0)
            elif self.agents[agent].number == 2:
                self.agents[agent].pos = Vector2D(3, 2)
        self.world[2][2] = 3  # goal

    def connect(self):
        logging.info('Wait for Agents')
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
                self.agents[address] = Agent()
                self.agents[address].name = message['value']['name']
                self.agents[address].address = address
                self.agents[address].number = len(self.agents)
                action_resp = str.encode('{"message_type":"connected"}')
                self.socket.sendto(action_resp, address)
                logging.info('agent {} connected on port number {}'
                             .format(self.agents[address].name, self.agents[address].address))
            else:
                logging.error('Client {} Want to Reconnect'.format(address))
            if len(self.agents) == self.agent_number:
                break
            time.sleep(1)
        logging.info('{} agents connected'.format(len(self.agents)))

    def run(self):
        logging.info('Game Started')
        self.make_world()
        self.print_world()
        for s in range(self.max_cycle):
            self.send_world()
            start_time = time.time()
            while time.time() - start_time < 5:
                try:
                    msg = self.action_queue.get(block=True, timeout=0.001)
                    logging.debug('Receive {}'.format(msg))
                except:
                    continue
                self.action_parse(msg)
            while self.action_queue.qsize() > 0:
                msg = self.action_queue.get()
            logging.debug('Receive Action Finished')
            self.update()

            self.print_world()
            time.sleep(1)

    def action_parse(self, msg):
        action = eval(str(msg[0].decode("utf-8")))
        address = msg[1]
        if action['message_type'] is not 'action':
            logging.error('message type is not action, client: {}'
                          .format(self.agents.get(address, Agent()).name))
            return False
        if address not in self.agents:
            logging.error('message from invalid address, address: {}'.format(address))
            return False
        action = action['value']['name']
        if action is 'u':
            action = Vector2D(-1, 0)
        elif action is 'd':
            action = Vector2D(1, 0)
        elif action is 'l':
            action = Vector2D(0, -1)
        elif action is 'r':
            action = Vector2D(0, 1)
        else:
            action = self.agents[address].last_action
        self.agents[address].last_action = action
        return True

    def world_to_string(self):
        world_string = [str(v) for t in self.world for v in t]
        world_string = ','.join(world_string)
        return world_string

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

            if self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] == 3:
                self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = 0
                self.world[random.randint(0, self.max_i - 1)][random.randint(0, self.max_j - 1)] = 3
                self.agents[key].score += 1
            else:
                self.world[self.agents[key].pos.i][self.agents[key].pos.j] = 0
            self.agents[key].pos = self.agents[key].next_pos
            self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = self.agents[key].number
        self.cycle += 1

    def send_world(self):
        world_string = self.world_to_string()
        for key in self.agents:
            self.socket.sendto(str.encode(world_string), key)

    def print_world(self):
        logging.info('cycle:{}'.format(self.cycle))
        for key in self.agents:
            logging.info('score {} : {}'.format(self.agents[key].name, str(self.agents[key].score)))
        for c in self.world:
            logging.info(str(c))
