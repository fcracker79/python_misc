from misc.linear_algebra.matrices import Matrix

c1 = Matrix.create(
    (
        (-1, 2),
        (2, 1)
    )
)

r = Matrix.create(
    (
        (1, ),
        (1, )
    )
)
c1_gs = c1.gram_schmidt()
r1_gs = c1_gs * r
r1 = c1 * r

print('r1', r1, sep='\n')
print(r1.transposed() * c1.column(0))
print(r1.transposed() * c1.column(1))

print('r1 graham schmidt', r1_gs, sep='\n')
print(r1_gs.transposed() * c1_gs.column(0))
print(r1_gs.transposed() * c1_gs.column(1))
