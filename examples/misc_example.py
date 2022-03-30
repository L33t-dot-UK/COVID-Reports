'''
This script gives examples of how the COVID toolset can be used.

All charts will be saved in the reports/images folder
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
from GetCovidData import GetCOVIDData as getData
from ReadHospitalData import readHospitalData as HOSPITALDATA

'''
pull data from the UK COVID dashboard using their API
'''
pullData = getData("England") #get the latest data for England

'''
Create a LoadDatasets object and load the data from the csv files pulled earlier
'''
govData = govDataClass(True, "England") #Load data from the CSV file into memory

#Now I will create a chart using the govData class and COVID Chart class
chart = CovidChart() #Create a charty object to store chart settings
chart.set_chart_params(False, False, False, True) #Set the chart params so we dont show the chart or add vlines but we will time stamp them


chart.set_chart_params(False, True, True, True) #To show the plot, to show legend, to add VLINES, to add timestamp
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.get_new_cases(), "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.draw_chart("", "Cases", "Example Chart Showing Cases using Lists", "Example_Cases", True)


#I will now draw the same chart but using dataframes rather than lists
#With this example the VLINES won't be drawn as the yaxis must be a list rather than a dataframe for these lines to be drawn
chart.clear_chart() #Always clear the chart before creating a new one
print(govData.fullDataFrame.info()) #This will print out column names in our dataframe
chart.add_scatter_plot(govData.fullDataFrame["date"], govData.fullDataFrame["newCasesBySpecimenDate"], "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.draw_chart("", "Cases", "Example Chart Showing Cases using DataFrames", "Example_Cases_DF", True)


#I will now add 2 datasets to the same graph
#I will use dataframes for the data and a list for the dates
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newAdmissions"], "purple", "Hospital Cases", False, False) #VLINES would be drawn using this line
chart.draw_chart("", "Cases", "Example Chart Showing Deaths and Hospitalisations using DataFrames", "Example_DeathsHos_DF", True)


#Here I will plot deaths by reported date, this data has hogh rates of oscillation due to how deaths are recorded over the weekend
#The solid line will show deaths averaged over 7 days and the dotted line will show them averaged over 56 days to show the averaging effect
#I will use dataframes for the data and a list for the dates
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 7 Day Average", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.set_LOBF_time(56)
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 56 Day Average", True, False)
chart.draw_chart("", "Cases", "Example Chart Showing Deaths using DataFrames", "Example_Deaths_DF", True)
chart.set_LOBF_time(7)

#This plots death by death date and deaths by reported date to show the differences in the spread of the data using dataframes for the data and a list for the dates
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByDeathDate"], "red", "Deaths by Death Date", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "blue", "Deaths by Reported Date", True, False)
chart.draw_chart("", "Deaths", "Example Chart Showing Deaths using DataFrames", "Example_Deaths2_DF", True)
chart.set_LOBF_time(7)

chart.clear_chart()

#I will now use hospital data to create some graphs

#First load the datasets and join them as these are in different excel files
hospitalData = HOSPITALDATA()
df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total") #Get all data from the admissions Total worksheet
df2 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total") #Get all data from the diagnoses Total worksheet

totalAdmission =  df1["ENGLAND"].sum() #sum up the admisison data
totalDiag = df2["ENGLAND"].sum() #sum up the diagnoses data

chart.add_treemap([totalAdmission, totalDiag], ["Admissions", "Diagnoses"], ["blue", "red"]) #add the above data to a treemap
chart.draw_chart("","","Hospital Admissions vs Diagnoses", "Example_TreeMap", False) #draw the treemap and save to file

chart.clear_chart()
chart.set_chart_params(True, False, False, True) #Were now going to change the parameters so we can view the chart as well as saving it as a png image
chart.add_bar_chart(["Admissions", "Diagnoses"] , [totalAdmission, totalDiag], "teal")
chart.draw_chart("","","Hospital Admissions vs Diagnoses", "Example_BarChart", False)
