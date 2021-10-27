import math


def h_0(data, n, b) -> int:
    return 0


def h_NtoB_x(data, n, b) -> int:
    return abs(data[n][0] - data[b][0])


def h_NtoB_y(data, n, b) -> int:
    return abs(data[n][1] - data[b][1])


def h_crowFly(data, n, b) -> float:
    d1 = abs(data[n][0] - data[b][0])
    d2 = abs(data[n][1] - data[b][1])
    return math.sqrt(d1 ** 2 + d2 ** 2)


def h_manhattan(data, n, b) -> int:
    return abs(data[n][0] - data[b][0]) + \
           abs(data[n][1] - data[b][1])


class HeuristicsStrategy:

    def __init__(self):
        self.definitions = {
            'h0': h_0,
            'h1': h_NtoB_x,
            'h2': h_NtoB_y,
            'h3': h_crowFly,
            'h4': h_manhattan
        }
