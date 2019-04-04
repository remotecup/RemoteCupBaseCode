from Base.Server import *
import Games.Snake.Server.Conf as Conf
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


class SnakeAgent(Agent):
    def __init__(self):
        super().__init__()
        self.last_action = Vector2D(0, 0)
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)
        self.last_action_cycle = 0
        self.body = []

    def update_next_pos(self):
        self.next_pos.i = self.pos.i + self.last_action.i
        self.next_pos.j = self.pos.j + self.last_action.j
        logging.debug('pos {} action {} to {}'.format(self.pos, self.last_action, self.next_pos))


class SnakeServer(Server):
    def __init__(self):
        print('Server __init')
        super().__init__()
        self.null_agent = SnakeAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.agent_numbers, 'goal_id': Conf.agent_numbers + 1}
        self.goal_id = 5

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
        self.world = [[0 for x in range(Conf.max_j)] for y in range(Conf.max_i)]
        self.walls = []
        temp_positions = [Vector2D(x, y) for x in range(Conf.max_j) for y in range(Conf.max_i)]
        random.shuffle(temp_positions)
        random.shuffle(temp_positions)
        ok_wall_6_number = 0
        ok_wall_3_number = 0
        ok_wall_2_number = 0
        pos = 0
        while ok_wall_6_number < Conf.wall_6_number:
            setted = False
            temp_position = temp_positions[pos]
            if temp_position.i < Conf.max_i - 2 and temp_position.j < Conf.max_j - 3:
                if (not (temp_position.i <= 1 and temp_position.j <= 3)) and \
                        (not (temp_position.i >= Conf.max_i - 2 and temp_position.j <= 3)) and \
                        (not (temp_position.i <= 1 and temp_position.j >= Conf.max_j - 6)) and \
                        (not (temp_position.i >= Conf.max_i - 2 and temp_position.j >= Conf.max_j - 6)):
                    is_ok = True
                    for i in range(temp_position.i, temp_position.i + 2):
                        for j in range(temp_position.j, temp_position.j + 3):
                            if Vector2D(i, j) in temp_positions:
                                pass
                            else:
                                is_ok = False
                                # break
                    if is_ok:
                        for i in range(temp_position.i, temp_position.i + 2):
                            for j in range(temp_position.j, temp_position.j + 3):
                                self.walls.append(Vector2D(i, j))
                                temp_positions.remove(Vector2D(i, j))
                        setted = True
                        ok_wall_6_number += 1
            if not setted:
                pos += 1
        pos = 0
        while ok_wall_3_number < Conf.wall_3_number:
            setted = False
            temp_position = temp_positions[pos]
            if temp_position.i < Conf.max_i - 1 and temp_position.j < Conf.max_j - 3:
                if not (temp_position.i <= 1 and temp_position.j <= 3) and \
                        not (temp_position.i >= Conf.max_i - 1 and temp_position.j <= 3) and \
                        not (temp_position.i <= 1 and temp_position.j >= Conf.max_j - 6) and \
                        not (temp_position.i >= Conf.max_i - 1 and temp_position.j >= Conf.max_j - 6):
                    is_ok = True
                    for i in range(temp_position.i, temp_position.i + 1):
                        for j in range(temp_position.j, temp_position.j + 3):
                            if Vector2D(i, j) in temp_positions:
                                pass
                            else:
                                is_ok = False
                                # break
                    if is_ok:
                        for i in range(temp_position.i, temp_position.i + 1):
                            for j in range(temp_position.j, temp_position.j + 3):
                                self.walls.append(Vector2D(i, j))
                                temp_positions.remove(Vector2D(i, j))
                        setted = True
                        ok_wall_3_number +=1
            if not setted:
                pos += 1
        while ok_wall_2_number < Conf.wall_2_number:
            setted = False
            temp_position = temp_positions[pos]
            if temp_position.i < Conf.max_i - 1 and temp_position.j < Conf.max_j - 2:
                if not (temp_position.i <= 1 and temp_position.j <= 2) and \
                        not (temp_position.i >= Conf.max_i - 1 and temp_position.j <= 2) and \
                        not (temp_position.i <= 1 and temp_position.j >= Conf.max_j - 5) and \
                        not (temp_position.i >= Conf.max_i - 1 and temp_position.j >= Conf.max_j - 5):
                    is_ok = True
                    for i in range(temp_position.i, temp_position.i + 1):
                        for j in range(temp_position.j, temp_position.j + 2):
                            if Vector2D(i, j) in temp_positions:
                                pass
                            else:
                                is_ok = False
                                # break
                    if is_ok:
                        for i in range(temp_position.i, temp_position.i + 1):
                            for j in range(temp_position.j, temp_position.j + 2):
                                self.walls.append(Vector2D(i, j))
                                temp_positions.remove(Vector2D(i, j))
                        setted = True
                        ok_wall_2_number += 1
            if not setted:
                pos += 1
        for w in self.walls:
            self.world[w.i][w.j] = -1

        for pos in temp_positions:
            if pos.i >= 2 and pos.j >= 4 and \
                pos.i <= Conf.max_i - 3 and pos.j <= Conf.max_j - 5:
                self.goal_pos = pos
                break
        self.world[pos.j][pos.i] = 5
        for key in self.agents:
            agent = self.agents[key]
            if agent.id == 1:
                agent.pos = Vector2D(1, 3)
                agent.body.append(agent.pos)
                agent.body.append(Vector2D(1, 2))
                agent.body.append(Vector2D(1, 1))
            elif agent.id == 2:
                agent.pos = Vector2D(1, Conf.max_j - 4)
                agent.body.append(agent.pos)
                agent.body.append(Vector2D(1, Conf.max_j - 3))
                agent.body.append(Vector2D(1, Conf.max_j - 2))
            elif agent.id == 3:
                agent.pos = Vector2D(Conf.max_i - 2, 3)
                agent.body.append(agent.pos)
                agent.body.append(Vector2D(Conf.max_i - 2, 2))
                agent.body.append(Vector2D(Conf.max_i - 2, 1))
            elif agent.id == 4:
                agent.pos = Vector2D(Conf.max_i - 2, Conf.max_j - 4)
                agent.body.append(agent.pos)
                agent.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 3))
                agent.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 2))
            for p in agent.body:
                self.world[p.i][p.j] = agent.id
        self.print_world()

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
