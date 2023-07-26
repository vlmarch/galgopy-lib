# -*- coding: utf-8 -*-
"""Module with gene types.

Module includes:
    AbstractGeneType
    BinaryType
    IntType
    FloatType
    StrType
    CostumeType

"""

import numbers
import random
import string
from abc import ABC, abstractmethod


class AbstractGeneType(ABC):
    """Abstract Gene type."""

    def __init__(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass

    @abstractmethod
    def get_random_val(self):
        """Generates a random value for the gene type.

        Returns:
            Random value.
        """

    @abstractmethod
    def validate(self, val) -> bool:
        """Validation of value. Whether it corresponds to a given type.

        Args:
            n : Value to be verified.

        Returns:
            bool: True if it corresponds to a type. False - if not.
        """


class BinaryType(AbstractGeneType):
    """Implementation of binary gene type. Possible options: 0 or 1."""

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, type(self))

    def __str__(self) -> str:
        return "BinaryType()"

    def get_random_val(self):
        return random.randint(0, 1)

    def validate(self, val):
        return val in [0, 1]


class IntType(AbstractGeneType):
    """Implementation of integer gene type."""

    def __init__(self, min_val=0, max_val=9) -> None:
        """Integer gene type.

        Args:
            min_val (int, optional): Minimum value. Defaults to 0.
            max_val (int, optional): Maximum value. Defaults to 9.
        """
        super().__init__()
        self._min_val = min(min_val, max_val)
        self._max_val = max(min_val, max_val)

    def __str__(self) -> str:
        return f"IntType(min={self._min_val} max={self._max_val})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self))
            and (self._min_val == __o._min_val)
            and (self._max_val == __o._max_val)
        )

    def get_random_val(self):
        return random.randint(self._min_val, self._max_val)

    def validate(self, val):
        return val in range(self._min_val, self._max_val + 1)


class FloatType(AbstractGeneType):
    """Implementation of float gene type. Possible options: [min_val, max_val)."""

    def __init__(self, min_val=0, max_val=1) -> None:
        """Float gene type.

        Args:
            min_val (int, optional): Minimum value. Defaults to 0.
            max_val (int, optional): Maximum value. Defaults to 1.
        """
        super().__init__()
        self._min_val = min(min_val, max_val)
        self._max_val = max(min_val, max_val)

    def __str__(self) -> str:
        return f"FloatType(min={self._min_val} max={self._max_val})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self))
            and (self._min_val == __o._min_val)
            and (self._max_val == __o._max_val)
        )

    def get_random_val(self):
        num = random.random() * (self._max_val - self._min_val) + self._min_val
        return num

    def validate(self, val):
        return isinstance(val, numbers.Number) and (
            self._min_val <= val < self._max_val
        )


class StrType(AbstractGeneType):
    """Implementation of string gene type."""

    def __init__(self, mode="all") -> None:
        """_summary_

        Args:
            mode (str, optional): String type mode.
            Modes of choice: 'all', 'lowercase', 'uppercase'. Defaults to "all".

        Raises:
            ValueError: Incorrect mode.
        """
        super().__init__()
        if mode not in ["all", "lowercase", "uppercase"]:
            raise ValueError(
                f"Incorrect mode: '{mode}'. Modes of choice: 'all', 'lowercase', 'uppercase'."
            )
        self._mode = mode
        if self._mode == "lowercase":
            self._data = list(string.ascii_lowercase)
        elif self._mode == "uppercase":
            self._data = list(string.ascii_uppercase)
        else:
            self._data = list(string.ascii_letters)

    def __str__(self) -> str:
        return f"StrType(mode={self._mode})"

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, type(self)) and self._data == __o._data

    def get_random_val(self):
        return random.choice(self._data)

    def validate(self, val):
        return val in self._data


class CostumeType(AbstractGeneType):
    """Implementation of costume gene type."""

    def __init__(self, costume_data: list) -> None:
        """Costume gene type.

        Args:
            costume_data (list): List of possible gene values.
        """
        super().__init__()
        self._costume_data = costume_data

    def __str__(self) -> str:
        return "CostumeType()"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self))
            and self._costume_data == __o._costume_data
        )

    def get_random_val(self):
        return random.choice(self._costume_data)

    def validate(self, val):
        return val in self._costume_data
