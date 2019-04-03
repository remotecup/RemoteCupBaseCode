from IMonitor.Monitor import *
from tkinter import Tk, Canvas, Frame, BOTH


class Ground:
    def __init__(self, main):
        self.main = main
        self.ground = Frame(main.root, height=390, width=500, background='green4')
        self.ground.place(x=0, y=90)
        # self.ground.bind("<Motion>", self.show_mouse_position)
        self.last_max_i = Conf.max_i
        self.last_max_j = Conf.max_j
        self.boards = {}
        for i in range(self.last_max_i):
            for j in range(self.last_max_j):
                frame = Frame(self.ground, width=500 / self.last_max_j - 5, height=390 / self.last_max_i - 5,
                              bg='black')
                frame.place(x=j*500/self.last_max_j, y=i*390/self.last_max_i)

                self.boards[(i, j)] = Canvas(frame, background='green4')
                self.boards[(i, j)].place(x=0, y=0)
                s = self.boards[(i, j)].create_oval(0, 0, 390 / self.last_max_i / 3, 500 / self.last_max_j*2.5, outline="#f11",
                                                fill='black', width=2)

                print(s)
                self.boards[(i, j)].bind("<Motion>",
                                         lambda event, arg=(i, j): self.show_mouse_board(event, arg))

    def show_mouse_position(self, event):
        self.main.statusbar.change_mouse_position(event.x, event.y)

    def show_mouse_board(self, event, arg):
        self.main.statusbar.change_mouse_position(arg[0], arg[1])

    def show_board(self, board):
        for i in range(Conf.max_i):
            for j in range(Conf.max_j):
                if board[i][j] == 1:
                    self.boards[(i, j)].itemconfigure(1, fill='red')
                elif board[i][j] == 2:
                    self.boards[(i, j)].itemconfigure(1, fill='blue')
                elif board[i][j] == 3:
                    self.boards[(i, j)].itemconfigure(1, fill='green')
                else:
                    self.boards[(i, j)].itemconfigure(1, fill='black')

    def reset(self):
        for i in range(self.last_max_i):
            for j in range(self.last_max_j):
                self.boards[(i, j)].destroy()

        self.last_max_i = Conf.max_i
        self.last_max_j = Conf.max_j
        self.boards.clear()
        for i in range(self.last_max_i):
            for j in range(self.last_max_j):
                frame = Frame(self.ground, width=500 / self.last_max_j - 5, height=390 / self.last_max_i - 5,
                              bg='black')
                frame.place(x=j * 500 / self.last_max_j, y=i * 390 / self.last_max_i)

                self.boards[(i, j)] = Canvas(frame)
                self.boards[(i, j)].create_oval(0, 0, 390 / self.last_max_i, 500 / self.last_max_j,
                                                outline="#f11",
                                                fill="black", width=2)
                self.boards[(i, j)].place(x=0, y=0)

                self.boards[(i, j)].bind("<Motion>",
                                         lambda event, arg=(i, j): self.show_mouse_board(event, arg))
