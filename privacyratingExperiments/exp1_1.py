import random
import math
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import string
import os
import pandas as pd
from datetime import datetime

#-------------------------------------------INPUTS-----------------------------------------------



experiment = "Exp1_1_"
iterations = 10			#number of iterations
N_buyer = 10000			#number of buyers
pri_ele = 6				#number of privacy elements in privacy practice
X_max = 10				#max number of transactions for each buyer
timespan = 10			#time period of all the transactions (0, timespan-1)
t = 10					#current time 
price_min_LCD = 10		# minimum price of low critical data
price_max_LCD = 500 	# maximum price of low critical data
price_min_HCD = 501 	#minimum price of low critical data
price_max_HCD = 1000 	#maximu price of high critical data
threshold_score = 2		#threshold for PRI 
DP = ["dp_u", "dp_p", "dp_f"]	#list of data-providers
input_likelihood = {"RSlowDSlowRISKvhigh": 0.9, "RSlowDShighRISKhigh": 0.7, "RShighDSlowRISKlow": 0.5, "RShighDShighRISKvlow": 0.3}

#####evaluate the price preference of each data-provider
dp_p_pref_price_wo_LCD = price_min_LCD + (50*(price_max_LCD-price_min_LCD)/100)
dp_p_pref_price_w_LCD = price_min_LCD + (10*(price_max_LCD-price_min_LCD)/100)
dp_p_pref_price_wo_HCD = price_min_HCD + (70*(price_max_HCD-price_min_HCD)/100)
dp_p_pref_price_w_HCD = price_min_HCD + (30*(price_max_HCD-price_min_HCD)/100)

dp_f_pref_price_wo_LCD = price_min_LCD + (60*(price_max_LCD-price_min_LCD)/100)
dp_f_pref_price_w_LCD = price_min_LCD + (20*(price_max_LCD-price_min_LCD)/100)
dp_f_pref_price_wo_HCD = price_min_HCD + (80*(price_max_HCD-price_min_HCD)/100)
dp_f_pref_price_w_HCD = price_min_HCD + (40*(price_max_HCD-price_min_HCD)/100)


#pref_dp_x = {'w': [], 'alpha': [], 'WoRate_LCD': [], 'WoRate_HCD': [], 'WRate_LCD': [], 'WRate_HCD': []}
#Rate = [PR, PR_pri, PR_pur, PR_lea, price]
#alpha = [current trade request, current possession, future acquistion]


##### preferences of providers
pref_dp_u = {'w': [1/3, 1/3, 1/3], 'alpha': [0.1, 0.7, 0.2], 'WoRate_LCD': [0, 0, 0, 0, 0], 'WoRate_HCD': [0, 0, 0, 0, 0], 'WRate_LCD': [0, 0, 0, 0, 0], 'WRate_HCD': [0, 0, 0, 0, 0]}

pref_dp_p = {'w': [1/3, 1/3, 1/3], 'alpha': [0.1, 0.7, 0.2], 'WoRate_LCD': [0, 0, 0, 0, dp_p_pref_price_wo_LCD], 'WoRate_HCD': [0, 0, 0, 0, dp_p_pref_price_wo_HCD], 'WRate_LCD': [0.5, 0, 0, 0, dp_p_pref_price_w_LCD], 'WRate_HCD': [0.5, 0, 0, 0, dp_p_pref_price_w_HCD]}

pref_dp_f = {'w': [1/3, 1/3, 1/3], 'alpha': [0.1, 0.7, 0.2], 'WoRate_LCD': [0, 0.6, 0, 0, dp_f_pref_price_wo_LCD], 'WoRate_HCD': [0, 0.8, 0, 0, dp_f_pref_price_wo_HCD], 'WRate_LCD': [0, 0.6, 0.6, 0.6, dp_f_pref_price_w_LCD], 'WRate_HCD': [0, 0.8, 0.8, 0.8, dp_f_pref_price_w_HCD]}

##+++++++++++++++++++storing inputs to record in excel+++++++++++++
inputs = [[iterations, DP, N_buyer, pri_ele, X_max, timespan, t, price_min_LCD, price_max_LCD, price_min_HCD, price_max_HCD, threshold_score, input_likelihood, pref_dp_u, pref_dp_p, pref_dp_f]]

parent_dir = "/home/pooja/simulation"
dateTimeObj = datetime.now()
timestampStr = experiment + dateTimeObj.strftime("%d%b%Y%H%M%S")
createdir = os.path.join(parent_dir, timestampStr)
os.mkdir(createdir)


def practiceRating(pri):										#function for evaluating practice profile
	Xp = sum(pri)
	return round(1/(1+math.exp(-Xp)),2)

#PRI = <A_int, A_age, A_per, samples, data_type, dimensions>

def purchaseRating(tr_LCD, tr_HCD, PRI_current, PRI_future):	#function for evaluating purchase profile
	
	PR = {'LCD': dict.fromkeys(DP, 0), 'HCD': dict.fromkeys(DP, 0)}
	
	#a_x = a1*trade request + a2 * current + a3 * future
	
	##dp_unconcerned
	a_int = (pref_dp_u['alpha'][0] * tr_LCD[0]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][0]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][0])
	a_age = (pref_dp_u['alpha'][0] * tr_LCD[1]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][1]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][1])
	a_per = (pref_dp_u['alpha'][0] * tr_LCD[2]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][2]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][2])
	a_sam = (pref_dp_u['alpha'][0] * tr_LCD[3]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][3]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][3])
	a_dim = (pref_dp_u['alpha'][0] * tr_LCD[5]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][5]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][5])
	PR['LCD']['dp_u'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	
	a_int = (pref_dp_u['alpha'][0] * tr_HCD[0]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][0]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][0])
	a_age = (pref_dp_u['alpha'][0] * tr_HCD[1]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][1]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][1])
	a_per = (pref_dp_u['alpha'][0] * tr_HCD[2]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][2]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][2])
	a_sam = (pref_dp_u['alpha'][0] * tr_HCD[3]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][3]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][3])
	a_dim = (pref_dp_u['alpha'][0] * tr_HCD[5]) + (pref_dp_u['alpha'][1] * PRI_current['dp_u'][5]) + (pref_dp_u['alpha'][2] * PRI_future['dp_u'][5])
	PR['HCD']['dp_u'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	
	
	##dp_pragmatist
	
	a_int = (pref_dp_p['alpha'][0] * tr_LCD[0]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][0]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][0])
	a_age = (pref_dp_p['alpha'][0] * tr_LCD[1]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][1]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][1])
	a_per = (pref_dp_p['alpha'][0] * tr_LCD[2]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][2]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][2])
	a_sam = (pref_dp_p['alpha'][0] * tr_LCD[3]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][3]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][3])
	a_dim = (pref_dp_p['alpha'][0] * tr_LCD[5]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][5]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][5])
	PR['LCD']['dp_p'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	
	a_int = (pref_dp_p['alpha'][0] * tr_HCD[0]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][0]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][0])
	a_age = (pref_dp_p['alpha'][0] * tr_HCD[1]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][1]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][1])
	a_per = (pref_dp_p['alpha'][0] * tr_HCD[2]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][2]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][2])
	a_sam = (pref_dp_p['alpha'][0] * tr_HCD[3]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][3]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][3])
	a_dim = (pref_dp_p['alpha'][0] * tr_HCD[5]) + (pref_dp_p['alpha'][1] * PRI_current['dp_p'][5]) + (pref_dp_p['alpha'][2] * PRI_future['dp_p'][5])
	PR['HCD']['dp_p'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	
	##dp_fundamentalist

	a_int = (pref_dp_f['alpha'][0] * tr_LCD[0]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][0]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][0])
	a_age = (pref_dp_f['alpha'][0] * tr_LCD[1]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][1]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][1])
	a_per = (pref_dp_f['alpha'][0] * tr_LCD[2]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][2]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][2])
	a_sam = (pref_dp_f['alpha'][0] * tr_LCD[3]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][3]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][3])
	a_dim = (pref_dp_f['alpha'][0] * tr_LCD[5]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][5]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][5])
	PR['LCD']['dp_f'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	a_int = (pref_dp_f['alpha'][0] * tr_HCD[0]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][0]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][0])
	a_age = (pref_dp_f['alpha'][0] * tr_HCD[1]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][1]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][1])
	a_per = (pref_dp_f['alpha'][0] * tr_HCD[2]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][2]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][2])
	a_sam = (pref_dp_f['alpha'][0] * tr_HCD[3]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][3]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][3])
	a_dim = (pref_dp_f['alpha'][0] * tr_HCD[5]) + (pref_dp_f['alpha'][1] * PRI_current['dp_f'][5]) + (pref_dp_f['alpha'][2] * PRI_future['dp_f'][5])
	PR['HCD']['dp_f'] = PRI_rules(a_age, a_per, a_int, a_sam, a_dim)
	
	return PR


