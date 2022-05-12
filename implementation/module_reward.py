def compute_reward_simple(Xs, Rs, L):
	"""
	Simple function to compute the reward.
	:param list Xs: List of throughputs, one for each request class
	:param list Rs: List of rewards, one for each request class
	:param float L: Duration of the considered profile
	:return float: The obtained reward
	"""
	rewardPerSecond = 0.0
	for X, R in zip(Xs, Rs):
		rewardPerSecond += X*R
	return rewardPerSecond * L


	
	
def compute_reward_penalty(Ns, Xs, Zs, Rs, L, SLA):
	"""
	Function to compute the reward with penalty based on SLA (i.e., latency) violation.
	:param list Ns: List of number of customers, one for each request class
	:param list Xs: List of throughputs, one for each request class
	:param list Zs: List of think times, one for each request class
	:param list Rs: List of rewards, one for each request class
	:param float L: Duration of the considered profile
	:param float SLA: Service Level Agreement
	:return float: The obtained reward
	"""
	RTs = []
	for n, x, z in zip(Ns, Xs, Zs):
		if x > 0:
			RTs.append(n/x - z)
		else:
			RTs.append(-1.0)
	R0 = 0.0
	X0 = sum(Xs)
	for x, rt in zip(Xs, RTs):
		R0 += (x/X0) * rt
	rewardPerSecond = compute_reward_simple(Xs, Rs, L)
	perc = 0.0
	if R0 > SLA:
		perc = min((R0 - SLA) / SLA, 1.0)
	return rewardPerSecond * (1.0 - perc)
