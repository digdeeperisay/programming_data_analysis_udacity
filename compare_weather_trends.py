# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 19:55:43 2019
@author: Prajamohan
Purpose: Plotting Weather trends as part of the Data Analyst course on Udacity
High level steps:
    Download the CSV files for the entire world and interested cities
    Compare and understand range of years in each etc.
    Plot them side by side and draw insights
    Write up a report with findings
"""

### Read the two datasets into Python dataframes ###
import pandas as pd

global_data = pd.read_csv(filepath_or_buffer = 'C:\Users\prajamohan\Desktop\Non client\Study\Becoming a Data Analyst\Weather Trends\Global_Weather.csv')
cities_data = pd.read_csv(filepath_or_buffer = 'C:\Users\prajamohan\Desktop\Non client\Study\Becoming a Data Analyst\Weather Trends\City_Weather.csv')

print global_data.head()
print cities_data.head()

### Understand the datasets better ###

print cities_data.groupby(['city']).count() #count ignores NULL values
#               year  country  avg_temp
#city                                  
#Bangalore       218      218       211
#New York        271      271       266
#San Francisco   165      165       165

#So SFO has no missing values but less years populated. NYC seems to be the most well populated

print global_data.count() #excludes NULL values
#year        266
#avg_temp    266
print global_data['year'].size #266 (size includes NULL values)

#Global data has no missing values in year column and has 266 years in total
#Since NYC also has 266 valid observations (and I live in NYC now!), using just that to compare with global weather

### Subset NYC data with just the needed columns ###

nyc_data = cities_data[['year','avg_temp']][cities_data['city'] == 'New York'].dropna(subset=['year','avg_temp'])

print nyc_data.head()
print global_data.head()

#looks same

### Compare min/max years and common years between nyc_data and global_data + combine them ###

print nyc_data['year'].agg(['min','max']) #1743 to 2013
print global_data['year'].agg(['min','max']) #1750 to 2015

#so more or less same date range. lets just use the overlapping years since it is a good population

global_local_data = pd.merge(left=global_data, right=nyc_data, left_on='year', right_on='year', suffixes=('_global', '_nyc'))
print global_local_data.head()
#   year  avg_temp_global  avg_temp_nyc
#0  1750             8.72         10.07
#1  1751             7.98         10.79
#2  1752             5.78          2.81
#3  1753             8.39          9.52
#4  1754             8.47          9.88

#check if there are missing values in avg temp
global_local_data.isna().any()    
#
#year               False
#avg_temp_global    False
#avg_temp_nyc       False

### Alright, now we have a clean valid data set. Plot them ###

ax = global_local_data.plot(x ='year', y=['avg_temp_global','avg_temp_nyc'], figsize=(10, 5), kind = 'line', title = 'Comparing global weather and NYC weather')	

ax.set_xlabel("Year")
ax.set_ylabel("Avg Temp in C")

#curios about those two dips
global_local_data[global_local_data['avg_temp_nyc']< 4]
#1752 and 1779

#Now we need to do the same for rolling averages and make minor tweaks here

#Using pandas rolling function to create two columns
global_local_data['avg_temp_global_MA_5'] = global_local_data['avg_temp_global'].rolling(window=5).mean()
global_local_data['avg_temp_nyc_MA_5'] = global_local_data['avg_temp_nyc'].rolling(window=5).mean()

#Manually verifying it [works fine]
pd.set_option('display.expand_frame_repr', False) #show output as is
global_local_data.head(100)

#Plotting it now
ax = global_local_data.plot(x ='year', y=['avg_temp_global_MA_5','avg_temp_nyc_MA_5'], figsize=(10, 5), kind = 'line', title = 'Comparing global weather and NYC weather using moving averages')	
ax.set_xlabel("Year")
ax.set_ylabel("Avg Temp in C")
