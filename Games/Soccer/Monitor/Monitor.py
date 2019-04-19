from reportlab.pdfbase._fontdata_widths_symbol import widths

from Base.Monitor import *
from Base.Math import *
from tkinter import *
import Conf.conf as conf
from Games.Soccer.Server.Server import PlayerAgent, Ball


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)


Canvas.create_circle = _create_circle


class Ground:
    def __init__(self, main, ground_config):
        self.main = main
        self.ground = Canvas(main.root, height=conf.monitor_height - 110, width=conf.monitor_width, background="green4")
        self.ground.pack()
        self.ground.place(x=0, y=90)
        self.ground_config = ground_config
        if ground_config is None:
            self.last_max_i = 0
            self.last_max_j = 0

    def show_mouse_position(self, event):
        self.main.statusbar.change_mouse_position(event.x, event.y)

    def show_mouse_board(self, event, arg):
        self.main.statusbar.change_mouse_position_ij(arg[0], arg[1])

    def show_board(self, world):
        self.ground.delete('all')
        for key in world['players']:
            agent = PlayerAgent()
            agent.__dict__ = world['players'][key]
            self.ground.create_circle(agent.pos[0], agent.pos[1], 5, fill="yellow", outline="#000", width=1)
        if world['ball'] is not None:
            ball = Ball(0, 0)
            ball.__dict__ = world['ball']
            self.ground.create_circle(ball.pos[0], ball.pos[1], 2, fill="white")

    def reset(self, ground_config):
        self.ground_config = ground_config
