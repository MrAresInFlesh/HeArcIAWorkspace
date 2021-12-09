import numpy as np
import matplotlib.pyplot as plt
import time
import random
from random import random, randint, choice
from deap import base
from deap import creator
from deap import tools
from enum import Enum


def generate_labyrinth(width, height, wall_ratio=0.3):
    """ Randomly generates the labyrinth matrix, the values are:
    0 if the cell is free
    1 if there is a wall
    :param width: width of the matrix
    :param height: height of the matrix
    :param wall_ratio: chance for a cell to be a wall
    :return: tuple composed of:
        <matrix>: numpy 2d array
        <start_cell>: tuple of i, j indices for the start cell
        <end_cell>: tuple of i, j indices for the end cell
    """
    grid = np.random.rand(width, height)
    grid[grid >= 1 - wall_ratio] = 1
    grid[grid < 1 - wall_ratio] = 0
    free_cell_top = [i for i in range(0, width) if grid[0][i] != 1]
    start_idx = choice(free_cell_top)
    start_cell = (0, start_idx)
    free_cell_bottom = [i for i in range(0, width) if grid[-1][i] != 1]
    end_idx = choice(free_cell_bottom)
    end_cell = (height - 1, end_idx)
    return grid, start_cell, end_cell


def display_labyrinth(grid, start_cell, end_cell, solution=None):
    """ Display the labyrinth matrix and possibly the solution with matplotlib.
    Free cell will be in light gray.
    Wall cells will be in dark gray.
    Start and end cells will be in dark blue.
    Path cells (start, end excluded) will be in light blue.
    :param grid np.array: labyrinth matrix
    :param start_cell: tuple of i, j indices for the start cell
    :param end_cell: tuple of i, j indices for the end cell
    :param solution: list of successive tuple i, j indices who forms the path
    """
    grid = np.array(grid, copy=True)
    START = 0
    END = 0
    PATH = 2
    WALL_CELL = 16
    FREE_CELL = 19
    grid[grid == 0] = FREE_CELL
    grid[grid == 1] = WALL_CELL
    grid[start_cell] = START
    grid[end_cell] = END
    if solution:
        solution = solution[1:-1]
        for cell in solution:
            grid[cell] = PATH
    else:
        print("No solution has been found")
    plt.matshow(grid, cmap="tab20c")


N_POPULATION = 100
CROSSOVER_PROBA = 0.02
MUTATE_PROBA = 0.35
RANDOM_PATH_PROBABILITY = 0.8


