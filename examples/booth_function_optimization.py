import os
import sys

sys.path.append(os.getcwd())

from galgopy import GA, ChromosomeTemplate, Population
from galgopy.genetypes import FloatType


def fitness_calc(chromosome):
    x = chromosome[0].value
    y = chromosome[1].value
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


ct = ChromosomeTemplate([FloatType(-10, 10), FloatType(-10, 10)])

population = Population.generate_random_population(
    population_size=10, chromosome_tmplt=ct
)

ga = GA(
    population=population,
    fitness_func=fitness_calc,
    fitness_mode="minimize",
    expected_fitness=0,
    max_generations=10000,
)
ga.start()
