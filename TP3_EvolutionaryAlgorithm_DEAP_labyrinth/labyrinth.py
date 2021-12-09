from typing import Any
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


POPULATION_SIZE = 256
CROSSOVER_PROBABILITY = 0.01
MUTATION_PROBABILITY = 0.1
RANDOM_PATH_PROBABILITY = 0.2
TOURNAMENT_SIZE = 3

class Direction(Enum):
    """
    Possible directions in a grid.
    """
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Genetics:
    """
    Class to apply operations on a population to solve a grid-like maze problem.
    """
    def __init__(self, grid, start, end, time_max):
        self.time = time_max
        self.grid = grid
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.start_cell = start
        self.end_cell = end
        self.toolbox = base.Toolbox()
        self.CXP = CROSSOVER_PROBABILITY
        self.MUP = MUTATION_PROBABILITY
        self.RPP = RANDOM_PATH_PROBABILITY
        self.chromosome_length = grid.shape[0] * grid.shape[1]

    def _decode(self, individual):
        """
        Transform the individual to a list(map()) of directions.
        """
        return list(map(lambda val: Direction(val), individual))

    def compute_chromosome(self, individual):
        """
        Transform an individual to a list of coordinates which will be the path.
        """
        directions = self._decode(individual)
        x, y = self.start_cell[0], self.start_cell[1]
        result = [(x, y)]

        for direction in directions:
            new_x, new_y = self.compute_coordinates(x, y, direction)
            new_coordinates = (new_x, new_y)

            # If it's going out of the grid or against a wall,
            # make it not moving.
            if 0 <= new_x < self.width \
                and 0 <= new_y < self.height \
                    and self.grid[new_coordinates] == 0:
                result.append(new_coordinates)
                x = new_x
                y = new_y

            # if at the end cut the chromosom
            if (x, y) == self.end_cell:
                return result

        return result

    def upgrade_chromosome(self, individual):
        """
        When a chromosome goes through a place it already went
        or went against a wall, this function will purify the 
        chromosome from those impurities.
        """
        directions = self._decode(individual)
        x, y = self.start_cell[0], self.start_cell[1]
        path = [(x, y)]

        for i, direction in enumerate(directions):
            new_x, new_y = self.compute_coordinates(x, y, direction)
            new_coordinates = (new_x, new_y)
            if 0 <= new_x < self.width - 1 \
                and 0 <= new_y < self.height - 1 \
                    and self.grid[new_coordinates] == 0 \
                        and not new_coordinates in path:
                path.append(new_coordinates)
                x, y = new_x, new_y
            else:
                # Find a new random direction or  the closest to the target
                if random() < self.RPP:
                    individual[i] = randint(0, len(Direction) - 1)
                else:
                    individual[i] = self.try_better_path(path[-1], self.end_cell)

                new_x, new_y = self.compute_coordinates(x, y, Direction(individual[i]))
                new_coordinates = (new_x, new_y)

                # Verify if the new direction is possible
                if 0 <= new_x < self.width \
                    and 0 <= new_y < self.height \
                        and self.grid[new_coordinates] == 0 \
                            and not new_coordinates in path:
                    path.append(new_coordinates)
                    x, y = new_x, new_y

            # If chromosome reaches the end of the labyrinth
            if (x, y) == self.end_cell:
                individual = individual[0:i]
                return

    def compute_coordinates(self, x, y, direction) -> tuple:
        """
        get the new x and y from a direction
        """
        if direction == Direction.UP:
            x -= 1
        elif direction == Direction.RIGHT:
            y += 1
        elif direction == Direction.DOWN:
            x += 1
        elif direction == Direction.LEFT:
            y -= 1
        return x, y

    def try_better_path(self, position, target) -> Direction:
        """
        Try to get the best direction for a point
        """
        if abs(position[0] - target[0]) > abs(position[1] - target[1]):
            if position[0] < target[0]:
                return Direction.DOWN
            else:
                return Direction.UP
        else:
            if position[1] < target[1]:
                return Direction.RIGHT
            else:
                return Direction.LEFT

    def manhattan(self, depart, destination) -> int:
        """
        manhattan distance between two points
        """
        return abs(depart[0] - destination[0]) + abs(depart[1] - destination[1])

    def fitness(self, individual) -> tuple:
        """
        fitness function, will calculate a fitness with the manhattan distance of the point,
        the length of the path and a malus if it doesn't reach the end.
        """
        path = self.compute_chromosome(individual)
        return self.manhattan(self.end_cell, path[-1]) + len(individual),

    def find_best(self, population):
        """
        Return the individual with the best fitness out of the population.
        """
        f = [ind.fitness.values[0] for ind in population]
        min_fit = min(f)
        return population[f.index(min_fit)]

    def evaluate_population(self, population):
        """
        Calculate the fitness for each individual
        """
        _fitness = [self.toolbox.fitness(ind) for ind in population]
        for ind, fit in zip(population, _fitness):
            ind.fitness.values = fit

    def toolbox_init(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        self.toolbox.register("fitness", self.fitness)
        # self.toolbox.register("evaluate", self.evaluate_population)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutShuffleIndexes, indpb=MUTATION_PROBABILITY)
        self.toolbox.register("select", tools.selTournament)
        self.toolbox.register("init_gene", randint, 0, 3)
        self.toolbox.register("init_individual", tools.initRepeat, creator.Individual, self.toolbox.init_gene, self.chromosome_length)
        self.toolbox.register("init_population", tools.initRepeat, list, self.toolbox.init_individual)

    def run(self):
        """
        Genetic algorithm to find the solution.
        """
        start_time = inter_time = time.time()

        self.toolbox_init()

        steps = 0

        population = self.toolbox.init_population(n=POPULATION_SIZE)

        if self.width >= 30:
            self.CXP = 0.04
            self.MUP = 0.40
            self.RPP = 0.5

        print(f"CXP : {self.CXP}, MUP: {self.MUP}, RPP: {self.RPP}")

        self.evaluate_population(population)

        solution = None

        # -------------------------------------------------------------------------------- #
        # Main Loop
        # -------------------------------------------------------------------------------- #
        
        while inter_time - start_time < self.time:

            old_solution = solution

            # ---------------------------------------------------------------------------- #
            # 1. Selection
            # ---------------------------------------------------------------------------- #
            offsprings = self.toolbox.select(population, len(population), TOURNAMENT_SIZE)
            offsprings = list(map(self.toolbox.clone, offsprings))

            # ---------------------------------------------------------------------------- #
            # 2. Populate
            # ---------------------------------------------------------------------------- #
            for i in range(0, len(population) - len(offsprings)):
                offsprings.append(self.toolbox.init_individual())

            # Apply crossover and mutation on the offspring
            for offspring1, offspring2 in zip(offsprings[::2], offsprings[1::2]):
                if random() < self.CXP:
                    self.toolbox.mate(offspring1, offspring2)

            # ---------------------------------------------------------------------------- #
            # 3. Applying mutations and upgrade on children
            # ---------------------------------------------------------------------------- #

            for offspring in offsprings:
                # add a new component
                if random() < self.MUP:
                    self.toolbox.mutate(offspring)
                self.upgrade_chromosome(offspring)

            # ---------------------------------------------------------------------------- #
            # 4. Evaluate population
            # ---------------------------------------------------------------------------- #
            
            self.evaluate_population(offsprings)

            population = offsprings

            # ---------------------------------------------------------------------------- #
            # 5. Search for the best solution in all the offsprings
            # ---------------------------------------------------------------------------- #
            
            best = self.find_best(offsprings)

            if not solution or best.fitness.values[0] < solution.fitness.values[0]:
                solution = best

            if old_solution != solution:
                old_solution = solution
                self.MUP = 0.02
                # print(f"The best solution was find after {time.time() - start_time:.2f} second(s) and has a chromosome's length of {len(solution)} number")
            else:
                steps += 1

            # Add a gene to all individual and increase the probability of mutation 
            # if there is 5 or more genertation without new best solution
            if steps >= 3 :
                if self.MUP < 0.2:
                    steps = 0
                    self.MUP *= 1.5
                [ind.insert(randint(0, len(ind)-1), randint(0,3)) for ind in population ]

            inter_time = time.time()

        return self.compute_chromosome(solution)


def solve_labyrinth(grid, start_cell, end_cell, max_time_s):
    """
    function of the genetic algorithm to find the solution
    """
    solution = Genetics(grid, start_cell, end_cell, max_time_s)
    return solution.run()
