#Auteurs 
#Nicolas Guillemette (MATRICULE)
#Raphael Louis-Seize (MATRICULE)
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

prm = parametre()
#-----------------------------------------------------------------------------


