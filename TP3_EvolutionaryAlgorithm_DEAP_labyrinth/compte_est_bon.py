from deap import base
from deap import creator
from deap import tools
from deap import algorithms
import operator
from enum import Enum
from collections import namedtuple
import random
import time

# Each operand or operator is described by 4 bits
CODE_LENGTH = 4

# In this example, we fix the number of operands to 5
NB_OPERANDS = 5

# The maximum number of operators is NB_OPERANDS - 1
# ex. 5 + 3 / 2
# three operands: 5, 3, 2
# two operators: +, /
NB_OPERATORS = NB_OPERANDS - 1

CHROMOSOME_LENGTH = NB_OPERANDS * CODE_LENGTH + NB_OPERATORS * CODE_LENGTH


# We have three type of code: operands, operators and undefined symbols
class CodeType(Enum):
    OPERAND = 1
    OPERATOR = 2
    NOTHING = 3


# namedtuple("typename, field_names[...]") returns a new tuple subclass named 'typename'.
# The new subclass is used to create tuple-like objects that have fields accessible
# by attribute lookup as well as being indexable and iterable
Code = namedtuple("Code", ["code_type", "apply", "str"])

OPERATORS = {
    10: (operator.add, "+"),  # Standard operators as functions, see https://docs.python.org/3/library/operator.html
    11: (operator.sub, "-"),
    12: (operator.mul, "*"),
    13: (operator.truediv, "/")
}


def _parse_code(code):
    """ Convert bit string to a Code namedtuple """
    int_value = int(code, 2)
    if int_value >= 0 and int_value < 10:
        return Code(CodeType.OPERAND, lambda: int_value, str(int_value))
    elif int_value >= 10 and int_value <= 13:
        return Code(CodeType.OPERATOR, OPERATORS[int_value][0], OPERATORS[int_value][1])
    else:
        return Code(CodeType.NOTHING, None, "_")


def _decode(individual):
    """ Parse each code of the full chromosome (aka individual) """
    chromosome_str = "".join([str(gene) for gene in individual])
    codes = [_parse_code(chromosome_str[i: i + CODE_LENGTH]) for i in range(0, len(chromosome_str), CODE_LENGTH)]
    return codes


def displayable_chromosome(individual):
    """ Convert chromosome to a readable format (e.g. 3 + 5 / 6) """
    return " ".join(code.str for code in _decode(individual))


def compute_chromosome(individual):
    """ Compute operations hidden in the chromosome """
    codes = _decode(individual)
    first_operand = None
    operation = None
    snd_operand = None
    result = 0
    for code in codes:
        if not first_operand:
            if code.code_type == CodeType.OPERAND:
                first_operand = code.apply()
        elif not operation:
            if code.code_type == CodeType.OPERATOR:
                operation = code.apply
        elif not snd_operand:
            if code.code_type == CodeType.OPERAND:
                snd_operand = code.apply()
                try:
                    result = operation(first_operand, snd_operand)
                except ZeroDivisionError:
                    pass
                first_operand = result
                operation = None
                snd_operand = None
    return result


toolbox = base.Toolbox()


def fitness(individual, target):
    return (abs(compute_chromosome(individual) - target),)  # Tuple !


toolbox.register("fitness", fitness)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
# toolbox.register("select", tools.selRoulette) # cannot be used for a minimization problem
toolbox.register("select", tools.selTournament)  # need an additional parameter turnsize
# toolbox.register("select", tools.selBest)

toolbox.register("init_gene", random.randint, 0, 1)
toolbox.register("init_individual", tools.initRepeat, creator.Individual, toolbox.init_gene, CHROMOSOME_LENGTH)
toolbox.register("init_population", tools.initRepeat, list, toolbox.init_individual)

TARGET = 126
MAX_TIME = 5  # seconds


def evaluate_population(population, target):
    for ind in population:
        ind.fitness.values = toolbox.fitness(ind, target)


def evaluate_population_2(population, target):
    fitnesses = [toolbox.fitness(ind, target) for ind in population]
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit


def find_winners(population):
    winners = [ind for ind in population if ind.fitness.values[0] == 0]
    return winners


toolbox.register("evaluate", evaluate_population)


start_time = inter_time = time.time()
tournsize = 8
# crossover probability
CXPB = 0.7
# mutation probability (of a chromosome)
# compare with the indpb=0.1 in the previous line toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
MUTPB = 0.2
#initialisation of the GA
population = toolbox.init_population(n=160)
toolbox.evaluate(population, TARGET)
solution = None

number_of_iterations = 0
while len(find_winners(population)) == 0 and inter_time - start_time < MAX_TIME:

    children = toolbox.select(population, len(population), tournsize)

    # Full alternative ---
    # Clone the selected individuals,
    # TODO: test your code without the cloning, print the
    children = list(map(toolbox.clone, children))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(children[::2], children[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)

    for mutant in children:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)

    # ---

    # Shorcut alternative ---
    # children = algorithms.varAnd(offspring, toolbox, 0.7, 0.2)
    # ---

    evaluate_population(children, TARGET)
    population = children

    # Search for the solution
    fitnesses = [ind.fitness.values[0] for ind in population]
    min_fit = min(fitnesses)
    best = population[fitnesses.index(min_fit)]
    if not solution or best.fitness.values[0] < solution.fitness.values[0]:
        solution = best

    inter_time = time.time()

    number_of_iterations += 1

duration = time.time() - start_time

# TODO 4 :) In which case the following line is execuded?
if not solution:
    solution = find_winners(population)[0]

elif duration >= MAX_TIME:
    print('Timeout - solution not found')

else:
    print('Solution found!')

compute_chromosome(solution)

solution.fitness

print(displayable_chromosome(solution))

#print the total time and the number iterations
print(f'Duration: {duration}')
print(f'Number of iterations: {number_of_iterations}')


# Display the final population
def printMatrix(matrix):
    for i, row in enumerate(matrix):
        print(i, ''.join(str(row)))


printMatrix(population)
