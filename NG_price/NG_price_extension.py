# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 22:16:34 2022

@author: jkern
"""
import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression

df = pd.read_csv('Predicted_2019.csv',header=0,index_col=0)

df_corr = pd.read_csv('BA_NG_Price_Coeff_Matrix.csv',header=0,index_col=0)

BAs = list(df_corr.index)

for b in BAs:
    
    new = np.zeros((365,1))
    for i in range(0,365):
        new[i] = df.loc[i,'Algonquin Citygates']*df_corr.loc[b,'ISO NEW ENGLAND INC.'] + df.loc[i,'Chicago Citygates']*df_corr.loc[b,'MIDCONTINENT INDEPENDENT TRANSMISSION SYSTEM OPERATOR, INC..'] + df.loc[i,'TETCO-M3']*df_corr.loc[b,'PJM INTERCONNECTION, LLC'] + df.loc[i,'Henry']*df_corr.loc[b,'SOUTHERN COMPANY SERVICES, INC. - TRANS']

    df[b] = new
    
df = df.rename(columns={'Algonquin Citygates':'ISO NEW ENGLAND INC.','Chicago Citygates':'MIDCONTINENT INDEPENDENT TRANSMISSION SYSTEM OPERATOR, INC..','TETCO-M3':'PJM INTERCONNECTION, LLC','Henry':'SOUTHERN COMPANY SERVICES, INC. - TRANS'})
   
df.to_csv('Average_NG_prices_BAs.csv')