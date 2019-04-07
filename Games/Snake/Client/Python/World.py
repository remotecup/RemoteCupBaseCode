from Base.Math import *


class World:
    def __init__(self):
        self.board = None
        self.cycle = None
        self.self_id = None
        self.goal_id = None
        self.self_position = None
        self.goal_position = None

    def set_id(self, self_id, goal_id):
        self.self_id = self_id
        self.goal_id = goal_id

    def update(self, message):
        self.board = message.world['board']
        self.cycle = message.cycle
        print(self.cycle)
        self.self_position = Vector2D(message.world['heads'][self.self_id][0], message.world['heads'][self.self_id][1])
        print(self.self_position)

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == self.goal_id:
                    self.goal_position = Vector2D(i, j)

        print('g id', self.goal_id, self.goal_position)

    def print(self):
        print('cycle: {}'.format(self.cycle))
        for f in self.board:
            print(f)
        print('------------------------------------')