##rules for PRI		
def PRI_rules(a_age, a_per, a_int, a_sam, a_dim):

	PRI = ' '
	if a_sam > threshold_score and a_age > threshold_score and a_per <= threshold_score and a_int <= threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age > threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'High'
	if a_sam > threshold_score and a_age >threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age >threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'High'
	if a_sam > threshold_score and a_age >threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age >threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'High'
	if a_sam > threshold_score and a_age >threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'High'
	if a_sam > threshold_score and a_age >threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'Very High'
	if a_sam > threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Low'	
	if a_sam > threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam > threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Average'		
	if a_sam > threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Average'	
	if a_sam > threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'High'

	if a_sam <= threshold_score and a_age > threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age >threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Average'
	if a_sam <= threshold_score and a_age >threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age >threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'Average'
	if a_sam <= threshold_score and a_age >threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age >threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Average'
	if a_sam <= threshold_score and a_age >threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Average'
	if a_sam <= threshold_score and a_age >threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'High'
	if a_sam <= threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Very Low'	
	if a_sam <= threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age <=threshold_score and a_per <=threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim < threshold_score:
		PRI = 'Low'
	if a_sam <= threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int <=threshold_score and a_dim >= threshold_score:
		PRI = 'Low'		
	if a_sam <= threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim < threshold_score:
		PRI = 'Low'	
	if a_sam <= threshold_score and a_age <=threshold_score and a_per >threshold_score and a_int >threshold_score and a_dim >= threshold_score:
		PRI = 'High'		
	
	if PRI == 'Very High':
		return 0.05
	if PRI == 'High':
		return 0.25
	if PRI == 'Average':
		return 0.5
	if PRI == 'Low':
		return 0.75
	if PRI == 'Very Low':
		return 0.9
	else:
		return 999
		
#tran = [timestamp, provider, A_int, A_age, A_per, samples, data_type, dimensions]
#PRI = [A_int, A_age, A_per, samples, data_type, dimensions]

def calcPRI_current(tran):			#function for calculating risk impact due to current possession
	
	dp_u_tran=[]
	dp_p_tran=[]
	dp_f_tran=[]
	
	for ele in tran["temporal"]:
		if ele[1] == DP[0]:
			dp_u_tran.append(ele)
		if ele[1] == DP[1]:
			dp_p_tran.append(ele)
		if ele[1] == DP[2]:
			dp_f_tran.append(ele)
	
	PRI = [0,0,0,0,0,0]
	if len(dp_u_tran)!= 0:
		for ele in dp_u_tran:
			PRI[0]+= ele[2] * math.exp(-(t-ele[0])/t)
			PRI[1]+= ele[3] * math.exp(-(t-ele[0])/t)
			PRI[2]+= ele[4] * math.exp(-(t-ele[0])/t)
		PRI_dp_u = [round(PRI[0]/(len(dp_u_tran)),2), round(PRI[1]/(len(dp_u_tran)),2), round(PRI[2]/(len(dp_u_tran)),2), tran["non_temp"]['dp_u'][0], tran["non_temp"]['dp_u'][1], tran["non_temp"]['dp_u'][2]]
	else:
		PRI_dp_u = PRI

	PRI = [0,0,0,0,0,0]
	if len(dp_p_tran) != 0:
		for ele in dp_p_tran:
			PRI[0]+= ele[2] * math.exp(-(t-ele[0])/t)
			PRI[1]+= ele[3] * math.exp(-(t-ele[0])/t)
			PRI[2]+= ele[4] * math.exp(-(t-ele[0])/t)
		PRI_dp_p = [round(PRI[0]/(len(dp_p_tran)),2), round(PRI[1]/(len(dp_p_tran)),2), round(PRI[2]/(len(dp_p_tran)),2), tran["non_temp"]['dp_p'][0], tran["non_temp"]['dp_p'][1], tran["non_temp"]['dp_p'][2]]
	else:
		PRI_dp_p = PRI

	
	PRI = [0,0,0,0,0,0]

	if len(dp_f_tran) != 0:
		for ele in dp_f_tran:
			PRI[0]+= ele[2] * math.exp(-(t-ele[0])/t)
			PRI[1]+= ele[3] * math.exp(-(t-ele[0])/t)
			PRI[2]+= ele[4] * math.exp(-(t-ele[0])/t)
		PRI_dp_f = [round(PRI[0]/(len(dp_f_tran)),2), round(PRI[1]/(len(dp_f_tran)),2), round(PRI[2]/(len(dp_f_tran)),2), tran["non_temp"]['dp_f'][0], tran["non_temp"]['dp_f'][1], tran["non_temp"]['dp_f'][2]]
	else:
		PRI_dp_f = PRI


	return ({"dp_u": PRI_dp_u, "dp_p": PRI_dp_p, "dp_f": PRI_dp_f})

