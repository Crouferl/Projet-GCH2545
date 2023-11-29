# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:38:00 2023

@author: crouf


"""
import numpy as np
import matplotlib.pyplot as plt
import pytest

from patinoire_fct import *


from matplotlib import cm
from matplotlib.ticker import LinearLocator



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
nz = nombre_de_points(4)
dt = 60
tf = 5400
Z = [0,prm.zb+prm.zg]
        
n,n_data = trouver_nombre_points(4, dt, tf, Z, prm, 0.5, 30)
#%%
    
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)


plt.plot(err_plot[1:-3,0],err_plot[1:-3,1])
plt.plot(err_plot[1:-3,0],err_plot[1:-3,2])
plt.plot(err_plot[1:-3,0],err_plot[1:-3:,3])

ax.set_xlabel = "Nombre de points"
ax.set_ylabel = "Erreur"
tick = np.arange(2, 25,2)
ax.set_yscale('log')
ax.set_xticks(tick)
ax.grid(True)


#%%




nz = nombre_de_points(20)
dt = 60
tf = 5400

import numpy as np

epaisseur_glace = np.arange(0.04,0.3,0.02)#[m]
epaisseur_beton = np.arange(0.04,0.3,0.02) #[m]
epaisseur_data = np.zeros((len(epaisseur_beton)*len(epaisseur_glace),3))
k = 0

for i,z_g in enumerate(epaisseur_glace) :
    prm.zg = round(z_g,5)
    # print("i: " + str(i))
    for j,z_b in enumerate(epaisseur_beton):
        # print("j: " + str(j))
        prm.zb = round(z_b,5) 
        Z = [0,prm.zb+prm.zg]
        t_glace = temperature_sans_echec(Z, nz, prm, dt, tf)
        epaisseur_data[k,:] = [prm.zg,prm.zb,t_glace]
        k+=1
        
fig, ax = plt.subplots(subplot_kw={"projection": "3d"},figsize=[10,20])


X, Y = np.meshgrid(epaisseur_glace, epaisseur_beton)
Z = epaisseur_data[:,2].reshape(len(epaisseur_glace),len(epaisseur_beton)).transpose()


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.1, aspect=10)


# Set the axis labels
ax.set_xlabel('Épaisseur glace')
ax.set_ylabel('Épaisseur béton')
ax.set_zlabel('Température')
ax.view_init(azim=175, elev=30)


# plt.savefig("test", dpi=300)

plt.show()







    
    
    
    