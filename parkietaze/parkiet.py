# Autor: Michal Adamaszek
#
# Demonstruje eksperymenty z programowaniem calkowitoliczbowym
# i certyfikatami niespelnialnosci
# na przykladzie problemow pokrywania prostokatow mniejszymi prostokatami
#
# Zob. http://www.math.uni.wroc.pl/~jwr/trapez/ zadania 77-126
#
#

# Te pakiety sa zupelnie standardowe
import sys
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Instrukcja instalacji pakietu cvxpy znajduje sie w README
import cvxpy as cvx

# Wyswietla pokrycie
def display(n, m, sol, T, col):
    fig,ax = plt.subplots(1)
    for p,q,k in sol:
        ax.add_patch(patches.Rectangle((q,n-1-p-T[k][0]), T[k][1], T[k][0], linewidth=2, facecolor=col[k]))
    ax.axis([0, m, 0, n])
    ax.axis('off')
    ax.set_aspect('equal')
    plt.show()

# Buduje model dla problemu
# n,m - wymiary
# T - lista typow prostokatow
def buildModel(n, m, T):
    numtypes = len(T)

    # Zmienne binarne - po jednej dla kazdego pola i typu x_{i,j}^T
    # Niestety cvxpy nie ma zmiennych o wiecej niz dwoch wymiarach...
    x = { t : cvx.Variable((n,m), boolean=True) for t in T }

    # lista wszystkich ograniczen
    cons = []

    # Wyeliminuj polozenia wystajace poza plansze
    for a,b in T:
        if b>=2: cons.append(x[(a,b)][:, max(0,m-b+1):] == 0)
        if a>=2: cons.append(x[(a,b)][max(0,n-a+1):, :] == 0)

    # Dodaj nm rownan liniowych (1)
    for i,j in product(range(n), range(m)):
        cover = []  # Lista polozen ktore pokrywaja (i,j)
        for a,b in T:
            for p,q in product(range(n), range(m)):
                # Klocek a x b z pole (p,q) pokrywa (i,j)
                if p<=i and q<=j and p+a>i and q+b>j:
                    cover.append(x[(a,b)][p,q])

        cons.append(cvx.sum(cover) == 1)

    # Objective - nieistotny, chcemy znalezc jakiekolwiek rozwiazanie
    prob = cvx.Problem(cvx.Maximize(0), cons)

    # Rozwiazujemy.
    # Zmien na verbose=True aby zobaczyc co robi kazdy solver
    prob.solve(verbose=False, solver=cvx.ECOS_BB)

    if prob.status == 'optimal':
        # Znaleziono rozwiazanie, ktore przetwarzamy i zwracamy
        return [(i,j,t) for i in range(n) for j in range(m) for t in range(numtypes) if x[T[t]].value[i,j] > 0.9]
    else:
        # Nie znaleziono parkietazu
        return None
    
# Znajduje certifikat dla problemu
# n,m - wymiary
# T - lista typow prostokatow
def findCertificate(n, m, T):
    numtypes = len(T)

    # Wspolczynniki wystepujace w certyfikacie
    y = cvx.Variable((n,m))

    # lista wszystkich ograniczen
    cons = []

    for i,j in product(range(n), range(m)):
        for a,b in T:
            # Jezeli polozenie klocka w polu (i,j) miesci sie na planszy:
            if i+a<=n and j+b<=m:
                # Suma pol zajetych przez klocek jest rowna 0
                cons.append(cvx.sum(y[i:i+a, j:j+b]) == 0)

    # Suma wszystkich liczb jest rozna od 0
    # Ten warunek nie jest wypukly, ale rownie dobrze mozemy napisac >= 1
    cons.append(cvx.sum(y) >= 1)

    # Objective - nieistotny, chcemy znalezc jakiekolwiek rozwiazanie
    prob = cvx.Problem(cvx.Minimize(0), cons)

    # Rozwiazujemy.
    prob.solve(verbose=False, solver=cvx.ECOS)

    if prob.status == 'optimal':
        # Znaleziono rozwiazanie, ktore wypiszemy
        for i in range(n):
            print(' '.join(['{0: .1f}'.format(y.value[i,j]) for j in range(m)]))
    else:
        # Nie znaleziono certyfikatu
        print('Brak certyfikatu')

##            ##
#  PRZYKLADY   #
##            ## 
# Maly przyklad ze wstepu, wyswietlamy gotowy parkietaz
def ex1():
    display(4, 2, 
        [(0,0,0), (1,0,1),  (1,1,2)],
        [(1,2),   (3,1),    (3,1)],
        ['blue',  'red',    'yellow'])

# Przyklad z pierwszego zdania artykulu
# Nie ma rozwiazania, wiec wypiszemy certifikat
def ex2():
    n, m = 15, 15
    T    = [(1,8), (8,1), (1,11), (11,1)] 
    solution = buildModel(n, m, T)
    if not solution:
        print('Nie znaleziono parkietazu. Certyfikat:')
        findCertificate(n, m, T)

# Wiekszy przyklad dla ktorego istnieje rozwiazanie
def ex3():
    n, m = 22, 27
    T    = [(8,2), (5,2), (1,7)]
    solution = buildModel(n, m, T)
    if solution:
        display(n, m, solution, T, ['red', 'green', 'yellow'])

# Przyklad z tresci artykulu
def ex4():
    n, m = 3, 4
    T    = [(1,3), (2,1)]
    solution = buildModel(n, m, T)
    if not solution:
        print('Nie znaleziono parkietazu. Certyfikat:')
        findCertificate(n, m, T)

