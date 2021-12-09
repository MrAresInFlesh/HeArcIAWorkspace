import numpy as np

from generate_labyrinth import generate_labyrinth
from labyrinth import display_labyrinth
from labyrinth import solve_labyrinth

levels = {
    "10": {"file": "data/grid10.npy", "time": 5},
    "20": {"file": "data/grid20.npy", "time": 5},
    "30": {"file": "data/grid30.npy", "time": 5},
    "40": {"file": "data/grid40.npy", "time": 5},
    "30**": {"file": "data/grid30180.npy", "time": 5}
}


def init_labyrinth(dimension):
    labyrinth = generate_labyrinth(dimension, dimension)
    _grid = labyrinth[0]
    _start = labyrinth[1]
    _end = labyrinth[2]
    return grid, start, end


def test_random(test=True, _time=10):
    if test:
        g, s, e = init_labyrinth(20)
        _solution = solve_labyrinth(g, s, e, _time)
        display_labyrinth(g, s, e)
        display_labyrinth(g, s, e, _solution)


if __name__ == '__main__':

    # USING RANDOMLY GENERATED LABYRINTH
    test_random(False)

    # WITH GIVEN LABYRINTH, WHICH IS NOT IMPOSSIBLE TO SOLVE

    level = levels["30**"]
    grid = np.load(level["file"])
    time = level["time"]
    start, end = (0, 0), (grid.shape[0] - 1, grid.shape[1] - 1)

    solution = solve_labyrinth(grid, start, end, time)

    display_labyrinth(grid, start, end)

    display_labyrinth(grid, start, end, solution)

