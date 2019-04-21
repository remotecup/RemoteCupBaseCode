from math import sin, cos

simple_color = {0: 'black', 1: 'red', 2: 'blue', 3: 'orange', 4: 'pink', 'g': 'green', 'w': 'brown'}
advance_color = {0: ['black'], 1: ['red', 'red4'], 2: ['blue', 'blue4'], 3: ['orange', 'dark goldenrod'],
                 4: ['pink', 'pink4'], 'g': ['green'], 'w': ['brown']}


class Vector2D:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return '(' + str(self.i) + ',' + str(self.j) + ')'

    def __repr__(self):
        return '(' + str(self.i) + ',' + str(self.j) + ')'

    def __eq__(self, other):
        if self.i == other.i and self.j == other.j:
            return True
        return False

    def is_near(self, other):
        dist = abs(self.i - other.i)
        dist += abs(self.j - other.j)
        if dist < 3:
            return True
        return False

    def dist(self, other):
        return ((self.i - other.i) ** 2 + (self.j - other.j) ** 2) ** 0.5

    def r(self):
        return (self.i ** 2 + self.j ** 2) ** 0.5

    def __add__(self, other):
        return Vector2D(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        tmp = Vector2D(-other.i, -other.j)
        return self + tmp

    @staticmethod
    def polar2vector(r, teta):
        return Vector2D(r * cos(teta), r * sin(teta))

    def scale(self, k):
        return Vector2D(self.i * k, self.j * k)


class Line2D:
    def __init__(self, pos1: Vector2D, pos2: Vector2D):
        self.m = (pos2.j - pos1.j) / (pos2.i - pos1.i)
        self.b = pos2.j - self.m * pos2.i

    def x(self, x):
        return Vector2D(x, self.m * x + self.b)

    def contain(self, pos: Vector2D):
        y = self.m * pos.i + self.b
        if y == pos.j:
            return True
        return False
