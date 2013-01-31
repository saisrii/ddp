import sympy
from getparameters import *
from currenteqs import *
from parsers import *
from config import *
from numericals import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# This file is the topmost layer of the project. Only function level calls and data transfer is shown here. 
global linPJac, B, C, D, linPVal, inputm, count, linP
#
# These functions are used in the integration process
# Derivative of the function at any point is given by
# dx/dt = Summation( weight*(Jacobian * ( state ) + B * ( input ) + ( Val @ state - Jacobian * linPoint )))
def dervPWL(y,t):
	#order = len(y)
	weights = normcalc( y )
	#count = len(weights)
	temp = 0
    
	for i in range(count):
		temp = temp +  weights[ i ] * ( linPVal[ i ] + (numpy.dot( linPJac[ i ], y )).reshape( order ,1 ) - (numpy.dot( linPJac[ i ], linP[ i ] )).reshape( order ,1 ) + (numpy.dot( B[ i ], inputm[ i ] )) )
	return (temp.reshape(1, order))[0]

# Calculates the weighing function depending on the proximity to linearizatoin points
def normcalc( y ) :
	norm = numpy.array([ 10**(-1*numpy.linalg.norm( linP[ i ] - y.reshape(order,1) )) for i in range(count) ])
	return norm/norm.sum()

initialcond = get_initialcond(file_voltage)

state = get_states(file_voltage)

stateorder = get_stateorder(state)

steadystate = get_steadystate(file_voltage,initialcond,stateorder, sim_end,order)

delta = get_linpdiff(initialcond,steadystate,stateorder,order)

print "Simulation begins at ", sim_begin

count,time = get_linPoints(file_voltage,initialcond,delta/denominator,order,stateorder)

datapoints = get_datapoints(file_voltage, count , time)

currents = get_currents(file_current,count,time)

regions = get_region_operation(datapoints,file_netlist,count)

Vth = get_vth()

regexp = get_regexp_eqs(input_list)

inputorder = get_inputorder(state, input_list )

linP = get_num_linP(count,order,datapoints,stateorder)

linPJac, B, C, D, linPVal, inputm = init_statematrices(count,order,input_list,output_list,stateorder)

linPJac, B, C, D, linPVal,inputm = get_statematrices( linPJac, B, C, D, linPVal, inputm, count, order, regions, state, regexp, datapoints, stateorder,inputorder, Vth)

y0 , time = get_parameters_integration( initialcond, intg_end, stateorder )

solnPWL = odeint(dervPWL, y0, time)

#--------------------------------------------------------------------------------------------
# Plotting the output obtained with integration
C_ones = [i for i in range( len( stateorder ) ) if str( stateorder[ i ] ) in output_list ]
for k in range(len(C_ones)):
	plt.figure(k)
	plt.plot(time, numpy.array([ float(solnPWL[i][C_ones[k]]) for i in range(len(time) )] ), '--')
	plt.ylabel(r'$V_{'+str(stateorder[C_ones[k]])+'}$' )
	plt.xlabel(r'$time$')
	plt.title(r'$Output\ as\ function\ of\ time$' )
plt.show()
