# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 10:09:25 2022

@author: kingw
"""

import pandas as pd
import numpy as np

# Read generator parameters and select oil
df = pd.read_csv('data_genparams.csv',header=0)

df_oil = df.loc[df['typ'] == 'oil']
df_oil = df_oil.reset_index(drop=True)

gens = list(df.loc[:,'name'])
gens_oil = list(df_oil.loc[:,'name'])
gens_cap = list(df.loc[:,'maxcap'])
gens_hr = list(df.loc[:,'heat_rate'])
gens_min = list(df.loc[:,'mincap'])
gens_var_om = list(df.loc[:,'var_om'])
gens_no_load = list(df.loc[:,'no_load'])
gens_st_cost = list(df.loc[:,'st_cost'])
gens_ramp = list(df.loc[:,'ramp'])


# Read nodes
FN = 'Results_500.xlsx'
df_nodes = pd.read_excel(FN, sheet_name = 'Bus', header=0)
all_nodes = list(df_nodes['bus_i'])

# Read generator-node matrix
df_gen_mat = pd.read_csv('gen_mat.csv',header=0)

######
# create gen-to-bus matrix for oil

for i in range(0,len(all_nodes)):
    all_nodes[i] = 'bus_' + str(all_nodes[i])

df_nodes['bus_i'] = all_nodes
            
A = np.zeros((len(gens),len(all_nodes)))
            
df_A = pd.DataFrame(A)
df_A.columns = all_nodes
df_A['name'] = gens
df_A.set_index('name',inplace=True)
            
for i in range(0,len(gens_oil)):
    node = df_oil.loc[i,'node']
    g = gens_oil[i]
    df_A.loc[g,node] = 1

######

# Calculate oil parameters for each node
tot_cap = np.zeros(len(all_nodes))
oil_cap = np.zeros(len(all_nodes))
oil_max = np.zeros(len(all_nodes))
oil_hr = np.zeros(len(all_nodes))
oil_min = np.zeros(len(all_nodes))
oil_var_om = np.zeros(len(all_nodes))
oil_no_load = np.zeros(len(all_nodes))
oil_st_cost = np.zeros(len(all_nodes))
oil_ramp = np.zeros(len(all_nodes))

for i in range(0,len(all_nodes)):
    tot_cap[i] = sum(gens_cap*df_gen_mat.iloc[:,i+1])
    oil_cap[i] = sum(gens_cap*df_A.iloc[:,i])
    oil_max[i] = sum(gens_cap)
    oil_hr[i] = sum(gens_hr*(gens_cap*df_A.iloc[:,i])/sum(gens_cap*df_A.iloc[:,i]))
    oil_min[i] = sum(gens_min*(gens_cap*df_A.iloc[:,i])/sum(gens_cap*df_A.iloc[:,i]))
    oil_var_om[i] = sum(gens_var_om*(gens_cap*df_A.iloc[:,i])/sum(gens_cap*df_A.iloc[:,i]))
    oil_no_load[i] = sum(gens_no_load*(gens_cap*df_A.iloc[:,i])/sum(gens_cap*df_A.iloc[:,i]))
    oil_st_cost[i] = sum(gens_st_cost*(gens_cap*df_A.iloc[:,i])/sum(gens_cap*df_A.iloc[:,i]))
    oil_ramp[i] = sum(gens_ramp*df_A.iloc[:,i])

# Write oil parameters into the nodes dataframe
df_oil = pd.DataFrame()
df_oil.loc[:,'node'] = list(df_nodes.loc[:,'bus_i'])
df_oil.loc[:,'maxcap'] = oil_max
df_oil.loc[:,'heat_rate'] = oil_hr
df_oil.loc[:,'mincap'] = oil_min
df_oil.loc[:,'var_om'] = oil_var_om
df_oil.loc[:,'no_load'] = oil_no_load
df_oil.loc[:,'st_cost'] = oil_st_cost
df_oil.loc[:,'ramp'] = oil_ramp
df_oil = df_oil.dropna().reset_index(drop=True)

df_oil.loc[:,'minup'] = 1
df_oil.loc[:,'mindn'] = 1
df_oil.loc[:,'typ'] = 'oil'

oil_name = []
for i in range(0,len(df_oil.index)):
    oil_name.append(df_oil.loc[i,'node'] + '_oil')
df_oil.loc[:,'name'] = oil_name

df_oil = df_oil[["name", "typ", "node", "maxcap", "heat_rate", "mincap", "var_om", "no_load", "st_cost", "ramp", "minup", "mindn"]]

# Substitute aggregated oil gens into the data_genparams.csv file
# Removing the old set of oil generators
df = df.loc[df['typ'] != 'oil']
df = pd.concat([df, df_oil], ignore_index=True)
df.to_csv('data_genparams_qian.csv',index=None)