#Auteurs 
#Nicolas Guillemette (2081046)
#Raphael Louis-Seize (2144924)
#Léo Croufer (2001374)

#Importation des modules 
import numpy as np
import matplotlib.pyplot as plt

#Fonctions
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



def interpolation_Tair(temps_interpo):
    """ Fonction qui permet d'interpoler la température de l'air  du système à un certain temps

    Entrées:
        - temps_interpo : Temps auquel on cherche la Température

    Sorties (dans l'ordre énuméré ci-bas):
        - temperature_interpo : Température interpolée au temps temps_interpo

    """
    temps = np.array([0, 2, 7, 15, 45, 90])*60  #Valeurs de temps spécifiés dans la question

    temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] #Valeurs de température spécifiées dans la question

    if temps_interpo > temps[-1] :
        return 14
    
    n = len(temps)
    omega = 0
    for i in range(n):
        if temps_interpo == temps[i]:
            return temperature[i]
        
        elif temps_interpo > temps[i] and temps_interpo < temps[i+1]:
            omega = i 

    return interpoler([temps[omega],temps[omega+1]],[temperature[omega],temperature[omega+1]],temps_interpo)

    

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


def fonction_plot(x_data_list, y_data_list, list_labels, list_linestyles, list_marker, savename='', xlabel='', ylabel='', title='',xlines='', log='',tick='', grid=True, legend=True):
    """fonction permettant de tracer une ou plusieurs courbes sur un graphique
    
    Entrées:
        - vecteur_x : vecteur de données pour l'abscice'
        - vecteur_y : vecteur de données pour l'ordonné

        
        - x_data_list : Valeurs en x de chaque courbe sous forme de liste (ex: [[liste des valeurs de x courbe 1],[liste des valeurs de x courbe 2]])
        - y_data_list : Valeurs en y de chaque courbe sous forme de liste (ex: [[liste des valeurs de y courbe 1],[liste des valeurs de y courbe 2]])
        - list_labels : liste de label pour les courbes
        - list_linestyles : Liste permettant de choisir le type de ligne (ex: ["solid","dashed"] donnera une première courbe avec une ligne pleine et une deuxième courve en traits discontinus)
        - list_marker : Liste permettant de choisir comment présenter les points de données (ex: ["","o"] donnera une première courbe avec aucun marqueur et une deuxième courbe avec des points comme marqueurs)
        - savename : Nom du fichier à enregistrer (ex: savename = "profile_temp_30")
        - xlabel : Titre abscise (string)
        - ylabel : Titre ordonné (string)
        - title : Tire du graphique (string)
        - xlines : Tracer une ligne pointillée verticale (ex: [0.05,0.15] tracera une ligne verticale en x = 0.05 et en x=0.15)
        - log : log = True permet d'obtenir un axe y logarithmique
        - tick : Permet d'ajouter d'ajouter des ticks (ex: tick= np.arange(3, 25,1) ajoutera des ticks à chaque valeur entière de 3 à 25)
        - grid : grid = true permet d'ajouter un grid au graphique
        - legend : legend = true permet d'ajouter une legende au graphique en fonction des de list_labels
        
    Sorties
        - graphique de une ou plusieurs courbes
    """
    
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(len(y_data_list)):
        if len(x_data_list) == 1:
            b = 0
        else :
            b= i
        plt.plot(x_data_list[b], y_data_list[i], label=list_labels[i], linestyle=list_linestyles[i], marker = list_marker[i])
        
        
    if xlines:
        for xline in xlines:
            plt.axvline(x=xline, color='red', linestyle='--', linewidth=1)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    if grid:
        plt.grid()
    
    if legend:
        plt.legend(loc="lower right")
    
    
    if log:
        ax.set_yscale('log')
    
    if len(tick) != 0:
        ax.set_xticks(tick)

    if savename != '':
        path = "Images/" + savename+".png"
        plt.savefig(path,dpi=300) 

    plt.show()


