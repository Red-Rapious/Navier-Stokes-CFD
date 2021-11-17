"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

import numpy as np
import sympy as sp
from sympy.utilities.lambdify import lambdify
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


"""Etape 4 : Equation de Burgers en 1 dimension"""
BLIT = False
SAVE = False

fig, axes = plt.subplots(figsize=(11,7), dpi=100)
axes.set_title("Equation de Burgers en 1 dimension")

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
t=0
u= np.asarray([ufunc(t, x0, nu) for x0 in x])


plt.xlim([0, 2*np.pi]) 
# condition aux limites périodiques : u(0) = u(2pi)
# on n'a alors besoin de tracer la fonction que sur [0, 2pi]
plt.ylim([0, 10])

u_analytical = np.asarray([ufunc(nt*dt, xi, nu) for xi in x])

line_computed, = axes.plot(np.linspace(0,2,nx), u)
line_analytical, = axes.plot(x, u_analytical)

# Animation 
def animate(n):
    u_n = u.copy()
    for i in range(1, nx-1): 
        # on commence à 1 car u_n dépend de u_n-1 ; on finit à u_n -1 car u_n dépend de u_n+1
        u[i] = u_n[i] - u_n[i] * dt / dx *(u_n[i] - u_n[i-1]) + nu * dt / dx**2 *(u_n[i+1] - 2 * u_n[i] + u_n[i-1])
    u[0]=u_n[0]-u_n[0]*dt/dx * (u_n[0]-u_n[-2]) + nu*dt/dx**2 *(u_n[1]-2*u_n[0]+u_n[-2])
    u[-1]=u[0]
    line_computed.set_data(x, u)
    line_analytical.set_data(x, [ufunc(n*dt, xi, nu) for xi in x])
    return line_computed, line_analytical,

anim = FuncAnimation(fig, animate, frames = nt, interval = dt, blit = BLIT)
if SAVE:
    writergif = PillowWriter(fps=30)
    anim.save('Images/animation-step4.gif', writer=writergif)

plt.show()