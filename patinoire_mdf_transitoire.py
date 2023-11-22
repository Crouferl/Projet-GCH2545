# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:00:38 2023

@author: crouf
"""

import numpy as np
import matplotlib.pyplot as plt


def mdf(X_limit,Z_limit,nx,nz,prm,dt,tf,ci) :
    
    """Fonction qui résoud le problème de différence fini et calcule la position pour chaque point pour chaque pas de temps
    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Z : Bornes du domaine en z, Z = [z_min, z_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - nz : Discrétisation de l'espace en z (nombre de points)
        - prm : objet contenant tous les paramètres physiques du problème
        - dt : pas de temps 
        - tf : temps final
        - ci : Matrice contenant la température initiale de chaque point [# numéro de point, température]

    Sortie (dans l'ordre énuméré ci-bas):
        - points_temps : Array contenants les points de temps où la température a été calculée
        - temperature_store : Array contenant la température pour chaque point à chaque point de temps 
            - [[# de point, température Temps 0],[# de points, Températuer Temp 1].....]
        
    """
    X_pos, Z_pos = mesh(X_limit,Z_limit,nx,nz) #Créer les matrices des positions pour les deux dimensions
    points = numeroter_mesh(X_pos,Z_pos) #Créer la matrices avec les positions et les adresses de chaque points
    points_temps = np.linspace(0,tf,dt,dtype="float") # Créer la matrice des points de temps où le problème sera évalué
    n_points = nx*nz #Nombre de points dans la discrétisation

    #Pas de discrétisation du domaine physique
    dx = abs((X[1]-X[0])/(nx-1))
    dz = abs((Z[1]-Z[0])/(nz-1))


    temperature_store = np.zeros(len(points_temps)) #Matrice pour enregister les résulats finals
    temp = np.zeros(n_points) #Matrice temporaire pour stocker le résultat de chaque itération

    for i,t in enumerate(points_temps) : #Boucle pour itérer sur chaque point de temps

        #Initialiser les matrices de différence finie
        A = np.zeros(len(n_points,n_points))
        B = np.zeros(len(n_points))
        
        for k in range(0,n_points) : #Boucle pour itérer sur l'espace
            X = points[k,1]
            Z = points[k,2]
            

            if Z == Z_limit[0] : #Vérifier si le point est sur la limite inférieure
                #Remplir A et B avec condition limite dessous
               
            elif Z == Z_limit[1] : #Vérifier si le point est sur la limite supérieure
                #Remplir A et B avec condition limite dessus
                

            else : #Remplir le coeur de la matrice
                
                if Z < prm.zb : #Vérifier si le point est dans la glace ou dans le béton
                    alpha = prm.alpha_b #
                else : 
                    alpha = prm.alpha_g
                #Remplir A et B avec coeur du problème

        temp = np.linalg.solve(A,B) #Résoudre le problème de différence fini

        ci = temp.copy() #Mettre à jour les conditions initiales

        temperature_store[i] = temp #Enregistrer la température de chaque point

    return points_temps, temperature_store 