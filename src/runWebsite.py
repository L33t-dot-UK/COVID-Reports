'''

COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

This script will use the covid toolset to create graphs for https://www.COVIDreports.uk all grpahs
apart from the hospital data are produced here

The below code shows how the covid toolset that can be used to easily produce graphs with autoimported data
for more information view the pyDoc html page included in this repo at https://github.com/L33t-dot-UK/COVID-Reports.

The examples below with exception of the vaccination data use lists to draw the graphs
toolset.LoadDatasets can return data as a list or a dataframe depending on your needs.

toolset.readVaxData only returns data as a dataframe and not lists, for this you will need to convert them yourself.

'''

#Import COVID Data with our COVIDTOOLSET
from numpy.core.shape_base import block
from numpy.lib import function_base
import pandas as pd

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.DataFunctions import Functions as functions
from toolset.CovidDashboard import Dashboard as DASH
from toolset.ReadVaxData import readVaxData as vaxData
from toolset.BenchMark import Benchmark as Benchmark

import numpy as np

nation = "England" #If this is set to anything else Age profiled data will always be for England as it is not available for the other nations

pullData = getData(nation) #get the latest data
govData = govDataClass(True, nation) #this object stores all downloaded data and loads it into memory when the argument is set to true

nonAgeDates = govData.getGOVdateSeries() #Gets xAxis dataset
ageDates = govData.getAgedGOVdateSeries() #Gets xAxis dataset for graphs that split data by age groups

data = govData.getDeathsByReportDate() #Gets a dataset

chart = CovidChart() #This will be the chart object that we will use

funcs = functions()

def page_01_Overview():
    '''
    Creates graphs on the overview page

        -Graph 1 Overview; daily deaths, cases, hospital admissions AND people in hospital
        -Graph 2 Deaths vs Deaths; Shows deaths by death date and deaths by reported date
    '''
    chart.setChartParams(False,True,True,True)

    '''
    ------------------------ DRAW THE OVERVIEW CHART ------------------------
    '''
    data = govData.getNewCases() #Gets new cases
    chart.addScatterplot(nonAgeDates, data, "orange", "New COVID-19 Cases ", False, False)

    data = govData.getHospitalCases() #Gets new deaths
    chart.addScatterplot(nonAgeDates, data, "indigo", "People in Hospital with COVID-19", False, True)

    data = govData.getnewAdmssions() #Gets new hospital admissions
    chart.addScatterplot(nonAgeDates, data, "darkslategrey", "New COVID-19 Hospital Admissions", False, False)

    data = govData.getNewDeaths() #Gets new deaths
    chart.addBarplot(nonAgeDates, data, "red", "New COVID-19 Deaths")

    chart.drawChart("Date", "Number of People", "COVID-19 Data - Hospital Cases, Hosptial Admissions, Cases and Deaths  (" + nation + ")" , "overview", True)

    '''
    ------------------------ DRAW THE DEATHS CHART ------------------------
    '''
    chart.clearChart() #first clear old data from the chart

    data = govData.getNewDeaths() #Gets new deaths by death date
    chart.addBarplot(nonAgeDates, data, "red", "Death by Death Date")

    data = govData.getDeathsByReportDate() #Gets new deaths
    chart.addBarplot(nonAgeDates, data, "blue", "Death by Reported Date")

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Death Reported Date vs Death Date (" + nation + ")" , "deathsAndDeaths", True) #create the chart


import numpy as np
def draw_Age_Deaths_Bar_Under_vs_Over(limit, firstAgeRange, secondAgeRange, title, filename):
    '''
    Draws a bar chart where deaths are compared from 2 age groups. These can be selected by the user.
    Example of how to call this is shown below;
        draw_Age_Deaths_Bar_Under_vs_Over(12, "Under 60's", "Over 60's", "COVID 19 - Age Profile of Deaths Under 60's Vs Over 60's","reports/images/ageUnder60VSover.png")

    This funciton contains 5 arguments;
        - Cut off limit this is the age group where the cut off is i.e. comapring under and over 60's this would be set to 12 (age / 5) then round down
        - firstAgeRange is the label for the first bar in the graph
        - secondAgeRange is the label for the second bar on the graph
        - title is the graphs title
        - filename will be the name of the saved png file
    '''
    chart.clearChart()

    totalDeaths = [0]*19
    totalRangedDeaths = [0]*2
    ageRange = [0]*2

    ageRange[0] = firstAgeRange
    ageRange[1] = secondAgeRange

    totalDeathsAllAges = 0
    for ii in range(0, 19):
        data = govData.getAgedDeathData(ii) #Gets new Deaths
        totalDeaths[ii] = np.sum(data) #sum up deaths in each age group
        totalDeathsAllAges = totalDeathsAllAges + totalDeaths[ii]

    
    for ii in range(0, limit):
        try:
            totalRangedDeaths[0] = totalRangedDeaths[0] + totalDeaths[ii]    
        except:
            pass
    
    for ii in range(limit, 19):
        try:
            totalRangedDeaths[1] = totalRangedDeaths[1] + totalDeaths[ii]    
        except:
            pass
    
    chart.addBarChart(ageRange, totalRangedDeaths,  'teal')

    chart.drawChart("Age Ranges","Number of Deaths", title, filename, False)

