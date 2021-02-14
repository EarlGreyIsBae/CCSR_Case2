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
###########################################################
#Input given variables.
dLGD = 0.3

#Create array to hold CDS maturities and rates and other data.
mD = {'iMaturity': [1, 3, 5, 7, 10],
        'iCDS_Rate': [160, 180, 200, 210, 250],
        'dFwd_Haz': np.zeros(5),
        'dCum_Haz': np.zeros(5),
        'dCum_D_Prob': np.zeros(5)}
mData = pd.DataFrame(data = mD)

#Calculate cumulative hazard rates.
mData['dCum_Haz'] = (mData['iCDS_Rate']/10000)/dLGD

#Loop through maturities and calculate cumulative default probability.
for i in range(0, len(mData)):
    mData.iloc[i, 4] = np.exp(-mData['dCum_Haz'][i] * mData['iMaturity'][i])


#Fill in forward hazard rate for t = 1 (to simplify loop).
mData['dFwd_Haz'][0] = -np.log(mData['dCum_D_Prob'][0]/1)/(mData['iMaturity'][0] - 0)

#Loop through remainder of values.
for j in range(1, len(mData)):
    mData['dFwd_Haz'][j] = -np.log(mData['dCum_D_Prob'][j]/mData['dCum_D_Prob'][j - 1])/(mData['iMaturity'][j] - mData['iMaturity'][j - 1])
