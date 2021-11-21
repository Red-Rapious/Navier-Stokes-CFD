"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.animation import FuncAnimation, PillowWriter

"""Etape 10 : Résolution de l'équation de Poisson en 2 dimensions"""
SAVE = True

# Code matplotlib
fig = plt.figure(dpi=100, figsize=(8,8))
axes = fig.add_subplot(projection='3d')
fig.suptitle("Résolution de l'équation de Poisson en 2 dimensions")

# Constantes
nx = 50
ny = 50
nt = 100
xmin = 0
xmax = 2
ymin = 0
ymax = 1
dx = (xmax - xmin) / (nx-1)
dy = (ymax - ymin) / (ny-1)

x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)

X, Y = np.meshgrid(x, y)


p  = np.zeros((ny, nx))
b  = np.zeros((ny, nx))
x  = np.linspace(xmin, xmax, nx)
y  = np.linspace(xmin, xmax, ny)

# deux sources, pics verticaux
b[int(ny/4), int(nx/4)] = 100
b[int(3 * ny /4), int(3 * nx /4)] = -100


axes.set_xlabel("$x$")
axes.set_ylabel("$y$")
axes.set_zlim(-1.0, 1.0)
axes.view_init(30, 225)
surf = axes.plot_surface(X,Y, p[:], cmap=cm.viridis, rstride=2, cstride=2, linewidth=0, antialiased=False)

axes.text2D(0.40, 0.98, "Pseudo-temps t="+str(0), transform=axes.transAxes)

# Animation 
def animate(n):
    pd = p.copy()

    p[1:-1,1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy**2 + (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx**2 - b[1:-1, 1:-1] * dx**2 * dy**2) / (2 * (dx**2 + dy**2)))

    p[0, :] = 0
    p[ny-1, :] = 0
    p[:, 0] = 0
    p[:, nx-1] = 0

    axes.set_xlabel("$x$")
    axes.set_ylabel("$y$")
    axes.set_zlim(-1.0, 1.0)
    
    axes.clear()
    surf = axes.plot_surface(X,Y, p[:], cmap=cm.viridis, rstride=1, cstride=1, linewidth=0, antialiased=False)
    # code pour éviter une erreur de matplotlib ; j'ai vraiment aucune idée de ce que c'est, je l'ai juste copy-paste de stackoverflow
    surf._facecolors2d = surf._facecolor3d
    surf._edgecolors2d = surf._edgecolor3d

    axes.text2D(0.40, 0.98, "Pseudo-temps t="+str(n), transform=axes.transAxes)

    return surf,

anim = FuncAnimation(fig, animate, frames = nt, blit = False)
if SAVE:
    writergif = PillowWriter(fps=30)
    anim.save('Images/animation-step10.gif', writer=writergif)

plt.show()