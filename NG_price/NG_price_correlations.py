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

df = pd.read_excel('ice_natgas-2017final.xlsx',header=0)
hubs = list(df['Price hub'].unique())


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
    y_v = y_v.reset_index(drop=True)
    dates = []
    d = y_v['Trade date']
    d = d.reset_index(drop=True)
    y = np.zeros((len(d),1))
    for i in range(0,len(d)):
        dates.append(str(d[i]))
        y[i,0] = y_v.loc[i,'High price $/MMBtu']

    H = df.loc[df['Price hub']=='Henry']
    H = H.reset_index(drop=True)
    X = np.zeros((len(dates),1))
    count = 0
    for i in range(0,len(H)):
        if str(H.loc[i,'Trade date']) in dates:
            X[count,0] = float(df.loc[i,'High price $/MMBtu'])
            count+=1
            
    plt.figure()
    plt.plot(X)
    plt.plot(y)
    plt.legend(['Henry Hub',h])
    
    ## Train the model using the training sets
    reg.fit(X,y)  
    
    # Predict 2019 data
    X_new = np.array(df_2019['Price'])
    X_new = X_new.reshape(len(X_new),1)
    
    predicted = []
    
    for i in range(0,len(X_new)):
        y_hat = reg.intercept_ + reg.coef_[0]*X_new[i]
        predicted.append(y_hat[0])
        
    df_predicted[h] = np.array(predicted)
    
df_predicted['Henry'] = X_new
df_predicted.to_csv('Predicted_2019.csv')
        
    