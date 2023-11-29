#Auteurs 
#Nicolas Guillemette (2081046)
#Raphael Louis-Seize (2144924)
#Léo Croufer (2001374)

# Importation des modules
import numpy as np
import matplotlib.pyplot as plt
import pytest
import time
try:
    from patinoire_fct import *
except:
    pass

import time 

start_time = time.time()


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
Z = [0,prm.zb+prm.zg]
dt = 60
tf = 5400

temperature_glace_experimental = np.array([-1.00,-6.35,-5.85,-5.50,-3.60,-3.25],dtype=float)
temps_temperature_experimental = t_test = np.array([0,2,7,15,45,90],dtype=int)
#%% Identifier pas adéquat de simulation (temporel et physique)



nz,n_data =trouver_nombre_points(4, dt, tf, Z, prm, 0.5, 25)

fonction_plot([n_data[:,0]], [n_data[:,1],n_data[:,2],n_data[:,3]], ["T=0min","T=15min","T=90min"], ["solid","solid","solid"], ["","",""],
              xlabel='Nombre de points', 
              ylabel='Erreur absolue', 
              title="Évolution de l'erreur en fonction du nombre de points",
              tick= np.arange(3, 25,1),
              log = True,
              savename="Erreur")

print("Le nombre de points minimal nécessaire est : " + str(nz))

#%%Exécuter la simulation par MDF



temperature_glace = mdf_1D_transitoire(Z,nz,prm,dt,tf)
temperature_glace_permanent = mdf_1D_permanent(Z,nz,prm,dt,tf)

#%% Créer les graphiques de l'air et du liquide

"Interpolation de la température de l'air"

n=200
x = np.linspace(0,tf,n)
y = np.zeros(n)
for i in range(n):
    y[i] = interpolation_Tair(x[i])

temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la question
for i in range(len(temps)):
    temps[i] = temps[i]*60
    
temperature_air = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] 

fonction_plot([x,temps],[y , temperature_air], ["Valeurs d'interpolation","Valeurs spécifiées"],["solid"," "],["","o"], 
                      xlabel='Temps (s)', 
                      ylabel='Temperature (°C)', 
                      title="Valeurs de température d'air interpolées et spécifiées", 
                      savename="lagrange")

fonction_plot([x,temps],[interpoler(temps,temperature_air,x) , temperature_air], ["Valeurs d'interpolation","Valeurs spécifiées"],["solid"," "],["","o"], 
                      xlabel='Temps (s)', 
                      ylabel='Temperature (°C)', 
                      title="Valeurs interpolées par un polynôme de degré 5", 
                      savename="lagrange_deg5")
 


"Comparaison Air et liquide"
points_temps_sec = np.arange(0,tf+dt,dt,dtype="float")
temperature_liquide = temperature_liquide(points_temps_sec)
temperature_air = np.zeros(len(points_temps_sec))
for i,t in enumerate(points_temps_sec):
    temperature_air[i] = interpolation_Tair(t)


points_temps_min = np.arange(0,tf+dt,dt,dtype="float")/60
fonction_plot([points_temps_min], [temperature_air,temperature_liquide[:,1],temperature_glace[1][-1,:]], ["Air","Glycol","Glace"],["solid","dashed","solid"], ["","",""], 
              xlabel="Temps [min]",
              ylabel="Température [C°]",
              title="Évolution de la température de l'air, du glycol et de la glace",
              savename="temp_glycol_air")


#%% Profil de température après 90min et évolution de la température

"Profil de température après 90min"

Z_pos = mesh_1D(Z, nz)

fonction_plot([Z_pos],[temperature_glace[1][:,-1],temperature_glace_permanent[1][:,-1]],["Transitoire","Permanent"],["solid","dashed"],["",""],
         xlabel = "Position [m]",
         ylabel = "Température [C°]",
         title = "Profil de température dans la glace et le béton après 90min",
         xlines=[0.05,0.15],
         savename = "profile_temp_90") 

"Profil de température après 30min"

fonction_plot([Z_pos],[temperature_glace[1][:,30],temperature_glace_permanent[1][:,30]],["Transitoire","Permanent"],["solid","dashed"],["",""],
         xlabel = "Position [m]",
         ylabel = "Température [C°]",
         title = "Profil de température dans la glace et le béton après 30min",
         xlines=[0.05,0.15],
         savename = "profile_temp_30") 

"Évolution de la température en fonction du temps "


fonction_plot([points_temps_min,temps_temperature_experimental],[temperature_glace[1][-1,:],temperature_glace_experimental],["MDF","Expérimental"],["solid","dashed"],["",""],
         xlabel = "Temps [sec]",
         ylabel = "Température [C°]",
         title = "Évolution de la température à la surface de la glace selon le temps",
         xlines=[14],
         savename = "évolution_temp")    

#%%Évolution de la température de la glace avec différentes épaisseurs


nz = nombre_de_points(20) #Il faut augementer le nombre de point pour faire varier l'épaisseur de la glace et du béton

epaisseur_glace = np.arange(0.04,0.3,0.02)#[m]
epaisseur_beton = np.arange(0.04,0.3,0.02) #[m]
epaisseur_data = np.zeros((len(epaisseur_beton)*len(epaisseur_glace),3))

k = 0 #Compteur global d'itération

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

#%%Créer figure
fig, ax = plt.subplots(subplot_kw={"projection": "3d"},figsize=[7,5])

#Réorganiser données
X, Y = np.meshgrid(epaisseur_glace, epaisseur_beton)
Z = epaisseur_data[:,2].reshape(len(epaisseur_glace),len(epaisseur_beton)).transpose()

#Créer surface
surf = ax.plot_surface(X, Y, Z, cmap="coolwarm",
                       linewidth=0, antialiased=False)

# Changer axe Z
#ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter('{x:.02f}')

# Ajouter colorbar
fig.colorbar(surf, shrink=0.4, aspect=10)


# Ajouter les labels
ax.set_xlabel('Épaisseur glace [m]')
ax.set_ylabel('Épaisseur béton[m]')
ax.set_zlabel('Température[C°]')
ax.view_init(azim=210, elev=25)
ax.set_title("Évolution de la température en surface de la glace après 90min \n en fonction des épaisseurs de glace et de béton")

plt.savefig("Images/temperature_3D", dpi=300)

#%%
print("--- %s seconds ---" % round((time.time() - start_time),3))
pytest.main(['-q', '--tb=long', 'patinoire_corr.py'])
