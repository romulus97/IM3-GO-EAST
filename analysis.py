# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:50:37 2022

@author: jkern
"""
import pandas as pd
import numpy as np

df = pd.read_csv('Exp500_simple_25/nodal_wind.csv',header=0)

df_BAs = pd.read_csv('BAs.csv',header=0)

df_original = pd.read_csv('nodes_to_BA_state.csv',header=0)

BAs = list(df_BAs['Name'])

buses = list(df.columns)
bus_digits = []
    
BA_wind = np.zeros((8760,len(BAs)))

for b in buses:
    
    res = ''.join(filter(lambda i: i.isdigit(), b))
    d = int(res)
    
    BA = df_original.loc[df_original['Number'] == d,'NAME'].values[0]
    
    idx = BAs.index(BA)
    
    BA_wind[:,idx] = BA_wind[:,idx] + df.loc[:,b]
    
BAs_abbr = list(df_BAs['Abbreviation'])
df_BA_wind = pd.DataFrame(BA_wind)
df_BA_wind.columns = BAs_abbr

df_BA_wind2 = pd.read_csv('BA_wind.csv',header=0,index_col=0)



    

                
                
 