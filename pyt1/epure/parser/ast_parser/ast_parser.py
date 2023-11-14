from _ast import Assign, Eq
import ast
from types import CodeType
from typing import Any, Dict
import inspect
import textwrap
from .term import Term

class AstParser(ast.NodeTransformer):

    astTypesDict:Dict[str, Any]

    def __init__(self) -> None:
        self.astTypesDict = {}
        super().__init__()

    def parse(self, func, *args, **kwargs) -> CodeType:
        func_source = inspect.getsource(func)
        dedent_src = textwrap.dedent(func_source)
        func_tree = ast.parse(dedent_src)
        func_args = func_tree.body[0].args.args

        if func_args[0].arg == "self":
            func_args.pop(0)

        if args:
            for i in range(len(func_args)):
                if issubclass(type(args[i]), Term):
                    func_args[i].type = type(args[i])
                    self.astTypesDict[func_args[i].arg] = func_args[i]

        visitor = AstParser()
        changed_tree = visitor.visit(func_tree)
        fixed_tree = ast.fix_missing_locations(changed_tree)
        return fixed_tree
    
    def visit_BoolOp(self, node: ast.BoolOp) -> Any:

        return ast.Constant("Hello, Monkeys!!!")
    
    def visit_Eq(self, node: Eq) -> Any:

        # return super().visit_Eq(node)
        return 
    
    def visit_Assign(self, node: Assign) -> Any:
        # return super().visit_Assign(node)
        if type(node.body[0].value) in [i.type for i in self.astTypesDict.values()]:
            node.body[0]
    