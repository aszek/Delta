# The field containing sqrt(5) for exact calculations
K.<sqrt5>=NumberField(x^2-5)

# Polynomials in t over that field
R.<t>=PolynomialRing(K)

# The constant tau appearing in the coordinates of the icosahedron
tau = sqrt5/4+1/4

# The polynomial equation corresponding to |AC|^2 - 3*|AB|^2 from the text
f = 4*((t-1/2)^2+tau^2) - 3*((1/2-1/2*t)^2 + (1/2*t-t*tau+tau-t+1/2)^2 + (t*tau-tau)^2)

# The equation for t appearing in the text 
print(f)

# Roots of the equation f (exact). One of them solves the problem.
print (f.roots())