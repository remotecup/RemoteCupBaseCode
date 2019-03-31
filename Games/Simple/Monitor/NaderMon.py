from tkinter import *
import socket
from Games.Simple.Server.Message import *
import Games.Simple.Server.Conf as Conf
import threading
import time
import queue
from tkinter import filedialog

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 20003)
visual_queue = queue.Queue(0)
visual_list = []


def push_online():
    print('push online')
    while True:
        r = sock.recvfrom(1024)
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            break
        visual_queue.put(message)
        visual_list.append(message)


class CMenu:
    def __init__(self, main):
        self.main = main
        menu = Menu(main.root)
        main.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Connect", command=self.send_connect_request)
        filemenu.add_command(label="Disconnect", command=self.menu_call)
        filemenu.add_command(label="Open...", command=self.onOpen)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.menu_call)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.menu_call)

    def onOpen(self):
        filename = filedialog.askopenfilename(initialdir="~", title="Select file",
                                                   filetypes=(("jpeg files", "*.rcg"), ("all files", "*.*")))
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            visual_list.clear()
            for l in lines:
                message = parse(l)
                if message.type == 'MessageRCGCycle':
                    visual_list.append(message)
        except:
            pass

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text

    def menu_call(self):
        print('menu call back')

    def send_connect_request(self, event=''):
        print('want connect')
        self.main.toolbar.reset_time()
        message_snd = MessageMonitorConnectRequest().build()

        print('send req')
        sock.sendto(message_snd, server_address)
        r = sock.recvfrom(1024)
        message_rcv = parse(r[0])
        if message_rcv.type is 'MessageMonitorConnectResponse':
            print('receive resp')
            th = threading.Thread(target=push_online)

            th.start()


class CResults:
    def __init__(self, main):
        self.main = main
        self.results = Frame(main.root, height=40, width=500, background='gray60')
        self.results.place(x=0, y=0)
        self.team_results = []
        self.team_results.append(Label(self.results, text='First_team: 0', bg='gray60', fg='red'))
        self.team_results[-1].place(x=0, y=0)
        self.team_results.append(Label(self.results, text='Second_team: 0', bg='gray60', fg='blue'))
        self.team_results[-1].place(x=150, y=0)

    def update(self, score):
        i = 0
        for key in score.keys():
            self.team_results[i]['text'] = key + ':' + str(score[key])
            i += 1


class CToolbar:
    def __init__(self, main):
        self.main = main
        self.toolbar = Frame(main.root, height=40, width=500, background='gray40')
        self.toolbar.place(x=0, y=40)
        self.make_timer()
        self.make_button()

    def make_timer(self):
        self.timer_scale = Scale(self.toolbar, from_=0, to=100, length=370, bg='gray40',
                                 orient=HORIZONTAL, borderwidth=0, showvalue=0, command=self.changed_scale)
        self.scale_mouse_click = False
        self.timer_scale.bind('<Button-1>', self.mouse_click)
        self.toolbar.bind('<Leave>', self.mouse_leave)
        self.timer_scale.place(x=40, y=0)
        self.timer_min = StringVar()
        self.timer_min.set('0')
        self.timer_min_label = Label(self.toolbar, textvariable=self.timer_min, height=1, width=4, background='red')
        self.timer_min_label.place(x=0, y=0)
        self.timer_max = StringVar()
        self.timer_max.set('100')
        self.timer_max_label = Label(self.toolbar, textvariable=self.timer_max, height=1, width=4, background='red')
        self.timer_max_label.place(x=463, y=0)
        self.timer_show = StringVar()
        self.timer_show.set('0')
        self.timer_show_label = Label(self.toolbar, textvariable=self.timer_show, height=1, width=4, background='green')
        self.timer_show_label.place(x=420, y=0)

    def mouse_click(self, event):
        self.scale_mouse_click = True

    def mouse_leave(self, event):
        self.scale_mouse_click = False

    def changed_scale(self, value):
        if self.scale_mouse_click:
            self.main.gui.show_cycle = int(self.timer_scale.get())
            self.main.gui.puse()
            print(self.timer_scale.get())

    def reset_time(self):
        print('reset label')
        self.timer_scale.set(0)
        self.timer_min.set('0')
        self.timer_max.set('100')
        self.timer_scale['to'] = Conf.max_cycle

    def make_button(self):
        self.play_button = Button(self.toolbar, height=1, width=1, text='P', command=self.main.gui.play)
        self.play_button.place(x=250, y=15)
        self.puse_button = Button(self.toolbar, height=1, width=1, text='u', command=self.main.gui.puse)
        self.puse_button.place(x=210, y=15)
        self.online_button = Button(self.toolbar, height=1, width=1, text='o', command=self.main.gui.online)
        self.online_button.place(x=290, y=15)


