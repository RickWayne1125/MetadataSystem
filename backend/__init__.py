from __future__ import annotations

import abc
import inspect
import re
from typing import Any, Dict, List, Set, Type as Class


class Table(object):
    """Class for accessing tables."""

    def __init__(self, file: str, name: str, desc: str, fields: List[Field]):
        self._file = open(file, 'w')
        self._name = name
        self._desc = desc
        self._fields = fields

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
        self._name = name
        self._desc = desc
        self._constraints = constraints

        types = [x for x in self._constraints if isinstance(x, Type)]
        if len(types) != 1:
            raise Exception('Expected one and only one type constraint')  # TODO Unify exceptions.
        self._type = types[0]

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
        self._constraints.remove(self._type)
        self._type = type
        self._constraints.add(type)

    @property
    def constraints(self) -> Set[Constraint]:
        """Access the field's constraints, including the field's type."""
        return self._constraints


class Constraint(object, metaclass=abc.ABCMeta):
    """Super class of all constraints. Extend this class to create new types of constraints."""

    registry: Dict[str, Class[Constraint]] = {}

    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls):
            Constraint.registry['_'.join(re.findall(r'[A-Z][a-z]*', cls.__name__)).upper()] = cls

    @abc.abstractmethod
    def verify(self, current: Any, whole: List[Any]) -> bool:
        """Check whether the constraint is fulfilled, giving the current record and the whole list of records of the
        corresponding field."""
        pass


class Type(Constraint, metaclass=abc.ABCMeta):
    """Super class of all data types. Extend this class to create new data types"""

    registry: Dict[str, Class[Type]] = {}

    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls):
            Type.registry['_'.join(re.findall(r'[A-Z][a-z]*', cls.__name__)).upper()] = cls

    @property
    @abc.abstractmethod
    def length(self) -> int:
        """How many bytes should this data type occupy. If it is not determined, returns -1."""
        pass
