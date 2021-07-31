#Custom Libs
import functions_load_Data as govDataset #Load the datasets
import functions_Chart as chart #Draws the chart woth certain data points such as lockdowns added

govDataset.get_Data() #This must be called before we can access any of the normal (non-aged) data from the load_Data module

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
def setupChart():
    global ax1
    fig, ax1 = plt.subplots()
   
def draw_Scatter_Cases_LFFT_PCR(): 

    setupChart()

    addedData = [0]*len(newLFDCases)
    for ii in range(0, len(newLFDCases)):
        addedData[ii] = newLFDCases[ii] + newLFDCasesConfPCR[ii]

    chart.addScatterplot(GOVdateSeries, addedData, 'violet', 'All Cases Found by LFTs')
    chart.addScatterplot(GOVdateSeries, newLFDCases,  'lightseagreen', 'Cases Found by LFT Only')
    chart.addScatterplot(GOVdateSeries, newLFDCasesConfPCR, 'orangered', 'Cases found by LFT With Conf PCR')
    chart.addScatterplot(GOVdateSeries, allPCR, 'seagreen', 'Cases found by PCR Only')
    chart.drawChart("Date","Number of Cases","COVID 19 Data - Cases Found Using PCR and LFT's", "casesPCRLFT", "false", "true", ax1, "true", "true") #Draws the chart with lockdowns etc drawn on

def addDatasets(set1, set2):
    newSet = set1.copy()
    for ii in range(len(set1)):
        newSet[ii] = set1[ii] + set2[ii]
    return newSet

def subDatasets(set1, set2):
    newSet = set1.copy()
    for ii in range(len(set1)):
        newSet[ii] = set1[ii] - set2[ii]
    return newSet

def calcRatio(set1, set2):
    newSet = set1.copy()
    for ii in range(len(set1)):
        newSet[ii] = set1[ii] / set2[ii]
        newSet[ii] = newSet[ii] * 100
    return newSet

def scaleData(data, scaleFactor):
    for ii in range(len(data)):
        data[ii] = data[ii] * scaleFactor
    return data

def draw_Scatter_PositivityRate():
    setupChart()
    chart.addScatterplot(GOVdateSeries,calcRatio(allPCR, totalPCR), 'steelblue', 'Positivity Rate PCR')
    chart.addScatterplot(GOVdateSeries,calcRatio(addDatasets(govDataset.newLFDCases, govDataset.positiveLFDconfirmedByPCR), totalLFD), 'darkolivegreen', 'Positivity Rate LFT''s')
    chart.addScatterplot(GOVdateSeries,calcRatio(newCases, addDatasets(p2Tests, p1Tests)), 'brown', 'Positivity Rate LFT & PCR')

    chart.drawChart("Date","Percentage of positive tests","COVID 19 Data - Positivity  Rate", "positivityRate", "false", "true", ax1, "true", "true") #Draws the chart with lockdowns etc drawn on

def draw_Scatter_pRate_Cases_deaths():
    setupChart()

    chart.addScatterplot(GOVdateSeries, scaleData(govDataset.newCases.copy(), 0.001), 'orange', 'C19 Cases in Thousands')
    chart.addScatterplot(GOVdateSeries,scaleData(govDataset.newDeaths.copy(), 0.01), 'red', 'C19 Deaths in Hundreds')
    plt.bar(GOVdateSeries, scaleData(govDataset.newDeaths.copy(), 0.01),  color = 'red', alpha = 0.2)

    chart.addScatterplot(GOVdateSeries,calcRatio(newCases, addDatasets(p2Tests, p1Tests)), 'brown', 'Positivity Rate LFT & PCR')

    chart.drawChart("Date","Percentage of Positive Tests, Number of Cases and Deaths (Scaled)","COVID 19 Data - Positivity  Rate, Cases and Deaths", "pRateCasesDeaths", "false", "true", ax1, "true", "true") #Draws the chart with lockdowns etc drawn on

def draw_Scatter_Tests_Conducted():
    setupChart()
    plt.bar(GOVdateSeries, totalLFD,  color = 'violet', alpha = 0.4)
    chart.addScatterplot(GOVdateSeries,totalLFD, 'violet', 'Pillar 1 & 2 Tests LFT Only')
    chart.addScatterplot(GOVdateSeries,totalPCR, 'darkslategray', 'Pillar 1 & 2 Tests PCR Only')
    chart.addScatterplot(GOVdateSeries,p1Tests, 'chocolate', 'Pillar 1 Tests PCR')
    chart.drawChart("Date","Number of Tests","COVID 19 Data - Tests Conducted Pillar 1 and 2", "testsConducted", "false", "true", ax1, "true", "true") #Draws the chart with lockdowns etc drawn on
