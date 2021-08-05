#Custom Libs
import functions_load_Data as govDataset #Load the datasets
import functions_Chart as chart #Draws the chart woth certain data points such as lockdowns added

import math

govDataset.get_Data()

hospitalCases = govDataset.hospitalCases #Number of people in hospital with C-19
newAdmssions = govDataset.newAdmssions #New admissions to hospital with possitive C-19 test within the first 10 days
newCases = govDataset.newCases #C-19 possitive cases
newDeaths = govDataset.newDeaths #Deaths with C-19 on death certificate by date of death
p2Tests = govDataset.pillarTwoTests #Total number of P2 tests that have been conducted
p1Tests = govDataset.newPillarOneTestsByPublishDate #Total number of P1 tests that have been conducted
GOVdateSeries = govDataset.GOVdateSeries

allPCR = govDataset.positivePCRtests #Total number of all PCR tests P1 and P2 that are positive
totalPCR = govDataset.newPCRTests #Total number of all PCR tests P1 and P2 that have been conducted
newLFDCasesConfPCR = govDataset.positiveLFDconfirmedByPCR #LFTs that are positive and confirmed by PCR
totalLFD = govDataset.newLFDTests #Total LFTs conducted

newLFDCases = govDataset.newLFDCases #Total LFD positive cases not confirmed by PCR

#DRAWING THE CHART ------------------------------------------------------------------------------------------------------------------

#Draw the chart
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime

#ADDING THE DATA TO THE CHART ------------------------------------------------------------------------------------------------------


colours = ["brown", "olive", "orange", "orangered", "darkgreen", "teal"] #6 years of colours, if you have more than that add more colours

def draw_Scatter_Year_Comp(data, toShow, label):
    global ax1
    fig, ax1 = plt.subplots()

    #the first thing to do is to check how many years of data we have
    numberOfYears = float(len(data) / 365)
    numberOfYears = math.ceil(numberOfYears) #round up the number of years

    yDates = govDataset.yearDates


    for ii in range(numberOfYears):
        totals = 0

        #We will cycle through the years splitting the data as necessary
        if ((len(data) - ((ii + 1) * 365)) > 0): #Multiple years so dimension this for 1 year
            plotData = [0] * 365
        else: #Less than 1 year so dimension the array for what ever is left
            plotData = [0] * (len(data) - (365 * (ii)))

            nDates = [0] * len(plotData)
            for iv in range (0, len(plotData)):
                nDates[iv] = yDates[iv]
            
            yDates = nDates

        for iii in range(len(plotData)):
            plotData[iii] = data[iii + (365 * ii)]
            totals = totals + plotData[iii]

        yNum = ii + 1

        dailyAvg = totals / len(plotData)
        dailyAvg = int(dailyAvg)
        dailyAvg = "{:,}".format(dailyAvg)

        totals = int(totals) #Remove the decimal point
        totals = "{:,}".format(totals)
        chart.addScatterplot(yDates, plotData, colours[ii], "Year " + str(yNum) + " " + label + " (Total: " + str(totals) + " / Daily Avg: " + str(dailyAvg) + ")")

    ax1.legend(loc='upper left' , fontsize = chart.globalLegendFontSize)

    chart.drawChart("Date","Number of People","COVID 19 Data - Yearly Comp (" + label + ")", "yearlyComp" + label ,toShow , "false", ax1, "flase", "true") #Draws the chart with lockdowns etc drawn on

def draw_Comp_Graphs():
    draw_Scatter_Year_Comp(newAdmssions, "false", "Hospital_Admissions")
    draw_Scatter_Year_Comp(hospitalCases, "false", "People_in_Hospital_With_C19")
    draw_Scatter_Year_Comp(newCases, "false", "Cases")
    draw_Scatter_Year_Comp(newDeaths, "false", "Deaths")
