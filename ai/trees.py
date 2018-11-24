import collections
import itertools
import time
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


def _create_example_graph() -> Graph:
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
            lambda d: Node(d, node, node.depth + 1, node.cost + 1),
            self.graph.get_children(node.state)
        )

    def solve(self) -> typing.Optional[Solution]:
        best_solution, best_score = None, -1
        while self.nodes:
            node = self.nodes.pop()  # type: Node
            self.log('Current path', node, list(self.get_parents(node))[::-1])
            self.log('Nodes', self.nodes)
            if node.state == self.goal:
                if node.cost < best_score or best_score < 0:
                    self.log(node)
                    best_solution, best_score = list(self.get_parents(node))[::-1], node.cost
                    self.log(best_solution)
                continue
            children = self.get_children(node)
            parent_states = set(map(lambda d: d.state, self.get_parents(node)))
            self.log('children', node, children)
            children = list(filter(lambda d: d.state not in parent_states, children))
            self.log('children cleaned', children)
            self.nodes = self.queuing_function(self.nodes, children)
            node in self.nodes and self.nodes.remove(node)

        return Solution(best_solution, best_score) if best_score > 0 else None

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


def _header(t: str):
    print('********** {} **********'.format(t))


def _print_solution(name: str, solution: typing.Optional[Solution]):
    _header(name)
    print('Score:', solution.score)
    print('Best path:', solution.nodes)


def _print_algo(name: str, graph: Graph, from_node: str, to_node: str, queuing_function: QueuingFunction):
    start = time.time()
    solution = SearchTree(graph, from_node, to_node, _breadth_first).solve()
    stop = time.time()
    _print_solution(name, solution)
    print('Elapsed time', stop - start)


def _run():
    g = _create_example_graph()
    _print_algo('BREADTH FIRST', g, 'Arad', 'Bucharest', _breadth_first)
    _print_algo('DEPTH FIRST', g, 'Arad', 'Bucharest', _depth_first)


if __name__ == '__main__':
    _run()
