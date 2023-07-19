import os
import sys

import pytest

sys.path.append(os.getcwd())

import galgopy.gtypes as gtypes

validation_data = [
    (gtypes.BinaryType(), 0, True),
    (gtypes.BinaryType(), 1, True),
    (gtypes.BinaryType(), 1.2, False),
    (gtypes.BinaryType(), 5, False),
    (gtypes.BinaryType(), -2, False),
    (gtypes.BinaryType(), "a", False),
    (gtypes.IntType(), 0, True),
    (gtypes.IntType(), 9, True),
    (gtypes.IntType(), 1.2, False),
    (gtypes.IntType(), 12, False),
    (gtypes.IntType(), "a", False),
    (gtypes.IntType(8, 4), 5, True),
    (gtypes.FloatType(), 0, True),
    (gtypes.FloatType(), 9, False),
    (gtypes.FloatType(), 1.2, True),
    (gtypes.FloatType(), 12, False),
    (gtypes.FloatType(), "a", False),
    (gtypes.FloatType(8, 4), 5.14, True),
    (gtypes.StrType(), "A", True),
    (gtypes.StrType(), "a", True),
    (gtypes.StrType(), ">", False),
    (gtypes.StrType(), 1.2, False),
    (gtypes.StrType(), 0, False),
    (gtypes.StrType(), 5, False),
    (gtypes.StrType("lowercase"), "A", False),
    (gtypes.StrType("lowercase"), "a", True),
    (gtypes.StrType("uppercase"), "A", True),
    (gtypes.StrType("uppercase"), "a", False),
]


@pytest.mark.parametrize("gen_type, val, expected", validation_data)
def test_validation(gen_type, val, expected):
    assert gen_type.validate(val) == expected


eq_data = [
    (gtypes.BinaryType(), gtypes.BinaryType(), True),
    (gtypes.IntType(), gtypes.IntType(), True),
    (gtypes.IntType(), gtypes.IntType(5, 9), False),
    (gtypes.FloatType(), gtypes.FloatType(), True),
    (gtypes.FloatType(), gtypes.FloatType(9, 0), True),
    (gtypes.FloatType(), gtypes.FloatType(5, 9, 3), False),
    (gtypes.FloatType(), gtypes.FloatType(ndigits=3), False),
    (gtypes.StrType(), gtypes.StrType(), True),
    (gtypes.StrType(), gtypes.StrType("lowercase"), False),
    (gtypes.StrType(), gtypes.StrType("uppercase"), False),
    (gtypes.StrType("lowercase"), gtypes.StrType("uppercase"), False),
    (gtypes.BinaryType(), gtypes.IntType(), False),
    (gtypes.BinaryType(), gtypes.FloatType(), False),
    (gtypes.BinaryType(), gtypes.StrType(), False),
    (gtypes.IntType(), gtypes.FloatType(), False),
    (gtypes.IntType(), gtypes.StrType(), False),
    (gtypes.FloatType(), gtypes.StrType(), False),
    (gtypes.StrType(), gtypes.FloatType(), False),
]


@pytest.mark.parametrize("gen_type1, gen_type2, expected", eq_data)
def test_eq(gen_type1, gen_type2, expected):
    assert (gen_type1 == gen_type2) == expected
