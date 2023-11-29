#Auteurs 
#Nicolas Guillemette (2081046)
#Raphael Louis-Seize (2144924)
#Léo Croufer (2001374)

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
tf = 2000
Z = [0,prm.zb+prm.zg]
nx = 2
nz = nombre_de_points(28)
dt = 60
tf = 5400

temperature_glace_experimental = np.array([-1.00,-6.35,-5.85,-5.50,-3.60,-3.25],dtype=float)
temps_temperature_experimental = t_test = np.array([0,2,7,15,45,90],dtype=int)
#-----------------------------------------------------------------------------

#Identifier pas adéquat de simulation (temporel et physique)


temperature_glace = mdf_1D_transitoire(Z,nz,prm,dt,tf)
temperature_glace_permanent = mdf_1D_permanent(Z,nz,prm,dt,tf)



#-----------------------------------------------------------------------------

#Graphique de la l'évolution de la température du liquide et de l'air

#Interpolation de la température de l'air

n=200
x = np.linspace(0,tf,n)
y = np.zeros(n)
for i in range(n):
    y[i] = interpolation_Tair(x[i])

temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la question
for i in range(len(temps)):
    temps[i] = temps[i]*60
    
temperature_air = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] 

# fonction_plot([x,temps],[y , temperature_air], ["Valeurs d'interpolation","Valeurs spécifiées"],["solid"," "],["","o"], 
#                       xlabel='Temps (s)', 
#                       ylabel='Temperature (°C)', 
#                       title="Valeurs de température d'air interpolées et spécifiées", 
#                       savename="lagrange")

# fonction_plot([x,temps],[interpoler(temps,temperature_air,x) , temperature_air], ["Valeurs d'interpolation","Valeurs spécifiées"],["solid"," "],["","o"], 
#                       xlabel='Temps (s)', 
#                       ylabel='Temperature (°C)', 
#                       title="Valeurs interpolées par un polynôme de degré 5", 
#                       savename="lagrange_deg5")
 

# Vérification température glace à la surface
temperature_verification = [-1,-6.35,-5.50,-3.25]
temps_verification = [0,2,15,90]

#Comparaison Air et liquide
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

#-----------------------------------------------------------------------------

# Comparaison MDF transitoire et permanent après 90 min (Graphiques de type color maps)

z = mesh_1D(Z, nz)
x_mesh=x = np.linspace(0, 1, nx)

temp_reshaped = temperature_glace[1][:, 1].reshape(nz).transpose()
temp_reshaped_permanent = temperature_glace_permanent[1][:, 1].reshape(nz).transpose()

tick = np.linspace(1, 2, 11)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 16))

fig1 = ax[0].pcolormesh(x_mesh, z, temp_reshaped, cmap="coolwarm")
fig2 = ax[1].pcolormesh(x_mesh, z, temp_reshaped_permanent, cmap="coolwarm")
ax[0].set_title('MDF transitoire')
ax[1].set_title('MDF regime permanent')

plt.colorbar(fig1, ax=ax[1], label="Température")

plt.suptitle("Distribution de la température de la patinoire à 90 minutes", fontsize=16)

ax[0].set_xlabel("Axe x [m]", fontsize=12)
ax[1].set_xlabel("Axe x [m]", fontsize=12)
ax[0].set_ylabel("Hauteur z [m]", fontsize=12)

plt.show()



#-----------------------------------------------------------------------------

#Profil de température après 90min (identifier limite entre glace et béton et surface de glace)

Z_pos = mesh_1D(Z, nz)

fonction_plot([Z_pos],[temperature_glace[1][:,-1],temperature_glace_permanent[1][:,-1]],["Transitoire","Permanent"],["solid","dashed"],["",""],
         xlabel = "Position [m]",
         ylabel = "Température [C°]",
         title = "Profil de température dans la glace et le béton après 90min",
         xlines=[0.05,0.15],
         savename = "profile_temp") 

fonction_plot([points_temps_min,temps_temperature_experimental],[temperature_glace[1][-1,:],temperature_glace_experimental],["MDF","Expérimental"],["solid","dashed"],["",""],
         xlabel = "Temps [min]",
         ylabel = "Température [C°]",
         title = "Évolution de la température à la surface de la glace selon le temps",
         xlines=[14],
         savename = "évolution_temp")    



#-----------------------------------------------------------------------------

#Profil de température pour la vérification (Études des 4 température clées)

fonction_plot([points_temps_min, temps_temperature_experimental, temps_verification],[temperature_glace[1][-1,:], temperature_glace_experimental, temperature_verification],["Température par simulation", "Températures expérimentales", "Points d'analyse"],["solid", "dashed", " "],["","","o"],
         xlabel = "Temps minutes [m]",
         ylabel = "Température [C°]",
         title = "Vérifiaction du profil de température à la glace obtenue par simulation",
         xlines=None,
         savename = "verification_Tglace") 


#-----------------------------------------------------------------------------
#Évolution de la température de la glace avec différentes épaisseurs









pytest.main(['-q', '--tb=long', 'patinoire_corr.py'])
