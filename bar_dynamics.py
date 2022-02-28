from read_constant_params import read_const_p
from read_dynamic_params import read_dynamic_p
from sys_quat_onsite import quat_onsite_eqns
from sys_quat_offsite import quat_offsite_eqns
from sys_ter_onsite import ter_onsite_eqns
from sys_ter_offsite import ter_offsite_eqns
import numpy as np
import numba as nb
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Read the parameters
# (change dynamic_p if needed after reading the file)
const_p = read_const_p()
dynamic_p = read_dynamic_p()
params = {**const_p, **dynamic_p}

# Temporary variables to save steady-state GFP level
num = 2
low_low = np.zeros(num*num)
low_hi = np.zeros(num*num)
hi_low = np.zeros(num*num)
hi_hi = np.zeros(num*num)

for j in range(num):
    for i in range(num):
        # For initial conditions
        
        # Variable notation
        # x g c C D
        # 0 1 2 3 4
        # d m G
        # 0 1 2

        i_arr_MCP_on = np.zeros(5)
        j_arr_MCP_on = np.zeros(5)
        sys_arr_MCP_on = np.zeros(3)
        i_arr_MCP_on[0] = i*10
        j_arr_MCP_on[0] = j*10
        sys_arr_MCP_on[0] = params["d_t"]
        sys_arr_MCP_on[1] = params["m_t"]

        i_arr_MCP_off = np.zeros(5)
        j_arr_MCP_off = np.zeros(5)
        sys_arr_MCP_off = np.zeros(3)
        i_arr_MCP_off[0] = i*10
        j_arr_MCP_off[0] = j*10
        sys_arr_MCP_off[0] = params["d_t"]
        sys_arr_MCP_off[1] = params["m_t"]

        i_arr_no_MCP_on = np.zeros(5)
        j_arr_no_MCP_on = np.zeros(5)
        sys_arr_no_MCP_on = np.zeros(3)
        i_arr_no_MCP_on[0] = i*10
        j_arr_no_MCP_on[0] = j*10
        sys_arr_no_MCP_on[0] = params["d_t"]
        sys_arr_no_MCP_on[1] = params["m_t"]

        i_arr_no_MCP_off = np.zeros(5)
        j_arr_no_MCP_off = np.zeros(5)
        sys_arr_no_MCP_off = np.zeros(3)
        i_arr_no_MCP_off[0] = i*10
        j_arr_no_MCP_off[0] = j*10
        sys_arr_no_MCP_off[0] = params["d_t"]
        sys_arr_no_MCP_off[1] = params["m_t"]

        dt = 0.01

        for t in range(10000):
            i_arr_MCP_on, j_arr_MCP_on, sys_arr_MCP_on = quat_onsite_eqns(i_arr_MCP_on, j_arr_MCP_on,
                                            sys_arr_MCP_on, params, dt)
            i_arr_MCP_off, j_arr_MCP_off, sys_arr_MCP_off = quat_offsite_eqns(i_arr_MCP_off, j_arr_MCP_off,
                                            sys_arr_MCP_off, params, dt)
            i_arr_no_MCP_on, j_arr_no_MCP_on, sys_arr_no_MCP_on = ter_onsite_eqns(i_arr_no_MCP_on, j_arr_no_MCP_on,
                                            sys_arr_no_MCP_on, params, dt)
            i_arr_no_MCP_off, j_arr_no_MCP_off, sys_arr_no_MCP_off = ter_offsite_eqns(i_arr_no_MCP_off, j_arr_no_MCP_off,
                                            sys_arr_no_MCP_off, params, dt)
        print(f"D_i = {i_arr_MCP_on[3]} AND C_i = {i_arr_MCP_on[4]}")
        print(f"D_j = {j_arr_MCP_on[3]} AND C_j = {j_arr_MCP_on[4]}")
        
        if (num*j+i) == 0:
            #print(i_arr_no_MCP_on[3], i_arr_no_MCP_off[3], 
            #            i_arr_MCP_on[3], i_arr_MCP_off[3])
            low_low = [sys_arr_no_MCP_on[2], sys_arr_no_MCP_off[2], 
                        sys_arr_MCP_on[2], sys_arr_MCP_off[2]]
        elif (num*j+i) == 1:
            #print(i_arr_no_MCP_on[3], i_arr_no_MCP_off[3], 
            #            i_arr_MCP_on[3], i_arr_MCP_off[3])
            hi_low = [sys_arr_no_MCP_on[2], sys_arr_no_MCP_off[2], 
                        sys_arr_MCP_on[2], sys_arr_MCP_off[2]]
        elif (num*j+i) == 2:
            #print(i_arr_no_MCP_on[3], i_arr_no_MCP_off[3], 
            #            i_arr_MCP_on[3], i_arr_MCP_off[3])
            low_hi = [sys_arr_no_MCP_on[2], sys_arr_no_MCP_off[2], 
                        sys_arr_MCP_on[2], sys_arr_MCP_off[2]]
        else:
            #print(i_arr_no_MCP_on[3], i_arr_no_MCP_off[3], 
            #            i_arr_MCP_on[3], i_arr_MCP_off[3])
            hi_hi = [sys_arr_no_MCP_on[2], sys_arr_no_MCP_off[2], 
                        sys_arr_MCP_on[2], sys_arr_MCP_off[2]]                        

labels = ['Ter onsite', 'Ter offsite', 'Quat onsite', 'Quat offsite',]

x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - 1.5*width, low_low, width, label="0-0")
rects2 = ax.bar(x - .5*width, low_hi, width, label="0-1")
rects3 = ax.bar(x + .5*width, hi_low, width, label="1-0")
rects4 = ax.bar(x + 1.5*width, hi_hi, width, label="1-1")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('GFP levels')
ax.set_title('Different systems')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=2)
ax.bar_label(rects2, padding=2)
ax.bar_label(rects3, padding=2)
ax.bar_label(rects4, padding=2)

fig.tight_layout()

plt.show()
