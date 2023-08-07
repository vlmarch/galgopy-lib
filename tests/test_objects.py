import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy as galgopy
import galgopy.genetypes as genetypes

init_gene_data = [
    (1, genetypes.BinaryType(), True),
    (0, genetypes.BinaryType(), True),
    (0.5, genetypes.BinaryType(), False),
    (5, genetypes.BinaryType(), False),
    ("a", genetypes.BinaryType(), False),
    (0, genetypes.IntType(), True),
    (0.5, genetypes.IntType(), False),
    (5, genetypes.IntType(), True),
    ("a", genetypes.IntType(), False),
    (0.5, genetypes.StrType(), False),
    (5, genetypes.StrType(), False),
    ("a", genetypes.StrType(), True),
    ("a", genetypes.StrType("lowercase"), True),
    ("A", genetypes.StrType("lowercase"), False),
    ("a", genetypes.StrType("uppercase"), False),
    ("A", genetypes.StrType("uppercase"), True),
    ("*", genetypes.StrType(), False),
    ("*", genetypes.CostumeType(["*", "a", 1]), True),
    ("a", genetypes.CostumeType(["*", "a", 1]), True),
    ("A", genetypes.CostumeType(["*", "a", 1]), False),
]


@pytest.mark.parametrize("val, gene_type, expected", init_gene_data)
def test_init_gene(val, gene_type, expected):
    try:
        galgopy.Gene(val, gene_type)
        assert True == expected
    except ValueError:
        assert False == expected


init_ct_data = [
    ([], False),
    ([1, 2], False),
    ([genetypes.BinaryType()], True),
    ([genetypes.BinaryType(), 1], False),
    ([genetypes.BinaryType(), genetypes.IntType(), genetypes.StrType()], True),
]


@pytest.mark.parametrize("types_list, expected", init_ct_data)
def test_init_chromosometemplate(types_list, expected):
    try:
        galgopy.ChromosomeTemplate(types_list)
        assert True == expected
    except ValueError:
        assert False == expected


eq_ct_data = [
    ([genetypes.BinaryType()], [genetypes.BinaryType()], True),
    (
        [genetypes.BinaryType(), genetypes.IntType()],
        [genetypes.BinaryType(), genetypes.IntType(max_val=20)],
        False,
    ),
    (
        [genetypes.BinaryType(), genetypes.IntType()],
        [genetypes.BinaryType(), genetypes.StrType()],
        False,
    ),
]


@pytest.mark.parametrize("types_list1, types_list2, expected", eq_ct_data)
def test_eq_chromosometemplate(types_list1, types_list2, expected):
    ct1 = galgopy.ChromosomeTemplate(types_list1)
    ct2 = galgopy.ChromosomeTemplate(types_list2)
    assert (ct1 == ct2) == expected


same_types_ct_data = [
    ([genetypes.BinaryType()], True),
    ([genetypes.BinaryType(), genetypes.BinaryType()], True),
    ([genetypes.BinaryType(), genetypes.IntType(), genetypes.StrType()], False),
    ([genetypes.IntType(0, 2), genetypes.IntType()], False),
]


@pytest.mark.parametrize("types_list, expected", same_types_ct_data)
def test_same_types_ct(types_list, expected):
    ct = galgopy.ChromosomeTemplate(types_list)
    assert ct.are_same_types() == expected


types_of_class_ct_data = [
    ([genetypes.BinaryType()], genetypes.BinaryType, True),
    ([genetypes.IntType(), genetypes.IntType()], genetypes.IntType, True),
    ([genetypes.IntType(0, 2), genetypes.IntType()], genetypes.IntType, True),
    ([genetypes.IntType(), genetypes.BinaryType()], genetypes.IntType, False),
    ([genetypes.IntType(), genetypes.IntType()], genetypes.BinaryType, False),
]


@pytest.mark.parametrize(
    "types_list, type_class, expected", types_of_class_ct_data
)
def test_types_of_class_ct(types_list, type_class, expected):
    ct = galgopy.ChromosomeTemplate(types_list)
    assert ct.types_of_class(type_class) == expected


chromosome_init_data = [
    ([galgopy.Gene()], True),
    ([galgopy.Gene(1, genetypes.IntType()), galgopy.Gene()], True),
    ([], False),
    ([galgopy.Gene(), 1], False),
    ([galgopy.Gene(), "Gene"], False),
]


@pytest.mark.parametrize("gene_list, expected", chromosome_init_data)
def test_init_chromosome(gene_list, expected):
    try:
        galgopy.Chromosome(gene_list)
        assert True == expected
    except ValueError:
        assert False == expected


chromosome_len_data = [
    ([galgopy.Gene()], 1),
    ([galgopy.Gene(1, genetypes.IntType()), galgopy.Gene()], 2),
]


@pytest.mark.parametrize("gene_list, expected", chromosome_len_data)
def test_chromosome_len(gene_list, expected):
    chromosome = galgopy.Chromosome(gene_list)
    assert len(chromosome) == expected


