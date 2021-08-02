import functions_Chart as chart #Draws the chart with certain data points such as lockdowns added
import functions_load_Data as dataAge #Loads age graduated data

import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
import squarify

def setupChart():
    global ax1
    fig, ax1 = plt.subplots()
  
def draw_Scatter_Aged_Cases_per_Million(lLimit, hLimit):
    '''
    Creates a Scatter diagram of cases per million broken down into 5 year age groups
    You can decide the lower and upper age group via the lLimit and hLimit arguments
    Age groups are from 0 to 19 where 0 is under 5 and 19 is 90+
    '''
    plt.cla()
    plt.clf()

    setupChart()

    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    agedCasesData = [0]*hLimit
    population = dataAge.population

    for iii in range(lLimit, hLimit):
        agedCasesData[iii] = dataAge.getData(iii, 'cases', 'true')

    agedCasesPerMillion = agedCasesData.copy()

    #Now calculate daily cases per million
    for ii in range(lLimit, hLimit):
        for iii in range(len(agedCasesData[ii])):
            agedCasesPerMillion[ii][iii] = float(agedCasesData[ii][iii]) / float(population[ii])
       
    for iii in range(lLimit, hLimit):
        lbl = ageCategoriesString[iii]
        
        chart.addScatterplot(dataAge.GOVdateSeries, agedCasesPerMillion[iii], lineColour[iii], lbl)

    fileName = "ageCasesPerCapita" + str(lLimit) + "_" + str(hLimit)
    leg = ax1.legend(loc='upper left')
    chart.drawChart("Date", "Cases Per Million",  "COVID 19 Data - Daily Cases Per Million by Age in England", fileName, "false", "false", ax1, "true", "true")
    plt.close

def draw_Bar_Aged_Cases_per_Million():
    '''
    Creates a Bar chart of cases per million broken down into 5 year age groups
    You can decide the lower and upper age group via the lLimit and hLimit arguments
    Age groups are from 0 to 19 where 0 is under 5 and 19 is 90+
    '''

    ageCategoriesString = dataAge.ageCategoriesString
    totalAgedCases = [0]*19

    plt.cla()
    plt.clf()

    agedCasesData = [0]*19
    population = dataAge.population

    for iii in range(0, 19):
        agedCasesData[iii] = dataAge.getData(iii, 'cases', 'true')

    agedCasesPerMillion = agedCasesData.copy()

    #Now calculate daily cases per million
    for ii in range(0, 19):
        for iii in range(len(agedCasesData[ii])):
            agedCasesPerMillion[ii][iii] = float(agedCasesData[ii][iii]) / float(population[ii])
       
    for ii in range(0, 19):
        totalAgedCases[ii] = sum(agedCasesPerMillion[ii])

    plt.bar(ageCategoriesString, totalAgedCases,  color = 'teal', alpha = 1)

    value = 0
    
    for x in range(len(totalAgedCases)):
        value = "{:.4f}".format(totalAgedCases[x])
        label3 = value
        plt.annotate(label3, # this is the text
                     (ageCategoriesString[x],totalAgedCases[x]), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center

    plt.title("COVID 19 - Age Profile of Total Cases per 1,000,000", fontsize=12)
    plt.xlabel("Age Ranges", fontsize=10)
    plt.ylabel("Number of Cases per 1,000,000", fontsize=10)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.yticks(fontsize = 8)

    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig('images/age_Bar_Cases_per_Cap.png')
    chart.createTimeStamp('images/age_Bar_Cases_per_Cap.png', 980, 970, 12)
    plt.close
    
def draw_Scatter_Aged_Cases(lLimit, hLimit):
    '''
    Creates a Scatter diagram of cases broken down into 5 year age groups
    You can decide the lower and upper age group via the lLimit and hLimit arguments
    Age groups are from 0 to 19 where 0 is under 5 and 19 is 90+
    '''
    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    plt.cla()
    plt.clf()

    setupChart()

    #We don't need to load the data in this funciton as the dataAge.getTotals funciton will load it for us.
    for iii in range(lLimit, hLimit):
        lbl = dataAge.ageCategoriesString[iii] + " (" + str(dataAge.getTotals(iii, 'cases', 'true')) + ")"
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getData(iii, 'cases', 'true'), lineColour[iii], lbl)

    fileName = "ageCases_" + str(lLimit) + "_" + str(hLimit)
    leg = ax1.legend(loc='upper left')
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily cases by Age in England", fileName, "false", "false", ax1, "true", "true")

