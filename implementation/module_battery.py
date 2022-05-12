from battery_kibam import *
 
 
def estimate_capacity_kibam(Cbatt_Wh_init, Volt, perc_avail_init, Power_W, Util, Cbatt_Wh_final, k=10, c=0.2, Dt=0.01):
	Cbatt_init = Cbatt_Wh_init / Volt
	Cbatt_final = Cbatt_Wh_final / Volt
	Cbatt = Cbatt_init
	Cavail = Cbatt * perc_avail_init
	Cbound = Cbatt - Cavail
	I = Power_W / Volt
	ts_hr = 0.0
	while Cavail > Cbatt_final and Cavail > 0.01:
		Cavail, Cbound = capacity_step(Cavail, Cbound, k, c, Cbatt, I, Dt) #Remove charge from Available well
		#Cbatt = Cavail + Cbound
		#Cavail, Cbound = capacity_step(Cavail, Cbound, k, c, Cbatt, 0.0, Dt*(1-Util)) #Move charge from Bound to Available well
		Cbatt = Cavail + Cbound
		ts_hr += Dt
	return ts_hr*3600, Cbatt*Volt, Cavail*Volt, Cbound*Volt, Cavail/Cbatt
	
	
	
def estimate_capacity_linear(Cbatt_Wh_init, Power_W, Cbatt_Wh_final):
	ts_hr = (Cbatt_Wh_init - Cbatt_Wh_final) / Power_W
	return ts_hr*3600, Cbatt_Wh_final, Cbatt_Wh_final, 0.0, 1.0

