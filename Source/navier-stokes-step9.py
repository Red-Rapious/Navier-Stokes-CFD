"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.animation import FuncAnimation, PillowWriter

"""Etape 9 : Résolution de l'équation de Laplace en 2 dimensions"""
SAVE = False
TARGET = False
# le mode TARGET affiche la solution finie où l'intervalle entre deux itérations est plus faible que la target
# le mode ANIMATION = not TARGET affiche n itérations successives

# Code matplotlib
fig = plt.figure(dpi=100, figsize=(8,8))
axes = fig.add_subplot(projection='3d')
fig.suptitle("Résolution de l'équation de Laplace en 2 dimensions")

# Constantes
nx = 31
ny = 31
c = 1
dx = 2 / (nx-1)
dy = 2 / (ny-1)
l1norm_target = 1e-4
iterations = 100

x, y = np.linspace(0, 2, nx), np.linspace(0, 1, ny)
X, Y = np.meshgrid(x, y)

axes.set_xlim(0,2)
axes.set_ylim(0,1)
axes.view_init(30, 225)
axes.set_xlabel("$x$")
axes.set_ylabel("$y$")

# Conditions initiales
p = np.zeros((ny, nx))

p[:, 0] = 0  # 0 au bord
p[:, -1] = y  
p[0, :] = p[1, :]  # dp/dy nulle au bord
p[-1, :] = p[-2, :]  # dp/dy nulle


if TARGET: # mode target
    l1norm = 1 # différence entre deux itérations consécutives 
    while l1norm > l1norm_target:
        p_n = p.copy()
        p[1:-1, 1:-1] = ((dy**2 * (p_n[1:-1, 2:] + p_n[1:-1, 0:-2]) + dx**2 * (p_n[2:, 1:-1] + p_n[0:-2, 1:-1])) / (2 * (dx**2 + dy**2)))
        
        
        p[:, 0] = 0  # 0 au bord
        p[:, -1] = y  
        p[0, :] = p[1, :]  # dp/dy nulle au bord
        p[-1, :] = p[-2, :]  # dp/dy nulle
        l1norm = (np.sum(np.abs(p[:]) - np.abs(p_n[:])) / np.sum(np.abs(p_n[:])))


    # Dessin
    surf = axes.plot_surface(X,Y, p[:], cmap=cm.viridis, rstride=1, cstride=1, linewidth=0, antialiased=False)
    surf._facecolors2d = surf._facecolor3d
    surf._edgecolors2d = surf._edgecolor3d


if not TARGET:
    axes.text2D(0.40, 0.98, "Itération "+str(0), transform=axes.transAxes)

    # Animation 
    def animate(n):
        p_n = p.copy()
        p[1:-1, 1:-1] = ((dy**2 * (p_n[1:-1, 2:] + p_n[1:-1, 0:-2]) + dx**2 * (p_n[2:, 1:-1] + p_n[0:-2, 1:-1])) / (2 * (dx**2 + dy**2)))
        
        p[:, 0] = 0  # 0 au bord
        p[:, -1] = y  
        p[0, :] = p[1, :]  # dp/dy nulle au bord
        p[-1, :] = p[-2, :]  # dp/dy nulle

        axes.clear()
        surf = axes.plot_surface(X,Y, p[:], cmap=cm.viridis, rstride=1, cstride=1, linewidth=0, antialiased=False)
        axes.set_xlabel("$x$")
        axes.set_ylabel("$y$")
        # code pour éviter une erreur de matplotlib ; j'ai vraiment aucune idée de ce que c'est, je l'ai juste copy-paste de stackoverflow
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d

        axes.text2D(0.40, 0.98, "Itération "+str(n), transform=axes.transAxes)

    anim = FuncAnimation(fig, animate, frames = iterations, blit = False)
    if SAVE:
        writergif = PillowWriter(fps=30)
        anim.save('Images/animation-step9.gif', writer=writergif)

plt.show()