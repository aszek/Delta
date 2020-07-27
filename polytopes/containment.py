from mosek.fusion import *
import numpy as np

# Models the biggest homothetic image of polytope P
# which can be contained in polytope Q rotated by rotation matix A (parametric).
def biggestPInQ(vertP, vertQ):
    d = len(vertP)
    n, m = len(vertP[0]), len(vertQ[0])
    assert len(vertQ) == d

    M = Model()

    t = M.variable([m, n], Domain.greaterThan(0.0))
    M.constraint(Expr.sum(t, 0), Domain.equalsTo(1))

    x = M.variable(d)      # Coordinates of one vertex of P's copy
    r = M.variable()       # Scaling factor for P's copy
    A = M.parameter([d, d])# Rotation matrix

    # Each vertex in P's copy belongs to Q rotated by A.
    # Symbolically
    # [x..x] + r * vertP = A * vertQ * t
    M.constraint(Expr.sub( Expr.add(Var.hrepeat(x,n), Expr.mul(r, vertP)),
                           Expr.mul(A, Expr.mul(vertQ, t)) ),
                 Domain.equalsTo(0.0))

    M.objective(ObjectiveSense.Maximize, r)

    return M, A, x, r

# Rotation by (alpha, beta, gamma) in R^3
def rot3(alpha, beta, gamma):
    ca, cb, cg = np.cos(alpha), np.cos(beta), np.cos(gamma)
    sa, sb, sg = np.sin(alpha), np.sin(beta), np.sin(gamma)
    return [[ca*cb, ca*sb*sg-sa*cg, ca*sb*cg+sa*sg],
            [sa*cb, sa*sb*sg+ca*cg, sa*sb*cg-ca*sg],
            [-sb,   cb*sg,          cb*cg]]

# Vertex lists of some interesting polytopes and polyhedra
square2  = np.array([[0,0], [0,1], [1,0], [1,1]]).transpose()
simplex2 = np.array([[0,0], [1,0], [0.5,np.sqrt(3)/2]]).transpose()
tri2 = np.array([[0,0], [1,0], [0.7,0.7]]).transpose()
cube3 = np.array([[0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]).transpose()

sqrt5 = np.sqrt(5)
icosahedron3 = np.array([
 [0, 1/2, 1/4*sqrt5 + 1/4],
 [0, -1/2, 1/4*sqrt5 + 1/4],
 [1/2, 1/4*sqrt5 + 1/4, 0],
 [1/2, -1/4*sqrt5 - 1/4, 0],
 [1/4*sqrt5 + 1/4, 0, 1/2],
 [1/4*sqrt5 + 1/4, 0, -1/2],
 [-1/2, 1/4*sqrt5 + 1/4, 0],
 [-1/2, -1/4*sqrt5 - 1/4, 0],
 [-1/4*sqrt5 - 1/4, 0, 1/2],
 [0, 1/2, -1/4*sqrt5 - 1/4],
 [0, -1/2, -1/4*sqrt5 - 1/4],
 [-1/4*sqrt5 - 1/4, 0, -1/2]]).transpose() # volume = 5/12*sqrt(5)+5/4

# Returns biggest copy of 3D polytope poly1 contained in polytope poly2
def MAX_CONTAINMENT_3D(poly1, poly2):
    # Solve a simple example - parametric
    M, A, x, r = biggestPInQ(poly1, poly2)
    
    # A selection of rotations (adapted to poly2 = icosahedron3)
    dom = list(np.linspace(0, 2*np.pi/5, 30))

    # Angles of maximum volume rotation
    alphamax, betamax, gammamax = 0, 0, 0

    h = -1
    for alpha in dom:
        for beta in dom:
            for gamma in dom:
                A.setValue(rot3(alpha,beta,gamma))
                M.solve()
                
                # Scaling factor for the maximum copy of poly1 in poly2
                side = r.level()[0]

                if side > h:
                    alphamax, betamax, gammamax = alpha, beta, gamma
                    h = side

    print("Maximum {h}, angles: {alpha}, {beta}, {gamma}".format(h=h, alpha=alphamax, beta=betamax, gamma=gammamax))

# Example: maximal cube in icosahedron
MAX_CONTAINMENT_3D(cube3, icosahedron3)