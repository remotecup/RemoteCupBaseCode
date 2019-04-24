from Games.Soccer.Client.Python.World import World
from Games.Soccer.Client.Python.World import Agent


def is_kickable(agent: Agent, wm: World) -> bool:
    if agent.pos().dist(wm.ball().pos()) > agent.kickable_r:
        return False
    return True


def do_move(wm: World):
    pass


def do_kick(wm: World):
    pass


def get_action(wm: World):
    if is_kickable(wm.self(), wm):
        do_move(wm)
    else:
        do_kick(wm)
