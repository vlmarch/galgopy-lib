import os
import sys

sys.path.append(os.getcwd())

import math

from galgopy import GA, ChromosomeTemplate, Population
from galgopy.genetypes import FloatType


def fitness_calc(chromosome):
    x = chromosome[0].value
    y = chromosome[1].value
    return math.sin(x + y) + (x - y) ** 2 - 1.5 * x + 2.5 * y + 1


ct = ChromosomeTemplate([FloatType(-1.5, 4), FloatType(-3, 4)])

population = Population.generate_random_population(
    population_size=10, chromosome_tmplt=ct
)

ga = GA(
    population=population,
    fitness_func=fitness_calc,
    fitness_mode="minimize",
    max_generations=10000,
)
ga.start()
