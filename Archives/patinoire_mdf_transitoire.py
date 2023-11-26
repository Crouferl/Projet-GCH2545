# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:00:38 2023

@author: nigui
"""

import numpy as np
import matplotlib.pyplot as plt
try:
    from patinoire_fct import *
except:
    pass


def temperature_liquide(t) :
    
    """Fonction qui retourne un array de la température du liquide en fonction du temps
    Entrées:
        - t = array de point de temps de 0 à tf

    Sortie (dans l'ordre énuméré ci-bas):
        - temp_liquide : array tf/dt x 2 [Temps, température liquide]
        
    """
    n_step = tf//dt
    temp_liquide = np.zeros(n_step,2)
    temp_instant = -1
    
    for i,t in enumerate(t):
        
        temp_liquide[i,0] = t
        temp_liquide[i,1] = temp_instant
        
        if temp_instant >-15 :
            temp_instant -=1
        else :
            temp_instant = -15
        
    return temp_liquide


def mdf_permanent(X_limit,Z_limit,nx,nz,prm,dt,tf) :
    
    """Fonction qui résoud le problème de différence fini et calcule la position pour chaque point pour chaque pas de temps
    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
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
    X_pos, Z_pos = mesh(X_limit,Z_limit,nx,nz) #Créer les matrices des positions pour les deux dimensions
    points = numeroter_mesh(X_pos,Z_pos) #Créer la matrices avec les positions et les adresses de chaque points
    n_points = nx*nz #Nombre de points dans la discrétisation

    #Pas de discrétisation du domaine physique
    dx = abs((X_limit[1]-X_limit[0])/(nx-1))
    dz = abs((Z_limit[1]-Z_limit[0])/(nz-1))
    
    ci = np.ones(n_points)*prm.Ti

    points_temps = np.arange(0,tf,dt,dtype="float")
    temperature_store = np.zeros((n_points,len(points_temps))) #Matrice pour enregister les résulats finals
    temp = np.zeros(n_points) #Matrice temporaire pour stocker le résultat de chaque itération
    
    t_L = temperature_liquide(points_temps)

    for i,t in enumerate(points_temps) : #Boucle pour itérer sur chaque point de temps

        #Initialiser les matrices de différence finie
        A = np.zeros((n_points,n_points))
        B = np.zeros(n_points)
        
        for k in range(0,n_points) : #Boucle pour itérer sur l'espace
            X = points[k,1]
            Z = points[k,2]
            

            if Z == Z_limit[0] : #Vérifier si le point est sur la limite inférieure
                   
                A[k,k-2] = 1
                A[k,k-1] = -4
                A[k,k] = 3- (2*dz*prm.h_l)/(prm.k_b) 
                B[k] = -(2*dz*prm.h_l*t_L[i,1])/(prm.k_b) 

            elif Z == Z_limit[1] : #Vérifier si le point est sur la limite supérieure
                A[k,k] = (3)/(2*dz) + (prm.h_air)/(prm.k_g)
                A[k,k-1] = (-4)/(2*dz)
                A[k,k-2] = 1/(2*dz)
                B[k] = (prm.h_air*interpolation_Tair(t))/prm.k_g  #!!!!! FONCTION D'INTERPOLATION DE TAIR À VALIDER
            
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