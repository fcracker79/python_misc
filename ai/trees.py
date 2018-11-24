import collections
import itertools
import typing


class Graph:

    def __init__(self):
        self.arch_count = 0
        self.nodes = set()
        self.archs = dict()  # type: typing.Dict[str, typing.Set[str]]

    def add_arch(self, node1, node2):
        self.arch_count += 1
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.archs.setdefault(node1, set()).add(node2)
        self.archs.setdefault(node2, set()).add(node1)

    def get_children(self, node):
        return self.archs.get(node, [])

g = Graph()
g.add_arch('Arad', 'Zerind')
g.add_arch('Arad', 'Timsoara')
g.add_arch('Arad', 'Sibiu')
g.add_arch('Zerind', 'Oradea')
g.add_arch('Oradea', 'Sibiu')
g.add_arch('Timsoara', 'Lugoj')
g.add_arch('Lugoj', 'Mehadia')
g.add_arch('Mehadia', 'Dobreta')
g.add_arch('Dobreta', 'Craovia')
g.add_arch('Craovia', 'Rimnicu Vilcea')
g.add_arch('Craovia', 'Pitesti')
g.add_arch('Rimnicu Vilcea', 'Sibiu')
g.add_arch('Rimnicu Vilcea', 'Pitesti')
g.add_arch('Sibiu', 'Faragas')
g.add_arch('Faragas', 'Bucharest')
g.add_arch('Pitesti', 'Bucharest')
g.add_arch('Bucharest', 'Giurgiu')
g.add_arch('Bucharest', 'Urziceni')
g.add_arch('Urziceni', 'Hisrova')
g.add_arch('Urziceni', 'Vaslui')
g.add_arch('Hisrova', 'Eforie')
g.add_arch('Vaslui', 'Iasi')
g.add_arch('Iasi', 'Neamt')


class SearchTree:
    def __init__(
            self, graph: Graph, root: str, goal: str,
            queuing_function: typing.Callable[[typing.List[str], typing.Sequence[str]], typing.List[str]]):
        self.graph, self.root, self.goal = graph, root, goal
        self.queuing_function = queuing_function
        self.nodes = collections.deque()
        self.parents = dict()  # type: typing.Dict[str, str]
        self.operators = dict()  # type: typing.Dict[str, Boh]
        self.depths = dict()  # type: typing.Dict[str, int]
        self.costs = dict()  # type: typing.Dict[str, int]
        self.nodes.append(root)
        self.parents[root] = None
        self.depths[root] = 0
        self.costs[root] = 0

    def log(self, *a, **kw):
        print(*a, **kw)

    def solve(self):
        best_solution, best_score = None, -1
        while self.nodes:
            node = self.nodes.pop()
            self.log('Current path', node, list(self.get_parents(node))[::-1])
            self.log('Nodes', self.nodes)
            if node == self.goal:
                if self.costs[node] < best_score or best_score < 0:
                    print(self.costs)
                    best_solution, best_score = list(self.get_parents(node))[::-1], self.costs[node]
                    print(best_solution)
                continue
            children = self.graph.get_children(node)
            parents = set(self.get_parents(node))
            self.log('children', node, children)
            children = list(set(children) - parents - set(self.nodes))
            self.log('children cleaned', children)
            for c in children:
                self.parents[c] = node
                self.depths[c] = self.depths[node] + 1
                self.costs[c] = self.costs[node] + 1
            self.nodes = self.queuing_function(self.nodes, children)
            node in self.nodes and self.nodes.remove(node)

        print(self.costs)
        return best_solution, best_score

    def get_parents(self, node: str):
        while self.parents.get(node):
            node = self.parents[node]
            yield node


def breadth_first(queue: typing.List[str], nodes: typing.Sequence[str]) -> typing.List[str]:
    queue.extend(nodes)
    return queue


def depth_first(queue: typing.List[str], nodes: typing.Sequence[str]) -> typing.List[str]:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


# print(SearchTree(g, 'Arad', 'Bucharest', breadth_first).solve())
print(SearchTree(g, 'Arad', 'Bucharest', depth_first).solve())