population_init_data = [
    ([], False),
    ([galgopy.Chromosome(), 1], False),
    ([galgopy.Chromosome(), "Chromosome"], False),
    ([galgopy.Chromosome()], True),
    ([galgopy.Chromosome(), galgopy.Chromosome()], True),
    (
        [
            galgopy.Chromosome(),
            galgopy.Chromosome.generate_random_chromosome(
                galgopy.ChromosomeTemplate(
                    [genetypes.IntType(), genetypes.StrType()]
                )
            ),
        ],
        False,
    ),
]


@pytest.mark.parametrize("chromosome_list, expected", population_init_data)
def test_init_population(chromosome_list, expected):
    try:
        galgopy.Population(chromosome_list)
        assert True == expected
    except ValueError:
        assert False == expected


population_len_data = [
    ([galgopy.Chromosome()], 1),
    ([galgopy.Chromosome(), galgopy.Chromosome()], 2),
]


@pytest.mark.parametrize("chromosome_list, expected", population_len_data)
def test_population_len(chromosome_list, expected):
    population = galgopy.Population(chromosome_list)
    assert len(population) == expected


chromosome_list = [
    galgopy.Chromosome([galgopy.Gene(1), galgopy.Gene(1), galgopy.Gene(1)]),
    galgopy.Chromosome([galgopy.Gene(1), galgopy.Gene(), galgopy.Gene()]),
    galgopy.Chromosome([galgopy.Gene(), galgopy.Gene(), galgopy.Gene()]),
]

population_fitness_data1 = [
    (chromosome_list, lambda x: sum([a.value for a in x]), "maximize", True),
    (chromosome_list, lambda x: sum([a.value for a in x]), "minimize", True),
    (chromosome_list, lambda x: sum([a.value for a in x]), "random", False),
]


@pytest.mark.parametrize(
    "chromosome_list, func, mode, expected", population_fitness_data1
)
def test_population_fitness1(chromosome_list, func, mode, expected):
    population = galgopy.Population(chromosome_list)
    try:
        population.fitness(func, mode)
        assert True == expected
    except ValueError:
        assert False == expected


population_fitness_data2 = [
    (chromosome_list, lambda x: sum([a.value for a in x]), "maximize", 3),
    (chromosome_list, lambda x: sum([a.value for a in x]), "minimize", 0),
]


@pytest.mark.parametrize(
    "chromosome_list, func, mode, expected", population_fitness_data2
)
def test_population_fitness2(chromosome_list, func, mode, expected):
    population = galgopy.Population(chromosome_list)
    population.fitness(func, mode)
    assert population[0].fitness == expected


population_get_parents_data1 = [
    (chromosome_list, 0, False),
    (chromosome_list, 2, True),
    (chromosome_list, 3, True),
    (chromosome_list, 8, False),
]


@pytest.mark.parametrize(
    "chromosome_list, parents_count, expected", population_get_parents_data1
)
def test_get_parents_data1(chromosome_list, parents_count, expected):
    population = galgopy.Population(chromosome_list)
    population.fitness(lambda x: sum([a.value for a in x]), "maximize")
    try:
        population.get_parents(parents_count)
        assert True == expected
    except ValueError:
        assert False == expected


chromosome_list2 = [
    galgopy.Chromosome([galgopy.Gene(-0.75, genetypes.FloatType(-1))]),
    galgopy.Chromosome([galgopy.Gene(0.25, genetypes.FloatType(-1))]),
    galgopy.Chromosome([galgopy.Gene(0, genetypes.FloatType(-1))]),
]


population_get_parents_data2 = [
    (
        chromosome_list,
        lambda x: sum([a.value for a in x]),
        "maximize",
        3,
        3 / 4,
    ),
    (
        chromosome_list,
        lambda x: sum([a.value for a in x]),
        "minimize",
        3,
        3 / 5,
    ),
    (
        chromosome_list2,
        lambda x: sum([a.value for a in x]),
        "maximize",
        2,
        1,
    ),
    (
        chromosome_list2,
        lambda x: sum([a.value for a in x]),
        "minimize",
        2,
        1,
    ),
    (
        chromosome_list2,
        lambda x: sum([a.value for a in x]),
        "maximize",
        3,
        1 / 1.75,
    ),
    (
        chromosome_list2,
        lambda x: sum([a.value for a in x]),
        "minimize",
        3,
        1 / 1.25,
    ),
]


@pytest.mark.parametrize(
    "chromosome_list, func, mode, parents_count, expected",
    population_get_parents_data2,
)
def test_get_parents_data2(
    chromosome_list, func, mode, parents_count, expected
):
    population = galgopy.Population(chromosome_list)
    population.fitness(func, mode)
    parents = population.get_parents(parents_count)
    for p in parents:
        print(p.proportional_fitness)
    assert parents[0].proportional_fitness == expected
