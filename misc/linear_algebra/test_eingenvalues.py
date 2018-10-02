import math

from misc.linear_algebra.matrices import Matrix

t = Matrix.create(
    (
        (1, -2),
        (3, -5)
    )
)

c = Matrix.create(
    (
        (2/(3-math.sqrt(3)), 1),
        (1, math.sqrt(3) / (math.sqrt(3) - 1))
    )
)

det_c = c.determinant()
c_1 = Matrix.create(
    (
        (math.sqrt(3) / (math.sqrt(3) - 1), -1),
        (-1, 2/(3-math.sqrt(3)))
    )
)

c_1 = c_1 * (1 / det_c)

print(c * c_1)

d = Matrix.create(
    (
        (-2+math.sqrt(3), 0),
        (0, -2-math.sqrt(3))
    )
)
print(c * d * c_1)
