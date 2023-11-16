import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# General configuration
# =============================================================================
# plt.style.use(['science', 'grid'])
# plt.rc('figure', figsize=(10, 5))
# font = {'size' : 16}
# plt.rc('font', **font)  # pass in the font dict as kwargs

plt.style.use(['ggplot'])
plt.rcParams.update({"text.usetex": True,
                     'font.size': 16, 
                     "font.sans-serif": "Palatino",
                     "axes.grid" : True, 
                     "grid.color": "white"})
plt.rcParams['font.family'] = 'serif'
plt.rcParams['legend.loc'] = "upper right"
plt.rcParams["figure.autolayout"] = "True"
plt.rcParams["figure.figsize"] = (10,5)

def zerothPlot(model):
    pp = model.plotConfig
    
    x = np.linspace(0, 1, pp["res"])
    V0 = model.V0(x); P0 = model.P0(x)
    
    fig, axs = plt.subplots(1, 2); fig.suptitle('Zeroth order solution')

    axs[0].plot(x, V0)
    axs[0].plot([0,1],[0,0], linestyle='--', color='black', linewidth=1.5)
    axs[0].set_ylabel('$V_0$'); axs[0].set_xlabel('$X$')
    
    axs[1].plot(x, P0)
    axs[1].plot([0,1],[0,0], linestyle='--', color='black', linewidth=1.5)
    axs[1].set_ylabel('$P_0$'); axs[1].set_xlabel('$X$')
    
    plt.tight_layout()
    
    if pp["savePlot"] is True:
        plt.savefig("output/" + str(model.caseName) + "_zerothOrder.pdf")
    
def firstPlot(model):
    pp = model.plotConfig
    
    omegaVal = np.linspace(pp["omegaMin"], pp["omegaMax"], pp["res"])
    MA, CA, KA = model.firstOrder(omegaVal)
    
    fig, axs = plt.subplots(1, 2); fig.suptitle('First order solutions')

    axs[0].plot(omegaVal, CA)
    axs[0].plot([0,pp["omegaMax"]],[0,0], linestyle='--', color='black', linewidth=1.5)
    axs[0].set_ylabel('$C_A$'); axs[0].set_xlabel('$\Omega$')
    
    axs[1].plot(omegaVal, KA)
    axs[1].plot([0,pp["omegaMax"]],[0,0], linestyle='--', color='black', linewidth=1.5)
    axs[1].set_ylabel('$K_A$'); axs[1].set_xlabel('$\Omega$')
    
    plt.tight_layout()
