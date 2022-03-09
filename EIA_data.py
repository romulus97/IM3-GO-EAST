# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 22:24:48 2021

@author: jkern
"""
import pandas as pd
import numpy as np
import xlrd

df_BAs = pd.read_csv('BAs.csv',header=0)

#assign EIA 930 load for 2019 to each BA
abbr = list(df_BAs['Abbreviation'])

for a in abbr:
    
    idx = abbr.index(a)
    filename = 'Raw_Data/' + a + '.xlsx'
    b = pd.read_excel(filename,header=0,sheet_name='Published Hourly Data')
    tz = b.loc[0,'Time zone']
    solar = b.loc[b['Local time'].dt.year == 2019,'Adjusted SUN Gen']
    wind = b.loc[b['Local time'].dt.year == 2019,'Adjusted WND Gen']
    hydro = b.loc[b['Local time'].dt.year == 2019,'Adjusted WAT Gen']
    
    filename = 'CSV_Files/' + a + '_Hourly_Load_Data.csv'
    b = pd.read_csv(filename,header=0)
    load = b.loc[b['Year']==2019,'Adjusted_Demand_MWh']
     
    
    if tz == 'Eastern':
        S = np.array(solar)
        W = np.array(wind)
        H = np.array(hydro)
        L = np.array(load)
        
    elif tz == "Eastern Standard":
        S = np.array(solar)
        W = np.array(wind)
        H = np.array(hydro)
        L = np.array(load)
        
    elif tz == 'Central':
        S = np.array(solar)
        S=np.insert(S,0,S[0])
        S = S[:-1]
        
        W = np.array(wind)
        W=np.insert(W,0,S[0])
        W = W[:-1]
        
        H = np.array(hydro)
        H = np.insert(H,0,H[0])
        H = H[:-1]
        
        L = np.array(load)
        L = np.insert(L,0,L[0])
        L = L[:-1]
        
    elif tz == 'Mountain':
        S = np.array(solar)
        S=np.insert(S,0,S[0])
        S=np.insert(S,0,S[0])
        S = S[:-2]
        
        W = np.array(wind)
        W=np.insert(W,0,S[0])
        W=np.insert(W,0,S[0])
        W = W[:-2]
        
        H = np.array(hydro)
        H = np.insert(H,0,H[0])
        H = np.insert(H,0,H[0])
        H = H[:-2]  
        
        L = np.array(load)
        L = np.insert(L,0,L[0])
        L = np.insert(L,0,L[0])
        L = L[:-2]   
        
    elif tz == 'Pacific':
        
        S = np.array(solar)
        S=np.insert(S,0,S[0])
        S=np.insert(S,0,S[0])
        S=np.insert(S,0,S[0])
        S = S[:-3]
        
        W = np.array(wind)
        W=np.insert(W,0,S[0])
        W=np.insert(W,0,S[0])
        W=np.insert(W,0,S[0])
        W = W[:-3]
        
        H = np.array(hydro)
        H = np.insert(H,0,H[0])
        H = np.insert(H,0,H[0])
        H = np.insert(H,0,H[0])
        H = H[:-3]   
        
        L = np.array(load)
        L = np.insert(L,0,L[0])
        L = np.insert(L,0,L[0])
        L = np.insert(L,0,L[0])
        L = L[:-3]   

    elif tz == 'Arizona':
        S = np.array(solar)
        S=np.insert(S,0,S[0])
        S=np.insert(S,0,S[0])
        S = S[:-2]
        
        W = np.array(wind)
        W=np.insert(W,0,S[0])
        W=np.insert(W,0,S[0])
        W = W[:-2]
        
        H = np.array(hydro)
        H = np.insert(H,0,H[0])
        H = np.insert(H,0,H[0])
        H = H[:-2]  
        
        L = np.array(load)
        L = np.insert(L,0,L[0])
        L = np.insert(L,0,L[0])
        L = L[:-2]   
        
    else:
        print([abbr,tz])
        
    if idx < 1:
        S_end = S
        W_end = W
        H_end = H
        L_end = L
    else:
        S_end = np.column_stack((S_end,S))
        W_end = np.column_stack((W_end,W))
        H_end = np.column_stack((H_end,H))
        L_end = np.column_stack((L_end,L))

r,c = np.shape(S_end)
for i in range(0,r):
    for j in range(0,c):
        if S_end[i,j] < 0:
            S_end[i,j] = 0
df_S = pd.DataFrame(S_end)
df_S.columns = abbr
df_S.to_csv('BA_solar.csv')

r,c = np.shape(W_end)
for i in range(0,r):
    for j in range(0,c):
        if W_end[i,j] < 0:
            W_end[i,j] = 0
df_W = pd.DataFrame(W_end)
df_W.columns = abbr
df_W.to_csv('BA_wind.csv')

r,c = np.shape(H_end)
for i in range(0,r):
    for j in range(0,c):
        if H_end[i,j] < 0:
            H_end[i,j] = 0
df_H = pd.DataFrame(H_end)
df_H.columns = abbr
df_H.to_csv('BA_hydro.csv')

r,c = np.shape(L_end)
for i in range(0,r):
    for j in range(0,c):
        if L_end[i,j] < 0:
            L_end[i,j] = 0
df_L = pd.DataFrame(L_end)
df_L.columns = abbr
df_L.to_csv('BA_load.csv')