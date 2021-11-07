from COVIDTOOLSET import LoadDataSets as govDataClass
from COVIDTOOLSET import CovidChart as COVIDchart
from COVIDTOOLSET import GetCOVIDData as getData
from COVIDTOOLSET import Functions as COVIDFUNCS
from COVIDTOOLSET import Dashboard as DASH

#pullData = getData("England")
govData = govDataClass('true')
dates = govData.getGOVdateSeries()
ageDates = govData.getAgedGOVdateSeries()
data = govData.getCumSecondDose()

chart = COVIDchart()
funcs = COVIDFUNCS()

chart.clearChart()

chart.setChartParams("false","false","false","true")
chart.clearChart()

for ii in range(0,50):
    print (govData.getAgedDeathData(15))

dash = DASH()
imageString = ["images/totals.png", "images/test1.png","images/test2.png","images/test3.png","images/test4.png","images/test5.png"]
#imageString = ["images/test1.png","images/test2.png","images/test3.png","images/test4.png","images/test5.png"]


#Does not work with images of different height
dash.createDashboard("COVID-19 Dashboard 90 Day History (England)", imageString, "TESTDASH")

####
#
#
# CREATE TABLE TESTING
# WORKS WITH AN ARRAY OF LIST VALUES
# NEED TO ADD A TABLE TITLE IN THE MAIN METHOD
#
'''
totals = [0] * 19
totalDeaths = [0] * 19

for ii in range(19):
    totals[ii] = sum(govData.getAgedCaseData(ii))
    totalDeaths[ii] = sum(govData.getAgedDeathData(ii))

mdLIST = [govData.getAgeCatStringArray(), totals, totalDeaths]

rowlbl = ['EMPTY', 'Cases', 'Deaths', 'test'] #row labels

dash.createTable(300, 400, 20, 20, mdLIST,'white', 'black', rowlbl, 'true', 'images/TESTDASH.png', 40 ,'true', "Test")

dd = [0] * 90
dates = [0] *90
dd = funcs.getLastRecords(90, govData.getNewCases())
dates = funcs.getLastRecords(90, govData.getGOVdateSeries())
print(dates)
print(len(dates))
'''
'''

import squarify


chart.clearChart()
ageCategoriesLabel = govData.getAgeCatStringArray()
totalCasesAllAges = 0
for ii in range (19):
    totalCasesAllAges = totalCasesAllAges + totData[ii]

percent = [0]*19
for ii in range(19):
    percent[ii] = (totData[ii] / totalCasesAllAges) * 100
    percent[ii] = str(round(percent[ii],2))
    ageCategoriesLabel[ii] = ageCategoriesLabel[ii] + " (" + str(percent[ii]) + "%)" 

squarify.plot(sizes=totData, label=ageCategoriesLabel, color=govData.getLineColourArray(), alpha=.8, bar_kwargs=dict(linewidth=0.5, edgecolor="black"))
'''