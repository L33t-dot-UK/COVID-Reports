'''
Code used to produce the 2 hump anaylsis article
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

import toolset.BoilerPlateImports  # Surpresses the boilerplate errors

govData = govDataClass(True, "England")  # Load the data
funcs = functions()

cases = govData.get_new_cases()
deaths = govData.get_new_deaths()
hospital_cases = govData.get_hospital_cases()

#Clip the data by using just the last 180 days worth
days_to_sub = 180

cases = funcs.get_last_records(days_to_sub, cases)
deaths = funcs.get_last_records(days_to_sub, deaths)
hospital_cases = funcs.get_last_records(days_to_sub, hospital_cases)
dates = funcs.get_last_records(days_to_sub, govData.get_gov_date_Series())

chart = CovidChart()

chart.clear_chart()
chart.set_chart_params(False, False, False, True)

chart.add_scatter_plot(dates, cases, "orange", "Cases", False, True, True)

chart.draw_chart("Date", "Cases", "COVID 19 - Cases", "twoHump_cases", True)

chart.clear_chart()
chart.add_scatter_plot(dates, hospital_cases, "purple", "Hospitalisations", False, True, False)
chart.draw_chart("Date", "Hospitalisations", "COVID 19 - Hospitalisations", "twoHump_hosp", True)

chart.clear_chart()
chart.add_scatter_plot(dates, deaths, "red", "Cases", False, True, False)
chart.draw_chart("Date", "Deaths", "COVID 19 - Deaths", "twoHump_deaths", True)

days_to_sub = 90

H1_deaths = funcs.get_first_records(days_to_sub, deaths)
H1_cases =  funcs.get_first_records(days_to_sub, cases)
H1_hos =  funcs.get_first_records(days_to_sub, hospital_cases)
H1_dates = funcs.get_first_records(days_to_sub, dates)

H2_deaths = funcs.get_last_records(days_to_sub, deaths)
H2_cases =  funcs.get_last_records(days_to_sub, cases)
H2_hos =  funcs.get_last_records(days_to_sub, hospital_cases)
H2_dates = funcs.get_last_records(days_to_sub, dates)

days = [0] * days_to_sub
for ii in range(0, days_to_sub):
    days[ii] = ii

#Deaths
chart.clear_chart()
H1_avg = "{:,}".format(int(np.sum(H1_deaths) / days_to_sub))
H2_avg = "{:,}".format(int(np.sum(H2_deaths) / days_to_sub))

chart.add_scatter_plot(days, H1_deaths, "red", "Deaths - Hump 1; Daily Average " + str(H1_avg) + "; Total " + str("{:,}".format(int(np.sum(H1_deaths)))), False, True, False)
chart.add_scatter_plot(days, H2_deaths, "red", "Deaths - Hump 2; Daily Average " + str(H2_avg) + "; Total " + str("{:,}".format(int(np.sum(H2_deaths)))), True, True, False)
chart.draw_chart("Date", "Deaths", "COVID 19 - Death Comparison Hump 1 vs Hump 2", "twoHump_Death_Comp", True)

#Cases and Hosp
chart.clear_chart()

H1_avg = "{:,}".format(int(np.sum(H1_cases) / days_to_sub))
H2_avg = "{:,}".format(int(np.sum(H2_cases) / days_to_sub))

chart.add_scatter_plot(days, H1_cases, "orange", "Cases - Hump 1; Daily Average " + str(H1_avg) + "; Total " + str("{:,}".format(int(np.sum(H1_cases)))), False, True, False)
chart.add_scatter_plot(days, H2_cases, "orange", "Cases - Hump 2; Daily Average " + str(H2_avg) + "; Total " + str("{:,}".format(int(np.sum(H2_cases)))), True, True, False)
chart.draw_chart("Date", "Cases", "COVID 19 - Cases Comparison Hump 1 vs Hump 2", "twoHump_case_Comp", True) 

chart.clear_chart()

H1_avg = "{:,}".format(int(np.sum(H1_hos) / days_to_sub))
H2_avg = "{:,}".format(int(np.sum(H2_hos) / days_to_sub))

chart.add_scatter_plot(days, H1_hos, "purple", "Hospital Cases - Hump 1; Daily Average " + str(H1_avg) + "; Total " + str("{:,}".format(int(np.sum(H1_hos)))), False, True, False)
chart.add_scatter_plot(days, H2_hos, "purple", "Hospital Cases - Hump 2; Daily Average " + str(H2_avg) + "; Total " + str("{:,}".format(int(np.sum(H2_hos)))), True, True, False)
chart.draw_chart("Date", "Hospitalisations", "COVID 19 - Hospitalisation Comparison Hump 1 vs Hump 2", "twoHump_hos_Comp", True) 

#Calc average age of death and average case age for each hump need to create the function first???????????



