from reportlab.pdfbase._fontdata_widths_symbol import widths

from Base.Monitor import *
from Base.Math import *
from tkinter import *
import Conf.conf as conf
import Conf.Monitor_Soccer_Conf as S_conf
import Conf.Server_Soccer_Conf as Server_conf
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
        self.objects = []
        self.o = Vector2D(conf.monitor_width / 2 - S_conf.max_i / 2, (conf.monitor_height - 110) / 2 - S_conf.max_j / 2)
        self.length = Vector2D(S_conf.max_i, S_conf.max_j)
        self.field = []
        self.make_field()

    def make_field(self):
        # Field Lines
        self.field.append(self.ground.create_line(self.o.i, self.o.j, self.o.i + self.length.i, self.o.j, fill='black'))
        self.field.append(self.ground.create_line(self.o.i, self.o.j, self.o.i, self.o.j + self.length.j, fill='black'))
        self.field.append(self.ground.create_line(self.o.i + self.length.i, self.o.j, self.o.i + self.length.i, self.o.j + self.length.j, fill='black'))
        self.field.append(self.ground.create_line(self.o.i, self.o.j + self.length.j, self.o.i + self.length.i, self.o.j + self.length.j, fill='black'))

        # Goals
        center = self.o + Vector2D(S_conf.max_i/2, S_conf.max_j/2)
        self.field.append(self.ground.create_rectangle(self.o.i - 20, center.j - Server_conf.goal_height/2, self.o.i, center.j + Server_conf.goal_height/2, fill="black"))
        self.field.append(self.ground.create_rectangle(self.o.i + self.length.i + 20, center.j - Server_conf.goal_height/2, self.o.i + self.length.i, center.j + Server_conf.goal_height/2, fill="black"))


    def show_mouse_position(self, event):
        self.main.statusbar.change_mouse_position(event.x, event.y)

    def show_mouse_board(self, event, arg):
        self.main.statusbar.change_mouse_position_ij(arg[0], arg[1])

    def show_board(self, world):
        self.remove_objects()
        for key in world['players']:
            agent = PlayerAgent()
            agent.__dict__ = world['players'][key]
            self.draw_object(agent, Server_conf.kick_able_r, "yellow")
        if world['ball'] is not None:
            ball = Ball(0, 0)
            ball.__dict__ = world['ball']
            self.draw_object(ball, S_conf.ball_r, "white")

    def remove_objects(self):
        while self.objects:
            self.ground.delete(self.objects.pop())

    def draw_object(self, obj, r, color):
        pos = Vector2D(obj.pos[0], obj.pos[1])
        pos = pos + self.o
        self.objects.append(self.ground.create_circle(pos.i, pos.j, r, fill=color, outline="#000", width=1))

    def reset(self, ground_config):
        self.ground_config = ground_config