def calcPRI_future(i, PRI):    #function for calculating risk impact due to future acquisition from other buyers
	
	PRI_future = []
	
	count_u = 0
	count_p = 0
	count_f = 0
	
	PRI_u = [0,0,0,0,0,0]
	PRI_p = [0,0,0,0,0,0]
	PRI_f = [0,0,0,0,0,0]
	
	for j in range(0,N_buyer):
		if i!=j:
			if sum(PRI[j]["dp_u"])!=0:
				PRI_u[0]+= PRI[j]["dp_u"][0]
				PRI_u[1]+= PRI[j]["dp_u"][1]
				PRI_u[2]+= PRI[j]["dp_u"][2]
				PRI_u[3]+= PRI[j]["dp_u"][3]
				PRI_u[4]+= PRI[j]["dp_u"][4]
				PRI_u[5]+= PRI[j]["dp_u"][5]
				count_u+= 1
			if sum(PRI[j]["dp_p"])!=0:
				PRI_p[0]+= PRI[j]["dp_p"][0]
				PRI_p[1]+= PRI[j]["dp_p"][1]
				PRI_p[2]+= PRI[j]["dp_p"][2]
				PRI_p[3]+= PRI[j]["dp_p"][3]
				PRI_p[4]+= PRI[j]["dp_p"][4]
				PRI_p[5]+= PRI[j]["dp_p"][5]
				count_p+= 1
			if sum(PRI[j]["dp_f"])!=0:
				PRI_f[0]+= PRI[j]["dp_f"][0]
				PRI_f[1]+= PRI[j]["dp_f"][1]
				PRI_f[2]+= PRI[j]["dp_f"][2]
				PRI_f[3]+= PRI[j]["dp_f"][3]
				PRI_f[4]+= PRI[j]["dp_f"][4]
				PRI_f[5]+= PRI[j]["dp_f"][5]
				count_f+= 1
	
	if count_u!=0:
		PRI_u[0]= round(PRI_u[0]/count_u,2)
		PRI_u[1]= round(PRI_u[1]/count_u,2)
		PRI_u[2]= round(PRI_u[2]/count_u,2)
		PRI_u[3]= round(PRI_u[3]/count_u,2)
		PRI_u[4]= round(PRI_u[4]/count_u,2)
		PRI_u[5]= round(PRI_u[5]/count_u,2)
	
	if count_p!=0:
		PRI_p[0]= round(PRI_p[0]/count_p,2)
		PRI_p[1]= round(PRI_p[1]/count_p,2)
		PRI_p[2]= round(PRI_p[2]/count_p,2)
		PRI_p[3]= round(PRI_p[3]/count_p,2)
		PRI_p[4]= round(PRI_p[4]/count_p,2)
		PRI_p[5]= round(PRI_p[5]/count_p,2)
	
	if count_f!=0:
		PRI_f[0]= round(PRI_f[0]/count_f,2)
		PRI_f[1]= round(PRI_f[1]/count_f,2)
		PRI_f[2]= round(PRI_f[2]/count_f,2)
		PRI_f[3]= round(PRI_f[3]/count_f,2)
		PRI_f[4]= round(PRI_f[4]/count_f,2)
		PRI_f[5]= round(PRI_f[5]/count_f,2)

	return ({"dp_u": PRI_u, "dp_p": PRI_p, "dp_f": PRI_f})
		
#leak = [RS, DS, senstivity, volume, agreements, providers]
def leakageRating(leak):



	if leak[0] <= 0.5 and leak[1] <= 0:
		likelihood = input_likelihood["RSlowDSlowRISKvhigh"]
	elif leak[0] <= 0.5 and leak[1] > 0:
		likelihood = input_likelihood["RSlowDShighRISKhigh"]
	elif leak[0] > 0.5 and leak[1] <= 0:
		likelihood = input_likelihood["RShighDSlowRISKlow"]
	elif leak[0] > 0.5 and leak[1] > 0:
		likelihood = input_likelihood["RShighDShighRISKvlow"]
	
	w1 = 0.25
	w2 = 0.25
	w3 = 0.25
	w4 = 0.25
	
	I = w1*leak[2] + w2*leak[3] + w3*leak[4] + w4*leak[5]
	
	R = I*likelihood

	return (likelihood, round((2/(1+math.exp(R))),2))
	

def selectandmatch(_PR, _pref):
	#print(_PR, _pref)
	if _PR[0] >= _pref[0] and _PR[1] >= _pref[1] and _PR[2] >= _pref[2] and _PR[3] >= _pref[3] and _PR[4] >= _pref[4]:
		#print(1)
		return 1
	else:
		#print(0)
		return 0

fonts = 10
	
def plotResult_buyer(xList, y1List, y2List, r1List, r2List, plottitle):
	plt.figure()
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.title(plottitle, fontsize=fonts)
	plt.xlabel('Buyer\'s Rating', fontsize=fonts)
	plt.ylabel('Criticality of requested data', fontsize=fonts)
	plt.scatter(xList, y1List, s=r1List, facecolors='none', edgecolors='b')
	plt.scatter(xList, y2List, s=r2List, facecolors='none', edgecolors='b')
	plottitle_wo_space = plottitle.replace(" ", "")
	_filename = createdir+"/"+plottitle_wo_space+str(iter)+".png"
	plt.savefig(_filename)
	plt.close()
	
	
def plotResult_provider(pointList, plottitle, leakList, leakplottitle, PR_LCD=0, PR_HCD=0):
	
	plt.figure()
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.title(plottitle, fontsize=fonts)
	plt.xlabel('Buyer\'s Rating', fontsize=fonts)
	plt.ylabel('Criticality of requested data', fontsize=fonts)
	plt.scatter(pointList[0], pointList[1], s=pointList[2], facecolors='none', edgecolors='b')
	plottitle_wo_space = plottitle.replace(" ", "")
	_filename = createdir+"/"+plottitle_wo_space+str(iter)+".png"
	plt.savefig(_filename)
	plt.close()
	plt.figure()
	plt.xlim(0,1)
	plt.ylim(0,1)
	plt.title(leakplottitle, fontsize=fonts)
	plt.xlabel('Buyer\'s Rating', fontsize=fonts)
	plt.ylabel('Criticality of requested data', fontsize=fonts)
	plt.scatter(pointList[0], pointList[1], s=pointList[2], facecolors='none', edgecolors='b', label='Selected requests')
	plt.scatter(leakList[0], leakList[1], s=leakList[2], facecolors='none', edgecolors='r', label='Affected requests')
	plt.legend(frameon=False, loc='lower center', ncol=2)
	leakplot_title_wo_space = leakplottitle.replace(" ", "")
	_filename = createdir+"/"+leakplot_title_wo_space+str(iter)+".png"
	plt.savefig(_filename)
	plt.close()

#final result summarization - used to store result in excel
result_dp_u = []
result_dp_p = []
result_dp_f = []
dataframe_buyer = []



  
#buyerprofile = ["ID": <>, "practice": <>, "purchase": {"temp": <>, "non_temp": <>}, "leakage": <>, "traderequest_LCD": <>, "traderequest_HCD": <>, "PRV": {'PR_pri': <>, 'PR_pur': {'LCD': <dp_u, dp_p, dp_f>, 'HCD': <dp_u, dp_p, dp_f>}, 'PR_lea': <>}, "PRI_current": {'dp_u': <>, 'dp_p': <>, 'dp_f': <>}, "PRI_future": {'dp_u': <>, 'dp_p': <>, 'dp_f': <>}]