class CGround:
    def __init__(self, main):
        self.main = main
        self.ground = Frame(main.root, height=400, width=500, background='green4')
        self.ground.place(x=0, y=80)
        # self.ground.bind("<Motion>", self.show_mouse_position)
        self.max_i = 8
        self.max_j = 5
        self.boards = {}
        for i in range(self.max_i):
            for j in range(self.max_j):
                self.boards[(i, j)] = Frame(self.ground, width=500/self.max_i - 5, height=400/self.max_j - 5,
                                            bg='black')
                self.boards[(i, j)].place(x=i*500/self.max_i, y=j*400/self.max_j)
                self.boards[(i, j)].bind("<Motion>",
                                         lambda event, arg=(i, j): self.show_mouse_board(event, arg))

    def show_mouse_position(self, event):
        self.main.statusbar.change_mouse_position(event.x, event.y)

    def show_mouse_board(self, event, arg):
        self.main.statusbar.change_mouse_position(arg[0], arg[1])

    def show_board(self, board):
        for i in range(self.max_i):
            for j in range(self.max_j):
                if board[i][j] == 1:
                    self.boards[(i, j)]['background'] = 'red'
                elif board[i][j] == 2:
                    self.boards[(i, j)]['background'] = 'blue'
                elif board[i][j] == 3:
                    self.boards[(i, j)]['background'] = 'green'
                else:
                    self.boards[(i, j)]['background'] = 'black'


class CStatusBar:
    def __init__(self, main):
        self.main = main
        self.status = Frame(main.root, height=20, width=500, background='gray66')
        self.status.place(x=0, y=480)
        self.mouse_position = {'x': 0, 'y': 0}
        self.mouse_label = Label(self.status, text=str(self.mouse_position), background='gray66')
        self.mouse_label.place(x=300, y=0)

    def change_mouse_position(self, x, y):
        self.mouse_position = {'x': x, 'y': y}
        self.mouse_label['text'] = '(x,y):({},{})'.format(self.mouse_position['x'], self.mouse_position['y'])


class MainWindow:
    def __init__(self, gui):
        self.gui = gui
        self.root = Tk()
        self.root.title('Monitor')
        self.root.geometry('500x500')
        self.root.pack_propagate(0)

        self.menu = CMenu(self)
        self.results = CResults(self)
        self.statusbar = CStatusBar(self)
        self.toolbar = CToolbar(self)
        self.ground = CGround(self)
        self.short_cut_key()

    def show_message(self, message):
        self.ground.show_board(message.board)
        self.results.update(message.score)

    def short_cut_key(self):
        self.root.bind("<space>", self.gui.play_pause)
        self.root.bind("<Control-c>", self.menu.send_connect_request)


class Gui:
    def __init__(self):
        self.show_cycle = 0
        self.show_puse = False
        pass

    def start(self):
        self.main_window = MainWindow(self)
        mainloop()

    def show(self):
        print('show start')
        while True:
            print('{} {}'.format(self.show_cycle, len(visual_list)))
            self.main_window.toolbar.timer_min.set(0 if len(visual_list) == 0 else visual_list[0].cycle)
            self.main_window.toolbar.timer_max.set(len(visual_list) + int(self.main_window.toolbar.timer_min.get()))
            self.main_window.toolbar.timer_show.set(self.show_cycle + int(self.main_window.toolbar.timer_min.get()))
            self.main_window.toolbar.timer_scale['to'] = len(visual_list)

            if self.show_cycle < len(visual_list):
                self.main_window.show_message(visual_list[self.show_cycle])

                if not self.show_puse:
                    self.main_window.toolbar.timer_scale.set(self.show_cycle)
                    self.show_cycle += 1
            time.sleep(0.1)

    def play(self):
        self.show_puse = False
        self.main_window.toolbar.scale_mouse_click = False

    def puse(self):
        self.show_puse = True

    def play_pause(self, event=''):
        if self.show_puse:
            self.play()
        else:
            self.puse()

    def online(self):
        self.play()
        self.show_cycle = len(visual_list) - 1


def run():
    gui = Gui()
    th = threading.Thread(target=gui.start)
    th.start()
    time.sleep(1)
    thshow = threading.Thread(target=gui.show)
    thshow.start()
    while True:
        time.sleep(1)
run()