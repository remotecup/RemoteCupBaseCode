from Base.Math import Vector2D, Line2D
from Games.Soccer.Client.Python.World import Agent


class Bhv:
    def __init__(self, target: Vector2D, pow: float):
        self.target: Vector2D = target
        self.pow: float = min(pow, 1)
        self.action = {
            'type': None,
            'pow': 0
        }

    def execute(self, agent: Agent):
        pass

    def make_action_dict(self, p: Vector2D):
        pass
