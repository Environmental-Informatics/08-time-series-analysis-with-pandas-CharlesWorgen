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
from pandas import Series, DataFrame, Panel

#The code next line does not work with the current version of pandas
#pd.set_option('display.max_rows',15) # this limit maximum numbers of rows

#%pylab inline

pd.__version__ #Check Pandas version

#Loading data
#!curl http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii >> 'monthly.ao.index.b50.current.ascii'
#!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii

ao = np.loadtxt('monthly.ao.index.b50.current.ascii')

ao[0:2] #three elements

ao.shape  #shape of our array

#Time Series
#Date starts at January 1950, frequency of the data is one month (freq='M').
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')
dates
dates.shape

#create time series
AO = Series(ao[:,2], index=dates)
AO
#plot
AO.plot()
AO['1980':'1990'].plot()
AO['1980-05':'1981-03'].plot()

#get values
AO[120] #by number
AO['1960-01'] # by index 
AO['1960']

AO[AO > 0] # return all values that are greater than 0

#Data Frame

#NOA time series 
#!curl http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii >> 'norm.nao.monthly.b5001.current.ascii'
#!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii

#Create time series
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)

NAO.index

#Create dataframe containing both
aonao = DataFrame({'AO' : AO, 'NAO' : NAO})

aonao.plot(subplots=True)

aonao.head()
aonao['NAO']
aonao.NAO

#Add in column of difference between AO & NAO
aonao['Diff'] = aonao['AO'] - aonao['NAO']
aonao.head()
#Delete the column
del aonao['Diff']
aonao.tail()

#Slicing
aonao['1981-01':'1981-03']

import datetime

#Plot all NAO values in the 1980s for months where AO is positive and NAO is negative
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0) 
        & (aonao.index > datetime.datetime(1980,1,1)) 
        & (aonao.index < datetime.datetime(1989,1,1)),
        'NAO'].plot(kind='barh')

#Statistics
aonao.mean()
aonao.max()
aonao.min()
aonao.mean(1)
aonao.describe()

#Resampling
AO_mm = AO.resample("A").mean() #calculates annual ('A') mean
AO_mm.plot(style='g--')

AO_mm = AO.resample("A").median()
AO_mm.plot()

AO_mm = AO.resample("3A").apply(np.max) # apply method, 3 year frequency
AO_mm.plot()

# specify several functions at once as a list
AO_mm = AO.resample("A").apply(['mean', np.min, np.max])
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()

AO_mm

#Moving (rolling) statistics
aonao.rolling(window=12, center=False).mean().plot(style='-g') #Rolling mean

aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g') #Rolling correlation

aonao.corr() # getting correlation coefficients for members of the Data Frame

#plots for evaluation
