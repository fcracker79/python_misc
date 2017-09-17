import abc
import ast

import logging
import typing
from functools import wraps


_DEFAULT_CONTEXT_NAME = 'context'

class UnparsableException(Exception):
    def __init__(self, node: ast.AST, *a):
        super(UnparsableException, self).__init__(*a)
        self.node = node


VISITOR_LOGGER = logging.getLogger('visitor')


def _log(fun):
    @wraps(fun)
    def _inner(visitor: ast.NodeVisitor, n: ast.AST):
        VISITOR_LOGGER.debug('Visiting %s (%s)', type(n), n.__dict__)
        return fun(visitor, n)
    return _inner


class ValueVisitor(ast.NodeVisitor, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def value(self):
        pass  # pragma: no cover


class _ExpressionVisitor(ValueVisitor):
    def __init__(
            self, context: typing.Dict,
            context_name: str=_DEFAULT_CONTEXT_NAME):
        self._stack = []
        self._context = context
        self._context_name = context_name
        self._known_functions = {}

    def add_known_function(self, name: str, fun: typing.Callable) -> None:
        self._known_functions[name] = fun

    def generic_visit(self, node):
        raise UnparsableException(node, 'Could not parse node {}({})'.format(node, node.__dict__))

    # noinspection PyPep8Naming
    @_log
    def visit_Module(self, n: ast.Module):
        for child in ast.iter_child_nodes(n):
            self.visit(child)

    # noinspection PyPep8Naming
    @_log
    def visit_Expr(self, n: ast.Expr):
        self.visit(n.value)

    # noinspection PyPep8Naming
    @_log
    def visit_IfExp(self, n: ast.IfExp):
        test_expression = n.test
        self.visit(test_expression)
        condition = self._stack.pop()
        if condition:
            self.visit(n.body)
        else:
            self.visit(n.orelse)

    # noinspection PyPep8Naming
    @_log
    def visit_BinOp(self, n: ast.BinOp):
        self.visit(n.left)
        self.visit(n.right)
        self.visit(n.op)

    # noinspection PyPep8Naming
    @_log
    def visit_Attribute(self, n: ast.Attribute):
        self.visit(n.value)
        self.visit(n.ctx)
        cur_data = self._stack.pop()
        VISITOR_LOGGER.debug('cur data: %s', cur_data)
        self._stack.append(cur_data[n.attr])

    # noinspection PyPep8Naming
    @_log
    def visit_Compare(self, n: ast.Compare):
        for c in n.comparators:
            self.visit(c)
        self.visit(n.left)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a == b)

    # noinspection PyPep8Naming
    def visit_BoolOp(self, n: ast.BoolOp):
        self._stack.append(n.values)
        self.visit(n.op)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_And(self, n: ast.And):
        expressions = self._stack.pop()
        cur_value = None
        for cur_expression in expressions:
            self.visit(cur_expression)
            cur_value = self._stack.pop()
            if not cur_value:
                break
        self._stack.append(cur_value)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Or(self, n: ast.Or):
        expressions = self._stack.pop()
        cur_value = None
        for cur_expression in expressions:
            self.visit(cur_expression)
            cur_value = self._stack.pop()
            if cur_value:
                break
        self._stack.append(cur_value)

    # noinspection PyPep8Naming
    @_log
    def visit_Num(self, n: ast.Num):
        self._stack.append(n.n)

    # noinspection PyPep8Naming
    @_log
    def visit_Str(self, n: ast.Str):
        self._stack.append(n.s)

    # noinspection PyPep8Naming
    @_log
    def visit_Load(self, n: ast.Load):
        pass

    # noinspection PyPep8Naming
    @_log
    def visit_Name(self, n: ast.Name):
        assert n.id == self._context_name, 'Undefined {}'.format(n.id)
        self._stack.append(self._context)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Mult(self, n: ast.Mult):
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a * b)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Add(self, n: ast.Add):
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a + b)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Sub(self, n: ast.Sub):
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b - a)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_UnaryOp(self, n: ast.UnaryOp):
        self.visit(n.operand)
        self.visit(n.op)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_USub(self, n: ast.USub):
        self._stack.append(-self._stack.pop())

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_UAdd(self, n: ast.UAdd):
        pass

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Not(self, n: ast.Not):
        self._stack.append(not self._stack.pop())

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Invert(self, n: ast.Invert):
        self._stack.append(~self._stack.pop())

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Div(self, n: ast.Sub):
        a = self._stack.pop()
        b = self._stack.pop()

        if type(b) == type(a) == int:
            self._stack.append(b // a)
        else:
            self._stack.append(b / a)

    # noinspection PyPep8Naming, PyUnusedLocal
    @_log
    def visit_Call(self, n: ast.Call):
        function_name = n.func.id
        if function_name not in self._known_functions:
            raise UnparsableException(n, 'Unknown function {}'.format(function_name))
        fun = self._known_functions[function_name]
        for arg in n.args:
            self.visit(arg)
        self._stack.append(
            fun(*[self._stack.pop() for _ in range(len(n.args))][::-1])
        )

    @property
    def value(self):
        return self._stack[0] if self._stack else None


def _parse(expr: str, visitor: ValueVisitor) -> typing.Any:
    visitor.visit(ast.parse(expr))
    return visitor.value


def parse(context: typing.Dict, expr: str, context_name: str=_DEFAULT_CONTEXT_NAME) -> typing.Any:
    return _parse(expr, _ExpressionVisitor(context, context_name=context_name))


class VisitorBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_context_name(self, context_name: str) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def add_function(self, function: typing.Callable, name: str = None) -> None:
        pass  # pragma: no cover

    @abc.abstractmethod
    def set_context(self, context: typing.Dict) -> None:
        pass  # pragma: no cover


class _VisitorBuilder(VisitorBuilder):
    def __init__(self):
        self._context_name = _DEFAULT_CONTEXT_NAME
        self._recorded_functions = {}
        self._context = {}

    def set_context_name(self, context_name: str) -> None:
        self._context_name = context_name

    def add_function(self, function: typing.Callable, name: str=None) -> None:
        self._recorded_functions[name or function.__name__] = function

    def set_context(self, context: typing.Dict) -> None:
        self._context = context

    def build(self) -> ValueVisitor:
        visitor = _ExpressionVisitor(self._context, context_name=self._context_name)
        for name, fun in self._recorded_functions.items():
            visitor.add_known_function(name, fun)
        return visitor


def create_visitor_builder() -> VisitorBuilder:
    return _VisitorBuilder()


def parse_from_builder(expr: str, builder: VisitorBuilder) -> typing.Any:
    # noinspection PyUnresolvedReferences
    return _parse(expr, builder.build())

__all__ = ['parse', 'parse_from_builder', 'create_visitor_builder', 'VISITOR_LOGGER', 'VisitorBuilder']
