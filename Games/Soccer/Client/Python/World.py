# from Games.Soccer.Server.Server import PlayerAgent, Ball
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
        pass


class Ball(Object):
    def __init__(self):
        super().__init__()

    def set_data(self, data: dict):
        self.M_pos = data['pos']
        self.M_vel = data['vel']
        self.M_decay = data['decay']


class World:
    def __init__(self, msg):
        self.ball: Ball = Ball()

    def set_id(self, self_id, goal_id):
        self.self_id = self_id
        self.goal_id = goal_id
