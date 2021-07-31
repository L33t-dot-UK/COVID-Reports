#Custom Libs
import functions_load_Data as govDataset #Load the datasets
import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added

govDataset.get_Data()

hospitalCases = govDataset.hospitalCases #Number of people in hospital with C-19
newAdmssions = govDataset.newAdmssions #New admissions to hospital with possitive C-19 test within the first 10 days
newCases = govDataset.newCases #C-19 possitive cases
newDeaths = govDataset.newDeaths #Deaths with C-19 on death certificate by date of death
pillarTwoTests = govDataset.pillarTwoTests #Total number of P2 tests that have been conducted

deathsByReportDate = govDataset.deathsByReportDate

GOVdateSeries = govDataset.GOVdateSeries

#Draw the chart
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime

def draw_Overview(toShow, toSave):
    '''
    Draws the overview graph showing;
        - Cases
        - People in Hospital
        - Hospital Admissions
        - Deaths
    '''

    plt.cla()
    plt.clf()

    fig, ax1 = plt.subplots()

    chart.addScatterplot(GOVdateSeries, newCases, 'orange', 'New C19 Cases (All)')
    chart.addScatterplot(GOVdateSeries, hospitalCases, 'indigo', 'People in Hospital with C19')
    chart.addScatterplot(GOVdateSeries, newAdmssions,'darkslategrey', 'Hospital Admissions')
    chart.addBarplot(GOVdateSeries, newDeaths, 'red', 'Deaths by Death Date')

    chart.drawChart("Date","Number of People","COVID 19 Data - Hospital Cases, Hosptial Admissions, General Cases and Deaths", "overview", toShow, toSave, ax1, "true", "true") #Draws the chart with lockdowns etc drawn on
    plt.close()

def draw_DeathsVdeaths(toShow, toSave):
    '''
    Draws a graph showing Death by Death Date and Death by Reported Date
    '''
    fig, ax1 = plt.subplots()
    #plt.cla()
    #plt.clf()

    #Normal Resolution Chart
    chart.addBarplot(GOVdateSeries, deathsByReportDate, 'blue', 'Deaths by Report Date')
    chart.addBarplot(GOVdateSeries, newDeaths, 'red', 'Deaths by Death Date')
    chart.drawChart("Date","Number of People","COVID 19 Data - Death Reported Date vs Death Date", "deathsAndDeaths",toShow, toSave, ax1, "true", "true") #Draws the chart with lockdowns etc drawn on

    #High Resolution Chart if this chart is shown the labels will be too big and look silly; only use high resolution to save HR images due to the amount of data being displayed
    fig, ax1 = plt.subplots()
    chart.addBarplot(GOVdateSeries, deathsByReportDate, 'blue', 'Deaths by Report Date')
    chart.addBarplot(GOVdateSeries, newDeaths, 'red', 'Deaths by Death Date')
    chart.drawChartHR("Date","Number of People","COVID 19 Data - Death Reported Date vs Death Date", "deathsAndDeathsHR",toShow, toSave, ax1, "true", "true") #Draws the chart with lockdowns etc drawn on
    plt.close()



