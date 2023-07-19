import numbers
import random
import string
from abc import ABC, abstractmethod


class GeneType(ABC):
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
        pass

    @abstractmethod
    def validate(self, n):
        pass


class BinaryType(GeneType):
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, type(self))

    def __str__(self) -> str:
        return "BinaryType()"

    def get_random_val(self):
        return random.randint(0, 1)

    def validate(self, n):
        return n in [0, 1]


class IntType(GeneType):
    def __init__(self, min_val=0, max_val=9) -> None:
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

    def validate(self, n):
        return n in range(self._min_val, self._max_val + 1)


class FloatType(GeneType):
    def __init__(self, min_val=0, max_val=9, ndigits=2) -> None:
        super().__init__()
        self._min_val = min(min_val, max_val)
        self._max_val = max(min_val, max_val)
        self._ndigits = ndigits

    def __str__(self) -> str:
        return f"FloatType(min={self._min_val} max={self._max_val} ndigits={self._ndigits})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self))
            and (self._min_val == __o._min_val)
            and (self._max_val == __o._max_val)
            and (self._ndigits == __o._ndigits)
        )

    def get_random_val(self):
        num = random.random() * (self._max_val - self._min_val) + self._min_val
        return round(num, ndigits=self._ndigits)

    def validate(self, n):
        return isinstance(n, numbers.Number) and (
            self._min_val <= n < self._max_val
        )


class StrType(GeneType):
    def __init__(self, mode="all") -> None:
        super().__init__()
        if mode not in ["all", "lowercase", "uppercase"]:
            raise ValueError("Invalid mode")
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

    def validate(self, n):
        return n in self._data
