'''
Sandbox area to run adhock tests
'''
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

df1, df2 = loadData.getAgedDataFrames()

ageCats = loadData.getage_groupsLiteral()
colours = loadData.getline_colourArray()

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.getAgedDataDeaths(ageCats[ii]).mean()))
    chartz.add_scatter_plot(loadData.getAgedGOVdateSeries(), loadData.getAgedDataDeaths(ageCats[ii]), colours[ii], ageCats[ii], False, False)

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.getAgedDataCases(ageCats[ii]).mean()))

chartz.set_chart_params(True,False,False,True)
#chartz.add_scatter_plot(loadData.getAgedGOVdateSeries(), loadData.getAgedDataDeaths("90+"), "red", "", False, False)
chartz.draw_chart("", "", "", "test", True)
'''

from toolset.CovidDashboard import Dashboard as chart

chart = chart()

chart.create_PNG(1920, 1080,'testTable', 10)

label = ['', 'Cases', 'Deaths', 'CFR']
title_row = ['0-4', '5-9', '10-14']
data = [title_row,[20156,22514,30145],[0,1,2],['0%','0%','0%']]

chart.create_table(500, 200, 15, 15, data, "white", "black", label, False, "reports/images/testTable.png", 30, True, "Just a test table")



