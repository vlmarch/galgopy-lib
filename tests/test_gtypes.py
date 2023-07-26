import os
import sys

sys.path.append(os.getcwd())

import pytest

import galgopy.genetypes as genetypes

validation_data = [
    (genetypes.BinaryType(), 0, True),
    (genetypes.BinaryType(), 1, True),
    (genetypes.BinaryType(), 1.2, False),
    (genetypes.BinaryType(), 5, False),
    (genetypes.BinaryType(), -2, False),
    (genetypes.BinaryType(), "a", False),
    (genetypes.IntType(), 0, True),
    (genetypes.IntType(), 9, True),
    (genetypes.IntType(), 1.2, False),
    (genetypes.IntType(), 12, False),
    (genetypes.IntType(), "a", False),
    (genetypes.IntType(8, 4), 5, True),
    (genetypes.FloatType(), 0, True),
    (genetypes.FloatType(), 9, False),
    (genetypes.FloatType(), 1.2, True),
    (genetypes.FloatType(), 12, False),
    (genetypes.FloatType(), "a", False),
    (genetypes.FloatType(8, 4), 5.14, True),
    (genetypes.StrType(), "A", True),
    (genetypes.StrType(), "a", True),
    (genetypes.StrType(), ">", False),
    (genetypes.StrType(), 1.2, False),
    (genetypes.StrType(), 0, False),
    (genetypes.StrType(), 5, False),
    (genetypes.StrType("lowercase"), "A", False),
    (genetypes.StrType("lowercase"), "a", True),
    (genetypes.StrType("uppercase"), "A", True),
    (genetypes.StrType("uppercase"), "a", False),
]


@pytest.mark.parametrize("gen_type, val, expected", validation_data)
def test_validation(gen_type, val, expected):
    assert gen_type.validate(val) == expected


eq_data = [
    (genetypes.BinaryType(), genetypes.BinaryType(), True),
    (genetypes.IntType(), genetypes.IntType(), True),
    (genetypes.IntType(), genetypes.IntType(5, 9), False),
    (genetypes.FloatType(), genetypes.FloatType(), True),
    (genetypes.FloatType(), genetypes.FloatType(9, 0), True),
    (genetypes.FloatType(), genetypes.FloatType(5, 9), False),
    (genetypes.FloatType(), genetypes.FloatType(), False),
    (genetypes.StrType(), genetypes.StrType(), True),
    (genetypes.StrType(), genetypes.StrType("lowercase"), False),
    (genetypes.StrType(), genetypes.StrType("uppercase"), False),
    (genetypes.StrType("lowercase"), genetypes.StrType("uppercase"), False),
    (genetypes.BinaryType(), genetypes.IntType(), False),
    (genetypes.BinaryType(), genetypes.FloatType(), False),
    (genetypes.BinaryType(), genetypes.StrType(), False),
    (genetypes.IntType(), genetypes.FloatType(), False),
    (genetypes.IntType(), genetypes.StrType(), False),
    (genetypes.FloatType(), genetypes.StrType(), False),
    (genetypes.StrType(), genetypes.FloatType(), False),
]


@pytest.mark.parametrize("gen_type1, gen_type2, expected", eq_data)
def test_eq(gen_type1, gen_type2, expected):
    assert (gen_type1 == gen_type2) == expected
