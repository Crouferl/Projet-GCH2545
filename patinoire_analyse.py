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
dt = 60
#-----------------------------------------------------------------------------

#Identifier pas adéquat de simulation (temporel et physique)





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
    
temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] 

plot = fonction_plot([x,temps],[y , temperature], ["Valeurs d'interpolation","Valeurs spécifiées"],["solid","dashed"], 
                     xlabel='Temps (s)', 
                     ylabel='Temperature (°C)', 
                     title="Valeurs de température d'air interpolées et spécifiées", 
                     savename="lagrange")
 


#Comparaison Air et liquide
points_temps_sec = np.arange(0,tf+60,dt,dtype="float")
temperature_liquide = temperature_liquide(points_temps_sec)
temperature_air = np.zeros(len(points_temps_sec))
for i,t in enumerate(points_temps_sec):
    temperature_air[i] = interpolation_Tair(t)

points_temps_min = np.arange(0,tf+60,dt,dtype="float")/60
fonction_plot([points_temps_min], [temperature_air,temperature_liquide[:,1]], ["Air","Glycol"],["solid","dashed"], 
              xlabel="Temps [min]",
              ylabel="Température [C°]",
              title="Évolution de la température de l'air et du glycol",
              savename="temp_glycol_air")


#-----------------------------------------------------------------------------

#Profil de température après 90min (identifier limite entre glace et béton et surface de glace)



pytest.main(['-q', '--tb=long', 'patinoire_corr.py'])
