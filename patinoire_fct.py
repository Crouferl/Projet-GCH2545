#Importation des modules 
import numpy as np
import matplotlib.pyplot as plt

#Fonctions à faire : test nico

# Optimiser nombre de points (Optionnel)
    #Input : erreur voulue
    #Out : Nombre de points en x et en y

#Interpoler température lagrange (RAPH)
    #Input : temps, température
    #Out : Coefficients du polyôme

#mesh : discrétiser l'espace à étudier (RAPH)
    #Input : nx,ny,x_min, x_max, z_min, z_max
    #Out : matrices des positions x, matrices des positions y

#mdf : remplir les matrices A et B
    #Input : Bornes x, bornes y, nx, nz, prm
    #Out : matrices de la température à chaque position pour chaque pas de temps
    #Note : calculs euler implicite à faire pour remplir matrice 

# Plot (Optionnel) : 
    #Input : titre, noms des axes 
    #Out : oject figure


    
def mesh(X,Z,nx,nz): 
    """ Fonction générant deux matrices de discrétisation de l'espace à étudier

    Entrées:
        - X : Bornes du domaine en x, X = [x_min, x_max]
        - Z : Bornes du domaine en z, Z = [z_min, z_max]
        - nx : Discrétisation de l'espace en x (nombre de points)
        - nz : Discrétisation de l'espace en z (nombre de points)

    Sorties (dans l'ordre énuméré ci-bas):
        - x : Matrice (array) de dimension (nz x nx) qui contient la position en x
        - z : Matrice (array) de dimension (nz x nx) qui contient la position en z
            * Exemple d'une matrice position :
            * Si X = [-1, 1] et Z = [0, 1]
            * Avec nx = 3 et nz = 3
                x = [-1    0    1]
                    [-1    0    1]
                    [-1    0    1]

                z = [1    1    1  ]
                    [0.5  0.5  0.5]
                    [0    0    0  ]
    """
    x = np.zeros((nz,nx)) #Création de la matrice de position en x selon les dimensions contraintes par la discrétisation de l'espace
    z = np.zeros((nz,nx)) #Création de la matrice de position en z selon les dimensions contraintes par la discrétisation de l'espace
    
    x[:,0] = X[0] #La première colonne de la matrice aura comme valeur la borne minimale du domaine de x
    x[:,-1] = X[1] #La dernière colonne de la matrice aura comme valeur la borne maximale du domaine de x
    
    z[0,:] = Z[1] #La première ligne de la matrice aura comme valeur la borne maximale du domaine de z
    z[-1,:] = Z[0] #La dernière ligne de la matrice aura comme valeur la borne minimale du domaine de z
    
    dx = (abs(X[0])+abs(X[1]))/(nx-1) #Obtention de la valeur de pas entre chaque points en x
    dz = (abs(Z[0])+abs(Z[1]))/(nz-1) #Obtention de la valeur de pas entre chaque points en z
    
    xr = X[0] #Pose la valeur initiale permettant d'obtenir la valeur de x pour la deuxième colonne
    for i in range(1 , nx-1): #On saute les première et dernière valeurs qui ont déjà été obtenues plus haut
        xr = xr + dx #Ajoute la valeur du pas à la valeur de la colonne précédente
        x[:,i]=xr #Ajoute la nouvelle valeur à la colonne i
        
        
    zr = Z[1] #Pose la valeur initiale permettant d'obtenir la valeur de z pour la deuxième ligne
    for i in range(1  , nz-1): #On saute les première et dernière valeurs qui ont déjà été obtenues plus haut
        zr = zr - dz #Ajoute la valeur du pas à la valeur de la ligne précédente
        z[i,:]=zr #Ajoute la nouvelle valeur à la ligne i

    return x,z

def interpolation_Tair(temps_interpo):
    """ Fonction qui permet d'interpoler la température de l'air en fonction du temps

    Entrées:
        - temps_interpo : Temps auquel on cherche la Température

    Sorties (dans l'ordre énuméré ci-bas):
        - Temperature_interpo : Température interpolée au temps temps_interpo

    """
    temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la question
    temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] #Valeurs de température spécifiées dans la question

    n = len(temps) #Nombre de pts, (Degré du polynôme = n-1)

    Temperature_interpo = 0 

    for i in range(n):
        p=1
        for j in range(n):
            if j != i:
                p = p * (temps_interpo - temps[j])/(temps[i] - temps[j]) #Permet de trouver les polynôme L[i](temps)
                
        print(p)
                
        Temperature_interpo = Temperature_interpo + temperature[i]*p #T = f(x_0)L_0(x) + f(x_1)L_1(x) + ... + f(x_n-1)L_n-1(x)
        
    return Temperature_interpo


"Si nécessaire (On l'effacera sinon)."
def interpoler(x,y,x_interpo):
    """ Fonction qui permet d'interpoler la température de l'air en fonction du temps

    Entrées:
        - x : Ensemble de données (Couples de valeurs avec y)
        - y : Ensemble de données (Couples de valeurs avec x)
        - x_interpo : x auquel on cherche y
    Sorties (dans l'ordre énuméré ci-bas):
        - y_interpo : y interpolée couplé à x_interpo
        
    """
    n = len(x)    
    y_interpo = 0

    for i in range(n):
        p=1
        for j in range(n):
            if j != i:
                p = p * (x_interpo - x[j])/(x[i] - x[j]) #Permet de trouver les polynôme L[i](x)
                
        y_interpo = y_interpo + y[i]*p #T = f(x_0)L_0(x) + f(x_1)L_1(x) + ... + f(x_n-1)L_n-1(x)
        
    return y_interpo


