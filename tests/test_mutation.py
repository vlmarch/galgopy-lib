import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy
import galgopy.genetypes as genetypes
import galgopy.mutation as mutation

apply_swapmutation_data = [
    (galgopy.ChromosomeTemplate(), True),
    (
        galgopy.ChromosomeTemplate([genetypes.StrType(), genetypes.IntType()]),
        False,
    ),
    (
        galgopy.ChromosomeTemplate(
            [genetypes.IntType(-5), genetypes.IntType()]
        ),
        False,
    ),
    (
        galgopy.ChromosomeTemplate([genetypes.IntType(), genetypes.IntType()]),
        True,
    ),
]


@pytest.mark.parametrize("chromosome_tmplt, expected", apply_swapmutation_data)
def test_apply_swapmutation(chromosome_tmplt, expected):
    chromosome = galgopy.Chromosome.generate_random_chromosome(chromosome_tmplt)
    m = mutation.SwapMutation(1)
    try:
        m.apply_mutation(chromosome)
        assert True == expected
    except ValueError:
        assert False == expected
