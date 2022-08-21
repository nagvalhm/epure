from .binary import Binary
from ast import BinOp, Compare
from ..errors import UserInputError


class BinOperation(Binary, BinOp):
    def __init__(self, left, right, operator='') -> None:        
        from .leaf import TableProxy
        super().__init__(left, right, operator)

        left = self.left
        right = self.right

        if self.is_join() and isinstance(right, TableProxy):
            raise UserInputError('right operand of join must be logical expression, not table')
        

        if isinstance(left, Comparison) and isinstance(right, Comparison):
            self.set_parentheses()
        elif isinstance(left, Comparison) and isinstance(right, BinOperation)\
            and right.is_correct() and not right.is_join():
            self.set_parentheses()
        elif isinstance(left, BinOperation) and isinstance(right, Comparison)\
            and left.is_correct() and not left.is_join():
            self.set_parentheses()
        
    def is_join(self):
        from .leaf import TableProxy
        if self.operator not in ('<<', '>>'):
            return False
        res = isinstance(self.left, TableProxy)
        return res


    def is_correct(self):
        res = self.left_closed() and self.right_closed()
        return res

    def left_open(self):
        left_open = not self.left_closed()
        return left_open

    def right_open(self):
        right_open = not self.right_closed()
        return right_open

    def left_closed(self):
        from .leaf import TableProxy
        left_leaf = self.get_last_left_term()
        left_closed = isinstance(left_leaf, TableProxy) or isinstance(left_leaf.right_parent, Comparison)
        return left_closed

    def right_closed(self):
        from .leaf import TableProxy
        right_leaf = self.get_last_right_term()
        right_closed = isinstance(right_leaf, TableProxy) or isinstance(right_leaf.left_parent, Comparison)
        return right_closed



class Comparison(Binary, Compare):
    def __init__(self, left, right, operator='') -> None:
        from .leaf import ColumnProxy
        from .leaf import Primitive
        from .leaf import Leaf        

        super().__init__(left, right, operator)

        left = self.left
        right = self.right

        if self.is_join():
            self.set_join_parentheses()        
        

        if isinstance(left, ColumnProxy) and isinstance(right, ColumnProxy):
            self.set_parentheses()
        elif isinstance(left, ColumnProxy) and isinstance(right, Primitive):
            self.set_parentheses()
        elif isinstance(left, Primitive) and isinstance(right, ColumnProxy):
            self.set_parentheses() #raize Error?
        elif isinstance(left, Primitive) and isinstance(right, Primitive):
            self.set_parentheses()

        elif isinstance(left, BinOperation) and isinstance(right, Leaf):            
            # if left.is_correct():
            #     self.set_parentheses()
            if left.right_open() and left.left_closed():
                self.set_parentheses()

        elif isinstance(left, Leaf) and isinstance(right, BinOperation):            
            # if right.is_correct():
            #     self.set_parentheses()
            if right.left_open() and right.right_closed():
                self.set_parentheses()

        elif isinstance(left, BinOperation) and isinstance(right, BinOperation):
            if left.is_correct() and right.is_correct():
                self.set_parentheses()
            elif left.left_closed() and left.right_open() \
                and right.left_open() and right.right_closed():
                self.set_parentheses()

        
    def is_join(self):
        if not isinstance(self.left, Binary):
            return False
        left_right_leaf = self.left.get_last_right_term()
        x = left_right_leaf.left_parent
        res = hasattr(x, 'operator') and x.operator in ('<<', '>>')
        return res

    def set_join_parentheses(self):
        from .leaf import TableProxy
        right = self.right
        right_left_leaf = right
        left_right_leaf = self.left.get_last_right_term()
        if isinstance(right, Binary):
            right_left_leaf = right.get_last_left_term()
        if isinstance(right_left_leaf, TableProxy):
            raise UserInputError('right operand of join must be logical expression, not table')
        left_right_leaf.left_parentheses_count += 1        
        right_left_leaf.right_parentheses_count += 1