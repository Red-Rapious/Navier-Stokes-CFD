"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


"""Etape 3 : Diffusion en 1 dimension"""
BLIT = False
SAVE = False

fig, axes = plt.subplots(1,1, figsize=(8,8))
axes.set_title("Animation de la diffusion d'une vague en 1 dimension") # ne marche pas, ni pour plt, ni pour axes, ni pour fig

# Constantes
nx = 41 # nombre de points
dx = 2/(nx-1)
nt = 100 # nombre d'étapes à calculer
nu = .3 # viscosité
sigma = .2 # TODO
dt = sigma * dx**2 / nu # temps en chaque étape, dépendant de sigma et de la viscosité (delta t)

# Création du signal créneau
u = np.ones(nx) # niveau bas
u[int(.5/dx):int(1/dx+1)]=2 # niveau haut (entre .5 et 1)
# u=2 entre .5 et 1

# Calcul de u en fonction du temps : n et n+1 sont deux instants consécutifs
u_n = np.ones(nx)
line, = axes.plot(np.linspace(0,2,nx), u)

# Animation 
def animate(n):
    global u_n
    global line

    u_n = u.copy()
    for i in range(1, nx-1): 
        # on commence à 1 car u_n dépend de u_n-1 ; on finit à u_n -1 car u_n dépend de u_n+1
        u[i] = u_n[i] + nu * dt / dx**2 * (u_n[i+1] - 2* u_n[i] + u_n[i-1])
    line.set_data(np.linspace(0,2,nx), u)
    return line,

anim = FuncAnimation(fig, animate, frames = nt, interval = dt, blit = BLIT)
if SAVE:
    writergif = PillowWriter(fps=30)
    anim.save('Images/animation-step3.gif', writer=writergif)

plt.show()