#Auteurs 
#Nicolas Guillemette (2081046)
#Raphael Louis-Seize (2144924)
#Léo Croufer (2001374)

import numpy as np
try:
    from patinoire_fct import *
except:
    print("ERREUR! Il y a une erreur fatale dans le fichier patinoire_fct.py")


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

#-----------------------------------------------------------------------------

prm = parametre()




class Test:

    def test_mdf_transitoire(self):
        Z = [0,round(prm.zb+prm.zg,5)]
        nz = 10
        dt = 60
        tf = 5400
        
        T = np.array([-1.00,-5.50,-3.25],dtype=float)
        t_test = np.array([0,15,90],dtype=int)
        rep_mdf = mdf_1D_transitoire(Z,nz,prm,dt,tf)
        test_T = np.zeros(3)
        for i,t in enumerate(t_test) : 
            test_T[i] = rep_mdf[1][-1,t]
            
        err_mdf = abs(np.asarray(test_T - T))
        
    
        assert (all(err_mdf < 2))
    
    def test_mdf_permanent(self):
        Z = [0,round(prm.zb+prm.zg,5)]
        nz = 10
        dt = 60
        tf = 5400
        
        T = np.array([-3.25],dtype=float)
        t_test = np.array([90],dtype=int)
        rep_mdf = mdf_1D_permanent(Z,nz,prm,dt,tf)
        test_T = np.zeros(1)
        for i,t in enumerate(t_test) : 
            test_T[i] = rep_mdf[1][-1,t]
            
        err_mdf = abs(np.asarray(test_T - T))
        
    
        assert (all(err_mdf < 2))


