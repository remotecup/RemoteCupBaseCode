simple_color = {0: 'black', 1: 'red', 2: 'blue', 3: 'orange', 4: 'pink', 'g': 'green', 'w': 'brown'}


class Vector2D:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
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

