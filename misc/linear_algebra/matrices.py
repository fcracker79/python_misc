import math
import typing


class Matrix:
    def __init__(self, n: int, m: int):
        self.n, self.m = n, m
        self.items = [0] * (n * m)

    @classmethod
    def create(cls, rows: typing.Sequence[typing.Sequence[float]]):
        a = Matrix(len(rows), len(rows[0]))
        for i in range(a.n):
            for j in range(a.m):
                a.set_item(i, j, rows[i][j])
        return a

    def transposed(self):
        a = Matrix(self.m, self.n)
        for i in range(a.n):
            for j in range(a.m):
                a.set_item(i, j, self.item(j, i))
        return a

    def item(self, i: int, j: int) -> int:
        return self.items[i * self.m + j]

    def set_item(self, i: int, j: int, value):
        self.items[i * self.m + j] = value

    def __mul__(self, b: typing.Union['Matrix', float]) -> 'Matrix':
        if isinstance(b, float):
            new_matrix = Matrix(self.n, self.m)

            def _new_value(i, j):
                return self.item(i, j) * b
        else:
            new_matrix = Matrix(self.n, b.m)

            def _new_value(i, j):
                return sum(self.item(i, k) * b.item(k, j) for k in range(self.m))
        for i in range(new_matrix.n):
            for j in range(new_matrix.m):
                new_matrix.set_item(i, j, _new_value(i, j))
        return new_matrix

    def row(self, r: int) -> 'Matrix':
        m = Matrix(1, self.m)
        for j in range(self.m):
            m.set_item(0, j, self.item(r, j))
        return m

    def column(self, c: int) -> 'Matrix':
        m = Matrix(self.n, 1)
        for i in range(self.n):
            m.set_item(i, 0, self.item(i, c))
        return m

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        m = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                m.set_item(i, j, self.item(i, j) - other.item(i, j))
        return m

    def __add__(self, other: 'Matrix') -> 'Matrix':
        m = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                m.set_item(i, j, self.item(i, j) + other.item(i, j))
        return m

    def __iter__(self):
        return iter(self.items)

    def gram_schmidt(self) -> 'Matrix':
        m = Matrix(self.n, self.m)
        new_vectors = []
        for i in range(self.m):
            u = self.column(i)
            if new_vectors:
                u = u - sum((e * (u.transposed() * e) for e in new_vectors), Matrix(self.n, 1))
            e = u * (1 / math.sqrt(sum(x**2 for x in u)))
            new_vectors.append(e)
        for j, v in enumerate(new_vectors):
            for i, value in enumerate(v):
                m.set_item(i, j, value)
        return m

    def __str__(self):
        s = ''
        for i in range(self.n):
            s += '|'
            s += ', '.join(str(self.item(i, j)) for j in range(self.m))
            s += '|\n'
        return s

    def __repr__(self):
        return str(self)

    def determinant(self):
        if self.n == self.m == 1:
            return self.item(0, 0)

        result = 0.0

        sign = 1.0
        for c in range(self.m):
            result += sign * self.item(0, c) * self.submatrix(0, c).determinant()
            sign = -sign
        return result

    def submatrix(self, r: int, c: int) -> 'Matrix':
        m = Matrix(self.n - 1, self.m - 1)

        di = 0
        for i in range(self.n):
            if i == r:
                di = 1
                continue
            dj = 0
            for j in range(self.m):
                if j == c:
                    dj = 1
                    continue
                m.set_item(i - di, j - dj, self.item(i, j))
        return m
