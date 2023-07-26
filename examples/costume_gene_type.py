import os
import sys

sys.path.append(os.getcwd())

import string

from galgopy import GA, ChromosomeTemplate, Population
from galgopy.gtypes import CostumeType

STR = "To be, or not to be"


def fitness_calc(chromosome):
    return sum([g.value == l for g, l in zip(chromosome.genes_list, list(STR))])


costume_type = CostumeType(list(string.printable))
chromosome_template = ChromosomeTemplate([costume_type] * len(STR))

population = Population.generate_random_population(
    population_size=100, chromosome_tmplt=chromosome_template
)

ga = GA(
    population=population,
    fitness_func=fitness_calc,
    expected_fitness=len(STR),
    max_generations=10000,
)
ga.start()
