from Base.Math import Vector2D
from Games.Soccer.Client.Python.Bhv.Bhv import Bhv
from Games.Soccer.Client.Python.World import Agent


class KickToPoint(Bhv):
    def __init__(self, target: Vector2D, pow: float):
        super().__init__(target, pow)

    def execute(self, agent: Agent):
        r = self.target - agent.pos()
        r = r.scale(self.pow / r.r())
        return self.make_action_dict(r)

    def make_action_dict(self, p: Vector2D):
        return {
            "type": "kick",
            "pow": p
        }