def draw_Age_Cases_Treemap():
    '''
    Draws a treemap showing cases in all age groups and calulates the percentage for each age group
    '''
    totalcases = [0]*19
    ageRange = [0]*19

    plt.cla()
    plt.clf()

    totalCasesAllAges = 0

    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    for ii in range (19):
        totalcases[ii] = dataAge.getTotals(ii, 'cases', 'true')
        totalCasesAllAges = totalCasesAllAges + totalcases[ii]

    ageCategoriesLabel = ageCategoriesString.copy()

    percent = [0]*19
    for ii in range(19):
        percent[ii] = (totalcases[ii] / totalCasesAllAges) * 100
        percent[ii] = str(round(percent[ii],2))
        ageCategoriesLabel[ii] = ageCategoriesLabel[ii] + " (" + str(percent[ii]) + "%)" 

    labels = ageCategoriesLabel
    sizes = totalcases
    colors = lineColour

    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8, bar_kwargs=dict(linewidth=0.5, edgecolor="black"))

    plt.axis('off')
    plt.title("COVID 19 - Positive Cases by Age in England")

    fileName = "TreemapCases"
    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig("images/" + fileName + '.png')
    chart.createTimeStamp("images/" + fileName + '.png', 980, 970, 12)
    plt.close

def draw_Scatter_Aged_Deaths_per_Million(lLimit, hLimit):
    '''
    Creates a Scatter diagram of deaths broken down into 5 year age groups
    You can decide the lower and upper age group via the lLimit and hLimit arguments
    Age groups are from 0 to 19 where 0 is under 5 and 19 is 90+
    '''

    agedDeathsData = [0]*hLimit
    population = dataAge.population

    plt.cla()
    plt.clf()

    setupChart()

    for iii in range(lLimit, hLimit):
        agedDeathsData[iii] = dataAge.getData(iii, 'deaths', 'true')

    agedDeathsPerMillion = agedDeathsData.copy()

    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    #Now calculate daily deaths per million
    for ii in range(lLimit, hLimit):
        for iii in range(len(agedDeathsData[ii])):
            agedDeathsPerMillion[ii][iii] = float(agedDeathsData[ii][iii]) / float(population[ii])
           
    for iii in range(lLimit, hLimit):
        lbl = ageCategoriesString[iii]
        chart.addScatterplot(dataAge.GOVdateSeries, agedDeathsPerMillion[iii], lineColour[iii], lbl)

    fileName = "ageDeathsPerCapita" + str(lLimit) + "_" + str(hLimit)
    leg = ax1.legend(loc='upper left')
    chart.drawChart("Date", "Deaths per Million", "COVID 19 Data - Daily Deaths Per Million by Age in England", fileName, "false", "false", ax1, "true", "true")
    plt.close

