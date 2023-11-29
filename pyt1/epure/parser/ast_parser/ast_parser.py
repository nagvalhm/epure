from _ast import Assign, Attribute, Constant, Eq, FormattedValue, In, JoinedStr
import ast
from ast import Str
from types import CodeType
from typing import Any, Dict
# import inspect
# import textwrap
from .term import Term
from .db_proxy import DbProxy
from .table_proxy import TableProxy
from .column_proxy import ColumnProxy

class AstParser(ast.NodeTransformer):

    astTypesDict:Dict[str, Any]
    column_proxy_cls=ColumnProxy
    table_proxy_cls=TableProxy

    def __init__(self) -> None:
        self.astTypesDict = {}
        super().__init__()

    def parse(self, func) -> CodeType:
        # func_source = inspect.getsource(func)
        # dedent_src = textwrap.dedent(func_source)
        func_tree = ast.parse(func)
        func_args = func_tree.body[0].args.args

        # if func_args[0].arg == "self":
        #     func_args.pop(0)

        # if args:
        #     for i in range(len(func_args)):
        #         if issubclass(type(args[i]), Term):
        #             func_args[i].type = type(args[i])
        #             self.astTypesDict[func_args[i].arg] = func_args[i]

        self.first_arg_name = func_args[0].arg

        attr_tp = ast.Attribute()
        attr_dbp = ast.Attribute()
        attr_tp.type = TableProxy
        attr_dbp.type = DbProxy

        self.astTypesDict[f'{self.first_arg_name}.tp'] = attr_tp
        self.astTypesDict[f'{self.first_arg_name}.dbp'] = attr_dbp

        # visitor = AstParser()
        changed_tree = self.visit(func_tree)
        fixed_tree = ast.fix_missing_locations(changed_tree)
        return fixed_tree
    
    def visit_BoolOp(self, node: ast.BoolOp) -> Any:

        self.generic_visit(node)
        
        left_val = ast.unparse(node.values[0])
        compare_targ = ast.unparse(node.values[1])

        left_val_in_keys = left_val in self.astTypesDict.keys()
        comp_targ_in_keys = compare_targ in self.astTypesDict.keys()

        if left_val_in_keys and comp_targ_in_keys:
            # op_str = "|" if type(node.op) is ast.Or else "&"
            op_str = "_or" if type(node.op) is ast.Or else "_and"
            # new_node_str = f"(({left_val}) {op_str} ({compare_targ}))"
            # new_node_str = f"{left_val}.{op_str}({compare_targ})"
            new_node_str = f"{self.first_arg_name}.tp.{op_str}({left_val},{compare_targ})"
            node = ast.parse(new_node_str).body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node
        
        return node
    
    def visit_Compare(self, node: ast.Compare) -> Any:

        # self.generic_visit(node)
        if isinstance(node.ops[0], ast.In):
            node = self.handle_In(node)

        elif isinstance(node.ops[0], ast.Eq):
            node = self.handle_Eq(node)

        return node
    
    def visit_Attribute(self, node: Attribute) -> Any:

        left_val = ast.unparse(node.value)
        node_str = ast.unparse(node)

        if node_str in self.astTypesDict.keys():
            return node

        if left_val in self.astTypesDict.keys() and\
        self.astTypesDict[left_val].type == DbProxy:
            node.type = TableProxy
            self.astTypesDict[f'{node_str}'] = node

        if left_val in self.astTypesDict.keys() and\
        self.astTypesDict[left_val].type == TableProxy:
            node.type = ColumnProxy
            self.astTypesDict[f'{node_str}'] = node
        
        return node

    def visit_Assign(self, node: Assign) -> Any:

        self.generic_visit(node)

        # if type(node.body[0].value) in [i.type for i in self.astTypesDict.values()]:
        #     node.body[0]

        right_val = ast.unparse(node.value)
        assign_target = ast.unparse(node.targets)

        if assign_target not in self.astTypesDict and\
        right_val in self.astTypesDict.keys() and\
        issubclass(self.astTypesDict[right_val].type, Term):
            self.astTypesDict[assign_target] = self.astTypesDict[right_val]

        if assign_target in self.astTypesDict.keys() and\
        right_val not in self.astTypesDict.keys() and\
        issubclass(self.astTypesDict[assign_target].type, Term):
            # self.astTypesDict.pop(assign_target)
            self.astTypesDict = dict(filter(lambda x: assign_target not in x[0].split('.'), self.astTypesDict.items()))

        return node

    def handle_In(self, node: In) -> Any:
        self.generic_visit(node)

        left_val = ast.unparse(node.left)
        compare_targ = ast.unparse(node.comparators)

        left_val_in_keys = left_val in self.astTypesDict.keys()
        comp_targ_in_keys = compare_targ in self.astTypesDict.keys()

        if not left_val_in_keys:
            return node
        
        if left_val_in_keys: 
            left_val_type = self.astTypesDict[left_val].type

        if comp_targ_in_keys:
            comp_targ_type = self.astTypesDict[compare_targ].type

        if left_val_in_keys and left_val_type in (TableProxy, DbProxy):
            raise TypeError(f"'{left_val}' is of type '{left_val_type}' and not of type '{ColumnProxy}', so it cannot be present in '{compare_targ}'")
        
        if (comp_targ_in_keys and issubclass(comp_targ_type, Term))\
        or type(node.comparators[0]) not in (ast.Name, ast.List, ast.Tuple, ast.Set):
            comp_targ_type = type(node.comparators[0])
            raise TypeError(f"'{compare_targ}' is of type '{comp_targ_type}' and not of type List, Tuple or Set, so it cannot be right operand for SQL 'IN' operator")
        
        if left_val_in_keys and issubclass(left_val_type, ColumnProxy):
            new_node_str = f"{left_val}._in({compare_targ})"
            node = ast.parse(new_node_str).body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node

        return node
    
    def handle_Eq(self, node: Eq) -> Any:

        self.generic_visit(node)
        
        left_val = ast.unparse(node.left)
        compare_targ = ast.unparse(node.comparators)

        left_val_in_keys = left_val in self.astTypesDict.keys()
        comp_targ_in_keys = compare_targ in self.astTypesDict.keys()

        if not (left_val_in_keys or comp_targ_in_keys):
            return node

        if left_val_in_keys: 
            left_val_type = self.astTypesDict[left_val].type

        if comp_targ_in_keys:
            comp_targ_type = self.astTypesDict[compare_targ].type

        if left_val_in_keys and left_val_type in (TableProxy, DbProxy):
            raise TypeError(f"'{left_val}' is of type '{left_val_type}' and not of type '{ColumnProxy}', so it cannot be compared to '{compare_targ}'")

        elif comp_targ_in_keys and comp_targ_type in (TableProxy, DbProxy):
            raise TypeError(f"'{compare_targ}' is of type '{comp_targ_type}' and not of type '{ColumnProxy}', so it cannot be compared to '{left_val}'")
        
        # if "\\" in compare_targ:
        #     compare_targ = compare_targ.replace(r"\\","\\")
        
        if left_val_in_keys and ((compare_targ.count('%') > compare_targ.count('\%'))\
        or (compare_targ.count('_') > compare_targ.count('\_'))):
            # compare_targ = ast.unparse(self.handle_Like(node.comparators))
            new_node_str = f"{left_val}._like({compare_targ})"

        elif left_val_in_keys and issubclass(left_val_type, ColumnProxy):
            new_node_str = f"{left_val}._eq({compare_targ})"
            # new_node_str = f"{left_val} == {compare_targ}"

        elif comp_targ_in_keys and issubclass(comp_targ_type, ColumnProxy):
            new_node_str = f"{compare_targ}._eq({left_val})"
            # new_node_str = f"{compare_targ} == {left_val}"

        if left_val_in_keys or comp_targ_in_keys:
            new_node = ast.parse(new_node_str)
            node = new_node.body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node
        
        return node
    
    # def handle_Like(self, node) -> Any:

    #    node_str = ast.unparse(node)

    # def visit_Str(self, node: Str) -> Any:
        
        # str_unparsed = ast.unparse(node)

        # if "\\" in str_unparsed:
        #     node.value = node.value.replace(r"\\","\\")

        # return node