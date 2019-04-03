class Vector2D:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __str__(self):
        return '(' + str(self.i) + ',' + str(self.j) + ')'

    def is_near(self, other):
        dist = abs(self.i - other.i)
        dist += abs(self.j - other.j)
        if dist < 3:
            return True
        return False

