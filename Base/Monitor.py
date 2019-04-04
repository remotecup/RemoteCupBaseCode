from tkinter import *
import socket
from Base.Message import *
import threading
import time
from tkinter import filedialog
from tkinter import messagebox
import conf as conf
if conf.game == 'Simple':
    import Games.Simple.Monitor.Conf as Conf
    import Games.Simple.Monitor.Monitor as GameMonitor
elif conf.game == 'Snake':
    import Games.Snake.Monitor.Conf as Conf
    import Games.Snake.Monitor.Monitor as GameMonitor

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
server_address = (Conf.ip, Conf.monitor_port)
visual_list = []
is_run = True
is_connected = False
teams_number = 2
ground_config = None


def push_online():
    global is_connected
    print('push online')
    while is_connected:
        try:
            r = sock.recvfrom(4096)
        except:
            continue
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            is_connected = False
            break
        if message.type is not 'MessageClientWorld':
            continue
        visual_list.append(message)


class CMenu:
    def __init__(self, main):
        self.main = main
        menu = Menu(main.root)
        main.root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+o")
        filemenu.add_command(label="Connect", command=self.send_connect_request, accelerator="Ctrl+c")
        filemenu.add_command(label="Disconnect", command=self.disconnect, accelerator="Ctrl+d")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.main.close_window)
        helpmenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.menu_call)

    def open_file(self, event=''):
        global is_connected, ground_config
        if is_connected:
            is_connected = False
            self.disconnect()
        filename = filedialog.askopenfilename(initialdir="~", title="Select file",
                                              filetypes=(("jpeg files", "*.rcg"), ("all files", "*.*")))
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            self.main.gui.reset_show()
            visual_list.clear()
            for l in lines:
                message = parse(l)
                if message.type == 'MessageRCGHeader':
                    if ground_config != message.ground_config:
                        ground_config = message.ground_config
                        self.main.reset_ground()
                if message.type == 'MessageRCGCycle':
                    visual_list.append(message)
        except:
            pass

    def menu_call(self):
        print('menu call back')

    def send_connect_request(self, event=''):
        global is_connected, ground_config
        if is_connected:
            messagebox.showerror('connect error', 'please disconnect')
            print('please disconnected')
            return
        self.main.gui.reset_show()
        is_connected = True
        visual_list.clear()
        print('want connect')

        # self.main.toolbar.reset_time()
        message_snd = MessageMonitorConnectRequest().build()
        print('send req')
        sock.sendto(message_snd, server_address)
        try_number = 0
        while is_run:
            try:
                r = sock.recvfrom(4096)
            except:
                try_number += 1
                if try_number > 4:
                    break
                continue
            message_rcv = parse(r[0])
            print(message_rcv)
            if message_rcv.type is 'MessageMonitorConnectResponse':
                if ground_config != message_rcv.ground_config:
                    ground_config = message_rcv.ground_config
                    self.main.reset_ground()
                print('receive resp')
                th = threading.Thread(target=push_online)
                th.start()
                break
            else:
                continue

    def disconnect(self, event=''):
        global is_connected
        is_connected = False
        message_snd = MessageMonitorDisconnect().build()
        sock.sendto(message_snd, server_address)


class CResults:
    def __init__(self, main):
        self.main = main
        self.results = Frame(main.root, height=40, width=500, background='gray60')
        self.results.place(x=0, y=0)
        self.team_results = []
        self.team_results.append(Label(self.results, text='First_team: 0', bg='gray60', fg=simple_color[1]))
        self.team_results[-1].place(x=0, y=0)
        self.team_results.append(Label(self.results, text='Second_team: 0', bg='gray60', fg=simple_color[2]))
        self.team_results[-1].place(x=150, y=0)
        self.team_results.append(Label(self.results, text='Third_team: 0', bg='gray60', fg=simple_color[3]))
        self.team_results[-1].place(x=0, y=15)
        self.team_results.append(Label(self.results, text='Fourth_team: 0', bg='gray60', fg=simple_color[4]))
        self.team_results[-1].place(x=150, y=15)

    def update(self, score):
        for i in range(4):
            self.team_results[i]['text'] = str(0)
        i = 0
        for key in score.keys():
            self.team_results[i]['text'] = key + ':' + str(score[key])
            i += 1


