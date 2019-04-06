from Base.Server import *
import Conf.Server_Snake_Conf as Conf
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
        self.head = Vector2D(0, 0)
        self.next_head = Vector2D(0, 0)
        self.last_action_cycle = 0
        self.body = []
        self.goal_pos = None

    def update_next(self):
        logging.debug('id {} pos {} action {} to {}'.format(self.id, self.head, self.last_action, self.next_head))
        self.next_head.i = self.head.i + self.last_action.i
        self.next_head.j = self.head.j + self.last_action.j
        logging.debug('id {} pos {} action {} to {}'.format(self.id, self.head, self.last_action, self.next_head))

    def reset(self, board):
        for pos in self.body:
            board[pos.i][pos.j] = 0
        self.body.clear()
        if self.id == 1:
            self.head = Vector2D(1, 3)
            self.body.append(copy.deepcopy(self.head))
            self.body.append(Vector2D(1, 2))
            self.body.append(Vector2D(1, 1))
        elif self.id == 2:
            self.head = Vector2D(1, Conf.max_j - 4)
            self.body.append(copy.deepcopy(self.head))
            self.body.append(Vector2D(1, Conf.max_j - 3))
            self.body.append(Vector2D(1, Conf.max_j - 2))
        elif self.id == 3:
            self.head = Vector2D(Conf.max_i - 2, 3)
            self.body.append(copy.deepcopy(self.head))
            self.body.append(Vector2D(Conf.max_i - 2, 2))
            self.body.append(Vector2D(Conf.max_i - 2, 1))
        elif self.id == 4:
            self.head = Vector2D(Conf.max_i - 2, Conf.max_j - 4)
            self.body.append(copy.deepcopy(self.head))
            self.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 3))
            self.body.append(Vector2D(Conf.max_i - 2, Conf.max_j - 2))
        for p in self.body:
            board[p.i][p.j] = self.id

    def update_world(self, world):
        pass


class SnakeServer(Server):
    def __init__(self):
        print('Server __init')
        super().__init__()
        self.null_agent = SnakeAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.agent_numbers, 'goal_id': Conf.agent_numbers + 1}
        self.world = {'board': None, 'heads': {}}
        self.goal_id = 5

    def update(self):
        logging.debug('Update Worlddddd')
        for key in self.agents:
            self.agents[key].update_next()
            self.agents[key].next_head = self.normalize_pos(self.agents[key].next_head)
            logging.error('wall size:{}'.format(len(self.walls)))
            if self.agents[key].next_head in self.walls:
                logging.error('agent {} in wall body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                self.agents[key].reset(self.world['board'])
                logging.error(
                    'agent {} in wall body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                self.agents[key].score -= 5
            elif self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] == self.goal_id:
                logging.error('goad id: {}'.format(self.goal_id))
                logging.error(
                    'agent {} in goal body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))

                self.agents[key].head = copy.deepcopy(self.agents[key].next_head)
                self.agents[key].body.insert(0, copy.deepcopy(self.agents[key].next_head))
                self.agents[key].score += 1
                self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] = self.agents[key].id
                self.reset_game()
            else:
                logging.error('elseeeeeeee')
                snake_accident = False
                for s in self.agents:
                    if self.agents[key].next_head in self.agents[s].body:
                        snake_accident = True
                        break
                logging.error('afterrrrrrrr forrrrrr')
                if snake_accident:
                    logging.error('agent {} in other'.format(self.agents[key].id))
                    self.agents[key].reset(self.world['board'])
                    self.agents[key].score -= 5
                else:
                    logging.error('agent {} go body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                    end_body = self.agents[key].body[-1]
                    logging.error('agent {} end is {}'.format(self.agents[key].id, end_body))
                    self.world['board'][end_body.i][end_body.j] = 0
                    self.agents[key].body.insert(0, copy.deepcopy(self.agents[key].next_head))
                    del self.agents[key].body[-1]
                    self.agents[key].head = copy.deepcopy(self.agents[key].next_head)
                    logging.error('agent {} next head is {}'.format(self.agents[key].id, self.agents[key].next_head))
                    self.world['board'][self.agents[key].next_head.i][self.agents[key].next_head.j] = self.agents[key].id
                    logging.error('agent {} go body {}'.format(self.agents[key].id, [str(x) for x in self.agents[key].body]))
                    self.print_world()

        self.world['heads'].clear()
        for key in self.agents:
            self.world['heads'][self.agents[key].id] = (self.agents[key].head.i, self.agents[key].head.j)
        self.cycle += 1
        if self.cycle %50 == 0:
            self.reset_game()
        self.save_rcg_cycle()

    def make_world(self):
        logging.info('make new world')
        self.world['board'] = [[0 for x in range(Conf.max_j)] for y in range(Conf.max_i)]
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
        for i in range(Conf.max_i):
            self.walls.append(Vector2D(i, 0))
            self.walls.append(Vector2D(i, Conf.max_j - 1))
        for j in range(Conf.max_j):
            self.walls.append(Vector2D(0, j))
            self.walls.append(Vector2D(Conf.max_i - 1, j))

        for w in self.walls:
            self.world['board'][w.i][w.j] = -1

        for key in self.agents:
            self.agents[key].reset(self.world['board'])

        self.reset_game()


        self.world['heads'].clear()
        for key in self.agents:
            self.world['heads'][self.agents[key].id] = (self.agents[key].head.i, self.agents[key].head.j)
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

    def reset_game(self):
        try:
            self.world['board'][self.goal_pos.j][self.goal_pos.i] = 0
        except:
            print()
        temp_positions = [Vector2D(x, y) for x in range(Conf.max_j) for y in range(Conf.max_i)]
        print(temp_positions)
        random.shuffle(temp_positions)
        random.shuffle(temp_positions)
        for pos in temp_positions:
            if pos in self.walls:
                continue
            in_snakes = False
            for k in self.agents:
                if pos in self.agents[k].body:
                    in_snakes = True
                    break
            if in_snakes:
                continue
            self.goal_pos = pos
            self.world['board'][pos.j][pos.i] = self.goal_id
            break

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
        for c in self.world['board']:
            logging.info(str(c))
