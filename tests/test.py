'''
Sandbox area to run adhock tests
'''
import sys
sys.path.append('./src/toolset')

import warnings
warnings.simplefilter(action='ignore', category=UserWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=FutureWarning) #surpress various warnings to do with dataframes if you want to see the warnings comment these lines

import geopandas as gpd

print (gpd.__version__)

'''
import pandas as pd
import matplotlib.pyplot as plt
from toolset.CovidChart import CovidChart as chart


from toolset.LoadDatasets import LoadDataSets as data

import numpy as np

agedGOVdataset =  pd.read_csv('data/autoimport/dataAge.csv') #load the aged dataset from the CSV file

agedGOVdataset.drop(agedGOVdataset.tail(32).index,inplace=True) #Remove the first days_to_sub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
agedGOVdataset.fillna(0, inplace=True) #replace all null values with 0

agedGOVdataset.info()

print(agedGOVdataset.head())

loadData = data(True, "England")
chartz = chart()

#test = pd.DataFrame(agedGOVdataset["newCasesBySpecimenDateAgeDemographics"])
#print(test.head())

df1, df2 = loadData.get_aged_data_frames()

ageCats = loadData.get_age_groups_literal()
colours = loadData.get_line_colour_list()

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.get_aged_data_deaths(ageCats[ii]).mean()))
    chartz.add_scatter_plot(loadData.get_aged_gov_date_series(), loadData.get_aged_data_deaths(ageCats[ii]), colours[ii], ageCats[ii], False, False)

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.get_aged_data_cases(ageCats[ii]).mean()))

chartz.set_chart_params(True,False,False,True)
#chartz.add_scatter_plot(loadData.get_aged_gov_date_series(), loadData.get_aged_data_deaths("90+"), "red", "", False, False)
chartz.draw_chart("", "", "", "test", True)
'''

'''
from toolset.CovidDashboard import Dashboard as chart

chart = chart()

chart.create_PNG(1920, 1080,'testTable', 10)

label = ['', 'Cases', 'Deaths', 'CFR']
title_row = ['0-4', '5-9', '10-14']
data = [title_row,[20156,22514,30145],[0,1,2],['0%','0%','0%']]

chart.create_table(500, 200, 15, 15, data, "white", "black", label, False, "reports/images/testTable.png", 30, True, "Just a test table")

from toolset.LoadDatasets import LoadDataSets as dataset

ds = dataset(True,"England")

df = ds.unpack_data("newCasesBySpecimenDateAgeDemographics")

print(df.info())

'''

from CovidChart import CovidChart as cht
from LoadDatasets import LoadDataSets as govDataClass

#from src.toolset.CovidChart import CovidChart as cht
import numpy as np

chart = cht()
govData = govDataClass(True, "England")

chart.set_chart_params(False,True,True,True)
chart.clear_chart()

totData = [0]* 19

for ii in range(0, 19):
    chart.clear_chart()
    data = govData.get_aged_death_data(ii) #Gets new cases
    totData[ii] = np.sum(data) #sum up deaths in each age group
    totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
    
    chart.add_bar_chart(govData.get_aged_gov_date_series(), data, "red", label = govData.get_age_cat_string_list()[ii] + " (" + str(totData[ii]) + ")", display_vals = False, to_bar_over = False)

    file_name = "XXX_ageCases_" + str(ii)
    chart.draw_chart("Date", "Number of Deaths", "COVID 19 Data - Daily Deaths for Age Group ("+ govData.get_age_cat_string_list()[ii] + ")", file_name, True) #create the chart
    




