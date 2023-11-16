#Importation des modules 


#Fonctions à faire :

# Optimiser nombre de points (Optionnel)
    #Input : erreur voulue
    #Out : Nombre de points en x et en y

#Interpoler température lagrange
    #Input : temps, température
    #Out : Coefficients du polyôme

#Résidus : Calcul le résidu du système d'équation
    #Input : valeur actuelle (T), valeur intiale (Ti), prm, pas de temps
    #Out : résidus

#Jacobienne : Calcul jacobienne numérique
    #Input : Valeur actuelle (T), prm, pas de temps
    #Out : matrice jacobienne


# Euler implicite
    #Input : conditions initiales, pas de temps, temps final, tolérance, prm
    #Out : Température, temps

#mesh : discrétiser l'espace à étudier
    #Input : nx,ny,x_min, x_max, z_min, z_max
    #Out : matrices des positions x, matrices des positions y

#mdf : remplir les matrices A et B
    #Input : Bornes x, bornes y, nx, nz, prm
    #Out :Matrice A et matrice B
    #Note : calculs euler implicite à faire pour remplir matrice 

# Plot (Optionnel) :
    #Input : titre, noms des axes 
    #Out : oject figure

