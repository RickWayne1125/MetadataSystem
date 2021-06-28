from __future__ import annotations

import struct
from typing import Any, List, Set

from backend import Constraint, Type


class Integer(Type):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, int)

    @property
    def length(self) -> int:
        return struct.calcsize('P')


class Real(Type):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, int) or isinstance(current, float)

    @property
    def length(self) -> int:
        return struct.calcsize('d')


class Char(Type):
    # noinspection PyShadowingBuiltins
    def __init__(self, len: int):
        super().__init__(len=len)
        self._len = len

    def __hash__(self) -> int:
        return hash(self.__class__) ^ hash(self._len)

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, str) and len(current) <= self._len

    @property
    def length(self) -> int:
        return self._len


class Text(Type):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, str)

    @property
    def length(self) -> int:
        return -1


class AutoIncrement(Constraint):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return True

    @property
    def implicated_constraints(self) -> Set[Constraint]:
        return {self, Integer()}


class NotNull(Constraint):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is not None


class Unique(Constraint):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return whole.count(current) == 1


class PrimaryKey(Constraint):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return True  # TODO Actually verifies uniqueness.

    @property
    def implicated_constraints(self) -> Set[Constraint]:
        return {self, NotNull(), Unique()}


class ForeignKey(Constraint):
    def __init__(self, table: str):
        super().__init__(table=table)
        self._table = table

    def __hash__(self) -> int:
        return hash(self.__class__) ^ hash(self._table)

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return True  # TODO Actually verifies it.