class Direction(Enum):
    """
    Possible 4 directions in a grid.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Genetics:
    def __init__(self, grid, start, end, time_max) -> None:
        self.time = time
        self.grid = grid
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.start_cell = start
        self.end_cell = end
        self.time = time_max
        self.chromosome_length = self.width + self.height

    @staticmethod
    def _decode(individual):
        """
        transform the int of the chromosome to a list of direction
        """
        return list(map(lambda val: Direction(val), individual))

    def compute_chromosome(self, individual, start, end, grid):
        """
        Transform an individual in a list of coordinates (path)
        """
        directions = self._decode(individual)
        x, y = start[0], start[1]
        result = [(x, y)]

        for direction in directions:
            # add the next coordinates in the path
            new_x, new_y = self.compute_coordinates(x, y, direction)

            new_coordinates = (new_x, new_y)

            # if going out of the grid or against a wall, do not move
            if 0 <= new_x < grid.shape[0] \
                    and 0 <= new_y < grid.shape[1] \
                    and grid[new_coordinates] == 0:
                result.append(new_coordinates)
                x = new_x
                y = new_y

            # if at the end cut the chromosom
            if (x, y) == end:
                return result

        return result

    def upgrade(self, individual, grid, start_cell, end_cell):
        """
        fix a chromosom by finding place where he went already or go against a wall
        """
        directions = self._decode(individual)
        x, y = start_cell[0], start_cell[1]
        path = [(x, y)]

        for i, direction in enumerate(directions):
            # add the next coordinates in the path
            new_x, new_y = self.compute_coordinates(x, y, direction)

            new_coordinates = (new_x, new_y)

            if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1] \
                    and grid[new_coordinates] == 0 \
                    and not new_coordinates in path:

                path.append(new_coordinates)
                x, y = new_x, new_y
            else:
                # find a new direction random or closest to the target
                if random() < RANDOM_PATH_PROBABILITY:
                    individual[i] = randint(0, len(Direction) - 1)
                else:
                    individual[i] = self.find_better_path(path[-1], end_cell)
                    # always go the same places, not really good

                new_x, new_y = self.compute_coordinates(x, y, Direction(individual[i]))
                new_coordinates = (new_x, new_y)

                # Check the new direction is doable
                if 0 <= new_x < grid.shape[0] and 0 <= new_y < grid.shape[1] \
                        and grid[new_coordinates] == 0 \
                        and not new_coordinates in path:
                    path.append(new_coordinates)
                    x, y = new_x, new_y

            # if at the end cut the chromosom
            if (x, y) == end_cell:
                individual = individual[0:i]
                return

    @staticmethod
    def compute_coordinates(x, y, direction):
        """
        get the new x and y from a direction
        """
        if direction == Direction.TOP:
            x -= 1
        elif direction == Direction.RIGHT:
            y += 1
        elif direction == Direction.BOTTOM:
            x += 1
        elif direction == Direction.LEFT:
            y -= 1
        return x, y

    def find_better_path(self, position, target):
        """
        Try to get the best direction for a point
        """
        if abs(position[0] - target[0]) > abs(position[1] - target[1]):
            if position[0] < target[0]:
                return Direction.BOTTOM
            else:
                return Direction.TOP
        else:
            if position[1] < target[1]:
                return Direction.RIGHT
            else:
                return Direction.LEFT

    @staticmethod
    def manhattan(p1, p2):
        """
        manhattan distance between two points
        """
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def fitness(self, individual, grid, start_cell, end_cell, chromosome_length):
        """
        fitness function, will calculate a fitness with the manhattan distance of the point,
        the length of the path and a malus if it doesn't reach the end.
        """
        path = self.compute_chromosome(individual, start_cell, end_cell, grid)
        return self.manhattan(end_cell, path[-1]) * chromosome_length + len(individual),

    @staticmethod
    def evaluate_population(population, grid, start_cell, end_cell, toolbox, chromosome_length):
        """
        Calculate the fitness for each individual
        """
        f = [toolbox.fitness(ind, grid, start_cell, end_cell, chromosome_length) for ind in population]
        for ind, fit in zip(population, f):
            ind.fitness.values = fit

    def toolbox_init(self, toolbox, chromosome_length):
        toolbox.register("fitness", self.fitness)
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.3)
        toolbox.register("select", tools.selBest)

        toolbox.register("init_gene", randint, 0, 3)
        toolbox.register("init_individual", tools.initRepeat, creator.Individual, toolbox.init_gene, chromosome_length)
        toolbox.register("init_population", tools.initRepeat, list, toolbox.init_individual)

    @staticmethod
    def find_best(population):
        """
        find the best individual in a population,
        individual need a fitness attribute
        """
        f = [ind.fitness.values[0] for ind in population]
        min_fit = min(f)
        return population[f.index(min_fit)]

    def run(self):
        """
        function of the genetic algorithm to find the solution
        """
        CHROMOSOME_LENGTH = self.grid.shape[0] * self.grid.shape[1]

        toolbox = base.Toolbox()
        self.toolbox_init(toolbox, CHROMOSOME_LENGTH)
        start_time = inter_time = time.time()
        population = toolbox.init_population(n=N_POPULATION)

        self.evaluate_population(population, self.grid, self.start_cell, self.end_cell, toolbox, CHROMOSOME_LENGTH)
        solution = None

        # do not need a stop condition other than time because we always keep the best
        while inter_time - start_time < self.time:
            # selection
            children = toolbox.select(population, len(population))
            children = list(map(toolbox.clone, children))

            # spawning new child
            for i in range(0, len(population) - len(children)):
                children.append(toolbox.init_individual())
            print("1", inter_time - start_time)
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(children[::2], children[1::2]):
                if random() < CROSSOVER_PROBA:
                    toolbox.mate(child1, child2)
            # mutation
            for child in children:
                # add a new component
                if random() < MUTATE_PROBA:
                    toolbox.mutate(child)
                self.upgrade(child, self.grid, self.start_cell, self.end_cell)

            inter_time = time.time()
            print("2", inter_time - start_time)

            self.evaluate_population(children, self.grid, self.start_cell, self.end_cell, toolbox, CHROMOSOME_LENGTH)
            population = children

            # Search for the solution
            best = self.find_best(children)

            if not solution or best.fitness.values[0] < solution.fitness.values[0]:
                solution = best

            inter_time = time.time()
            print("3", inter_time - start_time)

        return self.compute_chromosome(solution, self.start_cell, self.end_cell, self.grid)


def solve_labyrinth(grid, start_cell, end_cell, max_time_s):
    """
    function of the genetic algorithm to find the solution
    """
    solution = Genetics(grid, start_cell, end_cell, max_time_s)
    return solution.run()
