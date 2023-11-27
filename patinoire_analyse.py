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
tf = 5400
Z = [0,prm.zb+prm.zg]
nx = 2
nz = 10
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
 


#Comparaison Air et liquide
points_temps_sec = np.arange(0,tf+dt,dt,dtype="float")
temperature_liquide = temperature_liquide(points_temps_sec)
temperature_air = np.zeros(len(points_temps_sec))
for i,t in enumerate(points_temps_sec):
    temperature_air[i] = interpolation_Tair(t)


points_temps_min = np.arange(0,tf+dt,dt,dtype="float")/60
fonction_plot([points_temps_min], [temperature_air,temperature_liquide[:,1]], ["Air","Glycol"],["solid","dashed"], ["",""], 
              xlabel="Temps [min]",
              ylabel="Température [C°]",
              title="Évolution de la température de l'air et du glycol",
              savename="temp_glycol_air")


#-----------------------------------------------------------------------------

#Profil de température après 90min (identifier limite entre glace et béton et surface de glace)

Z_pos = np.flip(mesh_1D(Z, nz))

fonction_plot([Z_pos],[temperature_glace[1][:,-1],temperature_glace_permanent[1][:,-1]],["Transitoire","Permanent"],["solid","dashed"],["",""],
         xlabel = "Position [m]",
         ylabel = "Température [C°]",
         title = "Profil de température dans la glace et le béton après 90min",
         xlines=[0.05,0.15],
         savename = "profile_temp") 

fonction_plot([points_temps_min,temps_temperature_experimental],[temperature_glace[1][-1,:],temperature_glace_experimental],["MDF","Expérimental"],["solid","dashed"],["",""],
         xlabel = "Temps [sec]",
         ylabel = "Température [C°]",
         title = "Évolution de la température à la surface de la glace selon le temps",
         xlines=[14],
         savename = "évolution_temp")    


#-----------------------------------------------------------------------------
#Évolution de la température de la glace avec différentes épaisseurs









pytest.main(['-q', '--tb=long', 'patinoire_corr.py'])