def growthRateGraph(xData, yData, colour, label, SF):

    sfA = yData.copy()
    for ii in range(len(sfA)):
        sfA[ii] = SF

    #SF is scale factor and will be used to set the base line and amplify the growth rate so it can be plotted in the graph
    #We will calculate the growth rate for averaged values over a 7 day period to make the data look smoother
    LOBF_data =  chart.averagedValues(yData.copy(), 7)
    growthRate = LOBF_data.copy()

    #To calculate the growth rate we will use the 7 day average for cases rather than the raw case data in order to smooth out the growth rate trend line
    for ii in range(len(LOBF_data)):
        try:
            growthRate[ii] = (float((LOBF_data[ii+1] / LOBF_data[ii]) * (SF * 2)) - (SF))
        except:
            growthRate[ii] = 0

    
    chart.addScatterplot(xData, growthRate, colour, label, False, False)
    chart.addScatterplot(xData, sfA, 'grey', 'Baseline', True, False) # This is the Baseline

def page_02_Cases_Deaths(lLimit, hLimit):
    '''
    Creates graphs on the Cases and Deaths page

    12 Graphs enter details later

    '''
    #------------------------ GRAPH 1: CASES BY AGE ------------------------
    chart.setChartParams(False,False,True,True) #Change params we dont want the VLINE legend
    chart.clearChart()
    
    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group
        totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
        chart.addScatterplot(ageDates, data, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii] + " (" + str(totData[ii]) + ")", False, True)
        

    fileName = "ageCases_" + str(lLimit) + "_" + str(hLimit)
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Cases by Age in " + nation, fileName, True) #create the chart

    #------------------------ GRAPH 2: BAR CHART SHOWING CASES BY AGE ------------------------
    chart.setChartParams(False,False,False,True) #Change params we dont want the VLINE legend
    chart.clearChart()

    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group

    chart.addBarChart(govData.getAgeCatStringArray(), totData, "teal")
    chart.drawChart("Age Categories", "Number of People", "COVID 19 Data - Age Profile of Cases (" + nation + ")", "BarCases", False) #create the chart 
        
    #------------------------ GRAPH 3: TREE MAP SHOWING CASES BY AGE ------------------------
    chart.clearChart()
    chart.setChartParams(False,False,False,True) #Change params we dont want the VLINE legend
    summedData = [0]* 19
    for ii in range(lLimit, hLimit):
        summedData[ii] = np.sum(govData.getAgedCaseData(ii))

    chart.addTreeMap(summedData, govData.getAgeCatStringArray(), govData.getLineColourArray())
    chart.drawChart("", "", "COVID 19 Data - Positive Cases by Age in " + nation, "TreemapCases", False) #create the chart
    
    #------------------------ GRAPH 4: DEATHS BY AGE ------------------------
    chart.setChartParams(False,False,True,True) #Change params we dont want the VLINE legend
    chart.clearChart()
    
    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group
        totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
        chart.addScatterplot(ageDates, data, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii] + " (" + str(totData[ii]) + ")", False, True)
        
    fileName = "ageDeaths_" + str(lLimit) + "_" + str(hLimit)
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in " + nation, fileName, True) #create the chart

    #------------------------ GRAPH 5: BAR CHART SHOWING DEATHS BY AGE ------------------------
    chart.setChartParams(False,False,False,True) #Change params we dont want the VLINE legend
    chart.clearChart()

    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group

    chart.addBarChart(govData.getAgeCatStringArray(), totData, "teal")
    chart.drawChart("Age Categories", "Number of People", "COVID 19 Data - Age Profile of Deaths (" + nation + ")", "BarDeaths", False) #create the chart 

    #------------------------ GRAPH 6: TREEMAP OF DEATHS ------------------------
    '''
    This tree map is alittle bit more complicated as were aggregating under 24 and under 50's deaths as they are really small
    '''
    chart.clearChart()
    chart.setChartParams(False,False,False,True) #Change params we dont want the VLINE legend
    summedData = [0] * 11
    ageCats = [0] * 11
    colours = [0] * 11

    ageCats[0] = "< 25 "
    colours[0] = 'whitesmoke'
    ageCats[1] = "25 to 49"
    colours[1] = 'gray'
    for ii in range(0, 5): #All under 24
        summedData[0] = summedData[0] + np.sum(govData.getAgedDeathData(ii))

    for ii in range(5, 10): #All under 50's
        summedData[1] = summedData[1] + np.sum(govData.getAgedDeathData(ii))

    for ii in range(10,19):
        ageCats[ii - 8] = govData.getAgeCatStringArray()[ii]
        colours[ii - 8] = govData.getLineColourArray()[ii]
        summedData[ii - 8] = np.sum(govData.getAgedDeathData(ii))

    chart.addTreeMap(summedData, ageCats, colours)
    chart.drawChart("", "", "COVID 19 Data - Deaths by Age in " + nation, "TreemapDeaths", False) #create the chart

    #------------------------ GRAPH 7: BAR CHART SHOWING UNDER 60'S VS OVER 60'S------------------------
    chart.setChartParams(False,False,False,True)
    draw_Age_Deaths_Bar_Under_vs_Over(12, "Under 60's", "Over 60's", "COVID 19 - Age Profile of Deaths Under 60's Vs Over 60's  (" + nation + ")" ,"ageUnder60VSover")

    #------------------------ GRAPH 8: BAR CHART SHOWING UNDER 50'S VS OVER 50'S ------------------------
    chart.setChartParams(False,False,False,True)
    draw_Age_Deaths_Bar_Under_vs_Over(10, "Under 50's", "Over 50's", "COVID 19 - Age Profile of Deaths Under 50's Vs Over 50's  (" + nation + ")" ,"ageUnder50VSover")

    #------------------------ GRAPH 9: DAILY CASES BY AGE PER MILLION  ------------------------
    chart.setChartParams(False,False,True,True)
    chart.clearChart()

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        permillionData = [0]*len(data)
        permillionData = funcs.calcTimeSeriesPerMillion(data, ii)

        chart.addScatterplot(ageDates, permillionData, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)

    fileName = "ageCasesPerCapita" + "0" + "_" + "19"
    chart.drawChart("Dates", "Cases Per Million", "COVID 19 Data - Daily Cases Per Million by Age in " + nation, fileName, True)

    #------------------------ GRAPH 10: DAILY DEATHS BY AGE PER MILLION  ------------------------
    chart.setChartParams(False,False,True,True)
    chart.clearChart()

    for ii in range(lLimit,hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        permillionData = [0]*len(data)
        permillionData = funcs.calcTimeSeriesPerMillion(data, ii)

        chart.addScatterplot(ageDates, permillionData, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)

    fileName = "ageDeathsPerCapita" + "0" + "_" + "19"
    chart.drawChart("Dates", "Deaths Per Million", "COVID 19 Data - Daily Deaths Per Million by Age in " + nation, fileName, True)

    #------------------------ GRAPH 11: BAR CHART SHOWING CASES BY AGE PER MILLION  ------------------------
    chart.setChartParams(False,False,False,True)
    chart.clearChart()

    permillionData = [0]* 19
    for ii in range(lLimit,hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        permillionData[ii] = funcs.calcTotalPerMillion(data, ii)
    
    chart.addBarChart(govData.getAgeCatStringArray(), permillionData,  "teal")

    fileName = "age_Bar_Cases_per_Cap"
    chart.drawChart("Age Categories", "Cases Per Million", "COVID 19 Data - Age Profile of Total Cases Per Million (" + nation + ")", fileName, False)
    #------------------------ GRAPH 12: BAR CHART SHOWING DEATHS BY AGE PER MILLION  ------------------------
    chart.setChartParams(False,False,False,True)
    chart.clearChart()

    permillionData = [0]* 19
    for ii in range(lLimit,hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        permillionData[ii] = funcs.calcTotalPerMillion(data, ii)

    chart.addBarChart(govData.getAgeCatStringArray(), permillionData,  "teal")
    fileName = "age_Bar_Deaths_per_Cap"
    chart.drawChart("Age Categories", "Deaths Per Million", "COVID 19 Data - Age Profile of Total Deaths Per Million (" + nation + ")", fileName, False)

def page_03_Dashboard():
    
    #-------------------------------------------------------------------------
    #------------------ Create the tables for the dashbaord ------------------
    #-------------------------------------------------------------------------

    #First we will create a png image to store the tables on
    dash = DASH()

    dash.createPNG(5000, 1500, 'totals', 56)
    
    totalCases = [0] * 19
    totalDeaths = [0] * 19
    CFR = [0] * 19

    for ii in range(19):
        totalCases[ii] = sum(govData.getAgedCaseData(ii))
        totalDeaths[ii] = sum(govData.getAgedDeathData(ii))

    CFR = funcs.calcRatioAsPercentage(totalDeaths , totalCases)

    rowLabel = ['EMPTY', 'Cases', 'Deaths', 'CFR']
    dashData = [govData.getAgeCatStringArray(), totalCases, totalDeaths, CFR] #This is the data for the first table

    dash.createTable(215, 50, 15, 20, dashData,'whitesmoke', 'pink', rowLabel, True, 'reports/images/totals.png', 40 ,True, "Total Cases and Deaths (All Time)")
    
    #Now we just want the last 90 Days
    cases = [0] * 19
    deaths = [0] * 19

    for ii in range(19):
        tmpCases = govData.getAgedCaseData(ii)
        tmpDeaths = govData.getAgedDeathData(ii)

        cases[ii] = funcs.getLastRecords(90, tmpCases)
        deaths[ii] = funcs.getLastRecords(90, tmpDeaths)

    #Now we want the first 45 days
    casesFirst45 = [0] * 19
    deathsFirst45 = [0] * 19
    for ii in range(19):
        tmpCases = cases[ii]
        tmpDeaths = deaths[ii]

        casesFirst45[ii] = funcs.getFirstRecords(45, tmpCases)
        deathsFirst45[ii] = funcs.getFirstRecords(45, tmpDeaths)
    
    #Now we want the last 45 days
    casesLast45 = [0] * 19
    deathsLast45 = [0] * 19

    for ii in range(19):
        tmpCases = cases[ii]
        tmpDeaths = deaths[ii]

        casesLast45[ii] = funcs.getLastRecords(45, tmpCases)
        deathsLast45[ii] = funcs.getLastRecords(45, tmpDeaths)

    #Now we can total the data and add to a table
    totalCases = [0] * 19
    totalDeaths = [0] * 19
    CFR = [0] * 19

    for ii in range(19):
        totalCases[ii] = sum(casesFirst45[ii])
        totalDeaths[ii] = sum(deathsFirst45[ii])

    CFR = funcs.calcRatioAsPercentage(totalDeaths , totalCases)
    
    dashData = [govData.getAgeCatStringArray(), totalCases, totalDeaths, CFR] #This is the data for the first table

    dash.createTable(215, 525, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, True, 'reports/images/totals.png', 40 ,True, "Total Cases and Deaths (First 45 Days)")
    
    totalCases = [0] * 19
    totalDeaths = [0] * 19
    CFR = [0] * 19

    for ii in range(19):
        totalCases[ii] = sum(casesLast45[ii])
        totalDeaths[ii] = sum(deathsLast45[ii])

    CFR = funcs.calcRatioAsPercentage(totalDeaths , totalCases)
    
    dashData = [govData.getAgeCatStringArray(), totalCases, totalDeaths, CFR] #This is the data for the first table

    dash.createTable(215, 1000, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, True, 'reports/images/totals.png', 40 ,True, "Total Cases and Deaths (Last 45 Days)")
    
    #-------------------------------------------------------------------------
    #-------------------- Create Graphs for the Dashboard --------------------
    #-------------------------------------------------------------------------
    #Now create the graphs for the dashboard
    chart.clearChart() #Clear the chart

    dates = funcs.getLastRecords(90, govData.getGOVdateSeries())

    #Cases and Hospitalisations (Last 90 Days)
    newCases = funcs.getLastRecords(90, govData.getNewCases())
    peopleinHos = funcs.getLastRecords(90, govData.getHospitalCases())
    hosAdmins = funcs.getLastRecords(90, govData.getnewAdmssions())

    peopleinHos = funcs.scaleData(peopleinHos, 5)
    hosAdmins = funcs.scaleData(hosAdmins, 10)

    CasesByReportDate = funcs.getLastRecords(90, govData.getnewCasesByReportDate())

    chart.setChartParams(False, False, False, False)
    chart.addBarplot(dates, CasesByReportDate, 'orange', 'Daily Cases (By Reported Date)')
    chart.addScatterplot(dates, peopleinHos, 'indigo', 'Number of People in Hospital (Scaled by 5)', False, False)
    chart.addScatterplot(dates, hosAdmins, 'darkslategrey', 'Number of Daily Admissions (Scaled by 10)', False, False)
    chart.drawChart('Date', 'Number of Cases (By Reported Date), Hospital Cases, Hospital Admission', 'Cases and Hospitalisations (Last 90 Days)', 'Dashboard_60_C_HC_HA', False)

    #Total Daily Deaths (Last 90 Days)
    chart.clearChart() #Clear the chart
    totalDeathsLast90 = funcs.getLastRecords(90, govData.getNewDeaths())
    totalDeathsRepLast90 = funcs.getLastRecords(90, govData.getDeathsByReportDate())
    chart.addBarplot(dates, totalDeathsLast90, 'red', 'Deaths by Death Date')
    #chart.addScatterplot(dates, totalDeathsRepLast90, 'pink', 'Deaths by Reported Date', False)
    chart.setChartParams(False, False, False, False)
    chart.drawChart('Date', 'Number of Deaths by Death Date', 'Total Daily Deaths (Last 90 Days)', 'Dashboard_60_Deaths', False)

    #Cases by Age Group
    chart.clearChart() #Clear the chart

    ageDate = funcs.getLastRecords(90, govData.getAgedGOVdateSeries())

    for ii in range(0, 19):
        chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)
        
    chart.drawChart('Date', 'Number of Cases', 'Total Daily Cases by Age Groups (Last 90 Days)', 'Dashboard_Cases_Age0_19', False)

    #Deaths by Age Group
    chart.clearChart() #Clear the chart

    for ii in range(0, 19):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups (Last 90 Days)', 'Dashboard_Deaths_Age0_19', False)

    #Deaths by Age Group under 50
    chart.clearChart() #Clear the chart

    for ii in range(0, 10):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups for Under 50s (Last 90 Days)', 'Dashboard_Deaths_Age0_10', False)

    #Deaths by Age Group over 50
    chart.clearChart() #Clear the chart

    for ii in range(10, 19):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups for Over 50s (Last 90 Days)', 'Dashboard_Deaths_Age10_19', False)

    #Cases in the Extremely Vulnerable groups
    chart.clearChart() #Clear the chart
    
    for ii in range(14, 19):
        chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)

    chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], False, True)

    chart.drawChart('Date', 'Number of Cases', 'Total Daily Cases in the Extremely Vulnerable Groups 70+ (Last 90 Days)', 'Dashboard_Cases_Age14_19', True)

    #-------------------------------------------------------------------------
    #-------------- Add the Tables and Graphs to the Dashboard ---------------
    #-------------------------------------------------------------------------

    #Now we can create the Dashboard with the above tables and graphs
    imageStr = ['reports/images/totals.png', 'reports/images/Dashboard_60_C_HC_HA.png', 'reports/images/Dashboard_60_Deaths.png', 'reports/images/Dashboard_Cases_Age0_19.png',
                'reports/images/Dashboard_Deaths_Age0_19.png', 'reports/images/Dashboard_Deaths_Age0_10.png', 'reports/images/Dashboard_Deaths_Age10_19.png', 
                'reports/images/Dashboard_Cases_Age14_19.png']

    dash.createDashboard('COVID-19 Data - Daily Cases, Deaths and Hospitalisations ' + nation + ' (90 Day History)', imageStr,'Dashboard_1')

