"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

import numpy as np
import sympy as sp
from sympy.utilities.lambdify import lambdify
import matplotlib.pyplot as plt

"""Etape 4 : Equation de Burgers"""
ANIMATED = False
if ANIMATED:
    fig, axes = plt.subplots(figsize=(11,7), dpi=100)
    axes.set_title("Signal en dents de scie")
else:
    plt.figure(figsize=(11,7), dpi=100)

# Calcul et dérivation des fonctions
x, nu, t = sp.symbols('x nu t')
phi = (sp.exp(-(x - 4 * t)**2 / (4 * nu * (t + 1))) + sp.exp(-(x - 4 * t - 2 * sp.pi)**2 / (4 * nu * (t + 1))))
phiprime = phi.diff(x)

u = -2 * nu * (phiprime/phi) + 4
ufunc = lambdify((t, x, nu), u)

# Constantes
nx = 101 # nombre de points
nt = 100 # nombre d'étapes à calculer
dx = 2*np.pi / (nx-1)
nu = .07 # viscosité
dt = dx*nu # intervalle de temps

# Calcul de u en fonction du temps : n et n+1 sont deux instants consécutifs
x=np.linspace(0, 2*np.pi, nx)
u_n = np.empty(nx)
t=0
u= np.asarray([ufunc(t, x0, nu) for x0 in x])


plt.xlim([0, 2*np.pi]) 
# condition aux limites périodiques : u(0) = u(2pi)
# on n'a alors besoin de tracer la fonction que sur [0, 2pi]
plt.ylim([0, 10])

# solution approchée
for n in range(nt): # nombre d'étapes temporelles
    u_n = u.copy()
    for i in range(1, nx-1): 
        # on commence à 1 car u_n dépend de u_n-1 ; on finit à u_n -1 car u_n dépend de u_n+1
        u[i] = u_n[i] - u_n[i] * dt / dx *(u_n[i] - u_n[i-1]) + nu * dt / dx**2 *(u_n[i+1] - 2 * u_n[i] + u_n[i-1])
    u[0]=u_n[0]-u_n[0]*dt/dx * (u_n[0]-u_n[-2]) + nu*dt/dx**2 *(u_n[1]-2*u_n[0]+u_n[-2])
    u[-1]=u[0]
    if ANIMATED:
        u_analytical = np.asarray([ufunc(n*dt, xi, nu) for xi in x])
        axes.clear()
        axes.plot(x,u,marker='o', lw=2, label="Approchée")
        axes.plot(x, u_analytical, label='Exacte')
        plt.pause(dt)

# solution exacte
if not ANIMATED:
    u_analytical = np.asarray([ufunc(nt*dt, xi, nu) for xi in x])

# Tracé des deux solutions
if not ANIMATED:
    plt.plot(x,u,marker='o', lw=2, label="Approchée")
    plt.plot(x, u_analytical, label='Exacte')
    plt.title("Signal en dents de scie")
    plt.legend()

plt.show()