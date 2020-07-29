# The field containing sqrt(5) for exact calculations
K.<sqrt5>=NumberField(x^2-5)

# Polynomials in t over that field
R.<t>=PolynomialRing(K)

# The constant tau appearing in the coordinates of the icosahedron
tau = sqrt5/4+1/4

# Coordinates of three selected vertices of the icosahedron
v1 = vector([0, 1/2, tau])
v2 = vector([0, -1/2, tau])
v3 = vector([1/2, tau, 0])

# Vertices of the inscribed cube from the text
A = t*v1+(1-t)*v2
B = t*v1+(1-t)*v3
C = - A

# Squared Euclidean distance of points
def distsq(x,y):
    return sum(c^2 for c in x-y)

# The polynomial equation corresponding to |AC|^2 - 3*|AB|^2 from the text
f = distsq(A, C) - 3 * distsq(A,B)

# The equation for t as appearing in the text
print(f)

# Roots of the equation f (exact). One of them solves the problem.
print (f.roots())

# Choose the correct root and compute length of AB
t = f.roots()[1][0]
A = t*v1+(1-t)*v2
B = t*v1+(1-t)*v3
side = norm(A - B)
print("AB = {0}".format(side))
