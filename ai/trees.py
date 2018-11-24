import collections
import itertools
import sys
import time
import typing


class Graph:

    def __init__(self):
        self.arch_count = 0
        self.nodes = set()
        self.archs = dict()  # type: typing.Dict[str, typing.Set[str]]
        self.costs = dict()  # type: typing.Dict[str, int]

    def add_arch(self, node1, node2, cost: int=1):
        self.arch_count += 1
        self.nodes.add(node1)
        self.nodes.add(node2)
        self.archs.setdefault(node1, set()).add(node2)
        self.archs.setdefault(node2, set()).add(node1)
        self.costs[','.join(sorted((node1, node2)))] = cost

    def get_cost(self, node1: str, node2: str) -> int:
        return self.costs[','.join(sorted((node1, node2)))]

    def get_children(self, node):
        return self.archs.get(node, [])


def _create_example_graph(add_costs: bool=False) -> Graph:
    g = Graph()
    g.add_arch('Arad', 'Zerind', add_costs and 1 or 1)
    g.add_arch('Arad', 'Timsoara', add_costs and 2 or 1)
    g.add_arch('Arad', 'Sibiu', add_costs and 3 or 1)
    g.add_arch('Zerind', 'Oradea', add_costs and 1 or 1)
    g.add_arch('Oradea', 'Sibiu', add_costs and 4 or 1)
    g.add_arch('Timsoara', 'Lugoj', add_costs and 2 or 1)
    g.add_arch('Lugoj', 'Mehadia', add_costs and 1 or 1)
    g.add_arch('Mehadia', 'Dobreta', add_costs and 1 or 1)
    g.add_arch('Dobreta', 'Craovia', add_costs and 2 or 1)
    g.add_arch('Craovia', 'Rimnicu Vilcea', add_costs and 3 or 1)
    g.add_arch('Craovia', 'Pitesti', add_costs and 3 or 1)
    g.add_arch('Rimnicu Vilcea', 'Sibiu', add_costs and 1 or 1)
    g.add_arch('Rimnicu Vilcea', 'Pitesti', add_costs and 2 or 1)
    g.add_arch('Sibiu', 'Faragas', add_costs and 2 or 1)
    g.add_arch('Faragas', 'Bucharest', add_costs and 5 or 1)
    g.add_arch('Pitesti', 'Bucharest', add_costs and 3 or 1)
    g.add_arch('Bucharest', 'Giurgiu', add_costs and 2 or 1)
    g.add_arch('Bucharest', 'Urziceni', add_costs and 1 or 1)
    g.add_arch('Urziceni', 'Hisrova', add_costs and 2 or 1)
    g.add_arch('Urziceni', 'Vaslui', add_costs and 4 or 1)
    g.add_arch('Hisrova', 'Eforie', add_costs and 2 or 1)
    g.add_arch('Vaslui', 'Iasi', add_costs and 2 or 1)
    g.add_arch('Iasi', 'Neamt', add_costs and 2 or 1)
    return g


Node = typing.NamedTuple(
        'Node',
        (
            ('state', typing.Any),
            ('parent', typing.Optional['Node']),
            # ('operator', 'Boh'),
            ('depth', int),
            ('cost', int),
        )
    )
Solution = typing.NamedTuple(
    'Solution',
    (
        ('nodes', typing.List[Node]),
        ('score', int)
    )
)

QueuingFunction = typing.NewType(
    'QueuingFunction',
    typing.Callable[[typing.Deque[Node], typing.Sequence[Node]], typing.Deque[Node]]
)


class SearchTree:
    def __init__(
            self, graph: Graph, root: str, goal: str,
            queuing_function: QueuingFunction):
        self.graph, self.root, self.goal = graph, root, goal
        self.queuing_function = queuing_function
        self.nodes = collections.deque()
        self.nodes.append(Node(root, None, 0, 0))

    def log(self, *a, **kw):
        pass
        # print(*a, **kw)

    def get_children(self, node: Node) -> typing.Iterable[Node]:
        return map(
            lambda d: Node(d, node, node.depth + 1, node.cost + self.graph.get_cost(node.state, d)),
            self.graph.get_children(node.state)
        )

    def solve(self) -> typing.Optional[Solution]:
        best_solution, best_score = None, sys.maxsize
        while self.nodes:
            node = self.nodes.pop()  # type: Node
            # Note:
            # Without this simple optimization, depth-first and breadth-first compare well in terms of performances.
            # With this optimization, depth-first is sligthly faster.
            if node.cost > best_score:
                continue
            path = list(self.get_parents(node))[::-1]
            self.log('Current path', node, path)
            self.log('Nodes', self.nodes)
            if node.state == self.goal:
                if node.cost < best_score:
                    self.log(node)
                    best_solution, best_score = path + [node], node.cost
                    self.log(best_solution)
                continue
            children = self.get_children(node)
            parent_states = set(map(lambda d: d.state, path))
            self.log('children', node, children)
            children = list(filter(lambda d: d.state not in parent_states, children))
            self.log('children cleaned', children)
            self.nodes = self.queuing_function(self.nodes, children)
            node in self.nodes and self.nodes.remove(node)

        return Solution(best_solution, best_score) if best_solution else None

    @classmethod
    def get_parents(cls, node: Node):
        while node.parent:
            node = node.parent
            yield node


def _breadth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    queue.extend(nodes)
    return queue


def _depth_first(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(
        itertools.chain(nodes, queue)
    )


def _uniform_cost(queue: typing.Deque[Node], nodes: typing.Sequence[Node]) -> typing.Deque[Node]:
    return collections.deque(sorted(itertools.chain(nodes, queue), key=lambda d: d.cost))


_LENGTH = 80


def _header(t: str):
    stars = '*' * ((_LENGTH - len(t) - 2) // 2)
    final_stars = stars if len(stars) * 2 + 2 + len(t) == _LENGTH else stars + '*'
    print(stars, t, final_stars, sep=' ')


def _str_node(node: Node) -> str:
    return 'Node(state={state}, depth={depth}, cost={cost})'.format(**node._asdict())


def _print_solution(name: str, solution: typing.Optional[Solution]):
    _header(name)
    print('Score:', solution.score)
    print('Best path:', '\n\t'.join(map(_str_node, solution.nodes)))


def _print_algo(name: str, graph: Graph, from_node: str, to_node: str, queuing_function: QueuingFunction):
    start = time.time()
    solution = SearchTree(graph, from_node, to_node, queuing_function).solve()
    stop = time.time()
    _print_solution(name, solution)
    print('Elapsed time', stop - start)


def _run_algos(add_costs: bool):
    _header('WITH COSTS' if add_costs else 'WITHOUT COSTS')
    g = _create_example_graph(add_costs=add_costs)
    _print_algo('BREADTH FIRST', g, 'Arad', 'Bucharest', _breadth_first)
    _print_algo('DEPTH FIRST', g, 'Arad', 'Bucharest', _depth_first)


def _run():
    _run_algos(False)
    _run_algos(True)


if __name__ == '__main__':
    _run()
