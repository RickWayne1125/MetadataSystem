from __future__ import annotations

import abc
from typing import Any, List, Set


class Table(object):
    """Class for accessing tables."""

    def __init__(self, file: str, name: str, desc: str, fields: List[Field]):
        pass  # TODO

    @staticmethod
    def load(file: str) -> Table:
        """Load metadata from a file on the disk."""
        pass  # TODO

    @staticmethod
    def save(table: Table):
        """Save a table back to its related file."""
        pass  # TODO

    @property
    def name(self) -> str:
        """Access the table's name. It cannot be modified since it's related to the filename."""
        return self._name

    @property
    def desc(self) -> str:
        """Access the table's description text."""
        return self._desc

    @desc.setter
    def desc(self, desc: str):
        self._desc = desc

    @property
    def fields(self) -> List[Field]:
        """Access the table's fields. Changes should be committed by calling :func:`Table.save()`."""
        return self._fields


class Field(object):
    """Class for accessing fields."""

    def __init__(self, name: str, desc: str, constraints: Set[Constraint]):
        pass  # TODO

    @property
    def name(self) -> str:
        """Access the field's name."""
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def desc(self) -> str:
        """Access the field's description text."""
        return self._desc

    @desc.setter
    def desc(self, desc: str):
        self._desc = desc

    @property
    def type(self) -> Type:
        """Access the constraint representing the field's type."""
        return self._type

    @type.setter
    def type(self, type: Type):
        self._type = type  # TODO

    @property
    def constraints(self) -> Set[Constraint]:
        """Access the field's constraints, including the field's type."""
        return self._constraints


class Constraint(object, metaclass=abc.ABCMeta):
    """Super class of all constraints. Extend this class to create new types of constraints."""

    def __init_subclass__(cls, **kwargs):
        pass  # TODO

    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def verify(self, current: Any, whole: List[Any]) -> bool:
        """Check whether the constraint is fulfilled, giving the current record and the whole list of records of the
        corresponding field."""
        pass


class Type(Constraint, metaclass=abc.ABCMeta):
    """Super class of all data types. Extend this class to create new data types"""

    def __init_subclass__(cls, **kwargs):
        pass  # TODO

    @abc.abstractmethod
    @property
    def length(self) -> int:
        """How many bytes should this data type occupy. If it is not determined, returns -1."""
        pass
