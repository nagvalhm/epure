def test_test():
    pass
#buildins
# str
# int, float, complex
# list, tuple, range
# dict
# set, frozenset
# bool
# bytes, bytearray, memoryview
# NoneType

# import types
# types.FunctionType
# types.LambdaType
# types.CodeType
# types.MappingProxyType
# types.SimpleNamespace
# types.CellType
# types.GeneratorType
# types.CoroutineType
# types.AsyncGeneratorType
# types.MethodType
# types.BuiltinFunctionType
# types.BuiltinMethodType
# types.WrapperDescriptorType
# types.MethodWrapperType
# types.MethodDescriptorType
# types.ClassMethodDescriptorType
# types.ModuleType
# types.GetSetDescriptorType
# types.MemberDescriptorType
# types.GenericAlias
# types.UnionType type(int | str)
# types.EllipsisType
# types.NoneType
# types.NotImplementedType

# import typing
# typing.Annotated
# typing.Any
# typing.Callable
# typing.ClassVar
# typing.Concatenate
# typing.Final
# typing.ForwardRef
# typing.Generic
# typing.Literal
# typing.Optional
# typing.ParamSpec
# typing.Protocol
# typing.Tuple
# typing.Type
# typing.TypeVar
# typing.Union

#     # ABCs (from collections.abc).
# typing.AbstractSet  # collections.abc.Set.
# typing.ByteString
# typing.Container
# typing.ContextManager
# typing.Hashable
# typing.ItemsView
# typing.Iterable
# typing.Iterator
# typing.KeysView
# typing.Mapping
# typing.MappingView
# typing.MutableMapping
# typing.MutableSequence
# typing.MutableSet
# typing.Sequence
# typing.Sized
# typing.ValuesView
# typing.Awaitable
# typing.AsyncIterator
# typing.AsyncIterable
# typing.Coroutine
# typing.Collection
# typing.AsyncGenerator
# typing.AsyncContextManager

#     # Structural checks, a.k.a. protocols.
# typing.Reversible
# typing.SupportsAbs
# typing.SupportsBytes
# typing.SupportsComplex
# typing.SupportsFloat
# typing.SupportsIndex
# typing.SupportsInt
# typing.SupportsRound

#     # Concrete collection types.
# typing.ChainMap
# typing.Counter
# typing.Deque
# typing.Dict
# typing.DefaultDict
# typing.List
# typing.OrderedDict
# typing.Set
# typing.FrozenSet
# typing.NamedTuple  # Not really a type.
# typing.TypedDict  # Not really a type.
# typing.Generator

#     # Other concrete types.
# typing.BinaryIO
# typing.IO
# typing.Match
# typing.Pattern
# typing.TextIO

#     # One-off things.
# typing.AnyStr
# typing.cast
# typing.final
# typing.get_args
# typing.get_origin
# typing.get_type_hints
# typing.is_typeddict
# typing.NewType
# typing.no_type_check
# typing.no_type_check_decorator
# typing.NoReturn
# typing.overload
# typing.ParamSpecArgs
# typing.ParamSpecKwargs
# typing.runtime_checkable
# typing.Text
# typing.TYPE_CHECKING
# typing.TypeAlias
# typing.TypeGuard







# @epure()
# class User:
#     pass


# class Note:
#     count = 7
#     note_name:str = 'note'
#     parent:Note
#     owner:User
#     students:List[User]
#     access:Dict[User,int]

# @epure()
# class Result:
#     student:User
#     course:Course
#     datetime:datetime
#     score:int

#     def save(self):
#         res = self.db.execute('select 65')
#         return res

# @epure()
# class Card(Note):
#     passed:bool
#     color:str

# @epure('dbt.akkl.cris')
# class Course:
#     notes:List[Note]
#     results:List[Result]

#     def __uniq__(self):
#         return [(), ()]