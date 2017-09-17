import ast

import logging
import typing


class UnparsableException(Exception):
    def __init__(self, node: ast.AST, *a):
        super(UnparsableException, self).__init__(*a)
        self.node = node


class _ExpressionVisitor(ast.NodeVisitor):
    def __init__(
            self, context: typing.Dict,
            context_name: str='context',
            logger: logging.Logger=logging.getLogger('visitor')):
        self._stack = []
        self._context = context
        self._context_name = context_name
        self._logger = logger

    def generic_visit(self, node):
        raise UnparsableException(node, 'Could not parse node {}'.format(node))

    # noinspection PyPep8Naming
    def visit_Module(self, n: ast.Module):
        self._logger.debug('Visiting module %s', list(ast.iter_child_nodes(n)))
        for child in ast.iter_child_nodes(n):
            self.visit(child)

    # noinspection PyPep8Naming
    def visit_Expr(self, n: ast.Expr):
        self._logger.debug('Visiting module %s', n.__dict__)
        self.visit(n.value)

    # noinspection PyPep8Naming
    def visit_IfExp(self, n: ast.IfExp):
        self._logger.debug('Visiting if %s', n.__dict__)
        test_expression = n.test
        self.visit(test_expression)
        condition = self._stack.pop()
        if condition:
            self.visit(n.body)
        else:
            self.visit(n.orelse)

    # noinspection PyPep8Naming
    def visit_BinOp(self, n: ast.BinOp):
        self._logger.debug('Visiting BinOp %s', n.__dict__)
        self.visit(n.right)
        self.visit(n.left)
        self.visit(n.op)

    # noinspection PyPep8Naming
    def visit_Attribute(self, n: ast.Attribute):
        self._logger.debug('Visiting Attribute %s', n.__dict__)
        self.visit(n.value)
        self.visit(n.ctx)
        cur_data = self._stack.pop()
        self._logger.debug('cur data: %s', cur_data)
        self._stack.append(cur_data[n.attr])

    # noinspection PyPep8Naming
    def visit_Compare(self, n: ast.Compare):
        self._logger.debug('Visiting Compare %s', n.__dict__)
        for c in n.comparators:
            self.visit(c)
        self.visit(n.left)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a == b)

    # noinspection PyPep8Naming
    def visit_Num(self, n: ast.Num):
        self._logger.debug('Visiting num %s', n.__dict__)
        self._stack.append(n.n)

    # noinspection PyPep8Naming
    def visit_Str(self, n: ast.Str):
        self._logger.debug('Visiting num %s', n.__dict__)
        self._stack.append(n.s)

    # noinspection PyPep8Naming
    def visit_Load(self, n: ast.Load):
        self._logger.debug('Visiting load %s', n.__dict__)

    # noinspection PyPep8Naming
    def visit_Name(self, n: ast.Name):
        self._logger.debug('Visiting name %s', n.__dict__)
        assert n.id == self._context_name, 'Undefined {}'.format(n.id)
        self._stack.append(self._context)

    # noinspection PyPep8Naming
    def visit_Mult(self, n: ast.Mult):
        self._logger.debug('Visiting Mult %s', n.__dict__)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a * b)

    # noinspection PyPep8Naming
    def visit_Add(self, n: ast.Add):
        self._logger.debug('Visiting Add %s', n.__dict__)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a + b)

    # noinspection PyPep8Naming
    def visit_Sub(self, n: ast.Sub):
        self._logger.debug('Visiting Sub %s', n.__dict__)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(a - b)

    @property
    def value(self):
        return self._stack[0] if self._stack else None


def parse(context: typing.Dict, expr: str, context_name: str='context') -> typing.Any:
    visitor = _ExpressionVisitor(context, context_name=context_name)
    visitor.visit(ast.parse(expr))
    return visitor.value


__all__ = ['parse']
