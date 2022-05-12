import subprocess


def performance_module_mva(Ns, cores, LD_TIMES, HD_TIMES):
	"""
	A method that call the performance module, i.e., the MVA algorithm (written in Octave)
	:param int Ns: Number of customers for each request class
	:param in cores: Number of active sensors
	:return list: List of throughputs, one for each request class
	:return float: Utilization of sensors
	:return float: Time for running the MVA
	"""
	mvaParams = ['octave', '-p', '~/Documents/queueing/inst/', 'mva_octave.m'] + [str(N) for N in Ns] + [str(cores)] + [str(s) for s in LD_TIMES] + [str(s) for s in HD_TIMES]
	mva = subprocess.Popen(mvaParams, stdout=subprocess.PIPE) #X1, X2, Uc, Time. Last character is '\n'
	performance = [float(x) for x in mva.stdout.read().decode("utf-8")[:-1].split(',')]
	Xs = performance[0:len(Ns)+1]
	return Xs, performance[2], performance[3]



def performance_module_amva(Ns, cores, LD_TIMES, HD_TIMES):
	"""
	A method that call the performance module, i.e., the MVA algorithm (written in Octave)
	:param int Ns: Number of customers for each request class
	:param in cores: Number of active sensors
	:return list: List of throughputs, one for each request class
	:return float: Utilization of sensors
	:return float: Time for running the MVA
	"""
	mvaParams = ['octave', '-p', '~/Documents/queueing/inst/', 'mvaApprox_octave.m'] + [str(N) for N in Ns] + [str(cores)] + [str(s) for s in LD_TIMES] + [str(s) for s in HD_TIMES]
	mva = subprocess.Popen(mvaParams, stdout=subprocess.PIPE) #X1, X2, Uc, Time. Last character is '\n'
	performance = [float(x) for x in mva.stdout.read().decode("utf-8")[:-1].split(',')]
	Xs = performance[0:len(Ns)+1]
	return Xs, performance[2], performance[3]
