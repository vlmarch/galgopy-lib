import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy as galgopy
import galgopy.crossover as crossover
import galgopy.genetypes as genetypes

init_multipoint_data = [
    (0, False),
    (1, False),
    (2, True),
    (5, True),
]


@pytest.mark.parametrize("cut_points_count, expected", init_multipoint_data)
def test_init_multipoint(cut_points_count, expected):
    try:
        crossover.MultipointCrossover(cut_points_count=cut_points_count)
        assert True == expected
    except ValueError:
        assert False == expected


init_intermediaterecombination_data = [
    (0, True),
    (-1, False),
    (0.5, True),
    (1, True),
    (5, False),
]


@pytest.mark.parametrize("a, expected", init_intermediaterecombination_data)
def test_init_intermediaterecombination(a, expected):
    try:
        crossover.IntermediateRecombinationCrossover(a=a)
        assert True == expected
    except ValueError:
        assert False == expected


generate_new_population_intermediaterecombination_data = [
    ([galgopy.Chromosome()], False),
    ([galgopy.Chromosome(), galgopy.Chromosome()], False),
    (
        [
            galgopy.Chromosome.generate_random_chromosome(
                galgopy.ChromosomeTemplate(
                    [genetypes.IntType(), genetypes.StrType()]
                )
            ),
            galgopy.Chromosome.generate_random_chromosome(
                galgopy.ChromosomeTemplate(
                    [genetypes.IntType(), genetypes.StrType()]
                )
            ),
        ],
        False,
    ),
    (
        [
            galgopy.Chromosome.generate_random_chromosome(
                galgopy.ChromosomeTemplate(
                    [genetypes.FloatType(), genetypes.FloatType()]
                )
            ),
            galgopy.Chromosome.generate_random_chromosome(
                galgopy.ChromosomeTemplate(
                    [genetypes.FloatType(), genetypes.FloatType()]
                )
            ),
        ],
        True,
    ),
]


@pytest.mark.parametrize(
    "parents_list, expected",
    generate_new_population_intermediaterecombination_data,
)
def test_generate_new_population_intermediaterecombination(
    parents_list, expected
):
    parents = galgopy.Population(parents_list)
    for p in parents:
        p.proportional_fitness = 1 / len(parents)
    try:
        c = crossover.IntermediateRecombinationCrossover()
        c.generate_new_population(parents, 5)
        assert True == expected
    except ValueError:
        assert False == expected
