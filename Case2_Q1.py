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
mData['dCum_Haz'] = mData['iCDS_Rate']/dLGD


