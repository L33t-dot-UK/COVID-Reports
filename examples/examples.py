'''
These examples are from the Example Code Snippets page in the docummentation
'''

import warnings
warnings.simplefilter(action='ignore', category=UserWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=RuntimeWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=FutureWarning) #surpress various warnings to do with dataframes if you want to see the warnings comment these lines

import sys
sys.path.append('./src/toolset')

#Ignore the below syntax highlighting. To get rid of this write you code in the src folder and use toolset.module_name for the imports. See the documentation at https://covidreports.l33t.uk/API for more info
from LoadDatasets import LoadDataSets as govDataClass
from CovidChart import CovidChart as CovidChart
from ReadHospitalData import readHospitalData as HOSPITALDATA
from DataFunctions import Functions as funcs
import numpy as np
nation = "England"

#create various objects
govData = govDataClass(True, nation) # Create the LoadDatasets object and load csv data into it
chart = CovidChart() # create the CovidChart object
hospitalData = HOSPITALDATA()

funcs = funcs()

'''
Create the bar chart
'''
chart.set_chart_params(False,False,False,True) #Change params we dont want the VLINE legend
chart.clear_chart()

totData = [0]* 19

for ii in range(0, 19):
    data = govData.get_aged_case_data(ii) #Gets new cases
    totData[ii] = np.sum(data) #sum up cases in each age group

chart.add_bar_chart(govData.get_age_cat_string_list(), totData, "teal")
chart.draw_chart("Age Categories", "Number of People", "COVID 19 Data - Age Profile of Cases (" + nation + ")", "BarCases", False) #create the chart 


'''
Create the bar plot
'''
# These params will ensure that the chart is not shown, VLINES are added,
# a legend is added and time stamp is added.
chart.set_chart_params(False,True,True,True)
chart.clear_chart() #first clear old data from the chart

data = govData.get_new_deaths() #Gets new deaths by death date
chart.add_bar_plot(govData.get_gov_date_Series(), data, "red", "Death by Death Date")

data = govData.get_deaths_by_report_date() #Gets new deaths
chart.add_bar_plot(govData.get_gov_date_Series(), data, "blue", "Death by Reported Date")

chart.draw_chart("Date", "Number of People", "COVID 19 Data - Death Reported Date vs Death Date (" + nation + ")" , "deathsAndDeaths", True) #create the chart


'''
Create bar scatter plot
'''

def addEnglandToChart(df, colour, label, to_dash):
    df = df.reset_index() # remove dates as the index
    chart.add_scatter_plot(df["Dates"].tolist(), df["ENGLAND"].tolist(), colour, label, to_dash, False)

chart.clear_chart()
chart.set_chart_params(False, False, True, True)

df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total")
df2= hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total")

addEnglandToChart(df2, "purple", "Daily Hospital Diagnoses (People Tested in Hospital with +ve PCR)", False)
addEnglandToChart(df1, "darkgoldenrod", "Daily Hospital Admissions (People going in to Hospital with +ve PCR)", False)

chart.draw_chart("Date", "Beds Used", "COVID-19: Daily Hospital Admissions and Diagnoses (England)", "HOSDATA_AdsDiagnoses", True, hos_data = True)

'''
Create another scatter plot
'''

chart.set_chart_params(False,False,True,True)
chart.clear_chart()

for ii in range(0, 19):
    data = govData.get_aged_death_data(ii) #Gets new cases
    permillionData = [0]*len(data)
    permillionData = funcs.calc_time_series_per_million(data, ii)

    chart.add_scatter_plot(govData.get_aged_gov_date_series(), permillionData, govData.get_line_colour_list()[ii], govData.get_age_cat_string_list()[ii], False, True)

file_name = "ageDeathsPerCapita" + "0" + "_" + "19"
chart.draw_chart("Dates", "Deaths Per Million", "COVID 19 Data - Daily Deaths Per Million by Age in " + nation, file_name, True)


'''
Create a treemap
'''

chart.clear_chart() #Clear the chart object
chart.set_chart_params(False,False,False,True) # Change params of the chart

# We're taking time series data and summing it up to create the summed data for 
# the tree map using lists
summedData = [0] * 11
ageCats = [0] * 11
colours = [0] * 11

# I'm now creating 2 new categories for the under 25 and under 50 age groups
ageCats[0] = "< 25 "
colours[0] = 'whitesmoke'
ageCats[1] = "25 to 49"
colours[1] = 'gray'
for ii in range(0, 5): # All under 25
    summedData[0] = summedData[0] + np.sum(govData.get_aged_death_data(ii))

for ii in range(5, 10): # All under 50's
    summedData[1] = summedData[1] + np.sum(govData.get_aged_death_data(ii))

for ii in range(10,19):
    ageCats[ii - 8] = govData.get_age_cat_string_list()[ii]
    colours[ii - 8] = govData.get_line_colour_list()[ii]
    summedData[ii - 8] = np.sum(govData.get_aged_death_data(ii))

chart.add_treemap(summedData, ageCats, colours) #Add the data to the tree map
chart.draw_chart("", "", "COVID 19 Data - Deaths by Age in " + nation, "TreemapDeaths", False) # create the chart


'''
Create another treemap
'''

chart.clear_chart() #Clear the chart object
chart.set_chart_params(False,False,False,True) # Change params of the chart

# Get all data from the admissions Total worksheet
df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total")

# Get all data from the diagnoses Total worksheet
df2 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total")

totalAdmission =  df1["ENGLAND"].sum() # sum up the admisison data
totalDiag = df2["ENGLAND"].sum() # sum up the diagnoses data

# add the above data to a treemap
chart.add_treemap([totalAdmission, totalDiag], ["Admissions", "Diagnoses"], ["blue", "red"])
# draw the treemap and save to file
chart.draw_chart("","","Hospital Admissions vs Diagnoses", "Example_TreeMap", False)



