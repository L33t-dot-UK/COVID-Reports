'''
looking at testing data
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

chart = CovidChart()
vData = vax_data("England")
govData = govDataClass(True, "England")
funcs = functions()


totalPCR =  govData.get_new_PCR_tests().sum()
totalLFD = govData.get_new_LFD_tests().sum()

test_list = [totalPCR, totalLFD]
cat_list = ["PCR", "LFD"]

totalPCR_cases =  govData.get_positive_PCR_tests().sum()
totalLFD_cases = govData.get_new_LFD_cases().sum()

case_list = [totalPCR_cases, totalLFD_cases]

chart.add_bar_chart(cat_list, test_list, "orange")
chart.add_bar_chart(cat_list, case_list, "red")
chart.draw_chart("Test Type","Number of People", "COVID-19: Total Tests and Positive Cases", "testing_comp", False, False, False)


pcr_false_tests_min = totalPCR * 0.024 #false pos of 2.4%
pcr_false_tests_max = totalPCR * 0.05 #false pos of 5%

case_minus_flase_pos_min = totalPCR_cases - pcr_false_tests_min
case_minus_flase_pos_max = totalPCR_cases - pcr_false_tests_max

ratio_min = float(case_minus_flase_pos_min / totalPCR_cases)
ratio_max = float(case_minus_flase_pos_max / totalPCR_cases)

ratio_min = ratio_min * 100
ratio_max = ratio_max * 100

ratio_min = 100 - ratio_min
ratio_max = 100 - ratio_max

#ratio_min = str(ratio_min + "%")
#ratio_max = str(ratio_max + "%")

chart.clear_chart()
chart.set_chart_params(False, True, False, False)
chart.add_bar_chart(["2.4%", "5.0%"], [ratio_min , ratio_max], ["green", "red"], label = ["test 1", "test 2"], to_bar_over = True)
chart.draw_chart("False Positive Rate","Percentage of False Positives %", "COVID-19: Percentage of Cases that were False Positives", "test_false_pos_comp", False, False, False)