import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added
import functions_load_Data as dataAge #Loads age graduated data

import pandas as pd
import matplotlib.pyplot as plt

from PIL import ImageFont, ImageDraw, Image, ImageOps #This lib will allow us to edit png images

ageCategoriesString = dataAge.ageCategoriesString

totalcases = [0]*19
ageRange = [0]*19
casesWeek = [0]*19

#Draw the table that shows cases broken down by age
def drawTable_AgeProfiledData():
    #We must first create the image that the tables will be added to
    img = Image.new('RGB', (5000, 1300), color = 'white')
    img = ImageOps.expand(img, border=2,fill='pink')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 56)
    d.text((2000,  30), "Total Cases and Deaths (All Time)", fill=(100,8,58), font=font)
    d.text((2000,  870), "Last 45 Days (RHS of the below graphs)", fill=(100,8,58), font=font)
    d.text((2000,  500), "First 45 Days (LHS of the below graphs)", fill=(100,8,58), font=font)

    img.save('images/totals.png') #We have now created an image with the titles and a border

    #We will now add the cases data
 
    for ii in range(19):
        totalcases[ii] = dataAge.getTotals(ii, 'cases', 'true')

    chart.drawRow(300, 140, 220, 100, ageCategoriesString.copy(), "gainsboro", "pink", "", "false", 'images/totals.png', 40)
    chart.drawRow(300, 240, 220, 100, totalcases.copy(), "whitesmoke", "pink", "Cases", "true", 'images/totals.png', 40)

    casesTotalWeek = [0]*19
    daysToGoBack = 45

    for ii in range(0, 19):
        casesWeek[ii] = dataAge.getSubData(ii, 'cases', 'true', dataAge.getDataLength() - daysToGoBack)
        casesTotalWeek[ii] = casesTotalWeek[ii] + sum(casesWeek[ii])

    chart.drawRow(300, 980, 220, 100, casesTotalWeek.copy(), "whitesmoke", "pink", "Cases", "true", 'images/totals.png', 40)

    casesWeek90 = [0]*19
    casesTotalWeek90 = [0]*19
    daysToGoBack = 90

    for ii in range(0, 19):
        casesWeek90[ii] = dataAge.getSubData(ii, 'cases', 'true', dataAge.getDataLength() - daysToGoBack)
        casesTotalWeek90[ii] = casesTotalWeek90[ii] + sum(casesWeek90[ii])
        casesTotalWeek90[ii] = casesTotalWeek90[ii] - casesTotalWeek[ii]
    
    chart.drawRow(300, 640, 220, 100, casesTotalWeek90.copy(), "whitesmoke", "pink", "Cases", "true", 'images/totals.png', 40)

    #Now add the death data to the tables
    totaldeaths = [0]*19
    deathsWeek = [0]*19

    for ii in range(19):
        totaldeaths[ii] = dataAge.getTotals(ii, 'deaths', 'true')
        ageRange[ii] = dataAge.getUnPackedData('true', 0)[0][ii]['age']


    img = Image.open('images/totals.png')
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 56)

    img.save('images/totals.png')

    chart.drawRow(300, 340, 220, 100, totaldeaths.copy(), "whitesmoke", "pink", "Deaths", "true", 'images/totals.png', 40)

    deathsWeek = [0]*19
    deathsTotalWeek = [0]*19
    daysToGoBack = 45

    for ii in range(0, 19):
        deathsWeek[ii] = dataAge.getSubData(ii, 'deaths', 'true', dataAge.getDataLength() - daysToGoBack)
        deathsTotalWeek[ii] = deathsTotalWeek[ii] + sum(deathsWeek[ii])

    chart.drawRow(300, 1080, 220, 100, deathsTotalWeek.copy(), "whitesmoke", "pink", "Deaths", "true", 'images/totals.png', 40)

    deathsWeek60 = [0]*19
    deathsTotalWeek60 = [0]*19
    daysToGoBack = 90

    for ii in range(0, 19):
        deathsWeek60[ii] = dataAge.getSubData(ii, 'deaths', 'true', dataAge.getDataLength() - daysToGoBack)
        deathsTotalWeek60[ii] = deathsTotalWeek60[ii] + sum(deathsWeek60[ii])
        deathsTotalWeek60[ii] = deathsTotalWeek60[ii] - deathsTotalWeek[ii]
        
    chart.drawRow(300, 740, 220, 100, deathsTotalWeek60.copy(), "whitesmoke", "pink", "Deaths", "true", 'images/totals.png', 40)

def setupCharts():
    global ax1
    fig, ax1 = plt.subplots()
    global fileName

def createChart(xAxis, yAxis, title, fileName):
    leg = ax1.legend(loc='upper left')
    chart.drawChart(xAxis, yAxis, title, fileName, "false", "false", ax1, "false", "false") #Draws the chart with lockdowns etc drawn on

def drawChart_DeathsOver50():
    setupCharts()
    daysToSub = len(dataAge.getData(0, 'deaths', 'true')) - 45

    for iii in range(10, 19):
        lbl = ageCategoriesString[iii]
        dataAge.getSubData(iii, 'deaths', 'true', daysToSub) #This must be called before calling addScatterPlot as the getSubData function also concats the govDatSeries array to the correct size
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getSubData(iii, 'deaths', 'true', daysToSub), dataAge.lineColour[iii], lbl)
    fileName = "ageDeaths_over50_45"
    createChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age for Over 50's in England", fileName)

