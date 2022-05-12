################################
### Battery Depletion Module ###
################################
Cstart = 12.9 #Wh
ratio_avail_total = 0.5 # This is c (KiBaM)
kp = 10 # This is k' (KiBaM)
E1 = 0.0299  #Watt-Second (low-quality)
E2 = 0.1286 #Watt-Second (high-quality)
Pidle = 0.2254 #Watt
Volt = 3.8 #Volt




#################################
### System Performance Module ###
#################################
Z1 = 0.1 #Seconds (low-quality)
Z2 = 0.1 #Seconds (high-quality)
Scam1 = 0.085 #Seconds (low-quality)
Scam2 = 0.4 #Seconds (high-quality)
Scloud1 = 1.0 #Seconds (low-quality)
Scloud2 = 2.5 #Seconds (high-quality)




#################################
### Reward Computation Module ###
#################################
SLA = 2.0 #Seconds
rho1 = 1 #(low-quality)
rho2 = 5 #(high-quality)
