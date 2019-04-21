from Base.Server import *
import Conf.Server_Soccer_Conf as Conf
import random
import json


class PlayerAgent(Agent):
    def __init__(self):
        super().__init__()
        self.pos = Vector2D(0, 0)
        self.next_pos = Vector2D(0, 0)
        self.team_id = 0
        self.max_acc = Conf.player_max_acc
        self.max_vel = Conf.player_max_vel
        self.decay = Conf.player_decay
        self.vel = Vector2D(0, 0)
        self.acc = Vector2D(0, 0)
        self.pow = Vector2D(0, 0)
        self.pow_type = ""  # kick or move
        self.last_action_cycle = 0
        self.kick_pow = Vector2D(0, 0)

    def update_next(self):
        if self.pow_type == "move":
            if self.pow.r() > 1:
                self.pow = self.pow.scale(1 / self.pow.r())
            self.acc = max_r(self.max_acc, self.acc + self.pow.scale(0.25))
        self.vel = max_r(self.max_vel, self.vel + self.acc - self.vel.scale(self.decay))
        self.next_pos += self.vel


def max_r(r, p: Vector2D):
    if p.r() <= r:
        return p
    return p.scale(r / p.r())


class Ball:
    def __init__(self, i, j):
        self.pos = Vector2D(i, j)
        self.next_pos = Vector2D(0, 0)
        self.vel = Vector2D(0, 0)
        self.max_vel = Conf.ball_max_vel
        self.decay = Conf.ball_decay

    def update_next(self):
        self.vel = self.vel.scale(self.decay)
        self.next_pos = self.pos + self.vel

    def kicked(self, pow: Vector2D):
        if pow.r() > 1:
            pow = pow.scale(1 / pow.r())
        self.vel = pow.scale(self.max_vel / pow.r())


def action_to_dic(string_action):
    return string_action


class SoccerServer(Server):
    def __init__(self):
        super().__init__()
        self.null_agent = PlayerAgent()
        self.dict_conf = {'max_i': Conf.max_i, 'max_j': Conf.max_j,
                          'team_number': Conf.team_number}
        self.ball = None
        self.world = {'players': {}, 'ball': None}

    def update(self):

        for key in self.agents:
            self.agents[key].update_next()
            self.check_player_pos(self.agents[key])
            self.agents[key].pos = self.agents[key].next_pos
            if self.agents[key].pow_type == "kick":
                if self.agents[key].pos.dist(self.ball.pos) > Conf.kick_able_r:
                    continue
                self.ball.kicked(self.agents[key].pow)
        self.ball.update_next()
        if self.check_goal():
            self.make_world()
        self.check_ball_pos()
        self.ball.pos = self.ball.next_pos
        self.update_world()

    def check_goal(self):
        ball_line = Line2D(self.ball.pos, self.ball.next_pos)
        point = ball_line.x(0)
        if Conf.max_j / 2 - Conf.goal_height / 2 < point.j < Conf.max_j / 2 + Conf.goal_height / 2:
            if self.ball.next_pos.i < 0:
                for key in self.agents:
                    if self.agents[key].team_id == 1:
                        self.agents[key].score += 1
                return True
        point = ball_line.x(Conf.max_i)
        if Conf.max_j / 2 - Conf.goal_height / 2 < point.j < Conf.max_j / 2 + Conf.goal_height / 2:
            if self.ball.next_pos.i > Conf.max_i:
                for key in self.agents:
                    if self.agents[key].team_id == 2:
                        self.agents[key].score += 1
                return True

        return False

    def update_world(self):
        self.world = {'players': {}, 'ball': None}
        for key in self.agents:
            self.world['players'][key] = self.agents[key].__dict__
        self.world['ball'] = self.ball.__dict__

    def make_world(self):
        self.ball = Ball(Conf.max_i / 2, Conf.max_j / 2)
        i = 1
        changed = False
        id = 1
        for key in self.agents:
            if i > len(self.agents) / 2 and not changed:
                id += 1
                changed = True
            self.agents[key].team_id = id
            i += 1
        left_team_pos = Vector2D(Conf.max_i / 4, Conf.max_j / Conf.agent_numbers)
        right_team_pos = Vector2D(Conf.max_i * 3 / 4, Conf.max_j / Conf.agent_numbers)
        for key in self.agents:
            if self.agents[key].team_id == 1:
                self.agents[key].pos = left_team_pos
                self.agents[key].next_pos = left_team_pos
                left_team_pos += Vector2D(0, Conf.max_j / Conf.agent_numbers * 2)
            elif self.agents[key].team_id == 2:
                self.agents[key].pos = right_team_pos
                self.agents[key].next_pos = right_team_pos
                right_team_pos += Vector2D(0, Conf.max_j / Conf.agent_numbers * 2)
        for key in self.agents:
            self.ball.pos = self.agents[key].pos
            self.ball.next_pos = self.agents[key].pos
            break
        self.update_world()

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
        self.agents[address].pow_type = action['type']
        self.agents[address].pow = Vector2D(action['pow'][0], action['pow'][1])
        if action is None:
            action = {
                'type': self.agents[address].pow_type,
                'pow': self.agents[address].pow
            }
        if self.agents[address].last_action_cycle < self.cycle:
            self.agents[address].last_action_cycle = self.cycle
            self.receive_action += 1
        return True

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
        if self.ball.next_pos.i < 0:
            self.ball.next_pos.i *= -1
            self.ball.vel.i *= -1
            # self.ball.acc.i *= -1
        if self.ball.next_pos.i > Conf.max_i:
            diff = self.ball.next_pos.i - Conf.max_i
            self.ball.next_pos.i = Conf.max_i - diff
            self.ball.vel.i *= -1
            # self.ball.acc.i *= -1
        if self.ball.next_pos.j < 0:
            self.ball.next_pos.j *= -1
            self.ball.vel.j *= -1
            # self.ball.acc.j *= -1
        if self.ball.next_pos.j > Conf.max_j:
            diff = self.ball.next_pos.j - Conf.max_j
            self.ball.next_pos.j = Conf.max_j - diff
            self.ball.vel.j *= -1
            # self.ball.acc.j *= -1