class CToolbar:
    def __init__(self, main):
        self.main = main
        self.toolbar = Frame(main.root, height=50, width=500, background='gray40')
        self.toolbar.place(x=0, y=40)
        self.make_timer()
        self.make_button()

    def make_timer(self):
        self.scale_mouse_click = False

        self.timer_scale = Scale(self.toolbar, from_=0, to=100, length=350, bg='gray40',
                                 orient=HORIZONTAL, borderwidth=0, showvalue=0, command=self.changed_scale)
        self.timer_scale.bind('<Button-1>', self.mouse_click)
        self.toolbar.bind('<Leave>', self.mouse_leave)
        self.timer_scale.place(x=100, y=0)

        self.timer_min = StringVar()
        self.timer_min.set('0')
        t1 = Frame(self.toolbar, height=20, width=40, background='gray40')
        t1.place(x=0, y=0)
        self.timer_min_label = Label(t1, textvariable=self.timer_min, background='gray40', width=4, justify=LEFT)
        self.timer_min_label.place(x=0, y=0)

        t3 = Frame(self.toolbar, height=20, width=20, background='gray40')
        t3.place(x=t1['width'], y=0)
        self.timer_to_label = Label(t3, text='to', background='gray40', justify=LEFT)
        self.timer_to_label.place(x=0, y=0)

        self.timer_max = StringVar()
        self.timer_max.set('100')
        t2 = Frame(self.toolbar, height=20, width=40, background='gray40')
        t2.place(x=t1['width'] + t3['width'], y=0)
        self.timer_max_label = Label(t2, textvariable=self.timer_max, width=4, background='gray40', justify=LEFT)
        self.timer_max_label.place(x=0, y=0)


        self.timer_show = StringVar()
        self.timer_show.set('0')
        t4 = Frame(self.toolbar, height=20, width=40, background='gray40')
        t4.place(x=t1['width'] + t3['width'] + t3['width'] + self.timer_scale['length'] + 25, y=0)
        self.timer_show_label = Label(t4, textvariable=self.timer_show, height=1, width=4,
                                      background='gray40', justify=LEFT,font=("bold"))
        self.timer_show_label.place(x=0, y=0)

    def mouse_click(self, event):
        self.main.gui.pause()
        self.scale_mouse_click = True

    def mouse_leave(self, event):
        self.scale_mouse_click = False

    def changed_scale(self, value):
        if self.scale_mouse_click:
            self.main.gui.show_cycle = int(self.timer_scale.get())
            self.main.gui.pause()
            print(self.timer_scale.get())

    def reset_time(self):
        print('reset label')
        self.timer_scale.set(0)
        self.timer_min.set('0')
        self.timer_max.set('100')
        self.timer_scale['to'] = 100

    def make_button(self):
        self.play_button = Button(self.toolbar, height=1, width=6, text='PLAY', command=self.main.gui.play)
        self.play_button.place(x=100, y=18)
        self.puse_button = Button(self.toolbar, height=1, width=6, text='PAUSE', command=self.main.gui.pause)
        self.puse_button.place(x=200, y=18)
        self.online_button = Button(self.toolbar, height=1, width=6, text='ONLINE', command=self.main.gui.online)
        self.online_button.place(x=300, y=18)


# class CGround:
#     def __init__(self, main):
#         pass
#
#     def show_mouse_position(self, event):
#         pass
#
#     def show_mouse_board(self, event, arg):
#         pass
#
#     def show_board(self, board):
#         pass
#
#     def reset(self):
#         pass


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
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.bind('<Left>', self.left_key)
        self.root.bind('<Right>', self.right_key)
        self.root.title('RemoteCup Monitor')
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='icons/icon.png'))
        self.root.geometry('500x500')
        self.root.pack_propagate(0)

        self.menu = CMenu(self)
        self.results = CResults(self)
        self.statusbar = CStatusBar(self)
        self.toolbar = CToolbar(self)
        self.ground = GameMonitor.Ground(self, ground_config)
        self.short_cut_key()

    def show_message(self, message):
        print(message)
        print(message.board)
        self.ground.show_board(message.board)
        self.results.update(message.score)

    def short_cut_key(self):
        self.root.bind("<space>", self.gui.play_pause)
        self.root.bind("<Control-c>", self.menu.send_connect_request)
        self.root.bind("<Control-d>", self.menu.disconnect)
        self.root.bind("<Control-o>", self.menu.open_file)

    def close_window(self):
        global is_run
        is_run = False
        time.sleep(1)
        self.root.quit()
        self.root.destroy()

        print('{} close windows'.format(threading.current_thread().ident))
        print('close')

    def right_key(self, event):
        self.gui.showed_cycle += 1
        if self.gui.showed_cycle >= len(visual_list):
            self.gui.showed_cycle = len(visual_list) - 1
        self.toolbar.timer_scale.set(self.gui.showed_cycle)
        self.gui.pause()

    def left_key(self, event):
        self.gui.showed_cycle -= 1
        if self.gui.showed_cycle < 0:
            self.gui.showed_cycle = 0
        self.toolbar.timer_scale.set(self.gui.showed_cycle)
        self.gui.pause()

    def reset_ground(self):
        self.ground.reset(ground_config)


class Gui:
    def __init__(self):
        self.showed_cycle = 0
        self.show_paused = False
        self.main_window = None
        pass

    def start(self):
        print('{} start'.format(threading.current_thread().ident))
        self.main_window = MainWindow(self)
        mainloop()

    def show(self):
        print('{} show'.format(threading.current_thread().ident))
        print('show start')
        while self.main_window is None and is_run:  # wait for start gui_thread
            time.sleep(1)
        print('show started')
        while is_run:
            print('{} {}'.format(self.showed_cycle, len(visual_list)))
            tmp = 0 if len(visual_list) == 0 else visual_list[0].cycle
            self.main_window.toolbar.timer_min.set(tmp)
            self.main_window.toolbar.timer_max.set(len(visual_list) + tmp)
            self.main_window.toolbar.timer_show.set(self.showed_cycle + tmp)
            self.main_window.toolbar.timer_scale['to'] = len(visual_list)

            if self.showed_cycle < len(visual_list):
                self.main_window.show_message(visual_list[self.showed_cycle])

                if not self.show_paused:
                    self.main_window.toolbar.timer_scale.set(self.showed_cycle)
                    self.showed_cycle += 1
            time.sleep(Conf.show_time_speed)
        print('show end')

    def play(self):
        self.show_paused = False
        self.main_window.toolbar.scale_mouse_click = False

    def pause(self):
        self.show_paused = True

    def play_pause(self, event=''):
        if self.show_paused:
            self.play()
        else:
            self.pause()

    def online(self):
        self.play()
        self.showed_cycle = len(visual_list) - 1

    def reset_show(self):
        self.showed_cycle = 0
        self.play()


def run():
    gui = Gui()
    gui_thread = threading.Thread(target=gui.start)  # main loop
    gui_thread.start()
    show_tread = threading.Thread(target=gui.show)  # show ground step by step
    show_tread.start()
    while is_run:
        time.sleep(1)
    # th.join()
    # thshow.join()
# run()