def page_04_Testing():

    dates = govData.getGOVdateSeries()

    chart.setChartParams(False, True, True, True)

    #Positivity Rate
    chart.clearChart()
    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getPositivePCRtests(), govData.getNewPCRTests()), 'steelblue', 'Positivity Rate PCR', False, False)

    chart.addScatterplot(dates, funcs.calcRatioAsInt(funcs.addDatasets(govData.getNewLFDCases(), govData.getPositiveLFDconfirmedByPCR()), govData.getNewLFDTests()), 'darkolivegreen', 'Positivity Rate LFT''s', False, False)
    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getNewCases(), funcs.addDatasets(govData.getPillarTwoTests(), govData.getNewPillarOneTestsByPublishDate())), 'brown', 'Positivity Rate LFT & PCR', False, False)

    chart.drawChart("Date","Percentage of positive tests","COVID 19 Data - Positivity  Rate  " + nation, "positivityRate", True) 

    #COVID 19 Data - Cases Found Using PCR and LFT's
    chart.clearChart()

    chart.addScatterplot(dates, govData.getPositiveLFDconfirmedByPCR(), 'orangered', 'Cases found by LFT With Conf PCR', False, False)
    chart.addScatterplot(dates, govData.getPositivePCRtests(), 'seagreen', 'Cases found by PCR Only', False, False)
    chart.addScatterplot(dates, govData.getNewLFDCases(),  'black', 'Cases Found by LFT Only', False, False)
    chart.drawChart("Date","Number of Cases","COVID 19 Data - Cases Found Using PCR and LFT's  " + nation, "casesPCRLFT", True) 

    #COVID 19 Data - Positivity  Rate, Cases and Deaths
    chart.clearChart()

    chart.addScatterplot(dates, funcs.scaleData(govData.getNewCases(), 0.001), 'orange', 'C19 Cases in Thousands', False, False)
    chart.addScatterplot(dates, funcs.scaleData(govData.getNewDeaths(), 0.01), 'red', 'C19 Deaths in Hundreds', False, False)
    chart.addBarplot(dates, funcs.scaleData(govData.getNewDeaths(), 0.01), 'red', 'C19 Deaths in Hundreds')

    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getNewCases(), funcs.addDatasets(govData.getPillarTwoTests(), govData.getNewPillarOneTestsByPublishDate())), 'brown', 'Positivity Rate LFT & PCR', False, False)
    chart.drawChart("Date","Percentage of Positive Tests, Number of Cases and Deaths (Scaled)","COVID 19 Data - Positivity  Rate, Cases and Deaths  " + nation, "pRateCasesDeaths", True) 

    #COVID 19 Data - Tests Conducted Pillar 1 and 2
    chart.clearChart()

    chart.addBarplot(dates, govData.getNewLFDTests(), 'violet', 'Total LFTs Conducted')

    chart.addScatterplot(dates,govData.getNewLFDTests(), 'violet', 'Pillar 1 & 2 Tests LFT Only', False, False)
    chart.addScatterplot(dates, govData.getNewPCRTests(), 'darkslategray', 'Pillar 1 & 2 Tests PCR Only', False, False)
    chart.addScatterplot(dates, govData.getNewPillarOneTestsByPublishDate(), 'chocolate', 'Pillar 1 Tests PCR', False, False)
    chart.drawChart("Date","Number of Tests","COVID 19 Data - Tests Conducted Pillar 1 and 2  " + nation, "testsConducted", True) 
 
