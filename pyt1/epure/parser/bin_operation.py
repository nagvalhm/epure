from .binary import Binary
from ast import BinOp, Compare


class BinOperation(Binary, BinOp):
    def __init__(self, left, right, operator='') -> None:
        from .leaf import TableProxy

        super().__init__(left, right, operator)

        left = self.left
        right = self.right
        

        if isinstance(left, Comparison) and isinstance(right, Comparison):
            self.set_parentheses()
        elif isinstance(left, Comparison) and isinstance(right, BinOperation)\
            and right.is_correct():
            self.set_parentheses()
        elif isinstance(left, BinOperation) and isinstance(right, Comparison)\
            and left.is_correct():
            self.set_parentheses()
        


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
        self.set_join_parentheses(left, right)
        
        

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

        


    def set_join_parentheses(self, left, right):     
        
        if not isinstance(left, Binary):
            return
        
        left_right_leaf = left.get_last_right_term()
        x = left_right_leaf.left_parent
        if hasattr(x, 'operator') and x.operator in ('<<', '>>'):
            right_left_leaf = right
            if isinstance(right, Binary):
                right_left_leaf = right.get_last_left_term()
            left_right_leaf.left_parentheses_count += 1
            right_left_leaf.right_parentheses_count += 1