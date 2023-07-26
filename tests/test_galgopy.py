import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy as galgopy
import galgopy.genetypes as genetypes

validation_data = [
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


@pytest.mark.parametrize("val, gene_type, expected", validation_data)
def test_init_gene(val, gene_type, expected):
    try:
        galgopy.Gene(val, gene_type)
        assert True == expected
    except ValueError:
        assert False == expected
