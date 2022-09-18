from conv_funct import *
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from math import *

# %% defining data selection

xdata = pd.read_csv(r'data\GFP_data.csv')
xdata = xdata.loc[xdata['AHL'] != 10] 
ydata = np.array(xdata['mean'])
dummy = np.transpose(np.array([xdata['category'],xdata['arabinose'],xdata['AHL']]))
# xdata = []
# for i in dummy:
#     xdata.append(np.array(i))
# xdata = np.array(xdata)

#### 

# %% trying massfit
popt, pcov = curve_fit(solver_func, dummy, ydata, bounds = (0,np.inf))

xdata1 = xdata.loc[xdata['category'] == 1]
ydata1 = np.array(xdata1['mean'])
dummy1 = np.transpose(np.array([xdata1['arabinose'],xdata1['AHL']]))

popt1log, pcov1log = curve_fit(solver_func_ternon_log,
                         dummy1, ydata1, 
                         bounds = ((-20,-20,-50,-50,-20,-20,-10,-10,0,-20,-20,-20,-10,-10,-10,-10)
                                                                       ,(20,20,15,15,30,30,20,20,10,10,10,10,20,20,20,20)))

popt1, pcov1 = curve_fit(solver_func_ternon,
                         dummy1, ydata1, 
                         bounds = (0, np.inf))
#gi,gj,dgi,dgj
#Ki,Kj,mt,dt
#Dt,ui,uj,dG
#ki1,kj1,qi1,qj1

popt1given = [1.01089220e+00, 4.34414008e-03, 6.78410449e+00, 1.16518971e+00,
              7.33485745e+00, 9.48188131e+00, 1.07280726e+00, 1.11538512e-01,
              1.05509747e+01, 1.05609933e+00, 1.39331544e+00, 7.78105162e-03,
              1.06844884e+00, 3.46792725e+00, 7.55166280e-01, 2.97377256e-01]
pcov1given = np.copy(pcov1)

# %% Trying individual model fits
from conv_funct import *
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from math import *
def std_cov(pcov):
    return(np.sqrt(np.diag(np.array(pcov))))

xdata = pd.read_csv(r'data\GFP_data.csv')
xdata = xdata.loc[xdata['AHL'] != 10] 
def cat_optimizer(xdata, cat):
    xdata = xdata.loc[xdata['category'] == cat]
    ydata = np.array(xdata['mean'])
    #print(np.size(ydata))
    ystd = np.array(xdata['sd'])
    dummy = np.transpose(np.array([xdata['arabinose'],xdata['AHL']]))
    
    stdt = 0
    if stdt == 0:
        if cat == 1 or cat == 2:
            popt, pcov = curve_fit(solver_func_ternon, dummy, ydata, bounds = (0, np.inf))
        else:
            popt, pcov = curve_fit(solver_func_quaton, dummy, ydata, bounds = (0, np.inf))
    elif stdt == 1:
        if cat == 1 or cat == 2:
            popt, pcov = curve_fit(solver_func_ternon, dummy, ydata,sigma = ystd, bounds = (0, np.inf))
        else:
            popt, pcov = curve_fit(solver_func_quaton, dummy, ydata,sigma = ystd, bounds = (0, np.inf))
    
    return(popt, std_cov(pcov))


popt1, pcov1 = cat_optimizer(xdata, 1)
popt2, pcov2 = cat_optimizer(xdata, 2)
popt3, pcov3 = cat_optimizer(xdata, 3)
popt4, pcov4 = cat_optimizer(xdata, 4)

pst1 = std_cov(pcov1)
pst2 = std_cov(pcov2)
pst3 = std_cov(pcov3)
pst4 = std_cov(pcov4)

#%% Trying only with common variables
from conv_funct import *
from scipy.optimize import curve_fit
import pandas as pd
import numpy as np
from math import *
def std_cov(pcov):
    return(np.sqrt(np.diag(np.array(pcov))))

xdata = pd.read_csv(r'data\GFP_data.csv')
xdata = xdata.loc[xdata['AHL'] != 10] 
def cat_optimizer_com(xdata, cat):
    xdata = xdata.loc[xdata['category'] == cat]
    ydata = np.array(xdata['mean'])
    #print(np.size(ydata))
    ystd = np.array(xdata['sd'])
    dummy = np.transpose(np.array([xdata['arabinose'],xdata['AHL']]))
    
    if cat == 1 or cat == 2:
        popt, pcov = curve_fit(solver_func_ter_com, dummy, ydata, bounds = (0, np.inf))
    else:
        popt, pcov = curve_fit(solver_func_quat_com, dummy, ydata, bounds = (0, np.inf))
    # elif stdt == 1:
    #     if cat == 1 or cat == 2:
    #         popt, pcov = curve_fit(solver_func_ter_com, dummy, ydata,sigma = ystd, bounds = (0, np.inf))
    #     else:
    #         popt, pcov = curve_fit(solver_func_quat_com, dummy, ydata,sigma = ystd, bounds = (0, np.inf))
    
    #return(popt, std_cov(pcov))
    return(popt, pcov)

popt1_used = [9.83998675e-01, 9.55710945e-01, 9.21118775e-01, 1.64378908e+00,
       1.77625088e+00, 2.46876100e+01, 1.18838752e+00, 1.66272060e-01,
       3.94813952e+00, 9.59500804e-01, 6.61835728e-01, 7.08982540e-03,
       1.29531198e+00, 6.33097230e-01, 4.64830267e-01, 7.70509267e-01]

popt1, pcov1 = cat_optimizer_com(xdata, 1)
popt2, pcov2 = cat_optimizer_com(xdata, 2)
popt3, pcov3 = cat_optimizer_com(xdata, 3)
popt4, pcov4 = cat_optimizer_com(xdata, 4)

pst1 = std_cov(pcov1)
pst2 = std_cov(pcov2)
pst3 = std_cov(pcov3)
pst4 = std_cov(pcov4)


# %% Multiple tries of individual shit
tot_popt1 = []
tot_cov1 = []
for i in range(0,15):
    print(i)
    tpt,tcv = cat_optimizer(xdata, 1)
    tot_popt1.append(tpt)
    tot_cov1.append(tcv)
    print(i)
    

from math import *
def std_cov(pcov):
    return(np.sqrt(np.diag(np.array(pcov))))

pst1 = std_cov(pcov1)
pst2 = std_cov(pcov2)
pst3 = std_cov(pcov3)
pst4 = std_cov(pcov4)


#%% Scaling and PCA Part ####
xdata = pd.read_csv(r'data\GFP_data.csv')
xdata = xdata.loc[xdata['AHL'] != 10]
data = xdata[['AHL','arabinose','mean','category']]
net_data = [data[data['category'] == i] for i in range(1,5)]
raw_data = [net_data[i].drop("category", axis = 1) for i in range(0,4)]
#AHL, arabinose, mean

from sklearn.preprocessing import StandardScaler
scaled_data = [StandardScaler().fit_transform(raw_data[i]) for i in range(0,4)]

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def taking_pca(i,scaled_data = scaled_data):
    pca = PCA()
    pca_data = pd.DataFrame(pca.fit_transform(scaled_data[i]))
    pca_loadings = pd.DataFrame(pca.components_, columns= ['AHL', 'arabinose', 'GFP'])
    print(f"category{i+1}")
    print(pca_loadings)
    print(pca.explained_variance_ratio_)
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('PC1', fontsize = 15)
    ax.set_ylabel('PC2', fontsize = 15)
    ax.set_title(f'Category {i+1}', fontsize = 20)
    ax.scatter(pca_data[0],pca_data[1])

#taking_pca(1)