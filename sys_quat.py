# Important packages
import numpy as np
import numba as nb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.optimize import brentq
import sys, os

# Variable notation
# x g c C D
# 0 1 2 3 4
# d m G
# 0 1 2

@nb.jit(nopython=True, nogil=True)
def free_d(d, m, ki, qi, gi, Dit, kj, qj, gj, Djt, dt):

    return (d + d*m*(ki*gi+kj*gj) + d*m*(
            ki*qi*gi*Dit/(1+qi*ki*gi*d*m) + 
            kj*qj*gj*Djt/(1+qj*kj*gj*d*m)) - dt)

@nb.jit(nopython=True, nogil=True)
def free_m(m, d, ki, qi, gi, Dit, kj, qj, gj, Djt, mt):

    return (m + d*m*(ki*gi+kj*gj) + d*m*(
            ki*qi*gi*Dit/(1+qi*ki*gi*d*m) + 
            kj*qj*gj*Djt/(1+qj*kj*gj*d*m)) - mt)

def quat_eqns(i_arr, j_arr, sys_arr, com_pars, circ_pars, dt):

    # temporary variables
    x_i = i_arr[0]
    g_i = i_arr[1]
    c_i = i_arr[2]
    C_i = i_arr[3]
    D_i = i_arr[4]
    x_j = j_arr[0]
    g_j = j_arr[1]
    c_j = j_arr[2]
    C_j = j_arr[3]
    D_j = j_arr[4]
    d = sys_arr[0]
    m = sys_arr[1]
    G = sys_arr[2]

    # 0   1  2   3  4  5  
    # gi gj dgi dgj Ki Kj 
    # 6  7  8  9 10 11
    # mt dt Dt ui uj dG
    
    # 0   1  2   3
    # ki  kj qi  qj
    
    gi = com_pars[0]
    gj = com_pars[1]
    dgi = com_pars[2] 
    dgj = com_pars[3]
    Ki = com_pars[4]
    Kj = com_pars[5]
    m_t = com_pars[6]
    d_t = com_pars[7]
    Dt = com_pars[8]
    ui = com_pars[9]
    uj = com_pars[10]
    dG = com_pars[11]
    
    ki = circ_pars[0]
    kj = circ_pars[1]
    qi = circ_pars[2]
    qj = circ_pars[3]
    
    # non linear solver to find free dCas9 and free MCP-SoxS concerntration
    sys_arr[0] = brentq(f=free_d, a=0, b=d_t, args=(sys_arr[1], ki, 
                                    qi, g_i, Dt, 
                                    kj, qj, 
                                    g_j, Dt, d_t))                                
    sys_arr[1] = brentq(f=free_m, a=0, b=m_t, args=(sys_arr[0], ki, 
                                    qi, g_i, Dt, 
                                    kj, qj, 
                                    g_j, Dt, m_t))                                                     

    # Update concentrations
    i_arr[0] = x_i
    j_arr[0] = x_j
    i_arr[1] += (ui + gi*x_i - dgi*g_i)*dt
    j_arr[1] += (uj + gj*x_j -dgj*g_j)*dt
    i_arr[2] = ki*g_i*d*m
    j_arr[2] = kj*g_j*d*m
    i_arr[3] = qi*ki*g_i*d*m*D_i
    j_arr[3] = qj*kj*g_j*d*m*D_j 
    i_arr[4] = Dt/(1+qi*ki*g_i*d*m)
    j_arr[4] = Dt/(1+qj*kj*g_j*d*m)
    sys_arr[2] += (Ki*C_i*D_j/Dt + Kj*D_j*D_i/Dt - dG*G)*dt
    #sys_arr[2] += (p["K_i"]*C_i + p["K_j"]*D_j - p["dG"]*G)*dt
    return i_arr, j_arr, sys_arr