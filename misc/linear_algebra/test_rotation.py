import math

from misc.linear_algebra.matrices import Matrix

theta = 30
theta_r = math.pi * theta / 180.0
m = Matrix.create(
    (
        (math.cos(theta_r), -math.sin(theta_r)),
        (math.sin(theta_r), math.cos(theta_r))
    )
)
m_r = Matrix.create(
    (
        (math.cos(-theta_r), -math.sin(-theta_r)),
        (math.sin(-theta_r), math.cos(-theta_r))
    )
)
m_i = Matrix.create(
    (
        (math.cos(theta_r), math.sin(theta_r)),
        (-math.sin(theta_r), math.cos(theta_r))
    )
)
print('Inverse:', m_i, sep='\n')
print('Transposed:', m.transposed(), sep='\n')
print('Rotated opposite:', m_r, sep='\n')
