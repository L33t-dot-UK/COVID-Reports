#Custom Libs
import functions_load_Data as govDataset #Load the datasets
import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added

govDataset.get_Data() #This must be called before we can access any of the normal (non-aged) data from the load_Data module

hospitalCases = govDataset.hospitalCases #Number of people in hospital with C-19
newAdmssions = govDataset.newAdmssions #New admissions to hospital with possitive C-19 test within the first 10 days
newCases = govDataset.newCases #C-19 possitive cases
newDeaths = govDataset.newDeaths #Deaths with C-19 on death certificate by date of death
pillarTwoTests = govDataset.pillarTwoTests #Total number of P2 tests that have been conducted
GOVdateSeries = govDataset.GOVdateSeries

#Draw the chart
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime

def draw_Daily_Growth_Rate():

    global ax1
    fig, ax1 = plt.subplots()

    #plt.gca()
    #plt.cla()
    #plt.close()
    chart.addScatterplot(GOVdateSeries, newCases, 'orange', 'New C19 Cases (All)') #Plot the cases data

    SF = 50000 #This is baseline
    sfA = newCases.copy()
    for ii in range(len (newCases)):
        sfA[ii] = SF

    LOBF_newCases =  chart.averagedValues(newCases.copy(),7)
    caseGR = LOBF_newCases.copy()

    #To calculate the growth rate we will use the 7 day average for cases rather than the raw case data in order to smooth out the growth rate trend line
    for ii in range(len(LOBF_newCases)):
        try:
            caseGR[ii] = float((LOBF_newCases[ii+1] / LOBF_newCases[ii]) * SF)
        except:
            caseGR[ii] = 0

    #plt.plot(GOVdateSeries, sfA, '--', color = 'grey', alpha = 0.5) # This is the Baseline at 50,000

    chart.addScatterplot(GOVdateSeries, caseGR, 'darkcyan', 'Cases Daily Growth Rate, 50,000 = Baseline')
    chart.addDashedLine(GOVdateSeries, sfA, 'grey', 'Baseline') # This is the Baseline at 50,000

    ax1.legend(loc='upper right', fontsize = chart.globalLegendFontSize)

    chart.drawChart("Date","Number of People","COVID 19 Data - Cases Daily Growth Rate", "gRateCases" ,"false", "false", ax1, "true", "true") #Draws the chart with lockdowns etc drawn on

