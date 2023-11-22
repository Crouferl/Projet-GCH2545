# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 10:10:04 2023

@author: crouf
"""

# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
try:
    from patinoire_fct import *
except:
    pass

#---------------------------------------------------------------------------


#Définir paramètres du problème

class parametre():
    zb = 0.05 #[m]
    zg = 0.10 #[m]
    alpha_b = 0.54 #[ms−1]
    alpha_g = 1.203 #[ms−1]
    k_b = 0.6 #[Wm−1 K−1]
    k_g = 2.1 #[Wm−1 K−1]
    h_l = 300 #[Wm−2 K−1]
    h_air = 5 #[Wm−2 K−1]
    Ti = -1 #[°C]

prm = parametre()
#-----------------------------------------------------------------------------

prm = parametre()

X = [-1,1]
Z = [0,prm.zb+prm.zg]

nx = 2
nz = 100
dt = 60
tf = 5340

a = plt.figure(1)
temperature_glace = mdf(X,Z,nx,nz,prm,dt,tf)

plt.plot(temperature_glace[0],(temperature_glace[1][0,:]))

plt.plot(temperature_glace[0],(temperature_glace[1][1,:]))

plt.legend(["Glace","Béton"])


x,z = mesh(X, Z, nx, nz)

# Graphiques de type color maps

temp_reshaped = temperature_glace[1][:,1].reshape(nx,nz).transpose()


tick = np.linspace(1,2,11)

ig,ax = plt.subplots(nrows=1,ncols=1,figsize=(12,16))


fig1 = ax.pcolormesh(x,z,temp_reshaped )
plt.colorbar(fig1, ax=ax[0],label="Concentration")

plt.suptitle("Profil de concentration pour différentes valeurs de Pe",fontsize=20)

ax[0].set_title("Concentration pour Pe=10")
ax[0].set_xlabel("Axe x [m]")
ax[0].set_ylabel("Axe y [m]")







