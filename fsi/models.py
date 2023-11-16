import numpy as np
from scipy import optimize

# =============================================================================
# General model class
# =============================================================================
class Model:
    def __init__(self, dict):
        self.caseName = dict["caseName"]
        self.pars = dict["pars"]
        self.control = dict["control"]
        self.plotConfig = dict["plotConfig"]
    
    def S0ecu(self):
        pass
    
    def solveZerothOrder(self):
        print("Solving zeroth order system...")
        self.S0 = optimize.newton(self.zerothOrder, 0, tol = 1e-9, maxiter=1000)
        print("Solution founded for S0 = "+str(round(self.S0,3)))
        print("-----------------------")
        
      
# =============================================================================
# SPHW: Single pipe horizontal wall model
# =============================================================================
class SPHW(Model):
    def __init__(self, dict):
        super().__init__(dict)
        self.VC = self.PC = 0 #Dummy initial values
    
    def V0(self,x):
        return self.VC + x*0 #dummy X
        
    def P0(self,x):
        self.K0V = self.f/(1 + self.S0)
        return -x * self.K0V * self.VC**2 + self.PC
    
        
class SPHW_reservoirs(SPHW):
    def __init__(self, dict):
        super().__init__(dict)
        self.solveZerothOrder()
    
    def zerothOrder(self, S0test):
        #FSI parameters
        M = self.pars['M']; VR = self.pars['VR']
        
        #Geometric Parameters
        epsilon = self.pars['epsilon']; c = self.pars['c']
        betaIbar = self.pars["betaIbar"]; betaObar = self.pars["betaObar"];

        #Fluid parameters
        pU = self.pars["pU"]; pD = self.pars["pD"]; deltaP = pD - pU
        
        #Energy looses
        c = self.pars["c"] ; k0I = self.pars["k0I"] ; k0O = self.pars["k0O"] 
        
        #Derived values
        self.betaI = (betaIbar + S0test) / (1 + S0test); 
        self.betaO = (betaObar + S0test) / (1 + S0test); 
        self.f = c/epsilon;
        self.K0I = k0I * self.betaI**2; 
        self.K0O = k0O * self.betaO**2; 
        self.K0V = self.f/(1 + S0test);
        self.Lambda = self.K0I + self.K0O + 2*self.K0V
        self.LambdaU = (-1 + self.K0O + 2*self.K0V) * (self.Lambda)**(-1) 
        self.LambdaD = (1 + self.K0I) * (self.Lambda)**(-1)  
        
        #Integration constants
        self.VC = np.sqrt( -2*deltaP / self.Lambda)
        self.PC = pU * self.LambdaU + pD * self.LambdaD
        
        integralP = -0.5 * self.K0V * self.VC**2 + self.PC

        return S0test * (4*np.pi**2) - M * VR**2 * epsilon**(-2) * integralP #just S0test here, (equilibrium possition)
        
    def firstOrder(self, omega):
        #FSI parameters
        M = self.pars['M']; VR = self.pars['VR']
        
        #Geometric Parameters
        epsilon = self.pars['epsilon']; c = self.pars['c']
        betaIbar = self.pars["betaIbar"]; betaObar = self.pars["betaObar"];

        #Fluid parameters
        pU = self.pars["pU"]; pD = self.pars["pD"]; deltaP = pD - pU
        
        #Energy looses
        c = self.pars["c"] ; 
        k0I = self.pars["k0I"]; k0O = self.pars["k0O"] 
        k1I = self.pars["k1I"]; k1O = self.pars["k1O"]
        self.xiI = (1 - self.betaI)/( 1 + self.S0 ); 
        self.xiO = (1 - self.betaO)/( 1 + self.S0 )

        #Derived values
        self.K1I = k1I * self.betaI**2
        self.K1O = k1O * self.betaO**2
        self.KtI = k0I * self.betaI * self.xiI
        self.KtO = k0O * self.betaO * self.xiO
        
        T0 = self.K0V - self.K1I - self.K1O - self.KtI - self.KtO
        T1 = self.K0O + self.K0V
 
        sigmaB = (2*self.Lambda*(self.S0+1)*T0*self.VC**3 + 2*T1*self.VC*omega**2 - self.Lambda*self.VC*omega**2) \
          * (2*self.Lambda**2*(self.S0+1)*self.VC**2 + 2*(self.S0+1)*omega**2)**(-1)
        sigmaT = (2*self.VC**2*(self.Lambda*T1-(self.S0+1)*T0) + omega**2)  \
          * (2*self.Lambda**2*(self.S0+1)*self.VC**2 + 2*(self.S0+1)*omega**2)**(-1)
    
        MA = (epsilon**2) / (12*VR**2*M*(1+self.S0))
        CA = ( (self.VC*epsilon**2)/(2*VR**2*M) ) * ( (1/(1+self.S0)) * (-1 + self.K0I + self.K0V/3) + sigmaT * (2 + self.K0I - self.K0O) )
        KA = ( (self.VC*epsilon**2)/(2*VR**2*M) ) * ( self.VC * (self.K1I - self.K1O + self.KtI - self.KtO ) + sigmaB * (2 + self.K0I - self.K0O) )

        return MA, CA, KA
# =============================================================================
# SPRW: Single pipe rotating wall model
# =============================================================================

class SPRW(Model):
    def __init__(self, dict):
        super().__init__(dict)
        self.VC = self.PC = 0 #Dummy initial values
    
    def V0(self,x):
        return 0
        
    def P0(self,x):
        self.K0V = self.f/self.S0
        return 0

class SPRW_reservoirs(SPRW):
    def __init__(self, dict):
        super().__init__(dict)
        self.solveZeroth()
    
    def zerothOrder(self,S0test):
        return 0





