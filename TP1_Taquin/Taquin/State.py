import copy


def legal():
    return True


class State(object):

    def __init__(self, values, parent=None):
        self.values = values
        self.parent = parent

    def final(self, final_v):
        return self.values == final_v

    def __hash__(self):
        return str(self).__hash__()

    def __str__(self):
        return str(self.values)

    def __eq__(self, other):
        return self.values == other.values

    def apply(self, op):
        return State(op, self)

    def applicableOps(self):
        ops = []
        len_l = len(self.values)
        col_l = len(self.values[0])

        i, j = State.search_x(self.values)

        # it is possible to swap with the line above
        if i > 0:
            ops.append(self.swap(self.values, i, j, i - 1, j))

        # it is possible to swap with the line below
        if i < len_l - 1:
            ops.append(self.swap(self.values, i, j, i + 1, j))

        # it is possible to swap with the column on the left
        if j > 0:
            ops.append(self.swap(self.values, i, j, i, j - 1))

        # it is possible to swap with the column on the right
        if j < col_l - 1:
            ops.append(self.swap(self.values, i, j, i, j + 1))

        return ops

    @staticmethod
    def swap(values, x1, y1, x2, y2):
        nvs = copy.deepcopy(values)
        nvs[x1][y1], nvs[x2][y2] = nvs[x2][y2], nvs[x1][y1]
        return nvs

    @staticmethod
    def search_x(values, x=0):
        for i, line in enumerate(values):
            for j, elem in enumerate(line):
                if elem == x:
                    return i, j