from _ast import Assign, Attribute, Call, Constant, FunctionDef, In, Not, UnaryOp
import ast
from types import CodeType
from typing import Any, Dict
# import inspect
# import textwrap
from .term import Term
from .domain import Domain
from .model import Model
from .column_proxy import ColumnProxy

# class AstParser(ast.NodeTransformer):
class InspectParser(ast.NodeTransformer):

    astTypesDict:Dict[str, Any]
    column_proxy_cls=ColumnProxy
    model_cls=Model
    ast_type_method_name_dict:Dict[ast.cmpop, str] = {
        ast.Eq: "__eq__",
        ast.NotEq: "__ne__",
        ast.Lt: "__lt__",
        ast.LtE: "__le__",
        ast.Gt: "__gt__",
        ast.GtE: "__ge__",
        ast.In: "_in",
        ast.NotIn: "not_in",
        ast.Or: "_or",
        ast.And: "_and",
        ast.Is: "_is",
        ast.IsNot: "is_not"
    }

    def __init__(self) -> None:
        self.astTypesDict = {}
        super().__init__()

    def parse(self, func) -> CodeType:
        # func_source = inspect.getsource(func)
        # dedent_src = textwrap.dedent(func_source)
        func_tree = ast.parse(func)
        func_args = func_tree.body[0].args.args
        self.first_arg_name = func_args[0].arg

        attr_tp = ast.Attribute()
        attr_dbp = ast.Attribute()
        attr_tp.type = Model
        attr_dbp.type = Domain

        self.astTypesDict[f'{self.first_arg_name}.md'] = attr_tp
        # self.astTypesDict[f'{self.first_arg_name}.querying_proxy'] = attr_tp
        self.astTypesDict[f'{self.first_arg_name}.dom'] = attr_dbp

        changed_tree = self.visit(func_tree)
        fixed_tree = ast.fix_missing_locations(changed_tree)
        return fixed_tree
    
    # def visit_FunctionDef(self, node: FunctionDef) -> Any:
        
    #     self.generic_visit(node)

    #     if node.decorator_list:
    #         i = next(i for i, v in enumerate(node.decorator_list) if v.id == "escript")
    #         node.decorator_list.pop(i)

    #     return node

    def is_bool_operand(self, operand_val, operand_val_str):
        res = operand_val_str in self.astTypesDict.keys()\
            or isinstance(operand_val, ast.Compare)\
            or isinstance(operand_val, ast.In)\
            or isinstance(operand_val, ast.NotIn)\
            or isinstance(operand_val, ast.BoolOp)
        
        return res
    
    def visit_BoolOp(self, node: ast.BoolOp) -> Any:

        self.generic_visit(node)
        
        left_val = node.values[0]
        compare_targ = node.values[1]

        left_val_str = ast.unparse(left_val)
        compare_targ_str = ast.unparse(compare_targ)

        left_val_in_keys = self.is_bool_operand(left_val, left_val_str)
        comp_targ_in_keys = self.is_bool_operand(compare_targ, compare_targ_str)

        if left_val_in_keys or comp_targ_in_keys:
            # op_str = "_or" if type(node.op) is ast.Or else "_and"
            op_str = self.ast_type_method_name_dict[type(node.op)]
            new_node_str = f"{self.first_arg_name}.md.{op_str}({left_val_str}, {compare_targ_str})"
            node = ast.parse(new_node_str).body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node
        
        return node
    
    def visit_UnaryOp(self, node: UnaryOp) -> Any:

        self.generic_visit(node)

        node_str = ast.unparse(node.operand)

        if type(node.op) == Not and node_str in self.astTypesDict:
            new_node_str = f"{self.first_arg_name}.md._not({node_str})"
            node = ast.parse(new_node_str).body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node
        
        return node
    
    def visit_Compare(self, node: ast.Compare) -> Any:

        self.generic_visit(node)

        # self.generic_visit(node)
        if type(node.ops[0]) in (ast.In, ast.NotIn):
            node = self.handle_In_and_Not_In(node)
        else:
            node = self.handle_Compare_Op(node)

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

        # if hasattr(node.value, "value") and node.value.value in (True, False):
        #     node.value.type = Term
        #     self.astTypesDict[assign_target] = node.value

        return node
    
    def visit_Attribute(self, node: Attribute) -> Any:

        self.generic_visit(node)

        left_val = ast.unparse(node.value)
        
        node = self.handle_getattr(node, left_val)
        
        return node
    
    def visit_Call(self, node: Call) -> Any:

        self.generic_visit(node)
        caller = None

        if hasattr(node.func, "value"):
            caller = ast.unparse(node.func.value)

        if hasattr(node.func,"id") and node.func.id == "getattr":
            left_val = ast.unparse(node.args[0])
            node = self.handle_getattr(node, left_val)

        elif caller and caller in self.astTypesDict and\
            hasattr(node.func,"attr") and node.func.attr == "select":
            node.type = Term
            self.astTypesDict[f'{ast.unparse(node)}'] = node

        elif caller and caller in self.astTypesDict and\
            hasattr(node.func,"attr") and node.func.attr == "like":
            node.type = Term
            self.astTypesDict[f'{ast.unparse(node)}'] = node

        elif caller and caller in self.astTypesDict and\
            hasattr(node.func,"attr") and node.func.attr == "model":
            node.type = Model
            self.astTypesDict[f'{ast.unparse(node)}'] = node

        return node
    
    # def visit_Constant(self, node: Constant) -> Any:
    #     if node.value in (True, False) and\
    #     str(node.value) not in self.astTypesDict.keys():
    #         node.type = Term
    #         self.astTypesDict[f'{ast.unparse(node)}'] = node
    #     return node
    
    def handle_getattr(self, node, left_val):

        self.generic_visit(node)

        node_str = ast.unparse(node)

        if node_str in self.astTypesDict.keys():
            return node

        if left_val in self.astTypesDict.keys() and\
        self.astTypesDict[left_val].type == Domain:
            node.type = Model
            self.astTypesDict[f'{node_str}'] = node

        if left_val in self.astTypesDict.keys() and\
        self.astTypesDict[left_val].type == Model:
            node.type = ColumnProxy
            self.astTypesDict[f'{node_str}'] = node

        return node

    def handle_In_and_Not_In(self, node: In) -> Any:
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

        if left_val_in_keys and left_val_type in (Model, Domain):
            raise TypeError(f"'{left_val}' is of type '{left_val_type}' and not of type '{ColumnProxy}', so it cannot be present in '{compare_targ}'")
        
        # if not (comp_targ_in_keys and isinstance(self.astTypesDict[compare_targ], ast.Call) and node.comparators[0].func.attr == "select") and (type(node.comparators[0]) not in (ast.Name, ast.List, ast.Tuple, ast.Set)):
            # comp_targ_type = type(node.comparators[0])
            # raise TypeError(f"'{compare_targ}' is of type '{comp_targ_type}' and not of type List, Tuple, Set or select method, so it cannot be right operand for SQL 'IN' operator")
        
        if left_val_in_keys and issubclass(left_val_type, ColumnProxy):
            op_method = self.ast_type_method_name_dict[type(node.ops[0])]
            new_node_str = f"{left_val}.{op_method}({compare_targ})"
            node = ast.parse(new_node_str).body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node

        return node
    
    # def handle_Eq_and_Like(self, node: Eq) -> Any:
    def handle_Compare_Op(self, node: Any) -> Any: # >=, <=, == 

        self.generic_visit(node)

        new_node_str = ""
        
        left_val = ast.unparse(node.left)
        compare_targ = ast.unparse(node.comparators)

        left_val_in_keys = left_val in self.astTypesDict.keys()
        comp_targ_in_keys = compare_targ in self.astTypesDict.keys()

        if left_val_in_keys: 
            left_val_type = self.astTypesDict[left_val].type

        if comp_targ_in_keys:
            comp_targ_type = self.astTypesDict[compare_targ].type

        if not ((left_val_in_keys and issubclass(left_val_type, ColumnProxy)) or\
            (comp_targ_in_keys and issubclass(comp_targ_type, ColumnProxy))):
            return node

        if left_val_in_keys and left_val_type in (Model, Domain):
            raise TypeError(f"'{left_val}' is of type '{left_val_type}' and not of type '{ColumnProxy}', so it cannot be compared to '{compare_targ}'")

        elif comp_targ_in_keys and comp_targ_type in (Model, Domain):
            raise TypeError(f"'{compare_targ}' is of type '{comp_targ_type}' and not of type '{ColumnProxy}', so it cannot be compared to '{left_val}'")

        # if left_val_in_keys and ((compare_targ.count('%') > compare_targ.count('\%'))\
        # or (compare_targ.count('_') > compare_targ.count('\_'))):

        # if left_val_in_keys and (compare_targ.count('%') > compare_targ.count('\%'))\
        #     and issubclass(left_val_type, ColumnProxy):
        #     # compare_targ = ast.unparse(self.handle_Like(node.comparators))
        #     new_node_str = f"{left_val}._like({compare_targ})"

        # elif comp_targ_in_keys and (left_val.count('%') > left_val.count('\%'))\
        #     and issubclass(comp_targ_type, ColumnProxy):
        #     # compare_targ = ast.unparse(self.handle_Like(node.comparators))
        #     new_node_str = f"{compare_targ}._like({left_val})"
        op_method = self.ast_type_method_name_dict[type(node.ops[0])]

        if left_val_in_keys and issubclass(left_val_type, ColumnProxy):
            new_node_str = f"{left_val}.{op_method}({compare_targ})"
            # new_node_str = f"{left_val} == {compare_targ}"

        elif comp_targ_in_keys and issubclass(comp_targ_type, ColumnProxy):
            new_node_str = f"{compare_targ}.{op_method}({left_val})"
            # new_node_str = f"{compare_targ} == {left_val}"

        if new_node_str and (left_val_in_keys or comp_targ_in_keys):
            new_node = ast.parse(new_node_str)
            node = new_node.body[0].value
            node.type = Term
            self.astTypesDict[new_node_str] = node
        
        return node

    # def visit_Str(self, node: Str) -> Any:
        
        # str_unparsed = ast.unparse(node)

        # if "\\" in str_unparsed:
        #     node.value = node.value.replace(r"\\","\\")

        # return node