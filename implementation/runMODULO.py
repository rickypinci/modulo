import sys
from profiles import *
from params import *
from module_battery import *
from module_performance import *
from module_reward import *


def getNextLevel(prof_dict, level, verbose=False):
	"""
	It returns a profile (from prof_dict) based on the battery level (level).
	:param dictionary prof_dict: The dictionary containing all the profiles
	:param float level: The level of the battery
	:param bool verbose: If the method should print debug messages
	:return float: The profile corresponding to the current battery level
	:return float: The next profile to use (only if it exists) to stop the current analysis
	"""
	if level > 1.0:	
		print('[Error] The passed battery level is larrger than 1.0, Clevel = ' + str(level))
		sys.exit(-1)
	keys = sorted(list(prof_dict.keys()))
	for i in range(len(keys)):
		key = keys[i]
		if level <= key:
			if verbose:
				print('Key ' + str(key) + ' selected strating from level ' + str(level))
			if i > 0:
				return key, keys[i-1]
			return key, _
	print('[Error] Something went wrong')
	sys.exit(-1)
	

def stillAlive(prof_dict, Cavail, Cstart, level):
	"""
	It returns True if there is still battery, False otherwise.
	:param dictionary prof_dict: The dictionary containing all the profiles
	:param float level: The level of the battery
	:return bool: True if there is still energy in the battery, False otherwise
	"""
	if Cavail <= min(prof_dict.keys())*Cstart:
		return False
	key, _ = getNextLevel(prof_dict, level)
	if profile_dict[key][0] == 'stop':
		return False
	return True
	
	
def compute_power(Xs, UtilSensors, Es, Pidle, cores):
	"""
	An helper method that compute the power (in Watt) of the current profile.
	:param float Xs: List of throughputs, one for each request class
	:param float UtilSensors: Utilization of sensors
	:param float Es: List of energies, one for each request class
	:param float Pidle: Idle power consumption of sensors
	:param int cores: Number of active sensors
	:return float: Sensor power (in Watt)
	"""
	Power_W = (1-UtilSensors) * Pidle * cores
	for X, E in zip(Xs, Es):
		Power_W += X*E
	return Power_W



if __name__ == '__main__':

	if len(sys.argv) != 2:
		print('Please, provide a file to save outputs. Exiting...')
		sys.exit(-1)
	output_file = sys.argv[1]



	Cavail_start = Cstart * ratio_avail_total
	Cbatt = Cstart
	Cavail = Cavail_start
	Es = [E1, E2]

	LD_TIMES = [Z1, Scam1, Scloud1]
	HD_TIMES = [Z2, Scam2, Scloud2]

	Rewards = [rho1, rho2]


	#profile_dict = profile_mix
	profile_dict = {}
	keys = sorted(list(profile_mix.keys()))
	for l in [n/100 for n in range(1,101)]:
		for k in keys:
			if l <= k:
				profile_dict[l] = profile_mix[k]
				break
			

	while stillAlive(profile_dict, Cavail, Cstart, Cavail/Cavail_start):
		Clevel, change_at = getNextLevel(profile_dict, Cavail/Cavail_start)
		profile = profile_dict[Clevel]
		Ns = [profile[0], profile[1]]
		cores = profile[2]
		
		############################################
		### Choose the System Performance Module ###
		############################################
		#Xs, UtilSensors, analTime = performance_module_mva(Ns, cores, LD_TIMES, HD_TIMES)
		Xs, UtilSensors, analTime = performance_module_amva(Ns, cores, LD_TIMES, HD_TIMES)
		############################################
		############################################
		############################################
		
		Power_W = compute_power(Xs, UtilSensors, Es, Pidle, cores)
			
		###########################################
		### Choose the Battery Depletion Module ###
		###########################################
		#L, Cbatt, Cavail, Cbound, ratio_avail_total = estimate_capacity_linear(Cavail, Power_W, change_at*Cavail_start)
		L, Cbatt, Cavail, Cbound, ratio_avail_total = estimate_capacity_kibam(Cbatt, Volt, ratio_avail_total, Power_W, UtilSensors, change_at*Cavail_start, k=kp, c=ratio_avail_total, Dt=1/3600)
		###########################################
		###########################################
		###########################################
		
		############################################
		### Choose the Reward Computation Module ###
		############################################
		#RewTot = compute_reward_simple(Xs, Rewards, L)
		RewTot = compute_reward_penalty(Ns, Xs, [Z1, Z2], Rewards, L, SLA)
		############################################
		############################################
		############################################
		
		outputString = ','.join([str(Ns[0]), str(Ns[1]), str(cores), str(Xs[0]), str(Xs[1]), str(UtilSensors), str(Power_W), str(Volt), str(L), str(RewTot), str(Cbatt), str(Cavail), str(Cbound), str(analTime)])
		with open(output_file, 'a') as f:
			f.write(outputString + '\n')
		
		if L <= 0:
			break

