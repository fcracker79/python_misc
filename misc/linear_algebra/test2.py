from misc.linear_algebra.matrices import Matrix

plane = Matrix.create(
    (
        (1, ),
        (2, ),
        (3, )
    )
)

m = Matrix.create(
    (
        (2,   1, 1),
        (-1,  1, 2),
        (0,  -1, 3)
    )
)
v = Matrix.create(
    (
        (2, ),
        (3, ),
        (5, )
    )
)

t = Matrix.create(
    (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, -1)
    )
)
g = m.gram_schmidt()
print(g * t * g.transposed() * v)