def page_05_Lockdown():
    chart.clearChart()
    chart.setChartParams(False, True, True, True)
    dates = govData.getGOVdateSeries()

    growthRateGraph(dates, govData.getNewCases(), 'darkcyan', 'Growth Rate of Cases', 100000)
    chart.addScatterplot(dates, govData.getNewCases(), 'orange', 'New Cases', False, False )

    chart.drawChart("Date","Number of People","COVID 19 Data - Cases Daily Growth Rate " + nation, "gRateCases", True) 

def draw_Scatter_Aged_Death_Grouped():
    chart.clearChart()

    data, dataStr = funcs.add_Aged_Data("deaths",0,6, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[3], "Age Group:  0 - 29  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("deaths",6,10, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[7], "Age Group:  30 - 49  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("deaths",10,14, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[12], "Age Group: 50 - 69  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("deaths",14,19, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[16], "Age Group: 70+  (" + dataStr + ")", False, False)

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in England by Age Group", 'ageGroupDeaths', True)

def draw_Scatter_Aged_Cases_Grouped():
    chart.clearChart()

    data, dataStr = funcs.add_Aged_Data("cases",0,6, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[3], "Age Group:  0 - 29  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("cases",6,10, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[7], "Age Group:  30 - 49  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("cases",10,14, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[12], "Age Group: 50 - 69  (" + dataStr + ")", False, False)

    data, dataStr = funcs.add_Aged_Data("cases",14,19, govData)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[16], "Age Group: 70+  (" + dataStr + ")", False, False)

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Cases by Age in England by Age Group", 'ageGroupCases', True)

def page_06_Vaccinations():
    dash = DASH()

    chart.draw_Scatter_Year_Comp(govData.getNewCases(), False, 'Cases', False, govData.getYearDates(), False)
    chart.draw_Scatter_Year_Comp(govData.getNewDeaths(), False, 'Deaths', False, govData.getYearDates(), False)
    chart.draw_Scatter_Year_Comp(govData.getnewAdmssions(), False, 'Hospital_Admissions', False, govData.getYearDates(), False)
    chart.draw_Scatter_Year_Comp(govData.getHospitalCases(), False, 'Hospital_Cases', False, govData.getYearDates(), False)

    #Now put the above images side by side
    img = ['reports/images/yearlyCompCases.png', 'reports/images/yearlyCompDeaths.png', 'reports/images/yearlyCompHospital_Admissions.png', 'reports/images/yearlyCompHospital_Cases.png']
    dash.createDashboard('', img, 'yearCompCasesDeaths')    #This will put the images side by side

    chart.setChartParams(False,True,True,False)
    draw_Scatter_Aged_Death_Grouped()
    draw_Scatter_Aged_Cases_Grouped()

    img = ['reports/images/ageGroupCases.png', 'reports/images/ageGroupDeaths.png']
    dash.createDashboard('', img, 'agedGroupedData')    #This will put the images side by side
    

    #WIP
    
    for ii in range(0, 19): #Draw a year comp for each age group
        label = "CFR " + govData.getAgeCatStringArray()[ii]  
        data = funcs.CalcCFR(18, govData.getAgedDeathData(ii), govData.getAgedCaseData(ii))
        chart.draw_Scatter_Year_Comp(data, False, label, True, govData.getYearDates(), False)
    

    #WIP
    
    for ii in range(0, 19): #Draw a year comp for each age group
        label = "Cases " + govData.getAgeCatStringArray()[ii]  
        chart.draw_Scatter_Year_Comp(govData.getAgedCaseData(ii), False, label, False, govData.getYearDates(), False)
        label = "Deaths " + govData.getAgeCatStringArray()[ii]  
        chart.draw_Scatter_Year_Comp(govData.getAgedDeathData(ii), False, label, False, govData.getYearDates(), False)

        img = ['reports/images/yearlyCompCases ' + govData.getAgeCatStringArray()[ii]  + '.png', 'reports/images/yearlyCompDeaths ' + govData.getAgeCatStringArray()[ii]  + '.png']
        dash.createDashboard('', img, 'XXXyearCompVax' + str(ii))    #This will put the images side by side
    
    #
    #
    #   THE BELOW CODE IS FOR THE VACCINATION DASHBOARD
    #

    vData = vaxData(nation)
    chart.setLegendBottom(False)

    numberofRecords = len(vData.getVaxAgedData(vData.getVaxAgeGroups()[0]))
    numberofRecords = numberofRecords - 1

    #Plot vaccine by age group
    chart.setChartParams(False, False, False, False, )
    chart.clearChart()
    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedFirstDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], vData.getVaxAgeGroups()[ii] + " (" + str(int(ratio_df[numberofRecords])) + "%)", False, True)

    
    chart.drawChart("Date", "Percentage of People Vaccinated in Each Age Group", "COVID-19: 1st Dose Administered by Age (Cumulative)", "VAX_1Dose", False)
    chart.clearChart()
    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedSecondDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], vData.getVaxAgeGroups()[ii] + " (" + str(int(ratio_df[numberofRecords])) + "%)", False, True)

    chart.drawChart("Date", "Percentage of People Vaccinated in Each Age Group", "COVID-19: 2nd Dose Administered by Age (Cumulative)", "VAX_2Dose", False)

    chart.clearChart()
    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedThirdInjectionByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], vData.getVaxAgeGroups()[ii] + " (" + str(int(ratio_df[numberofRecords])) + "%)", False, True)

    chart.drawChart("Date", "Percentage of People Vaccinated in Each Age Group", "COVID-19: 3rd Dose Administered by Age (Cumulative)", "VAX_3dose", False)


    chart.clearChart()
    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedFirstDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], "", False, True)
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedSecondDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], "", True, True)
        ratio_df = funcs.calcRatioAsInt(df["cumPeopleVaccinatedThirdInjectionByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
        chart.addScatterplot(df["date"].tolist(), ratio_df, govData.getLineColourArray()[ii], "", False, True)

    chart.drawChart("Date", "Percentage of People Vaccinated in Each Age Group", "COVID-19: All Doses Administered by Age", "VAX_ALLdose", True)

    #Daily total uptake
    chart.clearChart()
    populationSum = 0
    total_df = vData.getPackedData()
    date_df = vData.getVaxAgedData("90+") #Any agegroup will do

    complete_total_df = pd.DataFrame({"totalFirstJab": [], "totalSecondJab": [], "totalThirdJab": []})
    date = date_df["date"]

    date_list = date_df["date"].tolist() #This will be a list of dates to be used later


    for ii in range(0, len(date_df)):
        subset = total_df[total_df["date"] == date_list[ii]]
        totalValue1 = subset["newPeopleVaccinatedFirstDoseByVaccinationDate"].sum()
        totalValue2 = subset["newPeopleVaccinatedSecondDoseByVaccinationDate"].sum()
        totalValue3 = subset["newPeopleVaccinatedThirdInjectionByVaccinationDate"].sum()
        complete_total_df.loc[ii, "totalFirstJab"] = totalValue1
        complete_total_df.loc[ii, "totalSecondJab"] = totalValue2
        complete_total_df.loc[ii, "totalThirdJab"] = totalValue3

    print(complete_total_df.sample())

    chart.setChartParams(False, False, True, False)
    chart.addScatterplot(date_list, complete_total_df["totalFirstJab"], "firebrick", "Daily 1st Doses", False, True)
    chart.addScatterplot(date_list, complete_total_df["totalSecondJab"], "darkgoldenrod", "Daily 2nd Doses", False, True)
    chart.addScatterplot(date_list, complete_total_df["totalThirdJab"], "darkgreen", "Daily 3rd Doses", False, True)
    chart.addScatterplot(govData.getGOVdateSeries(), funcs.scaleData(govData.getNewCases(), 5), "orange", "Daily Cases (Scaled Up by 5)", True, False)
    chart.drawChart("Date", "Number of People", "COVID-19: Daily Vaccinations Administered and Cases (Scaled)", "VAX_DailyDosesCases", True)

    #CUMULATIVE total uptake
    chart.clearChart()
    for ii in range(0, len(date_df)):
        subset = total_df[total_df["date"] == date_list[ii]]
        totalValue1 = subset["cumPeopleVaccinatedFirstDoseByVaccinationDate"].sum()
        totalValue2 = subset["cumPeopleVaccinatedSecondDoseByVaccinationDate"].sum()
        totalValue3 = subset["cumPeopleVaccinatedThirdInjectionByVaccinationDate"].sum()
        complete_total_df.loc[ii, "totalFirstJab"] = totalValue1
        complete_total_df.loc[ii, "totalSecondJab"] = totalValue2
        complete_total_df.loc[ii, "totalThirdJab"] = totalValue3

    print(complete_total_df.sample())

    first_Dose = [0] * len(vData.getVaxAgeGroups())
    second_Dose = [0] * len(vData.getVaxAgeGroups())
    third_Dose =  [0] * len(vData.getVaxAgeGroups())

    first_DoseP = [0] * len(vData.getVaxAgeGroups())
    second_DoseP = [0] * len(vData.getVaxAgeGroups())
    third_DoseP =  [0] * len(vData.getVaxAgeGroups())

    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        first_Dose[ii] = df.iloc[numberofRecords, 4]
        second_Dose[ii] = df.iloc[numberofRecords, 6]
        third_Dose[ii] = df.iloc[numberofRecords, 8]

        first_DoseP[ii] = int((df.iloc[numberofRecords, 4] / df.iloc[numberofRecords, 1]) * 100)
        second_DoseP[ii] = int((df.iloc[numberofRecords, 6] / df.iloc[numberofRecords, 1]) * 100)
        third_DoseP[ii] = int((df.iloc[numberofRecords, 8] / df.iloc[numberofRecords, 1]) * 100)

    percent1st = "(" + str(int(np.sum(first_DoseP) / len(vData.getVaxAgeGroups()))) + "% " + "of Eligible Total Population)"
    percent2nd = "(" + str(int(np.sum(second_DoseP) / len(vData.getVaxAgeGroups()))) + "% " + "of Eligible Total Population)"
    percent3rd = "(" + str(int(np.sum(third_DoseP) / len(vData.getVaxAgeGroups()))) + "% " + "of Eligible Total Population)"

    chart.setChartParams(False, False, False, False)
    chart.addScatterplot(date_list, complete_total_df["totalFirstJab"], "firebrick", "Cumulative 1st Doses" + " (" + f'{int(complete_total_df["totalFirstJab"][numberofRecords]):,}' + ")" + percent1st, False, True)
    chart.addScatterplot(date_list, complete_total_df["totalSecondJab"], "darkgoldenrod", "Cumulative 2nd Doses" + " (" + f'{int(complete_total_df["totalSecondJab"][numberofRecords]):,}' + ")"+ percent2nd, False, True)
    chart.addScatterplot(date_list, complete_total_df["totalThirdJab"], "darkgreen", "Cumulative 3rd Doses" + " (" + f'{int(complete_total_df["totalThirdJab"][numberofRecords]):,}' + ")"+ percent3rd, False, True)
    chart.drawChart("Date", "Number of People", "COVID-19: Cumulative Administered Vaccinations, All Ages", "VAX_CUMDoses", False)


    dash = DASH()

    dash.createPNG(5600, 800, 'VAX_totals', 40)

    rowLabel = ['EMPTY', '1st Jab',  '1st Jab %', '2nd Jab', '2nd Jab %', '3rd Jab', '3rd Jab %']

    first_Dose = [0] * len(vData.getVaxAgeGroups())
    second_Dose = [0] * len(vData.getVaxAgeGroups())
    third_Dose =  [0] * len(vData.getVaxAgeGroups())

    first_DoseP = [0] * len(vData.getVaxAgeGroups())
    second_DoseP = [0] * len(vData.getVaxAgeGroups())
    third_DoseP =  [0] * len(vData.getVaxAgeGroups())

    for ii in range(0, len(vData.getVaxAgeGroups())):
        df = vData.getVaxAgedData(vData.getVaxAgeGroups()[ii])
        first_Dose[ii] = df.iloc[numberofRecords, 4]
        second_Dose[ii] = df.iloc[numberofRecords, 6]
        third_Dose[ii] = df.iloc[numberofRecords, 8]

        first_DoseP[ii] = str(int((df.iloc[numberofRecords, 4] / df.iloc[numberofRecords, 1]) * 100)) + "%"
        second_DoseP[ii] = str(int((df.iloc[numberofRecords, 6] / df.iloc[numberofRecords, 1]) * 100)) + "%"
        third_DoseP[ii] = str(int((df.iloc[numberofRecords, 8] / df.iloc[numberofRecords, 1]) * 100)) + "%"


    ageGroups = vData.getVaxAgeGroupsString()
    dashData = [ageGroups, first_Dose, first_DoseP, second_Dose, second_DoseP, third_Dose, third_DoseP] #This is the data for the first table

    dash.createTable(315, 20, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, True, 'reports/images/VAX_totals.png', 40 ,True, "Number and Percentage of Vaccinaiton Doses Given to Each Age Group")

    dashPics = ["reports/images/VAX_totals.png", "reports/images/VAX_CUMDoses.png", "reports/images/VAX_1Dose.png", "reports/images/VAX_2Dose.png", "reports/images/VAX_3Dose.png", 
                    "reports/images/VAX_ALLdose.png","reports/images/VAX_DailyDosesCases.png"]

    dash.createDashboard("Vaccination Dashboard", dashPics, "VAX_DASH")

    chart.setLegendBottom(True)
    
def calcAgedCFR(lag, yLimit):
    deaths, deathsStr = funcs.add_Aged_Data('deaths', 0, 6, govData)
    cases, casesStr = funcs.add_Aged_Data('cases', 0, 6, govData)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    
    CFRChart.addScatterplot(dates, data, govData.getLineColourArray()[3], 'Age Range: 0 - 29', False, True)

    deaths, deathsStr = funcs.add_Aged_Data('deaths', 6, 10, govData)
    cases, casesStr = funcs.add_Aged_Data('cases', 6, 10, govData)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    chart.addScatterplot(dates, data, govData.getLineColourArray()[7], 'Age Range: 30 - 49', False, True)

    deaths, deathsStr = funcs.add_Aged_Data('deaths', 10, 14, govData)
    cases, casesStr = funcs.add_Aged_Data('cases', 10, 14, govData)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    chart.addScatterplot(dates, data, govData.getLineColourArray()[12], 'Age Range: 50 - 69', False, True)

    deaths, deathsStr = funcs.add_Aged_Data('deaths', 14, 19, govData)
    cases, casesStr = funcs.add_Aged_Data('cases', 14, 19, govData)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    CFRChart.addScatterplot(dates, data, govData.getLineColourArray()[16], 'Age Range: 70+', False, True)

    CFRChart.setMaxYvalue(yLimit)
    CFRChart.setChartParams(False, False, True, True)
    CFRChart.drawChart('Date', 'Case Fatality Ratio %', 'Case Fatality Ratio Between the Age Groups (18 Day Lag)', 'CFR18', True)

def Dashboard_2():
    chart.setChartParams(False, False, False, False)
    chart.clearChart()
    days = 14 #14
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getnewCasesByReportDate()), 'orange')
    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Cases by Reported Date, Previous ' + str(days) + ' Days', 'test', False)

    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getHospitalCases()), 'indigo')
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getnewAdmssions()), 'darkslategrey')

    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Hospital Cases & Admissions, Previous ' + str(days) + ' Days', 'testp', False)

    chart.clearChart()
    days = 45 #Should be 45

    cases = funcs.getLastRecords(days, govData.getNewCases())
    deaths = funcs.getLastRecords(days, govData.getNewDeaths())

    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), cases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), deaths, 'red')

    cases = funcs.getLastRecords(5, govData.getNewCases())
    deaths = funcs.getLastRecords(5, govData.getNewDeaths())
    chart.addBarChart(funcs.getLastRecords(5, govData.getGOVdateSeries()), cases, 'grey')
    chart.addBarChart(funcs.getLastRecords(5, govData.getGOVdateSeries()), deaths, 'black')
    chart.drawChart('Date', 'Cases/Deaths', 'COVID 19 Data - Cases & Deaths by Specimen Date Previous ' + str(days) + ' Days (Last 5 Days Will be Incomplete)', 'testSpec', True)

    chart.clearChart()
    agedCases, casesStr = funcs.add_Aged_Data('cases', 14, 19, govData)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = funcs.add_Aged_Data('deaths', 14, 19, govData)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases/Deaths', 'COVID 19 Data - Cases & Deaths in the Extremely Vulnerable 70+ Age Groups, Previous ' + str(days) + ' Days', 'testd', True)

    chart.clearChart()
    agedCases, casesStr = funcs.add_Aged_Data('cases', 10, 14, govData)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = funcs.add_Aged_Data('deaths', 10, 14, govData)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases/Deaths', 'COVID 19 Data - Cases & Deaths in the 50 - 69 Age Groups, Previous ' + str(days) + ' Days', 'teste', True)

    chart.clearChart()
    agedCases, casesStr = funcs.add_Aged_Data('cases', 0, 10, govData)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = funcs.add_Aged_Data('deaths', 0, 10, govData)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases/Deaths', 'COVID 19 Data - Cases & Deaths in the under 50s Age Groups, Previous ' + str(days) + ' Days', 'testf', True)

    days = 14 #14
    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getDeathsByReportDate()), 'pink')
    chart.drawChart('Date', 'Deaths', 'COVID 19 Data - Deaths by Report Date, Previous ' + str(days) + ' Days', 'testb', False)

    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getNewDeaths()), 'red')
    chart.addBarChart(funcs.getLastRecords(10, govData.getGOVdateSeries()), funcs.getLastRecords(10, govData.getNewDeaths()), 'grey')
    chart.drawChart('Date', 'Deaths', 'COVID 19 Data - Deaths by Death Date (Incomplete Data), Previous ' + str(days) + ' Days', 'testc', False)

    img = ['reports/images/test.png', 'reports/images/testp.png', 'reports/images/testb.png', 'reports/images/testc.png', 'reports/images/testSpec.png','reports/images/testf.png', 'reports/images/teste.png', 'reports/images/testd.png']

    dash = DASH()
    dash.createDashboard("Cases, Deaths and Hospitalisation (14 to 45 Day Review)", img, 'dashboard_2')

BENCH = Benchmark() #Used for benchmarking
BENCH.setBench(True) #Bechmark output will be printed if this is set to true

BENCH.benchStart()


page_01_Overview()
page_02_Cases_Deaths(0, 19)
page_03_Dashboard()
page_04_Testing()
page_05_Lockdown()
page_06_Vaccinations()

CFRChart = CovidChart() #Use a different object because we change the max Y value
CFRChart.clearChart()

calcAgedCFR(18, 40)
Dashboard_2()




'''
#WIP FOR WAVE COMP
chart.setChartParams(False,False,True,True) #Change params we dont want the VLINE legend
chart.clearChart()

totData = [0]* 19

for ii in range(0, 5):
    data = govData.getAgedDeathData(ii) #Gets new cases
    totData[ii] = np.sum(data) #sum up cases in each age group
    totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
    chart.addScatterplot(ageDates, data, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii] + " (" + str(totData[ii]) + ")", False, True)
    
fileName = "ageDeaths_" + str(0) + "_" + str(5)
chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in " + nation, fileName, True) #create the chart
'''

BENCH.benchEnd("TOTAL EXECUTION")





