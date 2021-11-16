"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.animation import FuncAnimation, PillowWriter

"""Etape 5 : Convection linéaire en 2 dimensions"""

BLIT = False # ne marche pas avec True
SAVE = True

fig = plt.figure(dpi=100, figsize=(8,8))
axes = fig.add_subplot(projection='3d')
axes.set_title("Animation de déplacement d'une vague en 2 dimensions à convection linéaire")


# Constantes
nx = 81 # nombre de points en x
ny = 81 # nombre de points en y
nt = 180 # nombre d'étapes à calculer
dx = 2/(nx-1)
dy = 2/(ny-1)
sigma = .2
dt = sigma * dx
c = 1 # célérité de l'onde

x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)

X, Y = np.meshgrid(x, y)


# Création du signal créneau, conditions initiales
u = np.ones((ny, nx)) # niveau bas ; u est un vecteur de taille 1 sur n
u[int(.5/dy):int(1/dy+1), int(.5/dx):int(1/dx +1)]=2 # niveau haut pour .5<=x<=1 et ;5<=y<=1 (simultanément)

# Calcul de u en fonction du temps : n et n+1 sont deux instants consécutifs
u_n = np.ones((ny, nx))
#line, = axes.plot(np.linspace(0,2,nx), u)

surf = axes.plot_surface(X,Y, u[:], cmap=cm.viridis)


# Animation 
def animate(n):
    global u_n
    global u
    global line

    u_n = u.copy()

    row, col = u.shape
    #for j in range(1, row):
    #    for i in range(1, col):
    #        u[j,i] = (u_n[j,i] - (c*dt/dx*(u_n[j,i]-u_n[j, i-1]))- (c*dt/dy*(u_n[j,i]-u_n[j-1, i])))
            
    # même effet que les boucles commentées, en plus élégant
    u[1:, 1:] = (u_n[1:, 1:] - (c*dt/dx*(u_n[1:, 1:]-u_n[1:, :-1])) - (c*dt/dy*(u_n[1:, 1:] - u_n[:-1, 1:])))
            
    # conditions aux bords
    u[0, :] = 1
    u[-1, :] = 1
    u[:, 0] = 1
    u[:, -1] = 1
    axes.clear()
    surf = axes.plot_surface(X, Y, u[:], cmap=cm.viridis)
    # code pour éviter une erreur de matplotlib ; j'ai vraiment aucune idée de ce que c'est, je l'ai juste copy-paste de stackoverflow
    surf._facecolors2d = surf._facecolor3d
    surf._edgecolors2d = surf._edgecolor3d

    return surf,

anim = FuncAnimation(fig, animate, frames = nt, interval = dt, blit = BLIT)
if SAVE:
    writergif = PillowWriter(fps=30)
    anim.save('Images/animation-step5.gif', writer=writergif)

plt.show()