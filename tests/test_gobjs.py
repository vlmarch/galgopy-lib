import os
import sys

import pytest

sys.path.append(os.getcwd())

import galgopy.gtypes as gtypes

validation_data = [
    (gtypes.BinaryType(), 0, True),
    (gtypes.BinaryType(), 1, True),
]


@pytest.mark.parametrize("gen_type, val, expected", validation_data)
def test_validation(gen_type, val, expected):
    assert gen_type.validate(val) == expected
