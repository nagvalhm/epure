import networkx as nx
import matplotlib.pyplot as plt
from uuid import UUID, uuid4
from pyvis.network import Network

class TermDebugger:
    pass

class MatplotTermDebugger(TermDebugger):
    debug_tree_step = 10
    # positions = {}

    def __init__(self, debug_tree_step=None) -> None:
        if debug_tree_step:
            self.debug_tree_step = debug_tree_step
        super().__init__()

    def show(self, terms):

        nx_edges = []
        for term in terms:
            term_name = str(term.id)[0:4]
            term_name = f'{term.val}_{term_name}'
            term.name = term_name

            # term_position = None
            # if term_name in self.positions:
            #     term_position = self.positions[term_name]

            if hasattr(term, 'left') and term.left:
                left_name = str(term.left.id)[0:4]
                left_name = f'{term.left.val}_{left_name}'
                nx_edges.append((term_name, left_name))

                # if left_name in self.positions:                    
                #     if term_name not in self.positions:
                #         left_position = self.positions[left_name]
                #         term_position = (left_position[0] + 1, left_position[1] + 1)
                #         self.positions[term_name] = term_position
                # elif term_position:
                #     left_position = (term_position[0] - 1, term_position[1] - 1)
                #     self.positions[left_name] = left_position


            if hasattr(term, 'right') and term.right:
                right_name = str(term.right.id)[0:4]
                right_name = f'{term.right.val}_{right_name}'
                nx_edges.append((term_name, right_name))

                # if right_name in self.positions:                    
                #     if term_name not in self.positions:
                #         right_position = self.positions[right_name]
                #         term_position = (right_position[0] + 1, right_position[1] - 1)
                #         self.positions[term_name] = term_position
                # elif term_position:
                #     right_position = (term_position[0] - 1, term_position[1] + 1)
                #     self.positions[left_name] = right_position

            # if not term_position:
            #     right_up = self._get_right_up_position()
            #     term_position = (right_up[0], right_up[1] + self.debug_tree_step)
            #     self.positions[term_name] = term_position

        positions = self.get_positions(terms)

        nx_graph = nx.DiGraph()
        nx_graph.add_edges_from(nx_edges)

        # net = Network()
        # net.from_nx(nx_graph)
        # net.show('tree.html')
        # net.show(str(uuid4())+'.html')
        
        plt.figure(str(uuid4()))
        nx.draw_networkx(nx_graph, pos=positions)
        plt.show()

    def get_positions(self, terms):
        tops = self.get_tops(terms)
        res = {}
        cur_pos = (0, 0)
        for top in reversed(tops):
            positions = self.get_positions_recurce(top, terms, cur_pos)
            cur_pos = self._get_right_up_position(positions)
            cur_pos = (cur_pos[0] + self.debug_tree_step, cur_pos[1])
            res.update(positions)
        return res

    def get_positions_recurce(self, term, terms, cur_pos):
        res = {}
        res[term.name] = cur_pos
        if hasattr(term, 'left') and term.left:
            left_position = (cur_pos[0] - 1, cur_pos[1] - 1)
            left_positions = self.get_positions_recurce(term.left, terms, left_position)
            res.update(left_positions)
        if hasattr(term, 'right') and term.right:
            right_position = (cur_pos[0] + 1, cur_pos[1] - 1)
            right_positions = self.get_positions_recurce(term.right, terms, right_position)
            res.update(right_positions)
        return res

    def get_tops(self, terms):
        not_tops = []
        for term in terms:
            if hasattr(term, 'left_parent') and term.left_parent:
                not_tops.append(term)
            elif hasattr(term, 'right_parent') and term.right_parent:
                not_tops.append(term)
        tops = []
        for term in terms:
            if term.index_of(not_tops) == None:
                tops.append(term)
        return tops

    def _get_right_up_position(self, positions):
        if not positions:
            return (0, 0)
        ziped = list(zip(*positions.values()))
        xes = ziped[0]
        yes = ziped[1]
        return (max(xes), max(yes))