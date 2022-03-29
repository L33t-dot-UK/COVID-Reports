'''
This script gives examples of how the COVID toolset can be used.

STILL A WORK IN PROGRESS
'''

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.ReadHospitalData import readHospitalData as HOSPITALDATA


pullData = getData("England") #get the latest data for England

govData = govDataClass(True, "England") #Load data from the CSV file into memory

#Now I will create a chart using the govData class and COVID Chart class
chart = CovidChart() #Create a charty object to store chart settings
chart.set_chart_params(False, True, True, True) #To show the plot, to show legend, to add VLINES, to add timestamp
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.get_new_cases(), "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.draw_chart("", "Cases", "Example Chart Showing Cases using Lists", "Example_Cases", True)

#I will now draw the same chart but using dataframes rather than lists
#With this example the VLINES won't be drawn as the yaxis must be a list rather than a dataframe for these lines to be drawn
chart.clear_chart() #Always clear the chart before creating a new one
print(govData.fullDataFrame.info()) #This will print out column names in our dataframe
chart.add_scatter_plot(govData.fullDataFrame["date"], govData.fullDataFrame["newCasesBySpecimenDate"], "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
#chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newCasesBySpecimenDate"], "orange", "New Cases", False, True) #VLINES would be drawn using this line
chart.draw_chart("", "Cases", "Example Chart Showing Cases using DataFrames", "Example_Cases_DF", True)

#I will now add 2 datasets in the same graph
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newAdmissions"], "purple", "Hospital Cases", False, False) #VLINES would be drawn using this line
chart.draw_chart("", "Cases", "Example Chart Showing Deaths and Hospitalisations using DataFrames", "Example_DeathsHos_DF", True)


#Here I will plot deaths by reported date, this data has hogh rates of oscillation due to how deaths are recorded over the weekend
#The solid line will show deaths averaged over 7 days and the dotted line will show them averaged over 56 days to show the averaging effect
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 7 Day Average", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.set_LOBF_time(56)
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 56 Day Average", True, False)
chart.draw_chart("", "Cases", "Example Chart Showing Deaths using DataFrames", "Example_Deaths_DF", True)
chart.set_LOBF_time(7)

#This plots death by death date and deaths by reported date to show the differences in the spread of the data
chart.clear_chart() #Always clear the chart before creating a new one
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByDeathDate"], "red", "Deaths by Death Date", False, False) #LoadDataSets will give 2 date lists get_gov_date_Series and get_aged_gov_date_series; one is to be used with non aged data and the other for age profiled data
chart.add_scatter_plot(govData.get_gov_date_Series(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "blue", "Deaths by Reported Date", True, False)
chart.draw_chart("", "Deaths", "Example Chart Showing Deaths using DataFrames", "Example_Deaths2_DF", True)
chart.set_LOBF_time(7)

chart.clear_chart()
chart.set_chart_params(True, False, False, True) #To show the plot, to show legend, to add VLINES, to add timestamp

hospitalData = HOSPITALDATA()
df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total")
df2 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total")

totalAdmission =  df1["ENGLAND"].sum()
totalDiag = df2["ENGLAND"].sum()

chart.add_treemap([totalAdmission, totalDiag], ["Admissions", "Diagnosisis"], ["blue", "red"])
chart.draw_chart("","","Hospital Admissions vs Diagnosisis", "Example_TreeMap", False)

chart.clear_chart()
chart.set_chart_params(True, False, False, True) #To show the plot, to show legend, to add VLINES, to add timestamp
chart.add_bar_chart(["Admissions", "Diagnosisis"] , [totalAdmission, totalDiag], "teal")
chart.draw_chart("","","Hospital Admissions vs Diagnosisis", "Example_BarChart", False)
