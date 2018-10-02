from misc.linear_algebra.matrices import Matrix

c_1 = Matrix.create(
    (
        (1, 0),
        (-1, 1)
    )
)
c = Matrix.create(
        (
            (1, 0),
            (1, 1)
        )
    )

print(c*c_1)

t = Matrix.create(
    (
        (1, 0),
        (2, -1)
    )
)

d = Matrix.create(
    (
        (1, 0),
        (0, -1)
    )
)
print(
    c*d*d*d*d*d*c_1
)

print(t*t*t*t*t)
