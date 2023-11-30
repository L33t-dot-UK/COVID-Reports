'''
categorising deaths and cases by age 

REFACTOR AND ADD TO DASHBOARD 1

'''
import toolset.BoilerPlateImports 
import numpy as np

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.DataFunctions import Functions as functions
from toolset.CovidDashboard import Dashboard as DASH
from toolset.ReadVaxData import readVaxData as vax_data
from toolset.BenchMark import Benchmark as Benchmark

funcs = functions()
govData = govDataClass(True, "England")
chart = CovidChart()


date_list = govData.get_aged_gov_date_series()
cases_df, deaths_df = govData.get_aged_data_frames()

mask = cases_df["age"] != "60+"
cases_df = cases_df[mask]  # Remove the column for 60+

mask = deaths_df["age"] != "60+"
deaths_df = deaths_df[mask]  # Remove the column for 60+

mask = cases_df["age"] != "00_59"
cases_df = cases_df[mask]  # Remove the column for 60+

mask = deaths_df["age"] != "00_59"
deaths_df = deaths_df[mask]  # Remove the column for 60+

values = []
values_cases = []


def get_median_age(value):
    '''
    This function assigns median ages for each age range
    '''

    if(value == "00_04"):
        return 2.5
    elif (value == "05_09"):
        return 7.5
    elif (value == "10_14"):
        return 12.5
    elif (value == "15_19"):
        return 17.5
    elif (value == "20_24"):
        return 22.5
    elif (value == "25_29"):
        return 27.5
    elif (value == "30_34"):
        return 32.5
    elif (value == "35_39"):
        return 37.5
    elif (value == "40_44"):
        return 42.5
    elif (value == "45_49"):
        return 47.5
    elif (value == "50_54"):
        return 52.5
    elif (value == "55_59"):
        return 57.5
    elif (value == "60_64"):
        return 62.5
    elif (value == "65_69"):
        return 67.5
    elif (value == "70_74"):
        return 72.5
    elif (value == "75_79"):
        return 77.5
    elif (value == "80_84"):
        return 82.5
    elif (value == "85_89"):
        return 87.5
    elif (value == "90+"):
        return 92.5  # The averge ages may be lower due to this number, the real median age for 90+ is likely to be higher
    else:
        return 65


#Now lets calculate the averge ages for each day
weighted_total = [0] * len(govData.get_age_cat_string_list())


avg_values_cases = []
summed_total = 0
summed_weighted_total = 0


avg_values_deaths = []
weighted_total_deaths = [0] * len(govData.get_age_cat_string_list())
summed_total_deaths = 0
summed_weighted_total_deaths = 0

#Calculate average death and case age
for dates in date_list:
    mask = cases_df["date"] == dates  # split the data into different days using a mask
    cases = cases_df[mask]

    mask = deaths_df["date"] == dates  # split the data into different days using a mask
    deaths = deaths_df[mask]
    
    summed_total = 0
    summed_total_deaths = 0
    for ii in range(0, len(govData.get_age_cat_string_list())):
        median_age = get_median_age(cases["age"].values[ii])
        weighted_total[ii] = median_age * cases["cases"].values[ii]
        summed_total = summed_total +  cases["cases"].values[ii]

        median_age_deaths = get_median_age(deaths["age"].values[ii])
        weighted_total_deaths[ii] = median_age_deaths * deaths["deaths"].values[ii]
        summed_total_deaths = summed_total_deaths +  deaths["deaths"].values[ii]

    summed_weighted_total = (np.sum(weighted_total))
    avg_values_cases.append(summed_weighted_total / summed_total)

    summed_weighted_total_deaths = (np.sum(weighted_total_deaths))
    avg_values_deaths.append(summed_weighted_total_deaths / summed_total_deaths)

#Calculate overall averages
length = len(govData.get_aged_gov_date_series())
print(np.sum(avg_values_cases) / length)

avg_values_deaths = np.array(avg_values_deaths)
nan_array = np.isnan(avg_values_deaths)
not_nan_array = ~ nan_array
array2 = avg_values_deaths[not_nan_array]

print(np.sum(array2)  / length)

death_overall_avg = np.sum(array2)  / length
case_overall_avg = np.sum(avg_values_cases) / length

#Create an array for the overall averages
arr1 = [0] * len(govData.get_aged_gov_date_series())
for ii in range(len(arr1)):
    arr1[ii] = death_overall_avg

arr2 = [0] * len(govData.get_aged_gov_date_series())
for ii in range(len(arr2)):
    arr2[ii] = case_overall_avg

chart.set_chart_params(False, True, True, True)
chart.clear_chart()

chart.add_scatter_plot(govData.get_aged_gov_date_series(), arr1, 'grey', "Overall Avgerage", True, True)

chart.add_scatter_plot(govData.get_aged_gov_date_series(), avg_values_cases, "orange", "Average Case Age", False, True)
chart.add_scatter_plot(govData.get_aged_gov_date_series(), avg_values_deaths, "red", "Average Age of death", False, True)
chart.add_scatter_plot(govData.get_aged_gov_date_series(), arr2, 'grey', "", True, True)
chart.draw_chart("Date", "Age", "COVID 19 - Average Case and Death Age by Date", "avg_death_cases", True)


#Yearly comps just for fun
chart.clear_chart()

chart.draw_Scatter_Year_Comp(avg_values_cases, False, "Average_Case_Age", False, govData.get_year_dates(), True)
chart.draw_Scatter_Year_Comp(array2, False, "Average_Death_Age", False, govData.get_year_dates(), True)
'''

def calc_averge_age(data_df, cat, date_name = "date", to_print = False):

    if to_print:
        print(data_df.info())
        print("###############")
        print(data_df.sample(50))

    #date_list = data_df[date_name].tolist()
    date_list = govData.get_aged_gov_date_series()

    #print(date_list)

    weighted_total = [0] * len(govData.get_age_cat_string_list())
    avg_values = []
    summed_total = 0
    summed_weighted_total = 0

    # pre-process the data by removing the 60+ and 00_59 age ranges
    mask = data_df["age"] != "60+"
    data_df = data_df[mask]  # Remove the column for 60+

    mask = data_df["age"] != "00_59"
    data_df = data_df[mask]  # Remove the column for 60+

    mask = data_df["age"] != "unassigned"
    data_df = data_df[mask] # Remove the column for unassigned+

    for dates in date_list:
        mask = data_df["date"] == dates  # split the data into different days using a mask
        data_aged = data_df[mask]

        summed_total = 0

        for ii in range(0, len(govData.get_age_cat_string_list())):
            median_age = get_median_age(data_aged["age"].values[ii])

            weighted_total[ii] = median_age * data_aged[cat].values[ii]
            summed_total = summed_total +  data_aged[cat].values[ii]

    summed_weighted_total = (np.sum(weighted_total))
    avg_values.append(summed_weighted_total / summed_total)

    overall_avg = np.sum(avg_values) / len(date_list)

    return avg_values #, overall_avg

cases_df, deaths_df = govData.get_aged_data_frames()

chart.add_scatter_plot(govData.get_aged_gov_date_series(), calc_averge_age(cases_df, "cases", to_print=True), "orange", "Average Case Age", False, True)
chart.add_scatter_plot(govData.get_aged_gov_date_series(), calc_averge_age(deaths_df, "deaths", to_print=True), "red", "Average Age of death", False, True)

chart.draw_chart("Date", "Age", "COVID 19 - Average Case and Death   ", "", True)
'''