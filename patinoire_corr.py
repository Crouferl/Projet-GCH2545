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
        X = [-1,1]
        Z = [0,prm.zb+prm.zg]
    
        nx = 2
        nz = 100
        dt = 60
        tf = 5400
        
        T = np.array([-1.00,-6.35,-5.85,-5.50,-3.60,-3.25],dtype=float)
        t_test = np.array([0,2,7,15,45,90],dtype=int)
        rep_mdf = mdf(X,Z,nx,nz,prm,dt,tf)
        test_T = np.zeros(6)
        for i,t in enumerate(t_test) : 
            test_T[i] = rep_mdf[1][0,t]
            
        err_mdf = abs(np.asarray(test_T - T))
        
    
        assert (all(err_mdf < 1e-04))
    
    def test_mdf_permanent(self):
        X = [-1,1]
        Z = [0,prm.zb+prm.zg]
    
        nx = 2
        nz = 100
        dt = 60
        tf = 5400
        
        T = np.array([-1.00,-6.35,-5.85,-5.50,-3.60,-3.25],dtype=float)
        t_test = np.array([0,2,7,15,45,90],dtype=int)
        rep_mdf = mdf_permanent(X,Z,nx,nz,prm,dt,tf)
        test_T = np.zeros(6)
        for i,t in enumerate(t_test) : 
            test_T[i] = rep_mdf[1][0,t]
            
        err_mdf = abs(np.asarray(test_T - T))
        
    
        assert (all(err_mdf < 1e-04))
    


