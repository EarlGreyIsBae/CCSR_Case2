"""
Case2_CCS.py

Purpose:
    Code for case 2 of ther course Credit, Complexity and Systemic Risk

Version:
    1       First start

Date:
    2020/02/14

Author:
    Niek de Meijier & Connor Stevens
"""
###########################################################
### Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import pandas as pd
from scipy.integrate import quad
from scipy.optimize import minimize
###########################################################
"""
Question 1
"""

#Input given variables.
dLGD = 0.3
dr = 0.005

#Create array to hold CDS maturities and rates and other data.
mD = {'iMaturity': [1, 3, 5, 7, 10],
        'iCDS_Rate': [160, 180, 200, 210, 250],
        'dFwd_Haz': np.zeros(5),
        'dCum_Haz': np.zeros(5),
        'dCum_D_Prob': np.zeros(5)}
mData1 = pd.DataFrame(data = mD)

#Calculate cumulative hazard rates.
mData1['dCum_Haz'] = (mData1['iCDS_Rate']/10000)/dLGD

#Loop through maturities and calculate cumulative default probability.
for i in range(0, len(mData1)):
    mData1.iloc[i, 4] = np.exp(-mData1['dCum_Haz'][i] * mData1['iMaturity'][i])


#Fill in forward hazard rate for t = 1 (to simplify loop).
mData1['dFwd_Haz'][0] = -np.log(mData1['dCum_D_Prob'][0]/1)/(mData1['iMaturity'][0] - 0)

#Loop through remainder of values.
for j in range(1, len(mData1)):
    mData1['dFwd_Haz'][j] = -np.log(mData1['dCum_D_Prob'][j]/mData1['dCum_D_Prob'][j - 1])/(mData1['iMaturity'][j] - mData1['iMaturity'][j - 1])

"""
Question 2
"""

#Create dataframe to hold results for question 2.
mData2 = pd.DataFrame(data = mD)
dCDS = {1: 160/10000, 3: 180/10000, 5: 200/10000, 7: 210/10000, 10: 250/10000}



####
#PREMIUM PAYMENTS
####

#Create function to give correct cumulative lambda for a given T.
def getLam(T):
    CumLam = 0
    if ((T > 0) and (T <= 1)):
        CumLam = (160/10000)/dLGD
    if ((T > 1) and (T <= 3)):
        CumLam = (180/10000)/dLGD
    if ((T > 3) and (T <= 5)):
        CumLam = (200/10000)/dLGD       
    if ((T > 5) and (T <= 7)):
        CumLam = (210/10000)/dLGD
    if ((T > 7) and (T <= 10)):
        CumLam = (250/10000)/dLGD
    return CumLam

#Set variables for following calculation.
iN = 1
dLGD = 0.3
dr = 0.005
Lamd = getLam(iN)

#Function which calculates premium payments, accrued premium and protection leg.
#Function is set out to be optimized later.
def Optim(Lamd, iN):
    
    ####
    #PREMIUM PAYMENTS
    ####
    
    #Function to calculate discounted quarterly premium payments.
    def PremPay(iN):
        dPremPay = 0
        for i in (np.linspace(0.25, iN, iN * 4 + 1)):
            dPremPay = dPremPay  + np.exp(-dr * i) * 0.25 * np.exp(-Lamd * i)
        return dPremPay
    
    dPremPay = PremPay(iN)
    
    ####
    #ACCRUED PREMIUM
    ####
    
    #Function to be integrated for integral portion of accrued premium. (Not sure about this one and how/if to treat quarterly payments here).
    def AccrIntegrand(u):
        dAccrIntegrand = np.exp(-dr * u) * (1/4)/2 * Lamd * np.exp(- Lamd * u)
        return dAccrIntegrand
    
    #Integrate function defined above.
    dAccrPrem = quad(AccrIntegrand, 0, iN)[0]    
    
    ####
    #PROTECTION LEG
    ####
    
    #Function to be integrated for the integral portion of the protection leg.
    def ProtecIntegrand(u):
        dProtecIntegrand = np.exp(-dr * u) * Lamd * np.exp(-Lamd * u)
        return dProtecIntegrand
    
    #Integrate functiond defined above and multiply by loss given default.
    dProtecLeg = dLGD * quad(ProtecIntegrand, 0, iN)[0]

    #Return CDS pricing formula which gives the pricing premium. 
    return dCDS[iN] * (dPremPay + dAccrPrem) - dProtecLeg

#Optim(Lamd,1)

#Define optimization function in terms of one input variable so that we can optimize it.
diff = lambda x: Optim(x, iN)

#Minimize the pricing premium (get to zero) by changing the cumulative hazard rates.
minimize(diff, dCDS[iN]/dLGD, method = 'Nelder-Mead', tol = 0.1)