def mdf_1D_transitoire(Z_limit,nz,prm,dt,tf) :
    
    """Fonction qui résoud le problème de différence fini et calcule la position pour chaque point pour chaque pas de temps
    Entrées:
        - Z_limit : Bornes du domaine en z, Z_limit = [z_min, z_max]
        - nz : Discrétisation de l'espace en z (nombre de points)
        - prm : objet contenant tous les paramètres physiques du problème
        - dt : pas de temps 
        - tf : temps final

    Sortie (dans l'ordre énuméré ci-bas):
        - points_temps : Array contenants les points de temps où la température a été calculée
        - temperature_store : Array contenant la température pour chaque point à chaque point de temps 
            - [[température Temps 0],[Températeur Temp 1].....]
        
    """
    Z_pos = mesh_1D(Z_limit,nz) #Créer les matrices des positions pour les deux dimensions
    Z_limit = np.round(Z_limit,5)
    #Pas de discrétisation du domaine physique
    dz = abs((Z_limit[1]-Z_limit[0])/(nz-1))
    ci = np.ones(nz)*prm.Ti

    points_temps = np.arange(0,tf+dt,dt,dtype="float")
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
                
            elif abs(Z-prm.zb) <1e-3 : #Vérifier si le point est sur la frontière 
                A[k,k+2] =-prm.k_g
                A[k,k+1] = 4*prm.k_g
                A[k,k] = -3*(prm.k_g+prm.k_b)
                A[k,k-1] = 4*prm.k_b
                A[k,k-2] = -prm.k_b
                B[k] = 0
                
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


