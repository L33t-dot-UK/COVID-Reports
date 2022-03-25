'''
This script gives examples of how the COVID toolset can be used.

In the below example I will create 3 graphs and add them to a dashboard
'''

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.ReadHospitalData import readHospitalData as HOSPITALDATA


pullData = getData("England") #get the latest data for England

govData = govDataClass(True, "England") #Load data from the CSV file into memory

#Now I will create a chart using the govData class and COVID Chart class
chart = CovidChart() #Create a charty object to store chart settings
chart.setChartParams(False, True, True, True) #To show the plot, to show legend, to add VLINES, to add timestamp
chart.addScatterplot(govData.getGOVdateSeries(), govData.getNewCases(), "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists getGOVdateSeries and getAgedGOVdateSeries; one is to be used with non aged data and the other for age profiled data
chart.drawChart("", "Cases", "Example Chart Showing Cases using Lists", "Example_Cases", True)

#I will now draw the same chart but using dataframes rather than lists
#With this example the VLINES won't be drawn as the yaxis must be a list rather than a dataframe for these lines to be drawn
chart.clearChart() #Always clear the chart before creating a new one
print(govData.fullDataFrame.info()) #This will print out column names in our dataframe
chart.addScatterplot(govData.fullDataFrame["date"], govData.fullDataFrame["newCasesBySpecimenDate"], "orange", "New Cases", False, True) #LoadDataSets will give 2 date lists getGOVdateSeries and getAgedGOVdateSeries; one is to be used with non aged data and the other for age profiled data
#chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newCasesBySpecimenDate"], "orange", "New Cases", False, True) #VLINES would be drawn using this line
chart.drawChart("", "Cases", "Example Chart Showing Cases using DataFrames", "Example_Cases_DF", True)

#I will now add 2 datasets in the same graph
chart.clearChart() #Always clear the chart before creating a new one
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths", False, False) #LoadDataSets will give 2 date lists getGOVdateSeries and getAgedGOVdateSeries; one is to be used with non aged data and the other for age profiled data
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newAdmissions"], "purple", "Hospital Cases", False, False) #VLINES would be drawn using this line
chart.drawChart("", "Cases", "Example Chart Showing Deaths and Hospitalisations using DataFrames", "Example_DeathsHos_DF", True)


#Here I will plot deaths by reported date, this data has hogh rates of oscillation due to how deaths are recorded over the weekend
#The solid line will show deaths averaged over 7 days and the dotted line will show them averaged over 56 days to show the averaging effect
chart.clearChart() #Always clear the chart before creating a new one
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 7 Day Average", False, False) #LoadDataSets will give 2 date lists getGOVdateSeries and getAgedGOVdateSeries; one is to be used with non aged data and the other for age profiled data
chart.changeLOBFtime(56)
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "red", "Deaths 56 Day Average", True, False)
chart.drawChart("", "Cases", "Example Chart Showing Deaths using DataFrames", "Example_Deaths_DF", True)
chart.changeLOBFtime(7)

#This plots death by death date and deaths by reported date to show the differences in the spread of the data
chart.clearChart() #Always clear the chart before creating a new one
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newDeaths28DaysByDeathDate"], "red", "Deaths by Death Date", False, False) #LoadDataSets will give 2 date lists getGOVdateSeries and getAgedGOVdateSeries; one is to be used with non aged data and the other for age profiled data
chart.addScatterplot(govData.getGOVdateSeries(), govData.fullDataFrame["newDeaths28DaysByPublishDate"], "blue", "Deaths by Reported Date", True, False)
chart.drawChart("", "Deaths", "Example Chart Showing Deaths using DataFrames", "Example_Deaths2_DF", True)
chart.changeLOBFtime(7)

chart.clearChart()
chart.setChartParams(True, False, False, True) #To show the plot, to show legend, to add VLINES, to add timestamp

hospitalData = HOSPITALDATA()
df1 = hospitalData.joinTotalsDataSets("data/hospitalData", "Admissions Total")
df2 = hospitalData.joinTotalsDataSets("data/hospitalData", "Diagnoses Total")

totalAdmission =  df1["ENGLAND"].sum()
totalDiag = df2["ENGLAND"].sum()

chart.addTreeMap([totalAdmission, totalDiag], ["Admissions", "Diagnosisis"], ["blue", "red"])
chart.drawChart("","","Hospital Admissions vs Diagnosisis", "Example_TreeMap", False)

chart.clearChart()
chart.setChartParams(True, False, False, True) #To show the plot, to show legend, to add VLINES, to add timestamp
chart.addBarChart(["Admissions", "Diagnosisis"] , [totalAdmission, totalDiag], "teal")
chart.drawChart("","","Hospital Admissions vs Diagnosisis", "Example_BarChart", False)
