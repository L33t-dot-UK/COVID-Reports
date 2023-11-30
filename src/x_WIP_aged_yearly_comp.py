'''
YEARLY COMP FOR DEATHS AND CASES IN EACH AGE GROUP

'''


import sys
sys.path.append('./src/toolset')

#Import COVID Data with our COVIDTOOLSET
from unicodedata import category
from numpy.core.shape_base import block
from numpy.lib import function_base
import pandas as pd

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.DataFunctions import Functions as functions
from toolset.CovidDashboard import Dashboard as DASH
from toolset.ReadVaxData import readVaxData as vax_data
from toolset.BenchMark import Benchmark as Benchmark

import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=UserWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=RuntimeWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=FutureWarning) #surpress various warnings to do with dataframes if you want to see the warnings comment these lines

nation = "England" #If this is set to anything else Age profiled data will always be for England as it is not available for the other nations

#pullData = getData(nation) #get the latest data
govData = govDataClass(True, nation) #this object stores all downloaded data and loads it into memory when the argument is set to true

nonAgeDates = govData.get_gov_date_Series() #Gets xAxis dataset
ageDates = govData.get_aged_gov_date_series() #Gets xAxis dataset for graphs that split data by age groups

chart = CovidChart() #This will be the chart object that we will use

funcs = functions()

dash = DASH()

for ii in range(0, len(govData.get_age_cat_string_list())):

    chart.draw_Scatter_Year_Comp(govData.get_aged_case_data(ii), False, 'Cases', True, govData.get_year_dates(), True)
    chart.draw_Scatter_Year_Comp(govData.get_aged_death_data(ii), False, 'Deaths', True, govData.get_year_dates(), True)

    img = ['reports/images/yearlyCompCases' + '.png', 'reports/images/yearlyCompDeaths' + '.png']
    dash.create_dashboard('Yearly Comparison Age Group ' + govData.get_age_cat_string_list()[ii], img, 'XXXyearCompVax' + str(ii), toStamp=False)    #This will put the images side by side


 