def mdf_1D_permanent(Z_limit,nz,prm,dt,tf) :
    
    
    """Fonction qui résoud le problème de différence fini et calcule la position pour chaque point pour chaque pas de temps
    Entrées:
        - Z_limit : Bornes du domaine en z, Z_limit = [z_min, z_max]
        - nz : Discrétisation de l'espace en z (nombre de points)
        - prm : objet contenant tous les paramètres physiques du problème
        - dt : pas de temps 
        - tf : temps final

    Sortie (dans l'ordre énuméré ci-bas):
        - points_temps : Array contenants les points de temps où la température a été calculée
        - temperature_store : Array contenant la température pour chaque point à chaque point de temps 
            - [[température Temps 0],[Températeur Temp 1].....]
        
    """
    Z_pos = mesh_1D(Z_limit,nz) #Créer les matrices des positions pour les deux dimensions
    Z_limit = np.round(Z_limit,5)
    #Pas de discrétisation du domaine physique
    dz = abs((Z_limit[1]-Z_limit[0])/(nz-1))
    
    ci = np.ones(nz)*prm.Ti

    points_temps = np.arange(0,tf+dt,dt,dtype="float")
    temperature_store = np.zeros((nz,len(points_temps))) #Matrice pour enregister les résulats finals
    temp = np.zeros(nz) #Matrice temporaire pour stocker le résultat de chaque itération
    
    t_L = -15
    T_air = 14

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
                B[k] = -(prm.h_l*t_L)/(prm.k_b)
            
            elif Z == Z_limit[1] : #Vérifier si le point est sur la limite supérieure
                A[k,k-2] = 1/(2*dz)
                A[k,k-1] = (-4)/(2*dz)
                A[k,k] = 3/(2*dz) + prm.h_air/prm.k_g
                B[k] = (prm.h_air*T_air)/prm.k_g 
                
            elif abs(Z-prm.zb) <1e-3 : #Vérifier si le point est sur la frontière 
                A[k,k+2] =-prm.k_g
                A[k,k+1] = 4*prm.k_g
                A[k,k] = -3*(prm.k_g+prm.k_b)
                A[k,k-1] = 4*prm.k_b
                A[k,k-2] = -prm.k_b
                B[k] = 0
                
            else : #Remplir le coeur de la matrice
                
                if Z < prm.zb : #Vérifier si le point est dans la glace ou dans le béton
                    alpha = prm.alpha_b #
                else : 
                    alpha = prm.alpha_g
                    
                A[k,k+1] = -(alpha*dt)/(dz**2)
                A[k,k] = 1 +(2*alpha*dt)/(dz**2)
                A[k,k-1] = -(alpha*dt)/(dz**2)
                B[k] = 0
                
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
        - z : Matrice (array) de dimension (nz) qui contient la position en z
            * Exemple d'une matrice position :
            * Si  et Z = [0, 1]
            * Avec nz = 3
            
                z = [0 0.5 1]
    """
    
    z = np.zeros(nz) #Création de la matrice de position en z selon les dimensions contraintes par la discrétisation de l'espace
    
    
    z[0] = Z[1] #La première ligne de la matrice aura comme valeur la borne maximale du domaine de z
    z[-1] = Z[0] #La dernière ligne de la matrice aura comme valeur la borne minimale du domaine de z
    

    dz = (abs(Z[0])+abs(Z[1]))/(nz-1) #Obtention de la valeur de pas entre chaque points en z
    
    zr = Z[1] #Pose la valeur initiale permettant d'obtenir la valeur de z pour la deuxième ligne
    for i in range(1  , nz-1): #On saute les première et dernière valeurs qui ont déjà été obtenues plus haut
        zr = zr - dz #Ajoute la valeur du pas à la valeur de la ligne précédente
        z[i]=zr #Ajoute la nouvelle valeur à la ligne i
    z = np.flip(np.round(z,5))
    return z


def nombre_de_points(n):
    """ Qui asssure que le nombre de point choisi place un point sur la frontière (cas où la proportion 
    glace:béton est 1:2)
    Entrées: 
        - n : nombre de points voulus

    Sorties (dans l'ordre énuméré ci-bas):
        - z : nombre de points qui assure un point sur la frontière

    """
    
    point = 1 + n//3 * 3
    return point
    

def temperature_sans_echec(Z_limit,nz,prm,dt,tf) :
    """Fonction qui permet l'utilisation de la MDF peu importe la proportion glace béton en utilisant
    un nombre de points dynamique.
    
    Entrées :
        - Z_limit : Bornes du domaine en z, Z_limit = [z_min, z_max]
        - nz : Discrétisation de l'espace en z (nombre de points)
        - prm : objet contenant tous les paramètres physiques du problème
        - dt : pas de temps 
        - tf : temps final
        
    Sorties
        -temp[1][-1,-1] : Temperature à la surface après 90min
    """
    
    Z = mesh_1D(Z_limit,nz)

    while prm.zb not in Z and nz<200 :
        nz +=1 
        Z = mesh_1D(Z_limit,nz)
        
    #print(nz)
        
    temp = mdf_1D_transitoire(Z_limit, nz, prm, dt, tf)
    return temp[1][-1,-1]
    

def trouver_nombre_points(n_start,dt,tf,Z,prm,tol,limit_points):
    """Fonction qui retourne le nombre de points minimum pour avoir une erreur minimum
    
    Entrées :
        - n_start : Nombre de points auquel on commence l'analyse'
        - dt : pas de temps
        - tf : temps final
        - Z : Bornes du domaine en z, Z = [z_min, z_max]
        - prm : objet contenant tous les paramètres physiques du problème
        - tol : tolerence à l'erreur
        - limit_points: nombre de points max à tester
        
    Sorties
         - n : nombre de point à utiliser
         - err_plot : évolution de l'erreur en fonction du nombre de points [nombre de points,erreur @ 0min,erreur @15min, erreur @90min]
    """
    T = np.array([-1.00,-5.50,-3.25],dtype=float)
    t_test = np.array([0,15,90],dtype=int)
    
    tol=0.8
    nz = n_start
    err = np.ones(3)
    err_plot = np.zeros((limit_points-n_start,4))
    nz_foud = False

    for j in range(n_start,limit_points):
        temp_to_test = mdf_1D_transitoire(Z, nz, prm, dt, tf)
        for i in range(0,3):
            err[i] = temp_to_test[1][-1,t_test[i]]
            
        err = abs(err-T)
        nz = nombre_de_points(j)
        err_plot[j-n_start, :] = [nz,err[0],err[1],err[2]]
        
        if any([err[0]<=tol,err[1]<=tol,err[2]<=tol]) and not nz_foud :
            n=nz
            nz_foud = True
            
    return n,err_plot

