#Importation des modules 
import numpy as np
import matplotlib.pyplot as plt



# Optimiser nombre de points (Optionnel)
    #Input : erreur voulue
    #Out : Nombre de points en x et en y


def temperature_liquide(t) :
    
    """Fonction qui retourne un array de la température du liquide en fonction du temps
    Entrées:
        - t = array de point de temps de 0 à tf

    Sortie (dans l'ordre énuméré ci-bas):
        - temp_liquide : array tf/dt x 2 [Temps, température liquide]
        
    """

    temp_liquide = np.zeros((len(t),2))
    increment_temp = -1
    temp_instant = -1
    
    
    for i,t in enumerate(t):
        minute = t//60
        
        if temp_instant >-15 :
            temp_instant = -1 + increment_temp*minute
        else :
            temp_instant = -15
        
        
        temp_liquide[i,0] = t
        temp_liquide[i,1] = temp_instant
        
       
    return temp_liquide


def mdf(X_limit,Z_limit,nx,nz,prm,dt,tf) :
    
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

    points_temps = np.arange(0,tf+60,dt,dtype="float")
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

    points_temps = np.arange(0,tf+60,dt,dtype="float")
    temperature_store = np.zeros((n_points,len(points_temps))) #Matrice pour enregister les résulats finals
    temp = np.zeros(n_points) #Matrice temporaire pour stocker le résultat de chaque itération
    
    T_l = -15
    T_air = 14

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
                B[k] = -(2*dz*prm.h_l*T_l)/(prm.k_b) 

            elif Z == Z_limit[1] : #Vérifier si le point est sur la limite supérieure
                A[k,k] = (3)/(2*dz) + (prm.h_air)/(prm.k_g)
                A[k,k-1] = (-4)/(2*dz)
                A[k,k-2] = 1/(2*dz)
                B[k] = (prm.h_air*T_air)/prm.k_g  
            
            
            else : #Remplir le coeur de la matrice
                
                if Z < prm.zb : #Vérifier si le point est dans la glace ou dans le béton
                    alpha = prm.alpha_b 
                else : 
                    alpha = prm.alpha_g
                    
                A[k,k+1] = 1
                A[k,k] = -2
                A[k,k-1] = 1
                B[k] = 0
                
        temp = np.linalg.solve(A,B) 

        ci = temp.copy() 

        temperature_store[:,i] = temp 

    return points_temps, temperature_store 





def numeroter_mesh(X,Z) :
    """Fonction qui génère une liste numéroté des points de l'espace
    Entrées:
        - X: Matrice (array) de dimension (nz x nx) qui contient la position en x
        - Z: Matrice (array) de dimension (nz x nx) qui contient la position en z

    Sortie (dans l'ordre énuméré ci-bas):
        - Matrice (array) de dimension (n_points x 3) [# de point, coordonée en x, coordonée en z]
        
    """
    nx = len(X[0,:]) #Récupérer nombre de points en x
    nz = len(Z[:,0]) #Récupérer nombre de points en z
    n_points = nx*nz #Nombre total de points
    points_pos = np.zeros((n_points,3)) #Matrice de point numérotés

    for k in range(0,n_points) :
        i_x = k//nz #Indice pour parcourir matrice X
        j_z = k-nz*(k//nz) #Indice pour parcourir matrice Z
        x = X[1,i_x] 
        z = Z[j_z,1]
        points_pos[k,:] = [k,x,z] # Remplir matrice point_pos

    return points_pos
    
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
        - temperature_interpo : Température interpolée au temps temps_interpo

    """
    temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la question
    for i in range(len(temps)):
        temps[i] = temps[i]*60
        
    temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] #Valeurs de température spécifiées dans la question

    n = len(temps)
    omega = 0
    for i in range(n):
        if temps_interpo == temps[i]:
            return temperature[i]
        
        elif temps_interpo > temps[i] and temps_interpo < temps[i+1]:
            omega = i 

    return interpoler([temps[omega],temps[omega+1]],[temperature[omega],temperature[omega+1]],temps_interpo)

    
    

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


def fonction_plot(x_data_list, y_data_list, list_labels, list_linestyles, xlabel='', ylabel='', title='', grid=True, legend=True):
    """fonction permettant de tracer une ou plusieurs courbes.
    
    Entrées:
        - vecteur_x : vecteur de données pour l'abscice'
        - vecteur_y : vecteur de données pour l'ordonné
        - list_label : liste de label pour les courbes
        - x_label : Titre abscise (string)
        - y_label : Titre ordonné (string)
        - title : Tire du graphique (string)
        
        
    Sorties
        - graphique de une ou plusieurs courbes
    """
    for i in range(len(x_data_list)):
        plt.plot(x_data_list[i], y_data_list[i], label=list_labels[i], linestyle=list_linestyles[i])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    if grid:
        plt.grid()
    
    if legend:
        plt.legend()
        
    # plt.savefig(nom_enregistrement,dpi=300)
    
    plt.show()


