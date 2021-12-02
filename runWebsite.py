'''

COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

This script will use the COVIDTOOLSET to create graphs for https://www.COVIDreports.uk

The below code shows how the COVIDTOOLSET class can be used to easily produce graphs with autoimported data
for more information view the pyDoc html page included in this repo.

'''

#Import COVID Data with our COVIDTOOLSET
from numpy.core.shape_base import block
from numpy.lib import function_base
from COVIDTOOLSET import LoadDataSets as govDataClass
from COVIDTOOLSET import CovidChart as CovidChart
from COVIDTOOLSET import GetCOVIDData as getData
from COVIDTOOLSET import Functions as functions
from COVIDTOOLSET import Dashboard as DASH

import numpy as np

nation = "England" #If this is set to anything else Age profiled data will always be for England as it is not available for the other nations

pullData = getData(nation) #get the latest data
govData = govDataClass('true') #this object stores all downloaded data and loads it into memory when the argument is set to true

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
    chart.setChartParams("false","true","true","true")

    '''
    ------------------------ DRAW THE OVERVIEW CHART ------------------------
    '''
    data = govData.getNewCases() #Gets new cases
    chart.addScatterplot(nonAgeDates, data, "orange", "New COVID-19 Cases ", "false")

    data = govData.getHospitalCases() #Gets new deaths
    chart.addScatterplot(nonAgeDates, data, "indigo", "People in Hospital with COVID-19", "false")

    data = govData.getnewAdmssions() #Gets new hospital admissions
    chart.addScatterplot(nonAgeDates, data, "darkslategrey", "New COVID-19 Hospital Admissions", "false")

    data = govData.getNewDeaths() #Gets new deaths
    chart.addBarplot(nonAgeDates, data, "red", "New COVID-19 Deaths")

    chart.drawChart("Date", "Number of People", "COVID-19 Data - Hospital Cases, Hosptial Admissions, Cases and Deaths  (" + nation + ")" , "overview", "true")

    '''
    ------------------------ DRAW THE DEATHS CHART ------------------------
    '''
    chart.clearChart() #first clear old data from the chart

    data = govData.getNewDeaths() #Gets new deaths by death date
    chart.addBarplot(nonAgeDates, data, "red", "Death by Death Date")

    data = govData.getDeathsByReportDate() #Gets new deaths
    chart.addBarplot(nonAgeDates, data, "blue", "Death by Reported Date")

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Death Reported Date vs Death Date (" + nation + ")" , "deathsAndDeaths", "true") #create the chart


