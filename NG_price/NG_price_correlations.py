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

df1 = pd.read_excel('ice_natgas-2015final.xlsx',header=0)
df2 = pd.read_excel('ice_natgas-2016final.xlsx',header=0)
df3 = pd.read_excel('ice_natgas-2017final.xlsx',header=0)

frames = [df1,df2,df3]

df = pd.concat(frames)
df = df.reset_index(drop=True)
df.drop_duplicates()

df['Trade date'] = pd.to_datetime(df['Trade date'])
df = df.set_index('Trade date')


df_2019 = pd.read_excel('2019_hh.xlsx',header=0)

for i in range(0,len(df_2019)):
    
    p = df_2019.loc[i,'Price']
    
    if np.isnan(p):
        
        p2 = df_2019.loc[i+1,'Price']
        
        if np.isnan(p2):
            
            p3 = df_2019.loc[i+2,'Price']
            
            if np.isnan(p3):
                
                p4 = df_2019.loc[i+3,'Price']
                
                if np.isnan(p4):
                        
                    df_2019.loc[i,'Price'] = df_2019.loc[i-1,'Price'] - (df_2019.loc[i-1,'Price'] - df_2019.loc[i+4,'Price'])/5
                    df_2019.loc[i+1,'Price'] = df_2019.loc[i,'Price'] - 2*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+4,'Price'])/5
                    df_2019.loc[i+2,'Price'] = df_2019.loc[i+1,'Price'] - 3*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+4,'Price'])/5
                    df_2019.loc[i+3,'Price'] = df_2019.loc[i+2,'Price'] - 4*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+4,'Price'])/5
                
                else:

                    df_2019.loc[i,'Price'] = df_2019.loc[i-1,'Price'] - (df_2019.loc[i-1,'Price'] - df_2019.loc[i+3,'Price'])/4
                    df_2019.loc[i+1,'Price'] = df_2019.loc[i,'Price'] - 2*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+3,'Price'])/4
                    df_2019.loc[i+2,'Price'] = df_2019.loc[i+1,'Price'] - 3*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+3,'Price'])/4

            else:
                
                df_2019.loc[i,'Price'] = df_2019.loc[i-1,'Price'] - (df_2019.loc[i-1,'Price'] - df_2019.loc[i+2,'Price'])/3
                df_2019.loc[i+1,'Price'] = df_2019.loc[i,'Price'] + 2*(df_2019.loc[i-1,'Price'] - df_2019.loc[i+2,'Price'])/3
        else:
            df_2019.loc[i,'Price'] = df_2019.loc[i-1,'Price'] - (df_2019.loc[i-1,'Price'] - df_2019.loc[i+2,'Price'])/3

df_2019.loc[len(df_2019),'Price'] = df_2019.loc[len(df_2019)-1,'Price'] 


EIC_hubs = ['Algonquin Citygates','Chicago Citygates','TETCO-M3']

df_predicted = pd.DataFrame()

for h in EIC_hubs:

    reg = LinearRegression()
    
    y_v = df[df['Price hub']==h]
    d_list = list(y_v.index.unique())
    
    H = df.loc[df['Price hub']=='Henry']
    hh_d_list = list(H.index.unique())
    
    common = set(d_list).intersection(hh_d_list)
    
    y = y_v.loc[common,'High price $/MMBtu']   
    # y = y.sort_index()
    
    y_f = []
    for i in common:
        a = y.loc[i]
        y_f.append(a)

    X = H.loc[common,'High price $/MMBtu']
    # X = X.sort_index()
    
    X_f = []
    for i in common:
        a = X.loc[i]
        X_f.append(a)
        
    combined = pd.DataFrame()
    combined['X'] = X_f
    combined['y'] = y_f
    combined['Trade date'] = list(common)
    combined['Trade date'] = pd.to_datetime(combined['Trade date'])
    combined = combined.sort_values(by='Trade date')
            
    X = combined['X'].values
    y = combined['y'].values
    
    X = np.reshape(X,(len(X),1))
    y = np.reshape(y,(len(y),1))
    
    plt.figure()
    plt.plot(X)
    plt.plot(y)
    plt.legend(['Henry Hub',h])
    
    ## Train the model using the training sets
    reg.fit(X,y)  
    
    # Predict 2019 data
    X_new = np.array(df_2019['Price'])
    X_new = X_new.reshape(len(X_new),1)
    X_new = X_new[:-1]
    
    predicted = []
    
    for i in range(0,len(X_new)):
        if np.isnan(X_new[i]):
            X_new[i] = X_new[i-1]
        
        y_hat = reg.intercept_ + reg.coef_[0]*X_new[i]
        predicted.append(y_hat[0])
        
    df_predicted[h] = np.array(predicted)
    
df_predicted['Henry'] = X_new
df_predicted.to_csv('Predicted_2019.csv')
        
    