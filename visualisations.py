'''

THIS CODE WAS USED TO CREATE VISUALISATION YOUTUBE VIDEOS THAT CAN BE VIEWed ON THE COVIDREPORTS.UK WEBSITE

'''


from COVIDTOOLSET import LoadDataSets as govDataClass
from COVIDTOOLSET import CovidChart as COVIDchart
from COVIDTOOLSET import GetCOVIDData as getData
from COVIDTOOLSET import Functions as COVIDFUNCS
from COVIDTOOLSET import Dashboard as DASH

pullData = getData("England")
govData = govDataClass('true')
dates = govData.getGOVdateSeries()
ageDates = govData.getAgedGOVdateSeries()
data = govData.getCumSecondDose()

chart = COVIDchart()
funcs = COVIDFUNCS()

chart.clearChart()

chart.setChartParams("false","false","false","true")
chart.clearChart()

ageDates = govData.getAgedGOVdateSeries()
print(len(ageDates))

for ii in range(0,50):
    print (govData.getAgedDeathData(15))

import numpy as np

cumData = [0] * 19

dataSTR = "Cases"
c = "orange"
max = 10000

chart.setChartParams("false", "false", "true", "false")

for ii in range (0, len(ageDates)):
    print(ii)
    chart.clearChart()
    chart.setMaxYvalue(max)

    total = 0
    for iii in range(0, 19):
        data = govData.getAgedCaseData(iii) #Change this for your data such as cases and deaths etc
        data = data[0:ii]
        cumData[iii] = np.sum(data)

        total = total + cumData[iii]

        chart.addScatterplot(govData.getAgedGOVdateSeries()[0:ii], data, govData.getLineColourArray()[iii], govData.getAgeCatStringArray()[iii], "false")

    actDate = ageDates[ii]

    total = '{:,}'.format(total)

    #chart.addBarChart(govData.getAgeCatStringArray(), cumData, c) #Use this for bar charts
    
    chart.drawChart("Date", "Number of " + dataSTR, "Evolution of COVID-19: " + dataSTR +  " Split by Age Groups (England) : Total " + dataSTR + " " + str(total), str(ii), "true") #Use this for time series graphs