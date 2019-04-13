from Base.Server import *
import Conf.Server_Soccer_Conf as Conf
import random


class PlayerAgent(Agent):
    def __init__(self):
        super().__init__()
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)
        self.team_id = 0
        self.max_acc = 0.25
        self.max_vel = 1
        self.decay = 0.1
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)
        self.pow = Vector2D(0, 0)
        self.pow_type = ""  # kick or move
        self.kick_pow = Vector2D(0, 0)

    def update_next(self):
        if self.pow_type == "move":
            if self.pow.r() > 1:
                self.pow.scale(1 / self.pow.r())
            self.acc = max(self.max_acc, self.acc + self.pow.scale(0.25))
        self.vel += max(self.max_vel, self.vel + self.acc - self.vel.scale(self.decay))
        self.next_pos += self.vel


class Ball:
    def __init__(self, i, j):
        self.pos = Vector2D(i, j)
        self.next_pos = Vector2D(0, 0)
        self.vel = Vector2D(0, 0)
        self.max_vel = 3
        self.decay = 0.94

    def update_next(self):
        self.vel.scale(0.94)
        self.next_pos = self.pos + self.vel

    def kicked(self, pow: Vector2D):
        self.vel = pow
        self.vel.scale(self.max_vel / self.vel.r)


def action_to_dic(string_action):
    return 


class SoccerServer(Server):
    def __init__(self):
        super().__init__()
        self.null_agent = PlayerAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.team_number}
        self.world = {'players': {}, 'ball': None}

    def update(self):
        for key in self.agents:
            self.agents[key].update_next()
            self.check_player_pos(self.agents[key])
            self.agents[key].pos = self.agents[key].next_pos
            if self.agents[key].pow_type == "kick":
                if self.agents[key].pos.dist(self.world['ball'].pos) > 0.5:
                    continue
                self.world['ball'].kicked(self.agents[key].pow)
        self.world['ball'].update_next()
        self.check_ball_pos()

    def make_world(self):
        self.world['ball'] = Ball(Conf.max_i / 2, Conf.max_j / 2)

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
        action = action_to_dic(message.string_action)

    def check_player_pos(self, agent):
        if agent.next_pos.i < 0 or agent.next_pos.i > self.dict_conf['max_i']:
            agent.next_pos.i = agent.pos.i
            agent.vel = Vector2D(0, agent.vel.j)
            agent.acc = Vector2D(0, agent.acc.j)
        if agent.next_pos.j < 0 or agent.next_pos.j > self.dict_conf['max_j']:
            agent.next_pos.j = agent.pos.j
            agent.vel = Vector2D(agent.vel.i, 0)
            agent.acc = Vector2D(agent.acc.i, 0)

    def check_ball_pos(self):
        if self.world['ball'].next_pos.i < 0:
            self.world['ball'].next_pos.i *= -1
            self.world['ball'].vel.i *= -1
            self.world['ball'].acc.i *= -1
        if self.world['ball'].next_pos.i > Conf.max_i:
            diff = self.world['ball'].next_pos.i - Conf.max_i
            self.world['ball'].next_pos.i = Conf.max_i - diff
            self.world['ball'].vel.i *= -1
            self.world['ball'].acc.i *= -1
        if self.world['ball'].next_pos.j < 0:
            self.world['ball'].next_pos.j *= -1
            self.world['ball'].vel.j *= -1
            self.world['ball'].acc.j *= -1
        if self.world['ball'].next_pos.j > Conf.max_j:
            diff = self.world['ball'].next_pos.j - Conf.max_j
            self.world['ball'].next_pos.j = Conf.max_j - diff
            self.world['ball'].vel.j *= -1
            self.world['ball'].acc.j *= -1
