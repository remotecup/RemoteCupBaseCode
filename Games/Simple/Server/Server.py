import Server.IServer
import time
import socket
import threading
import queue
import logging
import datetime
import random
import Games.Simple.Server.Conf as Conf
from Base.Message import *
from Base.Math import *
from Games.Simple.Server.Logger import *
import signal


is_run = True


def signal_handler(sig, frame):
    global is_run
    print('You pressed Ctrl+C!')
    is_run = False


signal.signal(signal.SIGINT, signal_handler)


log_file_name = datetime.datetime.now().strftime('{}-%Y-%m-%d-%H-%M-%S'.format(Conf.game_name))
rcg_logger = setup_logger('rcg_logger', log_file_name + '.rcg')
rcl_logger = setup_logger('rcl_logger', log_file_name + '.rcl')


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


def action_to_vector(string_action):
    if string_action is 'u':
        action = Vector2D(-1, 0)
    elif string_action is 'd':
        action = Vector2D(1, 0)
    elif string_action is 'l':
        action = Vector2D(0, -1)
    elif string_action is 'r':
        action = Vector2D(0, 1)
    else:
        action = None
    return action


class Agent:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.score = 0
        self.last_action = Vector2D(0, 0)
        self.address = ''
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)
        self.last_action_cycle = 0

    def update_next_pos(self):
        self.next_pos.i = self.pos.i + self.last_action.i
        self.next_pos.j = self.pos.j + self.last_action.j
        logging.debug('pos {} action {} to {}'.format(self.pos, self.last_action, self.next_pos))


