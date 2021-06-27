from __future__ import annotations

import struct
from typing import Any, List

from backend import Constraint, Type


class Integer(Type):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, int)

    @property
    def length(self) -> int:
        return struct.calcsize('P')


class Char(Type):
    # noinspection PyShadowingBuiltins
    def __init__(self, len: int):
        super().__init__(len=len)
        self._len = len

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is None or isinstance(current, str) and len(current) <= self._len

    @property
    def length(self) -> int:
        return self._len


class NotNull(Constraint):
    def __init__(self):
        super().__init__()

    def verify(self, current: Any, whole: List[Any]) -> bool:
        return current is not None
