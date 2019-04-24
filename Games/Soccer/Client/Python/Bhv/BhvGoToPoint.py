from Base.Math import Vector2D, Line2D
from Games.Soccer.Client.Python.World import Agent
from Games.Soccer.Client.Python.Bhv.Bhv import Bhv


class GoToPoint(Bhv):
    def __init__(self, target, pow=1, min_dist=10):
        super().__init__(target, pow)
        self.min_dist: float = min_dist

    def execute(self, agent: Agent) -> dict:
        r = Vector2D(0,0)
        if agent.pos().dist(self.target) >= self.min_dist:
            r = self.target - agent.pos()
        r = r.scale(self.pow / r.r())
        return self.make_action_dict(r)

    def make_action_dict(self, p: Vector2D) -> dict:
        return {
            "type": "move",
            "pow": p
        }
