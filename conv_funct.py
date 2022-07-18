from sys_quat import quat_eqns
from sys_ter import ter_eqns
import numpy as np

# 0   1  2   3  4  5  
# gi gj dgi dgj Ki Kj 
# 6  7  8  9 10 11
# mt dt Dt ui uj dG
# com_pars = [8.84*60, 8.84*60, 0.18*60, 0.18*60, 100, 5,
#             100, 100, 30.0, 0.0, 0.0, 0.0196*60]
# 0   1  2   3
# ki  kj qi  qj
# circ_pars = [1.2,10**5,2,100,
#               1.2,10**5,2,0,
#               1.2,1.2,2,2,
#               1.2,1.2,2,0]

# dumdum = [8.84*60, 8.84*60, 0.18*60, 0.18*60, 100, 5,100, 100, 30.0, 0.0, 0.0, 0.0196*60,1.2,10**5,2,100, 1.2,10**5,2,0, 1.2,1.2,2,2, 1.2,1.2,2,0]
# params = com_pars.copy()
# params.extend(circ_pars)

def solver_func(xdata, gi,gj,dgi,dgj,Ki,Kj,mt,dt,Dt,ui,uj,dG,
				ki1,kj1,qi1,qj1,ki2,kj2,qi2,qj2,
				ki3,kj3,qi3,qj3,ki4,kj4,qi4,qj4):
	
	com_pars = [gi,gj,dgi,dgj,Ki,Kj,mt,dt,Dt,ui,uj,dG]
	trange = 10000
	i_arr = np.zeros(5)
	j_arr = np.zeros(5)
	sys_arr = np.zeros(3)
	ydata = []
	if type(xdata[0]) == float:
		xdata = [xdata]
	for data in xdata:
		alpha, beta, gamma = data
		i_arr[0] = beta
		j_arr[0] = gamma
		sys_arr[0] = com_pars[7]
		sys_arr[1] = com_pars[6]
		dt = 0.01
		circ = int(alpha)
        
		
		if circ == 1:
			circ_pars = [ki1,kj1,qi1,qj1]
			for t in range(trange):
				i_arr, j_arr, sys_arr = ter_eqns(i_arr, j_arr,
												sys_arr , com_pars, circ_pars , dt)
		elif circ == 2:
			circ_pars = [ki2,kj2,qi2,qj2]
			for t in range(trange):
				i_arr, j_arr, sys_arr = ter_eqns(i_arr, j_arr,
												sys_arr , com_pars, circ_pars , dt)
		elif circ == 3:
			circ_pars = [ki3,kj3,qi3,qj3]
			for t in range(trange):
				i_arr, j_arr, sys_arr = quat_eqns(i_arr, j_arr,
												sys_arr ,com_pars, circ_pars , dt)
		elif circ == 4:
			circ_pars = [ki4,kj4,qi4,qj4]
			for t in range(trange):
				i_arr, j_arr, sys_arr = quat_eqns(i_arr, j_arr,
												sys_arr ,com_pars, circ_pars , dt)
		#print(sys_arr[2])    
		ydata.append(sys_arr[2])
	#return(sys_arr[2])
	return ydata

def solver_func_ternon_log(xdata, gi,gj,dgi,dgj,Ki,Kj,mt,dt,Dt,ui,uj,dG,
				ki1,kj1,qi1,qj1):
	# (-20,-20,-50,-50,-20,-20,-10,-10,0,-20,-20,-20,-10,-10,-10,-10)
    # (20,20,15,15,30,30,20,20,10,10,10,10,20,20,20,20)
	com_pars = [10**gi,10**gj,10**dgi,10**dgj,10**Ki,10**Kj,10**mt,10**dt,
             Dt,10**ui,10**uj,10**dG]
	trange = 10000
	i_arr = np.zeros(5)
	j_arr = np.zeros(5)
	sys_arr = np.zeros(3)
	ydata = []
	if type(xdata[0]) == float:
		xdata = [xdata]
	for data in xdata:
		beta, gamma = data
		i_arr[0] = beta
		j_arr[0] = gamma
		sys_arr[0] = com_pars[7]
		sys_arr[1] = com_pars[6]
		dt = 0.01      
		circ_pars = [10**ki1,10**kj1,10**qi1,10**qj1]
		for t in range(trange):
		    i_arr, j_arr, sys_arr = ter_eqns(i_arr, j_arr,
												sys_arr , com_pars, circ_pars , dt)
		#print(sys_arr[2])    
	ydata.append(sys_arr[2])
	#return(sys_arr[2])
	return ydata
	