import numpy as np
def draw_Age_Deaths_Bar_Under_vs_Over(limit, firstAgeRange, secondAgeRange, title, filename):
    '''
    Draws a bar chart where deaths are compared from 2 age groups. These can be selected by the user.
    Example of how to call this is shown below;
        draw_Age_Deaths_Bar_Under_vs_Over(12, "Under 60's", "Over 60's", "COVID 19 - Age Profile of Deaths Under 60's Vs Over 60's","images/ageUnder60VSover.png")

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

    chart.drawChart("Age Ranges","Number of Deaths", title, filename, "false")

def growthRateGraph(xData, yData, colour, label, SF):

    sfA = yData.copy()
    for ii in range(len(sfA)):
        sfA[ii] = SF

    #We will calculate the growth rate for averaged values over a 7 day period to make the data look smoother
    LOBF_newCases =  chart.averagedValues(yData.copy(), 7)
    caseGR = LOBF_newCases.copy()

    #To calculate the growth rate we will use the 7 day average for cases rather than the raw case data in order to smooth out the growth rate trend line
    for ii in range(len(LOBF_newCases)):
        try:
            caseGR[ii] = float((LOBF_newCases[ii+1] / LOBF_newCases[ii]) * SF)
        except:
            caseGR[ii] = 0

    chart.addScatterplot(xData, caseGR, colour, label, 'false')
    chart.addScatterplot(xData, sfA, 'grey', 'Baseline', 'true') # This is the Baseline at 50,000

def page_02_Cases_Deaths(lLimit, hLimit):
    '''
    Creates graphs on the Cases and Deaths page

    12 Graphs enter details later

    '''
    #------------------------ GRAPH 1: CASES BY AGE ------------------------
    chart.setChartParams("false","false","true","true") #Change params we dont want the VLINE legend
    chart.clearChart()
    
    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group
        totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
        chart.addScatterplot(ageDates, data, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii] + " (" + str(totData[ii]) + ")", "false")
        

    fileName = "ageCases_" + str(lLimit) + "_" + str(hLimit)
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Cases by Age in " + nation, fileName, "true") #create the chart

    #------------------------ GRAPH 2: BAR CHART SHOWING CASES BY AGE ------------------------
    chart.setChartParams("false","false","false","true") #Change params we dont want the VLINE legend
    chart.clearChart()

    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group

    chart.addBarChart(govData.getAgeCatStringArray(), totData, "teal")
    chart.drawChart("Age Categories", "Number of People", "COVID 19 Data - Age Profile of Cases (" + nation + ")", "BarCases", "false") #create the chart 
        
    #------------------------ GRAPH 3: TREE MAP SHOWING CASES BY AGE ------------------------
    chart.clearChart()
    chart.setChartParams("false","false","false","true") #Change params we dont want the VLINE legend
    summedData = [0]* 19
    for ii in range(lLimit, hLimit):
        summedData[ii] = np.sum(govData.getAgedCaseData(ii))

    chart.addTreeMap(summedData, govData.getAgeCatStringArray(), govData.getLineColourArray())
    chart.drawChart("", "", "COVID 19 Data - Positive Cases by Age in " + nation, "TreemapCases", "false") #create the chart
    
    #------------------------ GRAPH 4: DEATHS BY AGE ------------------------
    chart.setChartParams("false","false","true","true") #Change params we dont want the VLINE legend
    chart.clearChart()
    
    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group
        totData[ii] = f'{totData[ii]:,}' #add a comma to make the numbers readable
        chart.addScatterplot(ageDates, data, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii] + " (" + str(totData[ii]) + ")", "false")
        
    fileName = "ageDeaths_" + str(lLimit) + "_" + str(hLimit)
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in " + nation, fileName, "true") #create the chart

    #------------------------ GRAPH 5: BAR CHART SHOWING DEATHS BY AGE ------------------------
    chart.setChartParams("false","false","false","true") #Change params we dont want the VLINE legend
    chart.clearChart()

    totData = [0]* 19

    for ii in range(lLimit, hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        totData[ii] = np.sum(data) #sum up cases in each age group

    chart.addBarChart(govData.getAgeCatStringArray(), totData, "teal")
    chart.drawChart("Age Categories", "Number of People", "COVID 19 Data - Age Profile of Deaths (" + nation + ")", "BarDeaths", "false") #create the chart 

    #------------------------ GRAPH 6: TREEMAP OF DEATHS ------------------------
    '''
    This tree map is alittle bit more complicated as were aggregating under 24 and under 50's deaths as they are really small
    '''
    chart.clearChart()
    chart.setChartParams("false","false","false","true") #Change params we dont want the VLINE legend
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
    chart.drawChart("", "", "COVID 19 Data - Deaths by Age in " + nation, "TreemapDeaths", "false") #create the chart

    #------------------------ GRAPH 7: BAR CHART SHOWING UNDER 60'S VS OVER 60'S------------------------
    chart.setChartParams("false","false","false","true")
    draw_Age_Deaths_Bar_Under_vs_Over(12, "Under 60's", "Over 60's", "COVID 19 - Age Profile of Deaths Under 60's Vs Over 60's  (" + nation + ")" ,"ageUnder60VSover")

    #------------------------ GRAPH 8: BAR CHART SHOWING UNDER 50'S VS OVER 50'S ------------------------
    chart.setChartParams("false","false","false","true")
    draw_Age_Deaths_Bar_Under_vs_Over(10, "Under 50's", "Over 50's", "COVID 19 - Age Profile of Deaths Under 50's Vs Over 50's  (" + nation + ")" ,"ageUnder50VSover")

    #------------------------ GRAPH 9: DAILY CASES BY AGE PER MILLION  ------------------------
    chart.setChartParams("false","false","true","true")
    chart.clearChart()

    for ii in range(lLimit, hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        permillionData = [0]*len(data)
        permillionData = funcs.calcTimeSeriesPerMillion(data, ii)

        chart.addScatterplot(ageDates, permillionData, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], "false")

    fileName = "ageCasesPerCapita" + "0" + "_" + "19"
    chart.drawChart("Dates", "Cases Per Million", "COVID 19 Data - Daily Cases Per Million by Age in " + nation, fileName, "true")

    #------------------------ GRAPH 10: DAILY DEATHS BY AGE PER MILLION  ------------------------
    chart.setChartParams("false","false","true","true")
    chart.clearChart()

    for ii in range(lLimit,hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        permillionData = [0]*len(data)
        permillionData = funcs.calcTimeSeriesPerMillion(data, ii)

        chart.addScatterplot(ageDates, permillionData, govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], "false")

    fileName = "ageDeathsPerCapita" + "0" + "_" + "19"
    chart.drawChart("Dates", "Deaths Per Million", "COVID 19 Data - Daily Deaths Per Million by Age in " + nation, fileName, "true")

    #------------------------ GRAPH 11: BAR CHART SHOWING CASES BY AGE PER MILLION  ------------------------
    chart.setChartParams("false","false","false","true")
    chart.clearChart()

    permillionData = [0]* 19
    for ii in range(lLimit,hLimit):
        data = govData.getAgedCaseData(ii) #Gets new cases
        permillionData[ii] = funcs.calcTotalPerMillion(data, ii)
    
    chart.addBarChart(govData.getAgeCatStringArray(), permillionData,  "teal")

    fileName = "age_Bar_Cases_per_Cap"
    chart.drawChart("Age Categories", "Cases Per Million", "COVID 19 Data - Age Profile of Total Cases Per Million (" + nation + ")", fileName, "false")
    #------------------------ GRAPH 12: BAR CHART SHOWING DEATHS BY AGE PER MILLION  ------------------------
    chart.setChartParams("false","false","false","true")
    chart.clearChart()

    permillionData = [0]* 19
    for ii in range(lLimit,hLimit):
        data = govData.getAgedDeathData(ii) #Gets new cases
        permillionData[ii] = funcs.calcTotalPerMillion(data, ii)

    chart.addBarChart(govData.getAgeCatStringArray(), permillionData,  "teal")
    fileName = "age_Bar_Deaths_per_Cap"
    chart.drawChart("Age Categories", "Deaths Per Million", "COVID 19 Data - Age Profile of Total Deaths Per Million (" + nation + ")", fileName, "false")

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

    dash.createTable(215, 50, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, 'true', 'images/totals.png', 40 ,'true', "Total Cases and Deaths (All Time)")
    
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

    dash.createTable(215, 525, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, 'true', 'images/totals.png', 40 ,'true', "Total Cases and Deaths (First 45 Days)")
    
    totalCases = [0] * 19
    totalDeaths = [0] * 19
    CFR = [0] * 19

    for ii in range(19):
        totalCases[ii] = sum(casesLast45[ii])
        totalDeaths[ii] = sum(deathsLast45[ii])

    CFR = funcs.calcRatioAsPercentage(totalDeaths , totalCases)
    
    dashData = [govData.getAgeCatStringArray(), totalCases, totalDeaths, CFR] #This is the data for the first table

    dash.createTable(215, 1000, 20, 20, dashData,'whitesmoke', 'pink', rowLabel, 'true', 'images/totals.png', 40 ,'true', "Total Cases and Deaths (Last 45 Days)")
    
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

    chart.setChartParams('false', 'false', 'false', 'false')
    chart.addBarplot(dates, CasesByReportDate, 'orange', 'Daily Cases (By Reported Date)')
    chart.addScatterplot(dates, peopleinHos, 'indigo', 'Number of People in Hospital (Scaled by 5)', 'false')
    chart.addScatterplot(dates, hosAdmins, 'darkslategrey', 'Number of Daily Admissions (Scaled by 10)', 'false')
    chart.drawChart('Date', 'Number of Cases (By Reported Date), Hospital Cases, Hospital Admission', 'Cases and Hospitalisations (Last 90 Days)', 'Dashboard_60_C_HC_HA', 'false')

    #Total Daily Deaths (Last 90 Days)
    chart.clearChart() #Clear the chart
    totalDeathsLast90 = funcs.getLastRecords(90, govData.getNewDeaths())
    totalDeathsRepLast90 = funcs.getLastRecords(90, govData.getDeathsByReportDate())
    chart.addBarplot(dates, totalDeathsLast90, 'red', 'Deaths by Death Date')
    #chart.addScatterplot(dates, totalDeathsRepLast90, 'pink', 'Deaths by Reported Date', 'false')
    chart.setChartParams('false', 'false', 'false', 'false')
    chart.drawChart('Date', 'Number of Deaths by Death Date', 'Total Daily Deaths (Last 90 Days)', 'Dashboard_60_Deaths', 'false')

    #Cases by Age Group
    chart.clearChart() #Clear the chart

    ageDate = funcs.getLastRecords(90, govData.getAgedGOVdateSeries())

    for ii in range(0, 19):
        chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')
        
    chart.drawChart('Date', 'Number of Cases', 'Total Daily Cases by Age Groups (Last 90 Days)', 'Dashboard_Cases_Age0_19', 'false')

    #Deaths by Age Group
    chart.clearChart() #Clear the chart

    for ii in range(0, 19):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups (Last 90 Days)', 'Dashboard_Deaths_Age0_19', 'false')

    #Deaths by Age Group under 50
    chart.clearChart() #Clear the chart

    for ii in range(0, 10):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups for Under 50s (Last 90 Days)', 'Dashboard_Deaths_Age0_10', 'false')

    #Deaths by Age Group over 50
    chart.clearChart() #Clear the chart

    for ii in range(10, 19):
        chart.addScatterplot(ageDate, deaths[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')
        
    chart.drawChart('Date', 'Number of Deaths', 'Total Daily Deaths by Age Groups for Over 50s (Last 90 Days)', 'Dashboard_Deaths_Age10_19', 'false')

    #Cases in the Extremely Vulnerable groups
    chart.clearChart() #Clear the chart
    
    for ii in range(14, 19):
        chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')

    chart.addScatterplot(ageDate, cases[ii], govData.getLineColourArray()[ii], govData.getAgeCatStringArray()[ii], 'false')

    chart.drawChart('Date', 'Number of Cases', 'Total Daily Cases in the Extremely Vulnerable Groups 70+ (Last 90 Days)', 'Dashboard_Cases_Age14_19', 'true')

    #-------------------------------------------------------------------------
    #-------------- Add the Tables and Graphs to the Dashboard ---------------
    #-------------------------------------------------------------------------

    #Now we can create the Dashboard with the above tables and graphs
    imageStr = ['images/totals.png', 'images/Dashboard_60_C_HC_HA.png', 'images/Dashboard_60_Deaths.png', 'images/Dashboard_Cases_Age0_19.png',
                'images/Dashboard_Deaths_Age0_19.png', 'images/Dashboard_Deaths_Age0_10.png', 'images/Dashboard_Deaths_Age10_19.png', 
                'images/Dashboard_Cases_Age14_19.png']

    dash.createDashboard('COVID-19 Data - Daily Cases, Deaths and Hospitalisations ' + nation + ' (90 Day History)', imageStr,'Dashboard_1')

def page_04_Testing():

    dates = govData.getGOVdateSeries()

    chart.setChartParams('false', 'true', 'true', 'true')

    #Positivity Rate
    chart.clearChart()
    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getPositivePCRtests(), govData.getNewPCRTests()), 'steelblue', 'Positivity Rate PCR', 'false')

    chart.addScatterplot(dates, funcs.calcRatioAsInt(funcs.addDatasets(govData.getNewLFDCases(), govData.getPositiveLFDconfirmedByPCR()), govData.getNewLFDTests()), 'darkolivegreen', 'Positivity Rate LFT''s', 'false')
    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getNewCases(), funcs.addDatasets(govData.getPillarTwoTests(), govData.getNewPillarOneTestsByPublishDate())), 'brown', 'Positivity Rate LFT & PCR', 'false')

    chart.drawChart("Date","Percentage of positive tests","COVID 19 Data - Positivity  Rate  " + nation, "positivityRate", "true") 

    #COVID 19 Data - Cases Found Using PCR and LFT's
    chart.clearChart()

    chart.addScatterplot(dates, govData.getPositiveLFDconfirmedByPCR(), 'orangered', 'Cases found by LFT With Conf PCR', 'false')
    chart.addScatterplot(dates, govData.getPositivePCRtests(), 'seagreen', 'Cases found by PCR Only', 'false')
    chart.addScatterplot(dates, govData.getNewLFDCases(),  'black', 'Cases Found by LFT Only', 'false')
    chart.drawChart("Date","Number of Cases","COVID 19 Data - Cases Found Using PCR and LFT's  " + nation, "casesPCRLFT", "true") 

    #COVID 19 Data - Positivity  Rate, Cases and Deaths
    chart.clearChart()

    chart.addScatterplot(dates, funcs.scaleData(govData.getNewCases(), 0.001), 'orange', 'C19 Cases in Thousands', 'false')
    chart.addScatterplot(dates, funcs.scaleData(govData.getNewDeaths(), 0.01), 'red', 'C19 Deaths in Hundreds', 'false')
    chart.addBarplot(dates, funcs.scaleData(govData.getNewDeaths(), 0.01), 'red', 'C19 Deaths in Hundreds')

    chart.addScatterplot(dates, funcs.calcRatioAsInt(govData.getNewCases(), funcs.addDatasets(govData.getPillarTwoTests(), govData.getNewPillarOneTestsByPublishDate())), 'brown', 'Positivity Rate LFT & PCR', 'false')
    chart.drawChart("Date","Percentage of Positive Tests, Number of Cases and Deaths (Scaled)","COVID 19 Data - Positivity  Rate, Cases and Deaths  " + nation, "pRateCasesDeaths", 'true') 

    #COVID 19 Data - Tests Conducted Pillar 1 and 2
    chart.clearChart()

    chart.addBarplot(dates, govData.getNewLFDTests(), 'violet', 'Total LFTs Conducted')

    chart.addScatterplot(dates,govData.getNewLFDTests(), 'violet', 'Pillar 1 & 2 Tests LFT Only', 'false')
    chart.addScatterplot(dates, govData.getNewPCRTests(), 'darkslategray', 'Pillar 1 & 2 Tests PCR Only', 'false')
    chart.addScatterplot(dates, govData.getNewPillarOneTestsByPublishDate(), 'chocolate', 'Pillar 1 Tests PCR', 'false')
    chart.drawChart("Date","Number of Tests","COVID 19 Data - Tests Conducted Pillar 1 and 2  " + nation, "testsConducted", 'true') 
 
def page_05_Lockdown():
    chart.clearChart()
    chart.setChartParams('false', 'true', 'true', 'true')
    dates = govData.getGOVdateSeries()

    growthRateGraph(dates, govData.getNewCases(), 'darkcyan', 'Growth Rate of Cases', 50000)
    chart.addScatterplot(dates, govData.getNewCases(), 'orange', 'New Cases', 'false' )

    chart.drawChart("Date","Number of People","COVID 19 Data - Cases Daily Growth Rate " + nation, "gRateCases", 'true') 

def add_Aged_Data(cat, lLimit, hLimit):
    '''
    This function will iterate through age cats and add the data together
    using the addDataSet Method
    '''
    aggData = [0] * len(govData.getAgedGOVdateSeries())

    for ii in range(lLimit, hLimit):
        if cat == 'deaths':
            data = govData.getAgedDeathData(ii)
        elif cat == 'cases':
            data = govData.getAgedCaseData(ii)

        aggData = funcs.addDatasets(aggData, data)

    aggDataStr = np.sum(aggData)
    aggDataStr = f'{aggDataStr:,}'
    return aggData, aggDataStr

def draw_Scatter_Aged_Death_Grouped():
    chart.clearChart()

    data, dataStr = add_Aged_Data("deaths",0,6)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[3], "Age Group:  0 - 29  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("deaths",6,10)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[7], "Age Group:  30 - 49  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("deaths",10,14)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[12], "Age Group: 50 - 69  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("deaths",14,19)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[16], "Age Group: 70+  (" + dataStr + ")", 'false')

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in England by Age Group", 'ageGroupDeaths', 'true')

def draw_Scatter_Aged_Cases_Grouped():
    chart.clearChart()

    data, dataStr = add_Aged_Data("cases",0,6)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[3], "Age Group:  0 - 29  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("cases",6,10)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[7], "Age Group:  30 - 49  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("cases",10,14)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[12], "Age Group: 50 - 69  (" + dataStr + ")", 'false')

    data, dataStr = add_Aged_Data("cases",14,19)
    chart.addScatterplot(govData.getAgedGOVdateSeries(), data, govData.getLineColourArray()[16], "Age Group: 70+  (" + dataStr + ")", 'false')

    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Cases by Age in England by Age Group", 'ageGroupCases', 'true')

def page_06_Vaccinations():
    dash = DASH()
    
    chart.draw_Scatter_Year_Comp(govData.getNewCases(), 'false', 'Cases', 'false', govData.getYearDates(), 'false')
    chart.draw_Scatter_Year_Comp(govData.getNewDeaths(), 'false', 'Deaths', 'false', govData.getYearDates(), 'false')
    chart.draw_Scatter_Year_Comp(govData.getnewAdmssions(), 'false', 'Hospital_Admissions', 'false', govData.getYearDates(), 'false')
    chart.draw_Scatter_Year_Comp(govData.getHospitalCases(), 'false', 'Hospital_Cases', 'false', govData.getYearDates(), 'false')

    #Now put the above images side by side
    img = ['images/yearlyCompCases.png', 'images/yearlyCompDeaths.png', 'images/yearlyCompHospital_Admissions.png', 'images/yearlyCompHospital_Cases.png']
    dash.createDashboard('', img, 'yearCompCasesDeaths')    #This will put the images side by side

    chart.setChartParams("false","true","true","false")
    draw_Scatter_Aged_Death_Grouped()
    draw_Scatter_Aged_Cases_Grouped()

    img = ['images/ageGroupCases.png', 'images/ageGroupDeaths.png']
    dash.createDashboard('', img, 'agedGroupedData')    #This will put the images side by side
    

    #WIP
    
    for ii in range(0, 19): #Draw a year comp for each age group
        label = "CFR " + govData.getAgeCatStringArray()[ii]  
        data = funcs.CalcCFR(18, govData.getAgedDeathData(ii), govData.getAgedCaseData(ii))
        chart.draw_Scatter_Year_Comp(data, 'false', label, 'true', govData.getYearDates(), 'false')
    

    #WIP
    
    for ii in range(0, 19): #Draw a year comp for each age group
        label = "Cases " + govData.getAgeCatStringArray()[ii]  
        chart.draw_Scatter_Year_Comp(govData.getAgedCaseData(ii), 'false', label, 'false', govData.getYearDates(), 'false')
        label = "Deaths " + govData.getAgeCatStringArray()[ii]  
        chart.draw_Scatter_Year_Comp(govData.getAgedDeathData(ii), 'false', label, 'false', govData.getYearDates(), 'false')

        img = ['images/yearlyCompCases ' + govData.getAgeCatStringArray()[ii]  + '.png', 'images/yearlyCompDeaths ' + govData.getAgeCatStringArray()[ii]  + '.png']
        dash.createDashboard('', img, 'XXXyearCompVax' + str(ii))    #This will put the images side by side
    

    
def calcAgedCFR(lag):
    deaths, deathsStr = add_Aged_Data('deaths', 0, 6)
    cases, casesStr = add_Aged_Data('cases', 0, 6)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    CFRChart.addScatterplot(dates, data, govData.getLineColourArray()[3], 'Age Range: 0 - 29', 'false')

    deaths, deathsStr = add_Aged_Data('deaths', 6, 10)
    cases, casesStr = add_Aged_Data('cases', 6, 10)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    chart.addScatterplot(dates, data, govData.getLineColourArray()[7], 'Age Range: 30 - 49', 'false')

    deaths, deathsStr = add_Aged_Data('deaths', 10, 14)
    cases, casesStr = add_Aged_Data('cases', 10, 14)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    chart.addScatterplot(dates, data, govData.getLineColourArray()[12], 'Age Range: 50 - 69', 'false')

    deaths, deathsStr = add_Aged_Data('deaths', 14, 19)
    cases, casesStr = add_Aged_Data('cases', 14, 19)

    data = funcs.CalcCFR(lag, deaths, cases)
    dates = funcs.getFirstRecords((len(data)) , govData.getAgedGOVdateSeries())
    CFRChart.addScatterplot(dates, data, govData.getLineColourArray()[16], 'Age Range: 70+', 'false')

    CFRChart.setMaxYvalue(50)
    CFRChart.setChartParams('false', 'false', 'true', 'true')
    CFRChart.drawChart('Date', 'Case Fatality Ratio %', 'Case Fatality Ratio Between the Age Groups (18 Day Lag)', 'CFR18', 'true')

def Dashboard_2():
    chart.setChartParams('false', 'false', 'false', 'true')
    chart.clearChart()
    days = 14
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getnewCasesByReportDate()), 'orange')
    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Cases by Reported Date, Previous ' + str(days) + ' Days', 'test', 'false')

    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getHospitalCases()), 'indigo')
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getnewAdmssions()), 'darkslategrey')

    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Hospital Cases & Admissions, Previous ' + str(days) + ' Days', 'testp', 'false')

    chart.clearChart()
    days = 45
    agedCases, casesStr = add_Aged_Data('cases', 14, 19)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = add_Aged_Data('deaths', 14, 19)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Cases & Deaths in the Extremely Vulnerable 70+ Age Groups, Previous ' + str(days) + ' Days', 'testd', 'true')

    chart.clearChart()
    agedCases, casesStr = add_Aged_Data('cases', 10, 14)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = add_Aged_Data('deaths', 10, 14)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Cases & Deaths in the 50 - 69 Age Groups, Previous ' + str(days) + ' Days', 'teste', 'true')

    chart.clearChart()
    agedCases, casesStr = add_Aged_Data('cases', 0, 10)
    agedCases = funcs.getLastRecords(days, agedCases)

    agedDeaths, deathsStr = add_Aged_Data('deaths', 0, 10)
    agedDeaths = funcs.getLastRecords(days, agedDeaths)
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedCases, 'orange')
    chart.addBarChart(funcs.getLastRecords(days, govData.getAgedGOVdateSeries()), agedDeaths, 'red')
    chart.drawChart('Date', 'Cases', 'COVID 19 Data - Cases & Deaths in the under 50s Age Groups, Previous ' + str(days) + ' Days', 'testf', 'true')

    days = 14
    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getDeathsByReportDate()), 'pink')
    chart.drawChart('Date', 'Deaths', 'COVID 19 Data - Deaths by Report Date, Previous ' + str(days) + ' Days', 'testb', 'false')

    chart.clearChart()
    chart.addBarChart(funcs.getLastRecords(days, govData.getGOVdateSeries()), funcs.getLastRecords(days, govData.getNewDeaths()), 'red')
    chart.drawChart('Date', 'Deaths', 'COVID 19 Data - Deaths by Death Date, Previous ' + str(days) + ' Days', 'testc', 'false')

    img = ['images/test.png', 'images/testp.png', 'images/testb.png', 'images/testc.png', 'images/testf.png', 'images/teste.png', 'images/testd.png']

    dash = DASH()
    dash.createDashboard("Cases, Deaths and Hospitalisation (14 to 45 Day Review)", img, 'dashboard_2')

from BENCHMARK import Benchmark
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
calcAgedCFR(18)

Dashboard_2()
BENCH.benchEnd("TOTAL EXECUTION")





