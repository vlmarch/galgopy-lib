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


################################################################################
