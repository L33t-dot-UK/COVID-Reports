'''
COMPARING COVID DATA FOR THE 4 NATIONS OF THE UK

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


#pullDataEngland = getData("England") #get the latest data fro England
#pullDataScotland = getData("Scotland") #get the latest data fro England
#pullDataWales = getData("Wales") #get the latest data fro England
#pullDataNI = getData("Northern Ireland") #get the latest data fro England


govData_England = govDataClass(True, "England") #this object stores all downloaded data and loads it into memory when the argument is set to true
govData_Scotland = govDataClass(True, "Scotland") #this object stores all downloaded data and loads it into memory when the argument is set to true
govData_Wales = govDataClass(True, "Wales") #this object stores all downloaded data and loads it into memory when the argument is set to true
govData_NI = govDataClass(True, "Northern Ireland") #this object stores all downloaded data and loads it into memory when the argument is set to true

funcs = functions()

#cases Graph
chart = CovidChart()

nation_colour = ["red", "blue", "green", "orange"]

#----------------------------------------------------------------------------------------
#               SCATTER GRAPHS DEATHS, CASES, HOSPITALISATIONS
#----------------------------------------------------------------------------------------

chart.set_chart_params(False, False, True, True)
chart.add_scatter_plot(govData_England.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_England.get_new_cases(),"England"), nation_colour[0], "English Cases per Capita ", False,False, to_clip = True)
chart.add_scatter_plot(govData_Scotland.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Scotland.get_new_cases(),"Scotland"), nation_colour[1], "Scotish Cases per Capita ", False,False, to_clip = True)
chart.add_scatter_plot(govData_Wales.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Wales.get_new_cases(),"Wales"), nation_colour[2], "Welsh Cases per Capita ", False,False, to_clip = True)
chart.add_scatter_plot(govData_NI.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_NI.get_new_cases(),"Northern Ireland"), nation_colour[3], "NI Cases per Capita ", False,False, to_clip = True)

chart.draw_chart("Date", "Number of Cases Per Capita (clipped)", "COVID-19 Data - Daily Cases Four Nations" , "four_nations_overview_cases", True)

chart.clear_chart()

chart.add_scatter_plot(govData_England.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_England.get_new_deaths(),"England"), nation_colour[0], "English Deaths per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_Scotland.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Scotland.get_new_deaths(),"Scotland"), nation_colour[1], "Scotish Deaths per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_Wales.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Wales.get_new_deaths(),"Wales"), nation_colour[2], "Welsh Deaths per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_NI.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_NI.get_new_deaths(),"Northern Ireland"), nation_colour[3], "NI Deaths per Capita ", False,False, to_clip = False)

chart.draw_chart("Date", "Number of Deaths Per Capita", "COVID-19 Data - Daily Deaths Four Nations" , "four_nations_overview_deaths", True)


chart.clear_chart()

chart.add_scatter_plot(govData_England.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_England.get_hospital_cases(),"England"), nation_colour[0], "English Hospital Cases per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_Scotland.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Scotland.get_hospital_cases(),"Scotland"), nation_colour[1], "Scotish Hospital Cases per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_Wales.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_Wales.get_hospital_cases(),"Wales"), nation_colour[2], "Welsh Hospital Cases per Capita ", False,False, to_clip = False)
chart.add_scatter_plot(govData_NI.get_gov_date_Series(),funcs.calc_time_series_per_million_nation(govData_NI.get_hospital_cases(),"Northern Ireland"), nation_colour[3], "NI Hospital Cases per Capita ", False,False, to_clip = False)

chart.draw_chart("Date", "Hospital Cases Per Capita", "COVID-19 Data - Daily Hospital Cases Four Nations" , "four_nations_overview_hospital", True)

#----------------------------------------------------------------------------------------
#               BAR GRAPHS DEATHS, CASES, HOSPITALISATIONS (SUMMED UP DATA)
#----------------------------------------------------------------------------------------

chart.clear_chart()
chart.add_bar_chart(["England", "Scotland", "Wales", "NI"], [funcs.calc_per_million_nation(govData_England.get_new_cases(), "England"), funcs.calc_per_million_nation(govData_Scotland.get_new_cases(), "Scotland"),
    funcs.calc_per_million_nation(govData_Wales.get_new_cases(), "Wales"),funcs.calc_per_million_nation(govData_NI.get_new_cases(), "Northern Ireland")], "teal", "", display_vals= True)

chart.draw_chart("","Number of Cases per 1,000,000 People","COVID-19 - Four Nation Comparison Cases","four_nations_cases_bar", False)

chart.clear_chart()
chart.add_bar_chart(["England", "Scotland", "Wales", "NI"], [funcs.calc_per_million_nation(govData_England.get_new_deaths(), "England"), funcs.calc_per_million_nation(govData_Scotland.get_new_deaths(), "Scotland"),
    funcs.calc_per_million_nation(govData_Wales.get_new_deaths(), "Wales"),funcs.calc_per_million_nation(govData_NI.get_new_deaths(), "Northern Ireland")], "teal", "", display_vals= True)

chart.draw_chart("","Number of Deaths per 1,000,000 People","COVID-19 - Four Nation Comparison Deaths","four_nations_cases_bar_deaths", False)

chart.clear_chart()
chart.add_bar_chart(["England", "Scotland", "Wales", "NI"], [funcs.calc_per_million_nation(govData_England.get_hospital_cases(), "England"), funcs.calc_per_million_nation(govData_Scotland.get_hospital_cases(), "Scotland"),
    funcs.calc_per_million_nation(govData_Wales.get_hospital_cases(), "Wales"),funcs.calc_per_million_nation(govData_NI.get_hospital_cases(), "Northern Ireland")], "teal", "", display_vals= True)

chart.draw_chart("","Number of Hospital Cases per 1,000,000 People","COVID-19 - Four Nation Comparison Hospital Cases","four_nations_cases_bar_Hosp", False)

#----------------------------------------------------------------------------------------
#               YEARLY COMPS
#----------------------------------------------------------------------------------------

chart.clear_chart()
chart.draw_Scatter_Year_Comp(govData_England.get_new_deaths(), False, "English_Deaths", False, govData_England.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_England.get_hospital_cases(), False, "English_Hospitalisation", False, govData_England.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_England.get_new_cases(), False, "English_Cases", False, govData_England.get_year_dates(), True)

chart.clear_chart()
chart.draw_Scatter_Year_Comp(govData_Scotland.get_new_deaths(), False, "Scottish_Deaths", False, govData_Scotland.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_Scotland.get_hospital_cases(), False, "Scottish_Hospitalisation", False, govData_Scotland.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_Scotland.get_new_cases(), False, "Scottish_Cases", False, govData_Scotland.get_year_dates(), True)

chart.clear_chart()
chart.draw_Scatter_Year_Comp(govData_Wales.get_new_deaths(), False, "Welsh_Deaths", False, govData_Wales.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_Wales.get_hospital_cases(), False, "Welsh_Hospitalisation", False, govData_Wales.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_Wales.get_new_cases(), False, "Welsh_Cases", False, govData_Wales.get_year_dates(), True)

chart.clear_chart()
chart.draw_Scatter_Year_Comp(govData_NI.get_new_deaths(), False, "NI_Deaths", False, govData_NI.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_NI.get_hospital_cases(), False, "NI_Hospitalisation", False, govData_NI.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(govData_NI.get_new_cases(), False, "NI_Cases", False, govData_NI.get_year_dates(), True)