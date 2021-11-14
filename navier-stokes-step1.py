"""
Créé par Antoine Groudiev, 2021
Référence : lorenabarba.com/blog/cfd-python-12-steps-to-navier-stokes/
"""

import numpy as np
import matplotlib.pyplot as plt

"""Etape 1 : Convection linéaire en 1 dimension"""

ANIMATED = True
CLEAR = False

if ANIMATED:
    fig, axes = plt.subplots(1,1, figsize=(8,8))
    axes.set_title("Animation de déplacement d'une vague en 1 dimension à convection linéaire")
else:
    plt.title("Chronographie du déplacement d'une vague en 1 dimension à convection linéaire")

# Constantes
nx = 41 # nombre de points
dx = 2/(nx-1)
nt = 25 # nombre d'étapes à calculer
dt = .025 # temps en chaque étape (delta t)
c = 1 # célérité de l'onde

# Création du signal créneau
u = np.ones(nx) # niveau bas
u[int(.5/dx):int(1/dx+1)]=2 # niveau haut (entre .5 et 1)
# u=2 entre .5 et 1

# Calcul de u en fonction du temps : n et n+1 sont deux instants consécutifs
u_n = np.ones(nx)

for n in range(nt): # nombre d'étapes temporelles
    u_n = u.copy()
    for i in range(1, nx): # on commence à 1 car u_n dépend de u_n-1
        u[i] = u_n[i] - c*dt/dx*(u_n[i] - u_n[i-1])
    
    if ANIMATED:
        if CLEAR:
            axes.clear()
        axes.plot(np.linspace(0,2,nx), u)
        plt.pause(dt)
    else:
        plt.plot(np.linspace(0,2,nx), u)

plt.show()
plt.close()