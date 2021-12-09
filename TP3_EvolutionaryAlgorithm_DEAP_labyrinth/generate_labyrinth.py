from random import choice
from numpy.random.mtrand import rand


def generate_labyrinth(width, height, wall_ratio=0.3):
    """
    Randomly generates the labyrinth matrix, the values are:
    0 if the cell is free
    1 if there is a wall
    :param wall_ratio:
    :param width: width of the matrix
    :param height: height of the matrix
    :wall_ratio float: chance for a cell to be a wall
    :return: tuple composed of:
    <matrix>: numpy 2d array
    <start_cell>: tuple of i, j indices for the start cell
    <end_cell>: tuple of i, j indices for the end cell
    """
    grid = rand(width, height)

    grid[grid >= 1 - wall_ratio] = 1
    grid[grid < 1 - wall_ratio] = 0

    free_cell_top = [i for i in range(0, width) if grid[0][i] != 1]

    start_idx = choice(free_cell_top)
    start_cell = (0, start_idx)

    free_cell_bottom = [i for i in range(0, width) if grid[-1][i] != 1]

    end_idx = choice(free_cell_bottom)
    end_cell = (height - 1, end_idx)

    return grid, start_cell, end_cell
