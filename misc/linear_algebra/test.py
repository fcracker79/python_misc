from misc.linear_algebra.matrices import Matrix

m = Matrix.create(
    (
        (1, 2, 3),
        (1, 0, 1),
        (1, 1, -1)
    )
)

mirror = Matrix.create(
    (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, -1)
    )
)

v = Matrix.create(
    (
        (2, ),
        (3, ),
        (5, )
    )
)

g = m.gram_schmidt()
g_inv = g.transposed()
print(g * mirror * g_inv * v)