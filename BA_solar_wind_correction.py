# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 22:05:54 2021

@author: kakdemi
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn import linear_model


#reading the solar and wind time series
BA_solar = pd.read_csv('BA_solar.csv',header=0)
del BA_solar['Unnamed: 0']

BA_wind = pd.read_csv('BA_wind.csv',header=0)
del BA_wind['Unnamed: 0']

BA_hydro = pd.read_csv('BA_hydro.csv',header=0)
del BA_hydro['Unnamed: 0']
# BA_wind.fillna('', inplace=True)

#reindexing BA renewables data and getting the BA names
hours_2019 = pd.date_range(start='1-1-2019 00:00:00',end='12-31-2019 23:00:00', freq='H')
BA_solar.index = hours_2019
BA_wind.index = hours_2019
BA_hydro.index = hours_2019
BAs = list(BA_solar.columns)

#defining months and night hours
summer_night_hours = [20,21,22,23,0,1,2,3,4,5,6]
winter_night_hours = [18,19,20,21,22,23,0,1,2,3,4,5,6,7]
summer_months = [3,4,5,6,7,8,9]
winter_months = [1,2,10,11,12]

#if there are negative values for solar and wind, changing them with 0
BA_solar[BA_solar < 0] = 0
BA_wind[BA_wind < 0] = 0
BA_hydro[BA_hydro < 0] = 0

#selecting which BAs to exclude
solar_BAs = BAs.copy()
# solar_BAs.remove('BPAT')
# solar_BAs.remove('NWMT')
# solar_BAs.remove('AVA')

#filtering out anomalies (really high values) from solar data, replacing them with values from a different day but at the same hour
for BA in solar_BAs:
    
    for time in hours_2019:
        
        solar_val = BA_solar.loc[time,BA]
        
        time_before = time - timedelta(days=10)
        time_after = time - timedelta(days=10)
        max_gen_before = BA_solar.loc[time_before:time - timedelta(days=1),BA].max()
        max_gen_after = BA_solar.loc[time:time + timedelta(days=1),BA].max()
        
        min_gen_before = BA_solar.loc[time_before:time - timedelta(days=1),BA].min()
        min_gen_after = BA_solar.loc[time:time + timedelta(days=1),BA].min()
        
        if solar_val > 1.25*max_gen_before or solar_val > 1.25*max_gen_after:
            
            day_count = 0
            new_val = 0
            
            for i in range(1,6):

                day_count += i
                try:
                    day_before = time - timedelta(days=day_count)
                    new_val = BA_solar.loc[day_before,BA]
                    if new_val <= max_gen_before or new_val <= max_gen_after:
                        break
                    
                except KeyError:
                    try: 
                        day_after = time + timedelta(days=day_count)
                        new_val = BA_solar.loc[day_after,BA]
                        if new_val <= max_gen_before or new_val <= max_gen_after:
                            break
                    except KeyError:
                        pass
                        
            BA_solar.loc[time,BA] = new_val
               
        else:
            pass


        hydro_val = BA_hydro.loc[time,BA]
        
        time_before = time - timedelta(days=10)
        time_after = time - timedelta(days=10)
        max_gen_before = BA_hydro.loc[time_before:time - timedelta(days=1),BA].max()
        max_gen_after = BA_hydro.loc[time:time + timedelta(days=1),BA].max()
        
        min_gen_before = BA_hydro.loc[time_before:time - timedelta(days=1),BA].min()
        min_gen_after = BA_hydro.loc[time:time + timedelta(days=1),BA].min()
        
        if hydro_val > 1.25*max_gen_before or hydro_val > 1.25*max_gen_after:
            
            day_count = 0
            new_val = 0
            
            for i in range(1,6):

                day_count += i
                try:
                    day_before = time - timedelta(days=day_count)
                    new_val = BA_hydro.loc[day_before,BA]
                    if new_val <= max_gen_before or new_val <= max_gen_after:
                        break
                    
                except KeyError:
                    try: 
                        day_after = time + timedelta(days=day_count)
                        new_val = BA_hydro.loc[day_after,BA]
                        if new_val <= max_gen_before or new_val <= max_gen_after:
                            break
                    except KeyError:
                        pass
                        
            BA_hydro.loc[time,BA] = new_val
               
        else:
            pass
# #selecting which BAs to include
# wind_BAs = ['CHPD','PACE','PACW','WACM']

# #filtering out anomalies (really high values) from wind data by using percentiles
# for BA in wind_BAs:
    
#     if BA == 'CHPD' or BA == 'WACM':
    
#         exteme_value_limit = np.percentile(BA_wind.loc[:,BA], 99.9)
    
#     elif BA == 'PACE' or BA == 'PACW':
    
#         exteme_value_limit = np.percentile(BA_wind.loc[:,BA], 99.95)
    
#     for time in hours_2019:
        
#         wind_val = BA_wind.loc[time,BA]
           
#         if wind_val > exteme_value_limit:
            
#             day_count = 0
#             new_val = 0
            
#             for i in range(1,6):

#                 day_count += i
#                 try:
#                     day_before = time - timedelta(days=day_count)
#                     new_val = BA_wind.loc[day_before,BA]
#                     if new_val <= exteme_value_limit:
#                         break
                    
#                 except KeyError:
#                     try: 
#                         day_after = time + timedelta(days=day_count)
#                         new_val = BA_wind.loc[day_after,BA]
#                         if new_val <= exteme_value_limit:
#                             break
#                     except KeyError:
#                         pass
                        
#             BA_wind.loc[time,BA] = new_val
            
#         else:
#             pass


# #exporting the data
# BA_wind.reset_index(drop=True,inplace=True)
# BA_wind.to_csv('BA_wind_corrected.csv')

BA_solar.reset_index(drop=True,inplace=True)
BA_solar.to_csv('BA_solar_corrected.csv')           
        
BA_hydro.reset_index(drop=True,inplace=True)
BA_hydro.to_csv('BA_hydro_corrected.csv')              

