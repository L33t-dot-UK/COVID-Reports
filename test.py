import functions_load_Data as dataAge #Loads age graduated data
import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added
import matplotlib.pyplot as plt

dataAge.get_Data()
lineColour = dataAge.lineColour
ageCategoriesString = dataAge.ageCategoriesString

agedCasesData = [0]*19
agedDeathsData = [0]*19

def return_Aged_Data(cat, lLimit, hLimit):
    dataSet = [0] * len(dataAge.getData(0, cat, 'true'))
    for ii in range(lLimit, hLimit):
        tmpDataCases = [0] * len(dataSet)
        tmpDataCases = dataAge.getData(ii, cat, 'true')

        for iii in range(len(dataSet)):
            dataSet[iii] = dataSet[iii] + tmpDataCases[iii]

    return dataSet

filename = ""

global ax1
fig, ax1 = plt.subplots()

def resizeArray(data, size):

    newdata = [0] * (len(data) - size)
    for ii in range(0, len(newdata)):
        newdata[ii] = data[ii]

    return data

for ii in range (18, 19):

    plt.ylim(ymax = 40)

    lowLimit = 0
    highLimit = 6

    LOBF_dataDeath =  chart.averagedValues(return_Aged_Data("deaths",lowLimit,highLimit),7)
    LOBF_dataCases =  chart.averagedValues(return_Aged_Data("cases",lowLimit,highLimit),7)

    chart.addScatterplotSubbed(dataAge.GOVdateSeries , chart.calcRatios(LOBF_dataDeath, LOBF_dataCases, ii), lineColour[3], "Age 0 - 29" , ii + 4)
    
    lowLimit = 6
    highLimit = 10

    LOBF_dataDeath =  chart.averagedValues(return_Aged_Data("deaths",lowLimit,highLimit),7)
    LOBF_dataCases =  chart.averagedValues(return_Aged_Data("cases",lowLimit,highLimit),7)


    chart.addScatterplotSubbed(dataAge.GOVdateSeries , chart.calcRatios(LOBF_dataDeath, LOBF_dataCases, ii), lineColour[7], "Age 30 - 49",ii + 4)
    
    lowLimit = 10
    highLimit = 14

    LOBF_dataDeath =  chart.averagedValues(return_Aged_Data("deaths",lowLimit,highLimit),7)
    LOBF_dataCases =  chart.averagedValues(return_Aged_Data("cases",lowLimit,highLimit),7)

    chart.addScatterplotSubbed(dataAge.GOVdateSeries , chart.calcRatios(LOBF_dataDeath, LOBF_dataCases, ii), lineColour[12], "Age 50 - 69",ii + 4)
    
    lowLimit = 14
    highLimit = 19

    LOBF_dataDeath =  chart.averagedValues(return_Aged_Data("deaths",lowLimit,highLimit),7)
    LOBF_dataCases =  chart.averagedValues(return_Aged_Data("cases",lowLimit,highLimit),7)

    chart.addScatterplotSubbed(dataAge.GOVdateSeries , chart.calcRatios(LOBF_dataDeath, LOBF_dataCases, ii), lineColour[16], "Age 70+", ii + 4)


    filename = ("CFR" + str(ii))
    chart.drawWideChart("Date", "CFR %",  "COVID 19 Data - Case Fatality Ratio (" + str(ii) + " Day Lag Between Cases and Deaths)", filename, "false", "true", ax1, "true", "true")
