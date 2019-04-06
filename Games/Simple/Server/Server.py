from Base.Server import *
import Conf.Server_Simple_Conf as Conf
import random


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


class SimpleAgent(Agent):
    def __init__(self):
        super().__init__()
        self.last_action = Vector2D(0, 0)
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)
        self.last_action_cycle = 0

    def update_next_pos(self):
        self.next_pos.i = self.pos.i + self.last_action.i
        self.next_pos.j = self.pos.j + self.last_action.j
        logging.debug('pos {} action {} to {}'.format(self.pos, self.last_action, self.next_pos))


class SimpleServer(Server):
    def __init__(self):
        print('Server __init')
        super().__init__()
        self.null_agent = SimpleAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.agent_numbers, 'goal_id': Conf.agent_numbers + 1}
        self.goal_id = Conf.agent_numbers + 1

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

    def print_world(self):
        logging.info('cycle:{}'.format(self.cycle))
        for key in self.agents:
            logging.info('score {} : {}'.format(self.agents[key].name, str(self.agents[key].score)))
        for c in self.world:
            logging.info(str(c))
