import os
import sys

sys.path.append(os.getcwd())

from galgopy import GA, ChromosomeTemplate, Population

population = Population.generate_random_population(
    population_size=10, chromosome_tmplt=ChromosomeTemplate()
)

ga = GA(
    population=population,
    fitness_func=lambda chromosome: sum([g.value for g in chromosome]),
    expected_fitness=8,
)
ga.start()