def drawChart_DeathsUnder50():
    setupCharts()
    daysToSub = len(dataAge.getData(0, 'deaths', 'true')) - 45

    for iii in range(0, 10):
        lbl = ageCategoriesString[iii]
        dataAge.getSubData(iii, 'deaths', 'true', daysToSub) #This must be called before calling addScatterPlot as the getSubData function also concats the govDatSeries array to the correct size
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getSubData(iii, 'deaths', 'true', daysToSub), dataAge.lineColour[iii], lbl)

    fileName = "ageDeaths_under50_45"
    createChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age for Under 50's in England", fileName)

def drawChart_Deaths_Cases():
    setupCharts()

    for iv in range(19):
        print (str(iv) + " = " + str(ageCategoriesString[iv]))

    daysToSub = len(dataAge.getData(0, 'cases', 'true')) - 45

    for iii in range(0, 19):
        lbl = ageCategoriesString[iii]

        dataAge.getSubData(iii, 'cases', 'true', daysToSub)
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getSubData(iii, 'cases', 'true', daysToSub), dataAge.lineColour[iii], lbl)
        
    fileName = "Dashboard_Cases_Age" + str(0) + "_" + str(19)
    createChart("Date", "Cases", "Cases Broken Down into Age Groups", fileName)

    plt.clf()

    setupCharts()
    daysToSub = len(dataAge.getData(0, 'deaths', 'true')) - 45

    for iii in range(0, 19):
        lbl = ageCategoriesString[iii]

        dataAge.getSubData(iii, 'deaths', 'true', daysToSub)
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getSubData(iii, 'deaths', 'true', daysToSub), dataAge.lineColour[iii], lbl)

    fileName = "Dashboard_Deaths_Age" + str(0) + "_" + str(19)
    createChart("Date", "Deaths", "Deaths Broken Down into Age Groups", fileName)

def drawBar_Deaths_Cases():
    setupCharts()

    dataAge.get_Data()
    daysToSub = len(dataAge.getData(0, 'deaths', 'true')) - 90
    dataAge.reSizeDataSet(daysToSub)

    chart.addBarplot(dataAge.GOVdateSeries, dataAge.newCases, 'orange', label = 'New C19 Cases (All)')
    chart.addScatterplot(dataAge.GOVdateSeries, dataAge.hospitalCases, 'indigo', label = 'C19 People in Hospital')
    chart.addScatterplot(dataAge.GOVdateSeries, dataAge.newAdmssions, 'darkslategrey', label = 'Hospital Admissions')
    chart.drawChart("Date","Number of People","Cases and Hospitalisations", "Dashboard_60_C_HC_HA", "false", "true", ax1, "false", "false") #Draws the chart with lockdowns etc drawn on

    plt.clf()
    setupCharts()

    chart.addBarplot(dataAge.GOVdateSeries, dataAge.newDeaths, 'red', label = 'Deaths by Death Date')
    chart.drawChart("Date","Number of People","Total Daily Deaths", "Dashboard_60_Deaths", "false", "true", ax1, "false", "false") #Draws the chart with lockdowns etc drawn on

def mergeImages():
    from datetime import date
    from datetime import datetime

    img = Image.new('RGB', (5656, 7600), color = 'white')
    img = ImageOps.expand(img, border=2,fill='pink')

    d = ImageDraw.Draw(img)
    fontsize = 80
    font = ImageFont.truetype("arial.ttf", fontsize)


    im1 = Image.open('images/Dashboard_60_C_HC_HA.png')
    im2 = Image.open('images/Dashboard_60_Deaths.png')
    im3 = Image.open('images/Dashboard_Cases_Age0_19.png')
    im4 = Image.open('images/Dashboard_Deaths_Age0_19.png')
    im5 = Image.open('images/ageDeaths_under50_45.png')
    im6 = Image.open('images/ageDeaths_over50_45.png')
    im0 = Image.open('images/totals.png')

    #Must be in this order due to image overlap
    img.paste(im5, (40, 5400))
    img.paste(im6, (2848, 5400))
    img.paste(im3, (40, 3500))
    img.paste(im4, (2848, 3500))
    img.paste(im1, (40, 1600))
    img.paste(im2, (2848, 1600))

    img.paste(im0, (360, 300))

    d.text((1600,120), "COVID-19 Data - Dashboard Deaths and Cases 90 Day History (England)", fill=(100,8,58), font=font)

    from datetime import datetime
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    fontsize = 30
    font = ImageFont.truetype("arial.ttf", fontsize)  
    d.text((4600,7500), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=(100,8,58), font=font)

    img.save('images/Dashboard_1.png')

def createDashboard():
    drawTable_AgeProfiledData()
    drawChart_DeathsOver50()
    drawChart_DeathsUnder50()
    drawChart_Deaths_Cases()
    drawBar_Deaths_Cases()
    mergeImages()