#buyerprofile["practice"] = <PU, V, R, G, DS, CO>
#buyerprofile["purchase"] = <X, list of trade transactions <timestamp, provider, A_int, A_age, A_per, samples, dim, div>>
#buyerprofile["leakage"] = [RS, DS, senstivity, volume, agreements, provider]


for iter in range(0,iterations):
	print ("iteration: ", iter)
	buyerprofile = [dict() for x in range(N_buyer)]			#buyer's sample space
	
	print ("Generate sample space")
	#--------------------------------Generate sample space of data-buyers in the marketplace----------------------------
	for x in range(0,N_buyer):
		
		buyerprofile[x]["ID"] = x+1
		
		######generate privacy practice profile
		pri = list(np.random.randint(-1,2,size=6))			
		buyerprofile[x]["practice"] = pri
	
		#++++++++++generate purchase profile++++++++++++
		
		##temp = <timestamp, provider, A_int, A_age, A_per>
		##non_temp = {"dp_u": [samples, data_type, dimensions]}
		
		#generate temporal elements of historical trades
		X = random.randint(1, X_max) #number of purchases for each buyer
		tran = [[ random.randint(0,timespan-1), random.choice(DP)] + list(np.random.randint(1,4, size=3)) for i in range(0,X)]
		
		#generate non-temporal elements of historical trades++++++
		_dp = 0  ### used to count the number of providers with whom buyer has interacted in past
		non_tran={}
		if any('dp_u' in ele for ele in tran):
			non_tran["dp_u"] = list(np.random.randint(1,4, size=3))
			_dp += 1
		else:
			non_tran["dp_u"] = [0,0,0]
		if any('dp_p' in ele for ele in tran):
			non_tran["dp_p"] = list(np.random.randint(1,4, size=3))
			_dp += 1
		else:
			non_tran["dp_p"] = [0,0,0]
		if any('dp_f' in ele for ele in tran):
			non_tran["dp_f"] = list(np.random.randint(1,4, size=3))
			_dp += 1
		else:
			non_tran["dp_f"] = [0,0,0]
	
		buyerprofile[x]["purchases"] = {'temporal': tran, 'non_temp': non_tran}
		
		#+++++++++++++generate leakage profile++++++++++++++
		RS = round(random.uniform(0, 1),2)					##generate reputation score
		DS = pri[-2]										
		senstivity = round(sum([sum(ele[2:5]) for ele in tran])/(3*len(tran)),2)
		volume = round((buyerprofile[x]["purchases"]["non_temp"]["dp_u"][0]+buyerprofile[x]["purchases"]["non_temp"]["dp_p"][0]+buyerprofile[x]["purchases"]["non_temp"]["dp_f"][0])/3, 2)
		
		if X <= X_max/3:
			agreements = 1
		if X > X_max/3 and X <= 2*X_max/3:
			agreements = 2
		if X > 2*X_max/3:
			agreements = 3
			
		providers = _dp
		buyerprofile[x]["leakage"] = [RS, DS, senstivity, volume, agreements, providers]
		
		#+++++++++++++generate current trade requests+++++++++++
		#traderequest = <A_int, A_age, A_per, samples, data_type, dimensions, price>
		
		delta = round((price_max_LCD - price_min_LCD+1)/3)
		
		tr_LCD = list(np.random.randint(1,3, size=6))
		
		if tr_LCD[3] == 1:
			tr_LCD.append(random.randint(price_min_LCD, price_min_LCD+delta))
		elif tr_LCD[3] == 2:
			tr_LCD.append(random.randint(price_min_LCD+delta, price_min_LCD+(2*delta)+1))
		elif tr_LCD[3] == 3:
			tr_LCD.append(random.randint(price_min_LCD+2*delta, price_max_LCD))
			
		
		delta = round((price_max_HCD - price_min_HCD+1)/3)
		
		tr_HCD = list(np.random.randint(2,4, size=6))
		
		if tr_HCD[3] == 1:
			tr_HCD.append(random.randint(price_min_HCD, price_min_HCD+delta))
		elif tr_HCD[3] == 2:
			tr_HCD.append(random.randint(price_min_HCD+delta, price_min_HCD+(2*delta)+1))
		elif tr_HCD[3] == 3:
			tr_HCD.append(random.randint(price_min_HCD+2*delta, price_max_HCD))
			
		
		buyerprofile[x]["traderequest_LCD"] = tr_LCD
		buyerprofile[x]["traderequest_HCD"] = tr_HCD
		
		#+++++++++++++initialize PRV of data-buyer+++++++++++
		buyerprofile[x]["PRV"] = {'PR_pri': 0, 'PR_pur': {}, 'PR_lea': 0}
		
		#+++++++++++++initialize which provider has accepted data-buyer's trade requests+++++++++++
		buyerprofile[x]['accepted'] = {"without": {"LCD": {"dp_u": 999, "dp_p": 999, "dp_f": 999}, "HCD": {"dp_u": 999, "dp_p": 999, "dp_f": 999}}, "with": {"LCD": {"dp_u": 999, "dp_p": 999, "dp_f": 999}, "HCD": {"dp_u": 999, "dp_p": 999, "dp_f": 999}}}
		
		#+++++++++++++define leakage event for data-buyer+++++++++++
		buyerprofile[x]['Pro_leak'] = [random.uniform(0, 1)]
		
		
	print ("calculate current PRI")
	#-------------------------------calculate current PRI based on current accumulation=-------------------------
	PRI_list = []
	for i in range(0,N_buyer):
		buyerprofile[i]['PRI_current'] = calcPRI_current(buyerprofile[i]['purchases'])
		PRI_list.append(buyerprofile[i]['PRI_current'])
	
	print ("calculate future PRI")
	#--------------------------calculate future PRI based on future acquisition from other buyers--------------
	for i in range(0,N_buyer):
		buyerprofile[i]['PRI_future'] = calcPRI_future(i, PRI_list)
	
	print ("calculate ratings for buyer")
	#------------------calculate ratings for buyer based on his profile--------------------------------------
	for ele in buyerprofile:
		PR_pri = practiceRating(ele['practice'])
		PR_pur = purchaseRating(ele['traderequest_LCD'], ele['traderequest_HCD'], ele['PRI_current'], ele['PRI_future'])
		likelihood, PR_lea = leakageRating(ele['leakage'])
		
		ele["PRV"]['PR_pri'] = PR_pri
		ele["PRV"]['PR_pur'] = PR_pur
		ele["PRV"]['PR_lea'] = PR_lea
		ele['Pro_leak'].append(likelihood)
		
	print ("-Apply filteration")
	#----------------------Apply filteration based on data-providers preferences--------------------------------
	for _buyer in buyerprofile:
		
		#++++++++++++++++++++++dp_unconcerned ++++++++++++++
		PR_LCD = round((pref_dp_u['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_u['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_u']) + (pref_dp_u['w'][2]* _buyer['PRV']['PR_lea']),2)
		PR_HCD = round((pref_dp_u['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_u['w'][1]* _buyer["PRV"]['PR_pur']['HCD']['dp_u']) + (pref_dp_u['w'][2]* _buyer['PRV']['PR_lea']),2)
		
		##withoutRatingLCD
		 	
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_u'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_u['WoRate_LCD']	
		_buyer['accepted']['without']['LCD']['dp_u'] = selectandmatch(buyer_PR, provider_pref)
		
		##withoutRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_u'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_u['WoRate_HCD']	
		_buyer['accepted']['without']['HCD']['dp_u'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingLCD
		
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_u'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_u['WRate_LCD']	
		_buyer['accepted']['with']['LCD']['dp_u'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_u'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_u['WRate_HCD']	
		_buyer['accepted']['with']['HCD']['dp_u'] = selectandmatch(buyer_PR, provider_pref)
	
	
		#+++++++++++++++++++++++dp_pragmatist++++++++++++++++++
		
		PR_LCD = round((pref_dp_p['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_p['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_p']) + (pref_dp_p['w'][2]* _buyer['PRV']['PR_lea']),2)
		PR_HCD = round((pref_dp_p['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_p['w'][1]* _buyer["PRV"]['PR_pur']['HCD']['dp_p']) + (pref_dp_p['w'][2]* _buyer['PRV']['PR_lea']),2)
	
		
		##withoutRatingLCD
		 	
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_p'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_p['WoRate_LCD']	
		_buyer['accepted']['without']['LCD']['dp_p'] = selectandmatch(buyer_PR, provider_pref)
		
		##withoutRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_p'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_p['WoRate_HCD']	
		_buyer['accepted']['without']['HCD']['dp_p'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingLCD
		
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_p'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_p['WRate_LCD']	
		_buyer['accepted']['with']['LCD']['dp_p'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_p'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_p['WRate_HCD']	
		_buyer['accepted']['with']['HCD']['dp_p'] = selectandmatch(buyer_PR, provider_pref)
		
		
		#++++++++++++++++++++dp_fundamentalist+++++++++++++++++++++++
		
		PR_LCD = round((pref_dp_f['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_f['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_f']) + (pref_dp_f['w'][2]* _buyer['PRV']['PR_lea']),2)
		PR_HCD = round((pref_dp_f['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_f['w'][1]* _buyer["PRV"]['PR_pur']['HCD']['dp_f']) + (pref_dp_f['w'][2]* _buyer['PRV']['PR_lea']),2)
		
		##withoutRatingLCD
		 	
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_f'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_f['WoRate_LCD']	
		_buyer['accepted']['without']['LCD']['dp_f'] = selectandmatch(buyer_PR, provider_pref)
		
		##withoutRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_f'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_f['WoRate_HCD']	
		_buyer['accepted']['without']['HCD']['dp_f'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingLCD
		
		buyer_PR = [PR_LCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['LCD']['dp_f'], _buyer['PRV']['PR_lea'], _buyer["traderequest_LCD"][6]]
		provider_pref = pref_dp_f['WRate_LCD']	
		_buyer['accepted']['with']['LCD']['dp_f'] = selectandmatch(buyer_PR, provider_pref)
			
		##withRatingHCD
		
		buyer_PR = [PR_HCD, _buyer["PRV"]['PR_pri'], _buyer["PRV"]['PR_pur']['HCD']['dp_f'], _buyer['PRV']['PR_lea'], _buyer["traderequest_HCD"][6]]
		provider_pref = pref_dp_f['WRate_HCD']	
		_buyer['accepted']['with']['HCD']['dp_f'] = selectandmatch(buyer_PR, provider_pref)
	
	
	
	#---------------------------------------create results--------------------------------
	
	###results initializations
	dp_u_without_LCD_tr = 0
	dp_u_without_HCD_tr = 0
	dp_u_with_LCD_tr = 0
	dp_u_with_HCD_tr = 0
	
	dp_u_without_LCD_reve = 0 
	dp_u_without_HCD_reve = 0 
	dp_u_with_LCD_reve = 0 
	dp_u_with_HCD_reve = 0 
	
	dp_u_without_LCD_leak = 0 
	dp_u_without_HCD_leak = 0 
	dp_u_with_LCD_leak = 0 
	dp_u_with_HCD_leak = 0 
	
	
	dp_p_without_LCD_tr = 0
	dp_p_without_HCD_tr = 0
	dp_p_with_LCD_tr = 0
	dp_p_with_HCD_tr = 0
	
	dp_p_without_LCD_reve = 0 
	dp_p_without_HCD_reve = 0 
	dp_p_with_LCD_reve = 0 
	dp_p_with_HCD_reve = 0 
	
	dp_p_without_LCD_leak = 0 
	dp_p_without_HCD_leak = 0 
	dp_p_with_LCD_leak = 0 
	dp_p_with_HCD_leak = 0 
	
	dp_f_without_LCD_tr = 0
	dp_f_without_HCD_tr = 0
	dp_f_with_LCD_tr = 0
	dp_f_with_HCD_tr = 0
	
	dp_f_without_LCD_reve = 0 
	dp_f_without_HCD_reve = 0 
	dp_f_with_LCD_reve = 0 
	dp_f_with_HCD_reve = 0 
	
	dp_f_without_LCD_leak = 0 
	dp_f_without_HCD_leak = 0 
	dp_f_with_LCD_leak = 0 
	dp_f_with_HCD_leak = 0 
	
	
	####create the list of buyer's indices whose trade requests are accepted
	dp_u_wo_LCD_List =[]
	dp_u_wo_HCD_List =[]
	dp_u_w_LCD_List =[]
	dp_u_w_HCD_List =[]
	
	
	dp_p_wo_LCD_List =[]
	dp_p_wo_HCD_List =[]
	dp_p_w_LCD_List =[]
	dp_p_w_HCD_List =[]
	
	
	dp_f_wo_LCD_List =[]
	dp_f_wo_HCD_List =[]
	dp_f_w_LCD_List =[]
	dp_f_w_HCD_List =[]
	

	
	
	###variables for plotting accepted trade requests by each data-provider
	dp_u_wo_List =[[], [], []]
	dp_p_wo_List =[[], [], []]
	dp_f_wo_List =[[], [], []]
	dp_u_w_List =[[], [], []]
	dp_p_w_List =[[], [], []]
	dp_f_w_List =[[], [], []]
	
	###variables for recording points of leak of each data-provider
	dp_u_wo_leak = [[],[],[]]
	dp_u_w_leak = [[],[],[]]
	dp_p_wo_leak = [[],[],[]]
	dp_p_w_leak = [[],[],[]]
	dp_f_wo_leak = [[],[],[]]
	dp_f_w_leak = [[],[],[]]
	
	###variables for plotting buyer's sample space corrsponding to each data-providers [PR, critical, price]
	ratingList_dp_u = []
	ratingList_dp_p = []
	ratingList_dp_f = []
	LCDList = []
	HCDList = []
	priceLCD = []
	priceHCD = []
	
	
	print("Evaluate results")
	#--------------------------------------evaluating results----------------------------------------
	
	####count the accepted trade requests for each buyer, revenue generated
	
	count=0  ###index for buyers
	for ele in buyerprofile:
		
		#++++++++++++++++++++++dp_unconcerned+++++++++++++++++++++
				

		##withoutRatingLCD
		if ele['accepted']['without']['LCD']['dp_u'] == 1:
			dp_u_without_LCD_tr +=1
			dp_u_without_LCD_reve += ele["traderequest_LCD"][6]
			dp_u_wo_LCD_List.append(count)
		##withoutRatingHCD
		if ele['accepted']['without']['HCD']['dp_u'] == 1:
			dp_u_without_HCD_tr +=1
			dp_u_without_HCD_reve += ele["traderequest_HCD"][6]		
			dp_u_wo_HCD_List.append(count)
		##withRatingLCD
		if ele['accepted']['with']['LCD']['dp_u'] == 1:
			dp_u_with_LCD_tr +=1
			dp_u_with_LCD_reve += ele["traderequest_LCD"][6]
			dp_u_w_LCD_List.append(count)
		##withRatingHCD
		if ele['accepted']['with']['HCD']['dp_u'] == 1:
			dp_u_with_HCD_tr +=1
			dp_u_with_HCD_reve += ele["traderequest_HCD"][6]	
			dp_u_w_HCD_List.append(count)
		
		#+++++++++++++++++++++++++++dp_pragmatist++++++++++++++++++++++++++++++
				
		
		##withoutRatingLCD
		if ele['accepted']['without']['LCD']['dp_p'] == 1:
			dp_p_without_LCD_tr +=1
			dp_p_without_LCD_reve += ele["traderequest_LCD"][6]
			dp_p_wo_LCD_List.append(count)
		##withoutRatingHCD
		if ele['accepted']['without']['HCD']['dp_p'] == 1:
			dp_p_without_HCD_tr +=1
			dp_p_without_HCD_reve += ele["traderequest_HCD"][6]		
			dp_p_wo_HCD_List.append(count)
		##withRatingLCD
		if ele['accepted']['with']['LCD']['dp_p'] == 1:
			dp_p_with_LCD_tr +=1
			dp_p_with_LCD_reve += ele["traderequest_LCD"][6]
			dp_p_w_LCD_List.append(count)
		##withRatingHCD
		if ele['accepted']['with']['HCD']['dp_p'] == 1:
			dp_p_with_HCD_tr +=1
			dp_p_with_HCD_reve += ele["traderequest_HCD"][6]
			dp_p_w_HCD_List.append(count)
	
		#+++++++++++++++++dp_fundamentialist+++++++++++++++++++++++++++++++++++
	
		##withoutRatingLCD
		if ele['accepted']['without']['LCD']['dp_f'] == 1:
			dp_f_without_LCD_tr +=1
			dp_f_without_LCD_reve += ele["traderequest_LCD"][6]
			dp_f_wo_LCD_List.append(count)
			
		##withoutRatingHCD
		if ele['accepted']['without']['HCD']['dp_f'] == 1:
			dp_f_without_HCD_tr +=1
			dp_f_without_HCD_reve += ele["traderequest_HCD"][6]		
			dp_f_wo_HCD_List.append(count)
			
		##withRatingLCD
		if ele['accepted']['with']['LCD']['dp_f'] == 1:
			dp_f_with_LCD_tr +=1
			dp_f_with_LCD_reve += ele["traderequest_LCD"][6]
			dp_f_w_LCD_List.append(count)
			
		##withRatingHCD
		if ele['accepted']['with']['HCD']['dp_f'] == 1:
			dp_f_with_HCD_tr +=1
			dp_f_with_HCD_reve += ele["traderequest_HCD"][6]
			dp_f_w_HCD_List.append(count)
			
		count+=1
	
	
	
	#-------------------------------------making co-ordinated to plot on graphs and calculating leaks----------------------
	count=0
	for _buyer in buyerprofile:
		PR_u = round((pref_dp_u['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_u['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_u']) + (pref_dp_u['w'][2]* _buyer['PRV']['PR_lea']),2)
		PR_p = round((pref_dp_p['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_p['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_p']) + (pref_dp_p['w'][2]* _buyer['PRV']['PR_lea']),2)
		PR_f = round((pref_dp_f['w'][0]* _buyer["PRV"]['PR_pri']) + (pref_dp_f['w'][1]* _buyer["PRV"]['PR_pur']['LCD']['dp_f']) + (pref_dp_f['w'][2]* _buyer['PRV']['PR_lea']),2)
		
		
		
		LCD_critical = round(sum(_buyer['traderequest_LCD'][:-1])/18,2)
		LCD_price = _buyer['traderequest_LCD'][-1]/10
		HCD_critical = round(sum(_buyer['traderequest_HCD'][:-1])/18,2)
		HCD_price = _buyer['traderequest_HCD'][-1]/10
		
		#++++++++++++lists for generating buyer sample space plot+++++++++++++++++++++++
		ratingList_dp_u.append(PR_u)
		ratingList_dp_p.append(PR_p)
		ratingList_dp_f.append(PR_f)
		LCDList.append(LCD_critical)
		priceLCD.append(LCD_price)
		HCDList.append(HCD_critical)
		priceHCD.append(HCD_price)
		
		
		#++++++++++lists for generating accepted buyer's trade requests for unconcerned++++++++++++++++++
		
		#without LCD
		if count in dp_u_wo_LCD_List:
			dp_u_wo_List[0].append(PR_u)
			dp_u_wo_List[1].append(LCD_critical)
			dp_u_wo_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_u_wo_leak[0].append(PR_u)
				dp_u_wo_leak[1].append(LCD_critical)
				dp_u_wo_leak[2].append(LCD_price)
				dp_u_without_LCD_leak+=1
		#without HCD
		if count in dp_u_wo_HCD_List:
			dp_u_wo_List[0].append(PR_u)
			dp_u_wo_List[1].append(HCD_critical)
			dp_u_wo_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_u_wo_leak[0].append(PR_u)
				dp_u_wo_leak[1].append(HCD_critical)
				dp_u_wo_leak[2].append(HCD_price)
				dp_u_without_HCD_leak+=1
		#with LCD
		if count in dp_u_w_LCD_List:
			dp_u_w_List[0].append(PR_u)
			dp_u_w_List[1].append(LCD_critical)
			dp_u_w_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_u_w_leak[0].append(PR_u)
				dp_u_w_leak[1].append(LCD_critical)
				dp_u_w_leak[2].append(LCD_price)
				dp_u_with_LCD_leak+=1
		#with HCD
		if count in dp_u_w_HCD_List:
			dp_u_w_List[0].append(PR_u)
			dp_u_w_List[1].append(HCD_critical)
			dp_u_w_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_u_w_leak[0].append(PR_u)
				dp_u_w_leak[1].append(HCD_critical)
				dp_u_w_leak[2].append(HCD_price)
				dp_u_with_HCD_leak+=1
	
		#++++++++++lists for generating accepted buyer's trade requests for pragmatist++++++++++++++++++
		
		#without LCD
		if count in dp_p_wo_LCD_List:
			dp_p_wo_List[0].append(PR_p)
			dp_p_wo_List[1].append(LCD_critical)
			dp_p_wo_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_p_wo_leak[0].append(PR_p)
				dp_p_wo_leak[1].append(LCD_critical)
				dp_p_wo_leak[2].append(LCD_price)
				dp_p_without_LCD_leak+=1
		#without HCD
		if count in dp_p_wo_HCD_List:
			dp_p_wo_List[0].append(PR_p)
			dp_p_wo_List[1].append(HCD_critical)
			dp_p_wo_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_p_wo_leak[0].append(PR_p)
				dp_p_wo_leak[1].append(HCD_critical)
				dp_p_wo_leak[2].append(HCD_price)
				dp_p_without_HCD_leak+=1
		#with LCD
		if count in dp_p_w_LCD_List:
			dp_p_w_List[0].append(PR_p)
			dp_p_w_List[1].append(LCD_critical)
			dp_p_w_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_p_w_leak[0].append(PR_p)
				dp_p_w_leak[1].append(LCD_critical)
				dp_p_w_leak[2].append(LCD_price)
				dp_p_with_LCD_leak+=1
		#with HCD
		if count in dp_p_w_HCD_List:
			dp_p_w_List[0].append(PR_p)
			dp_p_w_List[1].append(HCD_critical)
			dp_p_w_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_p_w_leak[0].append(PR_p)
				dp_p_w_leak[1].append(HCD_critical)
				dp_p_w_leak[2].append(HCD_price)
				dp_p_with_HCD_leak+=1
		
		#++++++++++lists for generating accepted buyer's trade requests for fundamentalist++++++++++++++++++
		
		#without LCD
		if count in dp_f_wo_LCD_List:
			dp_f_wo_List[0].append(PR_f)
			dp_f_wo_List[1].append(LCD_critical)
			dp_f_wo_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_f_wo_leak[0].append(PR_f)
				dp_f_wo_leak[1].append(LCD_critical)
				dp_f_wo_leak[2].append(LCD_price)
				dp_f_without_LCD_leak+=1
		#without HCD
		if count in dp_f_wo_HCD_List:
			dp_f_wo_List[0].append(PR_f)
			dp_f_wo_List[1].append(HCD_critical)
			dp_f_wo_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_f_wo_leak[0].append(PR_f)
				dp_f_wo_leak[1].append(HCD_critical)
				dp_f_wo_leak[2].append(HCD_price)
				dp_f_without_HCD_leak+=1
		#with LCD	
		if count in dp_f_w_LCD_List:
			dp_f_w_List[0].append(PR_f)
			dp_f_w_List[1].append(LCD_critical)
			dp_f_w_List[2].append(LCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_f_w_leak[0].append(PR_f)
				dp_f_w_leak[1].append(LCD_critical)
				dp_f_w_leak[2].append(LCD_price)
				dp_f_with_LCD_leak+=1
		#without HCD
		if count in dp_f_w_HCD_List:
			dp_f_w_List[0].append(PR_f)
			dp_f_w_List[1].append(HCD_critical)
			dp_f_w_List[2].append(HCD_price)
			if _buyer['Pro_leak'][0] < _buyer['Pro_leak'][1]:
				dp_f_w_leak[0].append(PR_f)
				dp_f_w_leak[1].append(HCD_critical)
				dp_f_w_leak[2].append(HCD_price)
				dp_f_with_HCD_leak+=1
		count+=1
	
	
	#####---------------------------making final results---------------------------------
	
	result_dp_u.append([dp_u_without_LCD_tr, dp_u_with_LCD_tr, dp_u_without_HCD_tr, dp_u_with_HCD_tr, dp_u_wo_LCD_List,dp_u_w_LCD_List, dp_u_wo_HCD_List, dp_u_w_HCD_List, dp_u_without_LCD_reve, dp_u_with_LCD_reve, dp_u_without_HCD_reve, dp_u_with_HCD_reve, dp_u_without_LCD_leak, dp_u_with_LCD_leak, dp_u_without_HCD_leak, dp_u_with_HCD_leak])
	
	result_dp_p.append([dp_p_without_LCD_tr, dp_p_with_LCD_tr, dp_p_without_HCD_tr, dp_p_with_HCD_tr, dp_p_wo_LCD_List,dp_p_w_LCD_List, dp_p_wo_HCD_List, dp_p_w_HCD_List, dp_p_without_LCD_reve, dp_p_with_LCD_reve, dp_p_without_HCD_reve, dp_p_with_HCD_reve, dp_p_without_LCD_leak, dp_p_with_LCD_leak, dp_p_without_HCD_leak, dp_p_with_HCD_leak])
	
	result_dp_f.append([dp_f_without_LCD_tr, dp_f_with_LCD_tr, dp_f_without_HCD_tr, dp_f_with_HCD_tr, dp_f_wo_LCD_List,dp_f_w_LCD_List, dp_f_wo_HCD_List, dp_f_w_HCD_List, dp_f_without_LCD_reve, dp_f_with_LCD_reve, dp_f_without_HCD_reve, dp_f_with_HCD_reve, dp_f_without_LCD_leak, dp_f_with_LCD_leak, dp_f_without_HCD_leak, dp_f_with_HCD_leak])
	
	
	#####---------------------------Displaying final results---------------------------------
		
	if 0:
		print("dp_u without LCD_tr: ", dp_u_without_LCD_tr)
		print("dp_u with LCD_tr: ", dp_u_with_LCD_tr)
		print("dp_u without_HCD_tr: ", dp_u_without_HCD_tr)
		print("dp_u with_HCD_tr: ", dp_u_with_HCD_tr)
		print()
		print("dp_u without LCD_list: ", dp_u_wo_LCD_List)
		print("dp_u with LCD_list: ", dp_u_w_LCD_List)
		print("dp_u without_HCD_list: ", dp_u_wo_HCD_List)
		print("dp_u with_HCD_list: ", dp_u_w_HCD_List)
		print()
		print("dp_u without_LCD_reve: ", dp_u_without_LCD_reve)
		print("dp_u with_LCD_reve: ", dp_u_with_LCD_reve)
		print("dp_u without_HCD_reve: ", dp_u_without_HCD_reve)
		print("dp_u with_HCD_reve: ", dp_u_with_HCD_reve)
		print()
		print("dp_u without LCD_leak: ", dp_u_without_LCD_leak)
		print("dp_u with LCD_leak: ", dp_u_with_LCD_leak)
		print("dp_u without HCD_leak: ", dp_u_without_HCD_leak)
		print("dp_u with HCD_leak: ", dp_u_with_HCD_leak)
		print()
		print("dp_p without_LCD_tr: ", dp_p_without_LCD_tr)
		print("dp_p with_LCD_tr: ", dp_p_with_LCD_tr)
		print("dp_p without_HCD_tr: ", dp_p_without_HCD_tr)
		print("dp_p with_HCD_tr: ", dp_p_with_HCD_tr)
		print()
		print("dp_p without_LCD_list: ", dp_p_wo_LCD_List)
		print("dp_p with_LCD_list: ", dp_p_w_LCD_List)
		print("dp_p without_HCD_list: ", dp_p_wo_HCD_List)
		print("dp_p with_HCD_list: ", dp_p_w_HCD_List)
		print()
		print("dp_p without_LCD_reve: ", dp_p_without_LCD_reve)
		print("dp_p with_LCD_reve: ", dp_p_with_LCD_reve)
		print("dp_p without_HCD_reve: ", dp_p_without_HCD_reve)
		print("dp_p with_HCD_reve: ", dp_p_with_HCD_reve)
		print()
		print("dp_p without LCD_leak: ", dp_p_without_LCD_leak)
		print("dp_p with LCD_leak: ", dp_p_with_LCD_leak)
		print("dp_p without HCD_leak: ", dp_p_without_HCD_leak)
		print("dp_p with HCD_leak: ", dp_p_with_HCD_leak)
		print()
		print("dp_f without_LCD_tr: ", dp_f_without_LCD_tr)
		print("dp_f with_LCD_tr: ", dp_f_with_LCD_tr)
		print("dp_f without_HCD_tr: ", dp_f_without_HCD_tr)
		print("dp_f with_HCD_tr: ", dp_f_with_HCD_tr)
		print()
		print("dp_f without_LCD_list: ", dp_f_wo_LCD_List)
		print("dp_f with_LCD_list: ", dp_f_w_LCD_List)
		print("dp_f without_HCD_list: ", dp_f_wo_HCD_List)
		print("dp_f with_HCD_list: ", dp_f_w_HCD_List)
		print()
		print("dp_f without_LCD_reve: ", dp_f_without_LCD_reve)
		print("dp_f with_LCD_reve: ", dp_f_with_LCD_reve)
		print("dp_f without_HCD_reve: ", dp_f_without_HCD_reve)
		print("dp_f with_HCD_reve: ", dp_f_with_HCD_reve)
		print()
		print("dp_f without LCD_leak: ", dp_f_without_LCD_leak)
		print("dp_f with LCD_leak: ", dp_f_with_LCD_leak)
		print("dp_f without HCD_leak: ", dp_f_without_HCD_leak)
		print("dp_f with HCD_leak: ", dp_f_with_HCD_leak)
	
	
	
	
	#####---------------------------------plotting results on graph----------------------------------------
	PR_f_LCD = (pref_dp_f['w'][0]*pref_dp_f['WRate_LCD'][1]) + (pref_dp_f['w'][1]*pref_dp_f['WRate_LCD'][2]) + (pref_dp_f['w'][2]*pref_dp_f['WRate_LCD'][3]) 
	PR_f_HCD = (pref_dp_f['w'][0]*pref_dp_f['WRate_HCD'][1]) + (pref_dp_f['w'][1]*pref_dp_f['WRate_HCD'][2]) + (pref_dp_f['w'][2]*pref_dp_f['WRate_HCD'][3]) 
	
	if 0:
		plotResult_buyer(ratingList_dp_u, LCDList, HCDList, priceLCD, priceHCD, "Unconcerned- Buyers sample space")
		plotResult_buyer(ratingList_dp_p, LCDList, HCDList, priceLCD, priceHCD, "Pragmatist- Buyers sample space")
		plotResult_buyer(ratingList_dp_f, LCDList, HCDList, priceLCD, priceHCD, "Fundamentalist- Buyers sample space")
		plotResult_provider(dp_u_wo_List, "Selected trade requests for unconcerned without rating", dp_u_wo_leak, "Affected trade requests due to leakage for unconcerned without rating")
		plotResult_provider(dp_u_w_List, "Selected trade requests for unconcerned with rating", dp_u_w_leak,  "Affected trade requests due to leakage for unconcerned with rating")
		plotResult_provider(dp_p_wo_List, "Selected trade requests for Pragmatist without rating", dp_p_wo_leak,  "Affected trade requests due to leakage for Pragmatist without rating")
		plotResult_provider(dp_p_w_List, "Selected trade requests for Pragmatist with rating", dp_p_w_leak,  "Affected trade requests due to leakage for Pragmatist with rating", pref_dp_p['WRate_LCD'][0], pref_dp_p['WRate_HCD'][0], )
		plotResult_provider(dp_f_wo_List, "Selected trade requests for Fundamentalist without rating", dp_f_wo_leak,  "Affected trade requests due to leakage for Fundamentalist without rating")
		plotResult_provider(dp_f_w_List, "Selected trade requests for Fundamentalist with rating", dp_f_w_leak,  "Affected trade requests due to leakage for Fundamentalist with rating", PR_f_LCD, PR_f_HCD)
		#plt.show()

	#####save inputs 
	#----------------create data-frames for storing buyerprofiles for all iterations in excel
	dataframe_buyer.append(pd.DataFrame(data=buyerprofile))


print("Writing results in excel....")

df1 = pd.concat(dataframe_buyer)


df2 = pd.DataFrame(result_dp_u, columns = ["without_LCD_tr", "with_LCD_tr", "without_HCD_tr", "with_HCD_tr", "wo_LCD_List ", "w_LCD_List", "wo_HCD_List", "w_HCD_List", "without_LCD_reve", "with_LCD_reve", "without_HCD_reve", "with_HCD_reve", "without_LCD_leak", "with_LCD_leak", "without_HCD_leak", "with_HCD_leak"])

df3 = pd.DataFrame(result_dp_p, columns = ["without_LCD_tr", "with_LCD_tr", "without_HCD_tr", "with_HCD_tr", "wo_LCD_List ", "w_LCD_List", "wo_HCD_List", "w_HCD_List", "without_LCD_reve", "with_LCD_reve", "without_HCD_reve", "with_HCD_reve", "without_LCD_leak", "with_LCD_leak", "without_HCD_leak", "with_HCD_leak"])

df4 = pd.DataFrame(result_dp_f, columns = ["without_LCD_tr", "with_LCD_tr", "without_HCD_tr", "with_HCD_tr", "wo_LCD_List ", "w_LCD_List", "wo_HCD_List", "w_HCD_List", "without_LCD_reve", "with_LCD_reve", "without_HCD_reve", "with_HCD_reve", "without_LCD_leak", "with_LCD_leak", "without_HCD_leak", "with_HCD_leak"])


df5 = pd.DataFrame(inputs, columns = ["iterations", "DP", "N_buyer", "pri_ele", "X_max", "timespan", "t", "price_min_LCD", "price_max_LCD", "price_min_HCD", "price_max_HCD", "threshold_score", "input_likelihood", "pref_dp_u", "pref_dp_p", "pref_dp_f"])


with pd.ExcelWriter(createdir+"/"+experiment+'results.xlsx') as writer:
	
	df1.to_excel(writer, index=False, sheet_name ='buyerspace')
	df2.to_excel(writer, index=False, sheet_name = "unconcerned")
	df3.to_excel(writer, index=False, sheet_name = "pragmatist")
	df4.to_excel(writer, index=False, sheet_name = "fundamentalist")
	df5.to_excel(writer, index=False, sheet_name = "Inputs")

#df2.to_excel("results.xlsx", index=False, sheet_name = "fundamentalist")


	