class Server:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
        self.game_name = Conf.game_name
        self.agents = {}
        self.monitors = []
        self.world = []
        self.goal_id = Conf.agent_numbers + 1
        self.cycle = 1
        self.player_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.player_socket.settimeout(1)
        self.player_socket.bind((Conf.ip, Conf.player_port))
        self.monitor_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.monitor_socket.settimeout(1)
        self.monitor_socket.bind((Conf.ip, Conf.monitor_port))
        self.action_queue = queue.Queue(0)
        self.monitor_queue = queue.Queue(0)
        self.msg_size = 4096
        self.listener = threading.Thread(target=listener,
                                         args=(self.player_socket, self.msg_size, self.action_queue,))
        self.listener.start()
        self.monitor_listener = threading.Thread(target=monitor_listener,
                                                 args=(self.monitor_socket, self.msg_size, self.monitor_queue,))
        self.monitor_listener.start()
        self.start = False
        self.receive_action = 0

    def connect(self):
        logging.info('Wait for Agents')
        for i in range(100):
            if not is_run:
                return
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

            self.add_agent(address, message)

            if len(self.agents) == Conf.agent_numbers:
                break
            time.sleep(1)

        if Conf.auto_mode:
            self.start = True
        while not self.start:
            self.check_monitor_connected()
            time.sleep(0.1)

        logging.info('{} agents connected'.format(len(self.agents)))

    def disconnect(self):
        self.send_disconnected()

    def run(self):
        global is_run
        if not is_run:
            return
        logging.info('Game Started')
        self.save_rcg_header()
        start_time = time.time()
        self.make_world()
        self.print_world()
        for s in range(Conf.max_cycle):
            if not is_run:
                return
            self.check_monitor_connected()
            self.send_world()
            self.send_visual_to_monitors()
            start_time_cycle = time.time()

            self.receive_action = 0
            while (Conf.sync_mode and self.receive_action < Conf.agent_numbers) \
                    or (not Conf.sync_mode and time.time() - start_time_cycle < Conf.think_time):
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
        end_time = time.time()
        logging.info('run time is {}'.format(end_time - start_time))
        is_run = False

    def update(self):
        logging.debug('Update World')
        for key in self.agents:
            self.world[self.agents[key].pos.i][self.agents[key].pos.j] = 0
            self.agents[key].update_next_pos()
            self.agents[key].next_pos = self.normalize_pos(self.agents[key].next_pos)
            logging.debug('agent {} : {} to {}'
                          .format(self.agents[key].id, self.agents[key].pos, self.agents[key].next_pos))

            if self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] == self.goal_id:
                self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = 0
                seted_goal = False
                while not seted_goal:
                    rand_position = Vector2D(random.randint(0, Conf.max_i - 1), random.randint(0, Conf.max_j - 1))
                    is_near = False
                    for k in self.agents:
                        if self.agents[k].pos.is_near(rand_position):
                            is_near = True
                    if not is_near:
                        seted_goal = True
                self.world[rand_position.i][rand_position.j] = self.goal_id
                self.agents[key].score += 1
            else:
                self.world[self.agents[key].pos.i][self.agents[key].pos.j] = 0
            self.agents[key].pos = self.agents[key].next_pos
            self.world[self.agents[key].next_pos.i][self.agents[key].next_pos.j] = self.agents[key].id
        self.cycle += 1
        self.save_rcg_cycle()

    def make_world(self):
        logging.info('make new world')
        self.world = [[0 for x in range(Conf.max_j)] for x in range(Conf.max_i)]
        positions = [(i, j) for i in range(Conf.max_i) for j in range(Conf.max_j)]
        random.shuffle(positions)
        a = 0
        self.world[positions[a][0]][positions[a][1]] = self.goal_id
        a += 1
        for key in self.agents:
            self.world[positions[a][0]][positions[a][1]] = a
            self.agents[key].pos = Vector2D(positions[a][0], positions[a][1])
            a += 1

    def add_agent(self, address, message):
        if address not in self.agents:
            self.agents[address] = Agent()
            self.agents[address].name = message.client_name
            self.agents[address].address = address
            self.agents[address].id = len(self.agents)
            action_resp = MessageClientConnectResponse(self.agents[address].id, self.goal_id).build()
            self.player_socket.sendto(action_resp, address)
            logging.info('agent {} connected on port number {}'
                         .format(self.agents[address].name, self.agents[address].address))
        else:
            logging.error('Client {} Want to Reconnect'.format(address))

    def check_monitor_connected(self):
        if self.monitor_queue.qsize() > 0:
            try:
                msg_address = self.monitor_queue.get(block=True, timeout=0.001)
                message = parse(msg_address[0])
                if message.type == 'MessageMonitorConnectRequest':
                    if msg_address[1] not in self.monitors:
                        self.monitors.append(msg_address[1])
                    self.player_socket.sendto(MessageMonitorConnectResponse(self.goal_id,
                                                                            {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                                                                             'team_number': Conf.agent_numbers})
                                              .build(), msg_address[1])
                    self.start = True
                elif message.type == 'MessageMonitorDisconnect':
                    if msg_address[1] in self.monitors:
                        self.monitors.remove(msg_address[1])
            except:
                return

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
        action = action_to_vector(message.string_action)
        self.save_rcl(self.agents[address].id, message.string_message, action)
        if action is None:
            action = self.agents[address].last_action
        self.agents[address].last_action = action
        if self.agents[address].last_action_cycle < self.cycle:
            self.agents[address].last_action_cycle = self.cycle
            self.receive_action += 1
        return True

    def normalize_pos(self, pos):
        if pos.i >= Conf.max_i:
            pos.i = Conf.max_i - 1
        if pos.i < 0:
            pos.i = 0
        if pos.j >= Conf.max_j:
            pos.j = Conf.max_j - 1
        if pos.j < 0:
            pos.j = 0
        return pos

    def send_visual_to_monitors(self):
        score = dict([(self.agents[key].name, self.agents[key].score) for key in self.agents])
        message = MessageClientWorld(self.cycle, self.world, score).build()
        for key in self.monitors:
            self.player_socket.sendto(message, key)

    def send_world(self):
        score = dict([(self.agents[key].name, self.agents[key].score) for key in self.agents])
        message = MessageClientWorld(self.cycle, self.world, score).build()
        for key in self.agents:
            self.player_socket.sendto(message, key)

    def send_disconnected(self):
        message = MessageClientDisconnect().build()
        for key in self.agents:
            self.player_socket.sendto(message, key)
        for key in self.monitors:
            self.player_socket.sendto(message, key)

    def save_rcg_header(self):
        if not Conf.rcg_logger:
            return
        teams = []
        for key in self.agents:
            team = {'name': self.agents[key].name, 'id': self.agents[key].id}
            teams.append(team)
        message = MessageRCGHeader(teams, {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                                           'team_number': Conf.agent_numbers}).build()
        rcg_logger.info(message)

    def save_rcg_cycle(self):
        if not Conf.rcg_logger:
            return
        score = dict([(self.agents[key].name, self.agents[key].score) for key in self.agents])
        rcg_logger.info('{}'.format(MessageRCGCycle(self.cycle, self.world, score).build()))

    def save_rcl(self, id, string_message, vector_action):
        if not Conf.rcl_logger:
            return
        rcl_logger.info('cycle:{} id:{} message:{} action:{}'.format(self.cycle, id, string_message, vector_action))

    def print_world(self):
        logging.info('cycle:{}'.format(self.cycle))
        for key in self.agents:
            logging.info('score {} : {}'.format(self.agents[key].name, str(self.agents[key].score)))
        for c in self.world:
            logging.info(str(c))
