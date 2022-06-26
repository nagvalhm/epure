
from typing import *
from .ecommand import ECommand
from ..node.node import *
import inspect
import ast
from ast import Attribute, Constant
# from dill.source import getsource

class FileCommand(ECommand):
    arr: List[str] = None
    def __init__(self, foo:Callable[[Node],Any]) -> None:
        source = self._get_source(foo)        
        # if 'lambda' in source:
        #     lambda_position = source.index('lambda')
        #     source = source[lambda_position:]

        func: ast.AST = ast.parse(source)        
        if 'lambda' in source:
            for node in ast.walk(func):
                if type(node) is ast.Lambda:
                    func = node
                    break
        res = []
        for node in ast.walk(func):
            if type(node) is ast.Compare:
                const = node.comparators[0]
                if type(node.left) == Attribute and type(const) == Constant:
                    key = node.left.attr
                    val = const.value
                    if type(val) == str:
                        res.append(f'"{key}": "{val}"')
                    else:
                        res.append(f'"{key}": {val}')

        self.arr = res

    def _get_source(self, foo:Callable[[Node],Any]) -> str:
        return inspect.getsource(foo).strip()


    def __call__(self, *args: Any, **kwds: Any) -> Any:
        storage = args[0]
        return storage.search(self.arr)