import functions_load_Data as dataAge #Loads age graduated data
import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added
import matplotlib.pyplot as plt

dataAge.get_Data()
lineColour = dataAge.lineColour
ageCategoriesString = dataAge.ageCategoriesString

agedCasesData = [0]*19
agedDeathsData = [0]*19

global ax1
fig, ax1 = plt.subplots()

for iii in range(0, 19):
    agedCasesData[iii] = dataAge.getData(iii, 'cases', 'true')
    agedDeathsData[iii] = dataAge.getData(iii, 'deaths', 'true')


filename = ""

for ii in range (10, 24):

    plt.cla()
    plt.clf()
    plt.ylim(ymax = 100)

    for iii in range(0, 19):
        LOBF_dataDeath =  chart.averagedValues(agedDeathsData[iii].copy(),7)
        LOBF_dataCases =  chart.averagedValues(agedCasesData[iii].copy(),7)
        #chart.addScatterplot(dataAge.GOVdateSeries , chart.calcRatios(agedDeathsData[iii], agedCasesData[iii], ii),lineColour[iii], ageCategoriesString[iii])
        chart.addScatterplot(dataAge.GOVdateSeries , chart.calcRatios(LOBF_dataDeath, LOBF_dataCases, ii),lineColour[iii], ageCategoriesString[iii])
        
    filename = ("test" + str(ii))
    chart.drawChart("Date", "Test",  "COVID 19 Data - Test", filename, "false", "true", ax1, "true", "true")

