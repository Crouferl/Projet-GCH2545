import numpy as npimport matplotlib.pyplot as pltdef interpoler(x,y,x_interpo):    """ Fonction qui permet d'interpoler la température de l'air en fonction du temps    Entrées:        - x : Ensemble de données (Couples de valeurs avec y)        - y : Ensemble de données (Couples de valeurs avec x)        - x_interpo : x auquel on cherche y    Sorties (dans l'ordre énuméré ci-bas):        - y_interpo : y interpolée couplé à x_interpo            """    n = len(x)        y_interpo = 0    for i in range(n):        p=1        for j in range(n):            if j != i:                p = p * (x_interpo - x[j])/(x[i] - x[j]) #Permet de trouver les polynôme L[i](x)                        y_interpo = y_interpo + y[i]*p #T = f(x_0)L_0(x) + f(x_1)L_1(x) + ... + f(x_n-1)L_n-1(x)            return y_interpodef interpolation_Tair(temps_interpo):    """ Fonction qui permet d'interpoler la température de l'air en fonction du temps    Entrées:        - temps_interpo : Temps auquel on cherche la Température    Sorties (dans l'ordre énuméré ci-bas):        - temperature_interpo : Température interpolée au temps temps_interpo    """    temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la question    for i in range(len(temps)):        temps[i] = temps[i]*60            temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] #Valeurs de température spécifiées dans la question    n = len(temps)    omega = 0    for i in range(n):        if temps_interpo == temps[i]:            return temperature[i]                elif temps_interpo > temps[i] and temps_interpo < temps[i+1]:            omega = i     return interpoler([temps[omega],temps[omega+1]],[temperature[omega],temperature[omega+1]],temps_interpo)n=1000x = np.linspace(0,90*60,n)y = np.zeros(n)for i in range(n):    y[i] = interpolation_Tair(x[i])temps = [0, 2, 7, 15, 45, 90]  #Valeurs de temps spécifiés dans la questionfor i in range(len(temps)):    temps[i] = temps[i]*60    temperature = [-1, 3.81 , 7.07 , 9.06 , 11.92 , 13.73 ] plt.plot(temps,temperature, label = 'vrai')plt.plot(x,y, label = "interpo") plt.legend()plt.show   print(interpolation_Tair(90*60)) 