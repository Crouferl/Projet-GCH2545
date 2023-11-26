# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 11:51:38 2023

@author: crouf
"""

from patinoire_fct import *

def mdf_1D(Z_limit,nz,prm,dt,tf) :
    
    """Fonction qui résoud le problème de différence fini et calcule la position pour chaque point pour chaque pas de temps
    Entrées:
        - Z : Bornes du domaine en z, Z = [z_min, z_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - nz : Discrétisation de l'espace en z (nombre de points)
        - prm : objet contenant tous les paramètres physiques du problème
        - dt : pas de temps 
        - tf : temps final

    Sortie (dans l'ordre énuméré ci-bas):
        - points_temps : Array contenants les points de temps où la température a été calculée
        - temperature_store : Array contenant la température pour chaque point à chaque point de temps 
            - [[température Temps 0],[Températeur Temp 1].....]
        
    """
    Z_pos = np.flip(mesh_1D(Z_limit,nz)) #Créer les matrices des positions pour les deux dimensions
    
    #Pas de discrétisation du domaine physique
    dz = abs((Z_limit[1]-Z_limit[0])/(nz-1))
    
    ci = np.ones(nz)*prm.Ti

    points_temps = np.arange(0,tf+60,dt,dtype="float")
    temperature_store = np.zeros((nz,len(points_temps))) #Matrice pour enregister les résulats finals
    temp = np.zeros(nz) #Matrice temporaire pour stocker le résultat de chaque itération
    
    t_L = temperature_liquide(points_temps)

    for i,t in enumerate(points_temps) : #Boucle pour itérer sur chaque point de temps

        #Initialiser les matrices de différence finie
        A = np.zeros((nz,nz))
        B = np.zeros(nz)
        
        for k in range(0,nz) : #Boucle pour itérer sur l'espace
            Z = Z_pos[k]
            

            if Z == Z_limit[0] : #Vérifier si le point est sur la limite inférieure
                   
                A[k,k+2] = -1/(2*dz)
                A[k,k+1] = 4/(2*dz)
                A[k,k] = -3/(2*dz) - (prm.h_l/prm.k_b) 
                B[k] = -(prm.h_l*t_L[i,1])/(prm.k_b)
            
            elif Z == Z_limit[1] : #Vérifier si le point est sur la limite supérieure
                A[k,k-2] = 1/(2*dz)
                A[k,k-1] = (-4)/(2*dz)
                A[k,k] = 3/(2*dz) + prm.h_air/prm.k_g
                B[k] = (prm.h_air*interpolation_Tair(t))/prm.k_g 
                
                
            else : #Remplir le coeur de la matrice
                
                if Z < prm.zb : #Vérifier si le point est dans la glace ou dans le béton
                    alpha = prm.alpha_b #
                else : 
                    alpha = prm.alpha_g
                    
                A[k,k+1] = -(alpha*dt)/(dz**2)
                A[k,k] = 1 +(2*alpha*dt)/(dz**2)
                A[k,k-1] = -(alpha*dt)/(dz**2)
                B[k] = ci[k]
                
        temp = np.linalg.solve(A,B) 

        ci = temp.copy() 

        temperature_store[:,i] = temp 

    return points_temps, temperature_store 


def mesh_1D(Z,nz): 
    """ Fonction générant deux matrices de discrétisation de l'espace à étudier

    Entrées:
        - Z : Bornes du domaine en z, Z = [z_min, z_max]
        - nz : Discrétisation de l'espace en z (nombre de points)

    Sorties (dans l'ordre énuméré ci-bas):
        - z : Matrice (array) de dimension (nz x nx) qui contient la position en z
            * Exemple d'une matrice position :
            * Si X = [-1, 1] et Z = [0, 1]
            * Avec et nz = 3
            

                z = [1    1    1  ]
                    [0.5  0.5  0.5]
                    [0    0    0  ]
    """
    z = np.zeros(nz) #Création de la matrice de position en z selon les dimensions contraintes par la discrétisation de l'espace
    
    
    z[0] = Z[1] #La première ligne de la matrice aura comme valeur la borne maximale du domaine de z
    z[-1] = Z[0] #La dernière ligne de la matrice aura comme valeur la borne minimale du domaine de z
    

    dz = (abs(Z[0])+abs(Z[1]))/(nz-1) #Obtention de la valeur de pas entre chaque points en z
    
 
        
    zr = Z[1] #Pose la valeur initiale permettant d'obtenir la valeur de z pour la deuxième ligne
    for i in range(1  , nz-1): #On saute les première et dernière valeurs qui ont déjà été obtenues plus haut
        zr = zr - dz #Ajoute la valeur du pas à la valeur de la ligne précédente
        z[i]=zr #Ajoute la nouvelle valeur à la ligne i
    return z


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

Z = [0,prm.zb+prm.zg]

nx = 2
nz = 5
dt = 60
tf = 5400


t = mesh_1D([0,0.15],5)
test = mdf_1D(Z, nz, prm, dt, tf)