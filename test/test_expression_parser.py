import typing
import unittest

from misc import expression_parser


class TestExpressionParser(unittest.TestCase):
    def setUp(self):
        self._fixture_context = {
            'a': {
                'b': 1,
                'c': 2,
            },
            'd': 'hello',
            'e': 3
        }

    def _assert_expression(self, expected_value: typing.Any, expression: str):
        self.assertEqual(expected_value, expression_parser.parse(self._fixture_context,expression))

    def test_if(self):
        self._assert_expression(4, 'context.a.c * 2 if context.d == "hello" else context.a.b + context.a.c')
        self._assert_expression(3, 'context.a.c * 2 if context.d == "hello2" else context.a.b + context.a.c')

    def test_add(self):
        self._assert_expression(6, 'context.e + context.a.b + context.a.c')

    def test_sub(self):
        self._assert_expression(-1, 'context.e - context.a.c - context.a.c')
        self._assert_expression(1, 'context.a.c + context.a.c - context.e')

    def test_mul(self):
        self._assert_expression(6, 'context.e * context.a.c')
        self._assert_expression('hellohellohello', 'context.d * context.e')
