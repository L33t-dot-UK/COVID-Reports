'''
Sandbox area to run adhock tests
'''

import pandas as pd
import matplotlib.pyplot as plt
from toolset.CovidChart import CovidChart as chart


from toolset.LoadDatasets import LoadDataSets as data

import numpy as np

agedGOVdataset =  pd.read_csv('data/autoimport/dataAge.csv') #load the aged dataset from the CSV file

agedGOVdataset.drop(agedGOVdataset.tail(32).index,inplace=True) #Remove the first daysToSub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
agedGOVdataset.fillna(0, inplace=True) #replace all null values with 0

agedGOVdataset.info()

print(agedGOVdataset.head())

loadData = data(True, "England")
chartz = chart()

#test = pd.DataFrame(agedGOVdataset["newCasesBySpecimenDateAgeDemographics"])
#print(test.head())

df1, df2 = loadData.getAgedDataFrames()

ageCats = loadData.getAgeGroupsLiteral()
colours = loadData.getLineColourArray()

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.getAgedDataDeaths(ageCats[ii]).mean()))
    chartz.addScatterplot(loadData.getAgedGOVdateSeries(), loadData.getAgedDataDeaths(ageCats[ii]), colours[ii], ageCats[ii], False, False)

for ii in range (0, len(ageCats)):
    print(str(ageCats[ii]) + ": " + str(loadData.getAgedDataCases(ageCats[ii]).mean()))

chartz.setChartParams(True,False,True,True)
#chartz.addScatterplot(loadData.getAgedGOVdateSeries(), loadData.getAgedDataDeaths("90+"), "red", "", False, False)
chartz.drawChart("", "", "", "test", True)



