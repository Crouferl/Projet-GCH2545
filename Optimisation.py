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

T = np.array([-1.00,-5.50,-3.25],dtype=float)
t_test = np.array([0,15,90],dtype=int)

err = np.ones(3)
err_plot = np.zeros((26,4))
tol=0.2
    
    
for j in range(4,30):
    temp_to_test = mdf_1D_transitoire(Z, nz, prm, dt, tf)
    for i in range(0,3):
        err[i] = temp_to_test[1][-1,t_test[i]]
        
    err = abs(err-T)
    nz = nombre_de_points(j)
    err_plot[j-4, :] = [nz,err[0],err[1],err[2]]
    
    # if any([err[0]>=tol,err[1]>=tol,err[2]>=tol]) :
    #     print(nz)
    #     n=nz


    
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




nz = nombre_de_points(30)
dt = 60
tf = 5400





import numpy as np

epaisseur_glace = np.arange(0.04,0.3,0.01)#[m]
epaisseur_beton = np.arange(0.1,0.5,0.01) #[m]
epaisseur_data = np.zeros((len(epaisseur_beton)*len(epaisseur_glace),3))
k = 0

for i,z_g in enumerate(epaisseur_glace) :
    prm.zg = z_g
    print("i: " + str(i))
    for j,z_b in enumerate(epaisseur_beton):
        print("j: " + str(j))
        prm.zb = z_b 
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
ax.view_init(azim=120, elev=20)


# plt.savefig("test", dpi=300)


plt.fig()

plt.plot(epaisseur_data[:,1],epaisseur_data[:,2])
plt.plot(epaisseur_data[:,0],epaisseur_data[:,2])



plt.show()







    
    
    
    