def draw_Bar_Aged_Deaths_per_Million():
    '''
    Creates a Bar chart of deaths broken down into 5 year age groups
    '''
    #Now create a bar chart of total deaths per 1,000,000 split by age group
    totalAgedDeaths = [0]*19

    agedDeathsData = [0]*19

    population = dataAge.population
    ageCategoriesString = dataAge.ageCategoriesString
    
    for iii in range(0, 19):
        agedDeathsData[iii] = dataAge.getData(iii, 'deaths', 'true')

    agedDeathsPerMillion = agedDeathsData.copy()

    #Now calculate daily deaths per million
    for ii in range(0, 19):
        for iii in range(len(agedDeathsData[ii])):
            agedDeathsPerMillion[ii][iii] = float(agedDeathsData[ii][iii]) / float(population[ii])

    for ii in range(0, 19):
        totalAgedDeaths[ii] = sum(agedDeathsPerMillion[ii])

    import matplotlib.pyplot as plt

    plt.cla()
    plt.clf()
    plt.bar(ageCategoriesString, totalAgedDeaths,  color = 'teal', alpha = 1)

    value = 0
    
    for x in range(len(totalAgedDeaths)):
        value = "{:.4f}".format(totalAgedDeaths[x])
        label3 = value
        plt.annotate(label3, # this is the text
                     (ageCategoriesString[x],totalAgedDeaths[x]), # this is the point to label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center

    plt.xticks(rotation = 90)
    plt.title("COVID 19 - Age Profile of Total Deaths per 1,000,000")
    plt.xlabel("Age Ranges")
    plt.ylabel("Number of Deaths per 1,000,000")

    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig('images/age_Bar_Deaths_per_Cap.png')
    chart.createTimeStamp('images/age_Bar_Deaths_per_Cap.png', 980, 970, 12)
    plt.close

def draw_Age_Deaths_Treemap():
    '''
    Draws a treemap showing deaths in all age groups and calulates the percentage for each age group
    '''
    totalDeaths = [0]*19
    ageRange = [0]*19

    totalDeathsAllAges = 0

    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    #This will denote which age category label to display on the graph, for now all under 50's are not displayed as I total these up later
    ageCategories = ['', '', '', '', '', '', '', '', '', '', '50 to 54', '55 to 59', '60 to 64', '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90+']

    for ii in range (19):
        totalDeaths[ii] = dataAge.getTotals(ii, 'deaths', 'true')
        totalDeathsAllAges = totalDeathsAllAges + totalDeaths[ii]

    percent = [0]*19
    under50 = 0
    under24 = 0

    labels = ageCategories
    sizes = totalDeaths
    colors = lineColour

    plt.cla()
    plt.clf()

    for ii in range(19):
        try:
            percent[ii] = (totalDeaths[ii] / totalDeathsAllAges) * 100
            if (ii < 10):
                under50 = under50 + percent[ii]
            if (ii < 5):
                under24 = under24 + percent[ii]
        except Exception as e:
            print("Percentage Error")
            print(e)
        
    for ii in range(10, 19):
        percent[ii] = str(round(percent[ii],2))
        ageCategories[ii] = ageCategories[ii] + " (" + str(percent[ii]) + "%)"

    under50 = str(round(under50,2))
    under24 = str(round(under24,2))
    under50 = "All Deaths Under 50 (" + str(under50) + "%)"
    under24 = str(under24) + "%"

    plt.text(0.8,1,under24, rotation = "vertical", size = 10, color = "black", weight="bold")
    plt.text(0.8,35,under50, rotation = "vertical", size = 10, color = "black", weight="bold")

    squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8, bar_kwargs=dict(linewidth=0.5, edgecolor="black"))

    plt.axis('off')
    plt.title("COVID 19 - Positive Deaths by Age in England")

    fileName = "TreemapDeaths"
    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig("images/" + fileName + '.png')
    chart.createTimeStamp("images/" + fileName + '.png', 980, 970, 12)
    plt.close

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
    totalDeaths = [0]*19
    totalRangedDeaths = [0]*2
    ageRange = [0]*2

    ageRange[0] = firstAgeRange
    ageRange[1] = secondAgeRange

    plt.cla()
    plt.clf()

    totalDeathsAllAges = 0
    for ii in range (19):
        totalDeaths[ii] = dataAge.getTotals(ii, 'deaths', 'true')
        totalDeathsAllAges = totalDeathsAllAges + totalDeaths[ii]

    
    for ii in range(0, limit):
        try:
            totalRangedDeaths[0] = totalRangedDeaths[0] + totalDeaths[ii]    
        except:
            print("err")
    
    for ii in range(limit, 19):
        try:
            totalRangedDeaths[1] = totalRangedDeaths[1] + totalDeaths[ii]    
        except:
            print("err")
    
    plt.bar(ageRange, totalRangedDeaths,  color = 'teal', alpha = 1)

    for x in range(len(totalRangedDeaths)):
        label3 = totalRangedDeaths[x]
        plt.annotate(label3, # this is the text
                    (ageRange[x],totalRangedDeaths[x]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlabel("Age Ranges")
    plt.ylabel("Number of Deaths")

    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig(filename)
    chart.createTimeStamp(filename, 980, 970, 12)

    plt.close

def draw_Bar_Aged_Cases():
    plt.cla()
    plt.clf()

    setupChart()

    totalcases = [0]*19
    ageRange = dataAge.ageCategoriesString

    casesWeek = [0]*19

    for ii in range(19):
        totalcases[ii] = dataAge.getTotals(ii, 'cases', 'true')
            
    plt.bar(ageRange, totalcases,  color = 'teal', alpha = 1)

    for x in range(len(totalcases)):
        label3 = totalcases[x]
        plt.annotate(label3, # this is the text
                    (ageRange[x],totalcases[x]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center', # horizontal alignment can be left, right or center
                    fontsize='8')

    plt.xticks(rotation = 90)

    plt.title("COVID 19 - Age Profile of Cases England")
    plt.xlabel("Age Ranges")
    plt.ylabel("Number of cases")

    fileName = "BarCases"
    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig("images/" + fileName + '.png')
    chart.createTimeStamp("images/" + fileName + '.png', 980, 970, 12)
    plt.close()

def draw_Scatter_Aged_Deaths(lLimit, hLimit):
    lineColour = dataAge.lineColour
    ageCategoriesString = dataAge.ageCategoriesString

    plt.cla()
    plt.clf()

    setupChart()

    #We don't need to load the data in this funciton as the dataAge.getTotals funciton will load it for us.
    for iii in range(lLimit, hLimit):
        lbl = dataAge.ageCategoriesString[iii] + " (" + str(dataAge.getTotals(iii, 'deaths', 'true')) + ")"
        chart.addScatterplot(dataAge.GOVdateSeries, dataAge.getData(iii, 'deaths', 'true'), lineColour[iii], lbl)

    fileName = "ageDeaths_" + str(lLimit) + "_" + str(hLimit)
    leg = ax1.legend(loc='upper left')
    chart.drawChart("Date", "Number of People", "COVID 19 Data - Daily Deaths by Age in England", fileName, "false", "false", ax1, "true", "true")
    plt.close()

def draw_Bar_Aged_Deaths():

    plt.cla()
    plt.clf()

    setupChart()

    totalDeaths = [0]*19
    ageRange = dataAge.ageCategoriesString

    for ii in range(19):
        totalDeaths[ii] = dataAge.getTotals(ii, 'deaths', 'true')
            
    plt.bar(ageRange, totalDeaths,  color = 'teal', alpha = 1)

    for x in range(len(totalDeaths)):
        label3 = totalDeaths[x]
        plt.annotate(label3, # this is the text
                    (ageRange[x],totalDeaths[x]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.xticks(rotation = 90)

    plt.title("COVID 19 - Age Profile of Deaths England")
    plt.xlabel("Age Ranges")
    plt.ylabel("Number of Deaths")

    fileName = "BarDeaths"
    figure = plt.gcf()
    figure. set_size_inches(14, 10)
    plt.savefig("images/" + fileName + '.png')
    chart.createTimeStamp("images/" + fileName + '.png', 980, 970, 12)
    plt.close()




