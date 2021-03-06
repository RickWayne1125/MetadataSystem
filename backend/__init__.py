from __future__ import annotations

import abc
import inspect
import json
import re
from typing import Any, Dict, List, Set, Type as Class


def _to_unified_name(cls: Class) -> str:
    return '_'.join(re.findall(r'[A-Z][a-z]*', cls.__name__)).upper()


class Table(object):
    """Class for accessing tables."""

    def __init__(self, file: str, name: str, desc: str, fields: List[Field]):
        self._file = file
        self._name = name
        self._desc = desc
        self._fields = fields

    @staticmethod
    def load(file: str) -> Table:
        """Load metadata from a file on the disk."""
        with open(file, 'r') as f:
            table_meta = json.load(f)
        return Table(
            file,
            table_meta['name'],
            table_meta['desc'],
            [
                Field(
                    field_meta['name'],
                    field_meta['desc'],
                    set([
                        Constraint.registry[constraint_meta]()
                        if isinstance(constraint_meta, str) else
                        Constraint.registry[constraint_meta['type']](**constraint_meta['args'])
                        for constraint_meta in field_meta['constraints']
                    ])
                )
                for field_meta in table_meta['fields']
            ]
        )

    @staticmethod
    def save(table: Table):
        """Save a table back to its related file."""
        obj = {
            'name': table.name,
            'desc': table.desc,
            'fields': [
                {
                    'name': field.name,
                    'desc': field.desc,
                    'constraints': [
                        _to_unified_name(constraint.__class__)
                        if len(constraint.args) == 0 else
                        {'type': _to_unified_name(constraint.__class__), 'args': constraint.args}
                        for constraint in field.constraints
                    ]
                }
                for field in table.fields
            ]
        }
        with open(table._file, 'w') as f:
            json.dump(obj, f)

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

    class __ConstraintSet(set):
        def add(self, element: Constraint):
            super().update(element.implicated_constraints)

    def __init__(self, name: str, desc: str, constraints: Set[Constraint]):
        self._name = name
        self._desc = desc
        self._constraints = Field.__ConstraintSet()

        for c in constraints:
            self._constraints.add(c)
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
            Constraint.registry[_to_unified_name(cls)] = cls

    def __eq__(self, other: Constraint):
        if self.__class__ != other.__class__:
            return False
        return self._args == other._args

    def __hash__(self) -> int:
        return hash(self.__class__)

    @abc.abstractmethod
    def __init__(self, **kwargs):
        self._args = kwargs

    @abc.abstractmethod
    def verify(self, current: Any, whole: List[Any]) -> bool:
        """Check whether the constraint is fulfilled, giving the current record and the whole list of records of the
        corresponding field."""
        pass

    @property
    def args(self) -> Dict[str, Any]:
        """Access the specific arguments of this constraint."""
        return self._args

    @property
    def implicated_constraints(self) -> Set[Constraint]:
        """Get all implicated constraints, for example, PRIMARY_KEY to {NOT_NULL, UNIQUE}."""
        return {self}


class Type(Constraint, metaclass=abc.ABCMeta):
    """Super class of all data types. Extend this class to create new data types"""

    def __init_subclass__(cls, **kwargs):
        if not inspect.isabstract(cls):
            Constraint.registry[_to_unified_name(cls)] = cls

    @property
    @abc.abstractmethod
    def length(self) -> int:
        """How many bytes should this data type occupy. If it is not determined, returns -1."""
        pass
