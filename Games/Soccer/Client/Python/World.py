from Base.Math import Vector2D, Line2D
from copy import copy


class Object:
    def __init__(self):
        self.M_pos: Vector2D = None
        self.M_vel: Vector2D = None
        self.M_decay: float = None

    def pos(self) -> Vector2D:
        return self.M_pos

    def vel(self) -> Vector2D:
        return self.M_vel

    def decay(self) -> float:
        return self.M_decay

    def predict_pos(self, cycle: int):
        obj_pos: Vector2D = copy(self.pos)
        obj_vel: Vector2D = copy(self.vel)

        while cycle > 0:
            obj_pos += obj_vel
            obj_vel *= self.decay()
            cycle -= 1

        return obj_pos

    def set_data(self, data: dict):
        self.M_pos = data['pos']
        self.M_vel = data['vel']
        self.M_decay = data['decay']
        self.more_data(data)

    def more_data(self, data: dict):
        pass


class Ball(Object):
    def __init__(self):
        super().__init__()


class Agent(Object):
    def __init__(self):
        super().__init__()
        self.team_id: int = None
        self.kickable_r

    def more_data(self, data: dict):
        self.team_id = data['team_id']
        self.kickable_r = data['kickable_r']


class World:
    def __init__(self):
        self.M_ball: Ball = None
        self.M_agents: list = []
        self.M_cycle: int = 0
        self.self_id: int = 0

    def set_id(self, self_id):
        self.self_id = self_id

    def set_id2(self, agents):
        i = 0
        for _, agent in agents.item():
            if agent['id'] == self.self_id:
                self.self_id = i
                break
            i += 1

    def update(self, msg):
        self.M_cycle = msg.cycle

        agents_dict = msg.world['players']
        for key in agents_dict:
            agent = Agent()
            agent.set_data(agents_dict[key])
        self.set_id2(agents_dict)

        self.M_ball = Ball()
        self.M_ball.set_data(msg.world['ball'])

    def self(self) -> Agent:
        return self.M_agents[self.self_id]

    def our_players(self) -> list:
        return [agent for agent in self.M_agents if agent.team_id == self.self().team_id]

    def their_players(self) -> list:
        return [agent for agent in self.M_agents if agent.team_id != self.self().team_id]

    def ball(self):
        return self.M_ball
