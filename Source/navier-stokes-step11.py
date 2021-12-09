"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.animation import FuncAnimation, PillowWriter

"""Etape 11 : Résolution de l'équation de Navier-Stokes dans une cavité"""
SAVE = False

# Constantes
nx = 41
ny = 41
nt = 1000 # nombre d'itérations temporelles
nit = 50 # nombre d'itérations pour Poisson
c = 1
dx = 2 / (nx-1)
dy = 2 / (ny -1)

x = np.linspace(0, 2, nx)
y = np.linspace(0, 2, ny)
X, Y = np.meshgrid(x, y) # pour le tracé

rho = 1 # masse volumique
nu = .1 # viscosité cinématique du fluide (nu = mu/rho)
dt = .001 # intervalle de temps

u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))

def build_up_b(b, rho, dt, u, v, dx, dy):
    # fonction pour alléger l'écriture par la suite

    # formule bien compliquée, voir les calculs
    b[1:-1, 1:-1] = (rho * (1 / dt * ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) + (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) - ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 - 2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) * (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) - ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2))
    
    return b

def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p) # copie vide de p
    pn = p.copy()

    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 + (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) / (2 * (dx**2 + dy**2)) - dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * b[1:-1,1:-1])
        
        # CI
        p[:, -1] = p[:, -2] # dp/dx = 0 at x = 2
        p[0, :] = p[1, :]   # dp/dy = 0 at y = 0
        p[:, 0] = p[:, 1]   # dp/dx = 0 at x = 0
        p[-1, :] = 0        # p = 0 at y = 2
    
    return p

u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))

fig, axes = plt.subplots(figsize=(11,7), dpi=100)
axes.set_title("Résolution de l'équation de Navier-Stokes dans une cavité")

# mode contour de matplotlib pour les champs de pression
ctf = plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
plt.colorbar()
#ct = plt.contour(X, Y, p, cmap=cm.viridis)

quiver = plt.quiver(X[::2, ::2], Y[::2, ::2], u[::2, ::2], v[::2, ::2])

txt = fig.text(0.45, 0.96, "Temps t="+str(0))

plt.xlabel('X')
plt.ylabel('Y')

def animate(n):
    if n%50==0 and SAVE:
        print("Saving, t="+ str(n) + "/" + str(nt))
    global b, u, v, p
    un = u.copy()
    vn = v.copy()
    
    b = build_up_b(b, rho, dt, u, v, dx, dy)
    p = pressure_poisson(p, dx, dy, b)

    u[1:-1, 1:-1] = (un[1:-1, 1:-1]-
                        un[1:-1, 1:-1] * dt / dx *
                    (un[1:-1, 1:-1] - un[1:-1, 0:-2]) -
                        vn[1:-1, 1:-1] * dt / dy *
                    (un[1:-1, 1:-1] - un[0:-2, 1:-1]) -
                        dt / (2 * rho * dx) * (p[1:-1, 2:] - p[1:-1, 0:-2]) +
                        nu * (dt / dx**2 *
                    (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) +
                        dt / dy**2 *
                    (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])))

    v[1:-1,1:-1] = (vn[1:-1, 1:-1] -
                    un[1:-1, 1:-1] * dt / dx *
                    (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) -
                    vn[1:-1, 1:-1] * dt / dy *
                    (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) -
                    dt / (2 * rho * dy) * (p[2:, 1:-1] - p[0:-2, 1:-1]) +
                    nu * (dt / dx**2 *
                    (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) +
                    dt / dy**2 *
                    (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])))

    u[0, :]  = 0
    u[:, 0]  = 0
    u[:, -1] = 0
    u[-1, :] = 1    # la vitesse au bord est égale à 1
    v[0, :]  = 0
    v[-1, :] = 0
    v[:, 0]  = 0
    v[:, -1] = 0

    global ctf, quiver
    for c in ctf.collections:
        c.remove()
        
    """for c in ct.collections:
        c.remove()"""
    
    # champs de pressions
    ctf = plt.contourf(X, Y, p, alpha=0.5, cmap=cm.viridis)
    #ct = plt.contour(X, Y, p, cmap=cm.viridis)

    quiver.remove()
    
    np = 2
    quiver = plt.quiver(X[::np, ::np], Y[::np, ::np], u[::np, ::np], v[::np, ::np]) # un point sur np (ex : un sur deux)
    plt.xlabel('X')
    plt.ylabel('Y')

    txt.set_text("Temps t="+str(n))
    return ctf,

anim = FuncAnimation(fig, animate, frames = nt, interval = dt, blit = False)
if SAVE:
    writergif = PillowWriter(fps=30)
    anim.save('Images/animation-step11.gif', writer=writergif)

plt.show()