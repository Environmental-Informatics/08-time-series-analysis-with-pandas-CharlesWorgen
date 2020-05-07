#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2020/05/06
by Charles Huang

Lab08 - Time Series Analysis with Pandas

Tutorial code of tutorial Time Series Analysis with Pandas
    analysis of several time series data (AO, NAO)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series, DataFrame, Panel

#Read in data
WRDF = pd.read_table("WabashRiver_DailyDischarge_20150317-20160324.txt",delimiter='\t',
                     comment='#', header= 0, usecols=[2,4],names = ['Datetime','Discharge'],
                     parse_dates = ['Datetime'])
WRDF.head() #Check
WRDF = WRDF.drop([0]) #Remove the first row 

#Generate dates               
dates = pd.date_range('2015-03-17 00:00', periods=WRDF.shape[0], freq='15min')
dates.shape #Check the length

#Make sure that Discharge is numeric for calculation
WRDF['Discharge'] = WRDF['Discharge'].astype('float64') 

#Create time series
WRTS = Series(WRDF['Discharge'].values, index=dates)


#Create a plot of daily average streamflow
WRDS = WRTS.resample("D").mean()
plt.figure(1)
WRDS.plot(style='g--')
#Add in title, labe
plt.title("Plot of Daily Average Streamflow")
plt.xlabel("Time (day)")
plt.ylabel("Discharge (cubic feet per second)")
plt.savefig('DASF.pdf')
plt.show()

#identify and plot the 10 days with highest flow
WRTD = WRDS.resample("10D").apply(np.max)
plt.figure(2)
WRDS.plot(style='g--', label = 'Daily')
WRTD.plot(style='ro',label = '10 Days')
#Add in title, labe
plt.title("Plot of Highest Streamflow in 10 Days")
plt.xlabel("Time (day)")
plt.ylabel("Discharge (cubic feet per second)")
plt.savefig('TDSF.pdf')
plt.legend()
plt.show()

#plot of monthly average streamflow
WRMS = WRTS.resample("M").mean()
plt.figure(3)
WRMS.plot(style='g--')
#Add in title, labe
plt.title("Plot of Monthly Average Streamflow")
plt.xlabel("Time (Month)")
plt.ylabel("Discharge (cubic feet per second)")
plt.savefig('MASF.pdf')
plt.show()
