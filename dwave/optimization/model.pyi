# Copyright 2024 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import collections.abc
import contextlib
import tempfile
import typing

import numpy
import numpy.typing

from dwave.optimization.symbols import *


_ShapeLike: typing.TypeAlias = typing.Union[int, collections.abc.Sequence[int]]


class Model:
    def __init__(self): ...

    @property
    def objective(self) -> ArraySymbol: ...
    @property
    def states(self) -> States: ...

    def add_constraint(self, value: ArraySymbol) -> ArraySymbol: ...
    def binary(self, shape: typing.Optional[_ShapeLike] = None) -> BinaryVariable: ...
    def constant(self, array_like: numpy.typing.ArrayLike) -> Constant: ...
    def decision_state_size(self) -> int: ...

    def disjoint_bit_sets(
        self, primary_set_size: int, num_disjoint_sets: int,
        ) -> tuple[DisjointBitSets, tuple[DisjointBitSet, ...]]: ...

    def disjoint_lists(
        self, primary_set_size: int, num_disjoint_lists: int,
        ) -> tuple[DisjointLists, tuple[DisjointList, ...]]: ...

    def feasible(self, index: int = 0) -> bool: ...

    @classmethod
    def from_file(
        cls,
        file: typing.Union[typing.BinaryIO, collections.abc.ByteString, str],
        *,
        check_header: bool = True,
        ) -> Model: ...

    def integer(
        self,
        shape: typing.Optional[_ShapeLike] = None,
        lower_bound: typing.Optional[int] = None,
        upper_bound: typing.Optional[int] = None,
        ) -> IntegerVariable: ...

    def into_file(
        self,
        file: typing.Union[typing.BinaryIO, collections.abc.ByteString, str],
        *,
        max_num_states: int = 0,
        only_decision: bool = False,
        ): ...

    def is_locked(self) -> bool: ...
    def iter_constraints(self) -> collections.abc.Iterator[ArraySymbol]: ...
    def iter_decisions(self) -> collections.abc.Iterator[Symbol]: ...
    def iter_symbols(self) -> collections.abc.Iterator[Symbol]: ...
    def list(self, n: int) -> ListVariable: ...
    def lock(self) -> contextlib.AbstractContextManager: ...
    def minimize(self, value: ArraySymbol): ...
    def num_constraints(self) -> int: ...
    def num_decisions(self) -> int: ...
    def num_nodes(self) -> int: ...
    def num_symbols(self) -> int: ...

    # dev note: this is underspecified, but it would be quite complex to fully
    # specify the linear/quadratic so let's leave it alone for now.
    def quadratic_model(self, x: ArraySymbol, quadratic, linear=None) -> QuadraticModel: ...

    def remove_unused_symbols(self) -> int: ...

    def set(
        self,
        n: int,
        min_size: int = 0,
        max_size: typing.Optional[int] = None,
        ) -> SetVariable: ...

    def state_size(self) -> int: ...

    def to_file(
        self,
        *,
        max_num_states: int = 0,
        only_decision: bool = False,
        ) -> typing.BinaryIO: ...

    # networkx might not be installed, so we just say we return an object.
    def to_networkx(self) -> object: ...

    def unlock(self): ...


class Symbol:
    def __init__(self, *args, **kwargs) -> typing.NoReturn: ...
    def equals(self, other: Symbol) -> bool: ...
    def expired(self) -> bool: ...
    def has_state(self, index: int = 0) -> bool: ...
    def id(self) -> int: ...
    def iter_predecessors(self) -> collections.abc.Iterator[Symbol]: ...
    def iter_successors(self) -> collections.abc.Iterator[Symbol]: ...
    def maybe_equals(self, other: Symbol) -> int: ...
    def reset_state(self, index: int): ...
    def shares_memory(self, other: Symbol) -> bool: ...
    def state_size(self) -> int: ...
    def topological_index(self) -> int: ...


class ArraySymbol(Symbol):
    def __init__(self, *args, **kwargs) -> typing.NoReturn: ...
    def __abs__(self) -> Absolute: ...
    def __add__(self, rhs: ArraySymbol) -> Add: ...
    def __bool__(self) -> typing.NoReturn: ...
    def __eq__(self, rhs: ArraySymbol) -> Equal: ...

    def __getitem__(
        self,
        index: typing.Union[Symbol, int, slice, tuple],
        ) -> typing.Union[AdvancedIndexing, BasicIndexing, Permutation]: ...

    def __iadd__(self, rhs: ArraySymbol) -> NaryAdd: ...
    def __imul__(self, rhs: ArraySymbol) -> NaryMultiply: ...
    def __le__(self, rhs: ArraySymbol) -> LessEqual: ...
    def __mod__(self, rhs: ArraySymbol) -> Modulus: ...
    def __mul__(self, rhs: ArraySymbol) -> Multiply: ...
    def __neg__(self) -> Negative: ...
    def __pow__(self, exponent: int) -> ArraySymbol: ...
    def __sub__(self, rhs: ArraySymbol) -> Subtract: ...
    def __truediv__(self, rhs: ArraySymbol) -> Divide: ...
    def all(self) -> All: ...
    def any(self) -> Any: ...
    def max(self) -> Max: ...
    def min(self) -> Min: ...
    def ndim(self) -> int: ...
    def prod(self) -> Prod: ...
    def reshape(self, shape: _ShapeLike) -> Reshape: ...
    def shape(self) -> tuple[int, ...]: ...
    def size(self) -> typing.Union[int, Size]: ...
    def sqrt(self) -> ArraySymbol: ...
    def state(self, index: int = 0, *, copy: bool = True) -> numpy.ndarray: ...
    def state_size(self) -> int: ...
    def strides(self) -> tuple[int, ...]: ...
    def sum(self, axis: typing.Optional[int] = None) -> typing.Union[Sum, PartialSum]: ...
