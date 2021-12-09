import time
import numpy

from collections import namedtuple
from random import randint

from deap import base, algorithms
from deap import creator
from deap import tools


class Labyrinth:
    """
    Wrapper class for more readable access to the grid.
    """
    def __init__(self, grid, start, end):
        self.end = end
        self.start = start
        self.np_grid = grid
        self.height = grid.shape[0]
        self.width = grid.shape[1]
        self.walls = self.walls(grid)

    @staticmethod
    def walls(np_grid):
        """
        Returns the positions of the walls in the grid.
        Later use to calculate penalties for chromosomes.
        :param np_grid:
        :return:
        """
        coord = lambda y, r: [(x, y) for x, i in enumerate(r) if i == 1.0]
        coord_list = [coord(y, rows) for y, rows in enumerate(np_grid)]
        __walls = [i for sub in coord_list for i in sub]
        return __walls


# ____________________________      EVOLUTIONARY CONSTANTS      ____________________________

POPULATION_SIZE = 1000
TOURNAMENT_SIZE = 3

GENE_MUTATION_PROBABILITY = 0.02
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.35

EXPANSION = 1.25

# ____________________________         CHROMOSOME ENCODING      ____________________________


Gene = namedtuple("Gene", ["apply", "str"])
Choice = namedtuple("Choice", ["callback", "str"])

DIRECTIONS = {
    0: Choice(lambda position: (position[0], position[1] + 1), "D"),
    1: Choice(lambda position: (position[0], position[1] - 1), "U"),
    2: Choice(lambda position: (position[0] - 1, position[1]), "L"),
    3: Choice(lambda position: (position[0] + 1, position[1]), "R")
}


def _parse_code(_gene: int) -> Gene:
    """
    Convert bit string to Code namedtuple
    """
    return Gene(DIRECTIONS[_gene].callback, DIRECTIONS[_gene].str)


def genome(chromosome: list[int]) -> list[Gene]:
    """
    Gives the genes composing the genome of an individual.
    """
    return list(map(_parse_code, chromosome))


def pathing(chromosome: list[int], labyrinth: Labyrinth) -> list[tuple]:
    """
    Extract the coordinates from the chromosome.
    """
    genes = genome(chromosome)
    path = [labyrinth.start]
    for g in genes:
        path.append(g.apply(path[-1]))
    return path


def manhattan_distance(origin: tuple, destination: tuple) -> int:
    """
    Compute manhattan distance from the origin point to the destination
    """
    return abs(destination[0] - origin[0]) + abs(destination[1] - origin[1])


def compute_penalties(path: list[tuple], labyrinth: Labyrinth) -> tuple:
    """
    Because we cannot use the environment around to determine a solution,
    this function calculates the penalties to give to a solution if
    it goes through a wall, has to go back, or goes out of the labyrinth.
    It is also here that directions are given.
    """
    paths = set(path)
    x = lambda coord: coord < 0 or coord > labyrinth.width - 1
    y = lambda coord: coord < 0 or coord > labyrinth.height - 1
    out = sum([1 for coord in path if x(coord[0]) or y(coord[1])])
    itself = len(path) - len(paths)
    encountered_walls = len(paths.intersection(set(labyrinth.walls)))
    return out, itself, encountered_walls * 4


def fitness(chromosome: list[int], labyrinth: Labyrinth) -> int:
    """
    Fitness is the sum of manhattan distance (between the last
    gene of the chromosome and the end of the maze) and
    penalties.
    """
    path = pathing(chromosome, labyrinth)
    penalties = compute_penalties(path, labyrinth)
    manhattan = manhattan_distance(path[-1], labyrinth.end)
    return manhattan + sum(penalties)


def generations(x: int, y: int, expansion: float) -> int:
    return int((x + y) * expansion)


class GeneticAlgorithm:
    def __init__(self, grid, start, end, time_max) -> None:
        self.time = time
        self.width = grid.shape[0]
        self.height = grid.shape[1]
        self.time = time_max
        self.chromosome_length = self.width + self.height
        self.labyrinth = Labyrinth(grid, start, end)
        self.generations = int(generations(self.width, self.height, EXPANSION))

    @staticmethod
    def class_creation() -> None:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

    def register_functions(self, toolbox: base.Toolbox) -> None:
        def evaluate_individual(i): return fitness(i, self.labyrinth),

        toolbox.register("gene", randint, 0, 3)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.gene, self.chromosome_length)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", evaluate_individual)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=GENE_MUTATION_PROBABILITY)
        toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)

    @staticmethod
    def statistics():
        sample_size = tools.Statistics(len)
        fitness_stats = tools.Statistics(lambda individual: individual.fitness.values)
        multi_statistics = tools.MultiStatistics(fitness=fitness_stats, size=sample_size)
        multi_statistics.register("average", numpy.mean)
        return multi_statistics

    def run(self):
        self.class_creation()
        toolbox = base.Toolbox()
        self.register_functions(toolbox=toolbox)
        statistics = self.statistics()
        hall_of_fame = tools.HallOfFame(1)
        start_time = time.time()
        runs = 0

        while time.time() - start_time < self.time:
            runs += 1
            pop = toolbox.population(n=POPULATION_SIZE)
            _, log = algorithms.eaSimple(
                pop,
                toolbox,
                CROSSOVER_PROBABILITY,
                MUTATION_PROBABILITY,
                self.generations,
                stats=statistics,
                halloffame=hall_of_fame,
                verbose=True
            )

        path = pathing(hall_of_fame[0], self.labyrinth)
        score = fitness(hall_of_fame[0], self.labyrinth)

        score = f"Fitness: {score}\n"
        execution = "Execution time: {:.2f}s".format(time.time() - start_time)
        print(f"\n{runs} runs\n{execution}\nBest run: -> {score}")
        reversed_path_sequence = []
        for tu in path:
            (x, y) = tu.__getitem__(1), tu.__getitem__(0)
            reversed_path_sequence.append((x, y))
        return reversed_path_sequence
