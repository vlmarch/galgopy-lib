import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy as galgopy
import galgopy.gtypes as gtypes

validation_data = [
    (1, gtypes.BinaryType(), True),
    (0, gtypes.BinaryType(), True),
    (0.5, gtypes.BinaryType(), False),
    (5, gtypes.BinaryType(), False),
    ("a", gtypes.BinaryType(), False),
    (0, gtypes.IntType(), True),
    (0.5, gtypes.IntType(), False),
    (5, gtypes.IntType(), True),
    ("a", gtypes.IntType(), False),
]


@pytest.mark.parametrize("val, gene_type, expected", validation_data)
def test_init_gene(val, gene_type, expected):
    try:
        galgopy.Gene(val, gene_type)
        assert True == expected
    except ValueError:
        assert False == expected