def solver_func_ternon(xdata, gi,gj,dgi,dgj,Ki,Kj,mt,dt,Dt,ui,uj,dG,
				ki1,kj1,qi1,qj1):
	# (-20,-20,-50,-50,-20,-20,-10,-10,0,-20,-20,-20,-10,-10,-10,-10)
    # (20,20,15,15,30,30,20,20,10,10,10,10,20,20,20,20)
	com_pars = [gi,gj,dgi,dgj,Ki,Kj,mt,dt,
             Dt,ui,uj,dG]
	trange = 10000
	i_arr = np.zeros(5)
	j_arr = np.zeros(5)
	sys_arr = np.zeros(3)
	ydata = []
	if type(xdata[0]) == float:
		xdata = [xdata]
	for data in xdata:
		beta, gamma = data
		i_arr[0] = beta
		j_arr[0] = gamma
		sys_arr[0] = com_pars[7]
		sys_arr[1] = com_pars[6]
		dt = 0.01      
		circ_pars = [ki1,kj1,qi1,qj1]
		for t in range(trange):
		    i_arr, j_arr, sys_arr = ter_eqns(i_arr, j_arr,
												sys_arr , com_pars, circ_pars , dt)
		#print(sys_arr[2])    
	ydata.append(sys_arr[2])
	#return(sys_arr[2])
	return ydata

def solver_func_quaton(xdata, gi,gj,dgi,dgj,Ki,Kj,mt,dt,Dt,ui,uj,dG,
				ki1,kj1,qi1,qj1):
	# (-20,-20,-50,-50,-20,-20,-10,-10,0,-20,-20,-20,-10,-10,-10,-10)
    # (20,20,15,15,30,30,20,20,10,10,10,10,20,20,20,20)
	com_pars = [gi,gj,dgi,dgj,Ki,Kj,mt,dt,
             Dt,ui,uj,dG]
	trange = 10000
	i_arr = np.zeros(5)
	j_arr = np.zeros(5)
	sys_arr = np.zeros(3)
	ydata = []
	if type(xdata[0]) == float:
		xdata = [xdata]
	for data in xdata:
		beta, gamma = data
		i_arr[0] = beta
		j_arr[0] = gamma
		sys_arr[0] = com_pars[7]
		sys_arr[1] = com_pars[6]
		dt = 0.01      
		circ_pars = [ki1,kj1,qi1,qj1]
		for t in range(trange):
		    i_arr, j_arr, sys_arr = quat_eqns(i_arr, j_arr,
												sys_arr , com_pars, circ_pars , dt)
		#print(sys_arr[2])    
	ydata.append(sys_arr[2])
	#return(sys_arr[2])
	return ydata

def dum_solver_func(xdata, params):
	
	com_pars = params[0:12]
	i_arr = np.zeros(5)
	j_arr = np.zeros(5)
	sys_arr = np.zeros(3)
	i_arr[0] = xdata[1]
	j_arr[0] = xdata[2]
	sys_arr[0] = com_pars[7]
	sys_arr[1] = com_pars[6]
	dt = 0.01
	circ = int(xdata[0])
	circ_pars = params[12+(circ-1)*4:12+circ*4]
	
	if circ == 1 or circ == 2:
		for t in range(10000):
			i_arr, j_arr, sys_arr = ter_eqns(i_arr, j_arr,
											sys_arr , com_pars, circ_pars , dt)
	elif circ == 3 or circ == 4:
		for t in range(10000):
			i_arr, j_arr, sys_arr = quat_eqns(i_arr, j_arr,
											sys_arr ,com_pars, circ_pars , dt)
	#print(sys_arr[2])        
	return(sys_arr[2])
	

