'''

LOOKING AT DEATHS ETC BEFORE AND AFTER VACCINAITON WHERE A CUT OFF CAN BE SPECIFIED

NEED TO ALIGN AGE GROUPS


'''
import sys
sys.path.append('./src/toolset')

#Import COVID Data with our COVIDTOOLSET
from unicodedata import category
from numpy.core.shape_base import block
from numpy.lib import function_base
import pandas as pd

from toolset.LoadDatasets import LoadDataSets as govDataClass
from toolset.CovidChart import CovidChart as CovidChart
from toolset.GetCovidData import GetCOVIDData as getData
from toolset.DataFunctions import Functions as functions
from toolset.CovidDashboard import Dashboard as DASH
from toolset.ReadVaxData import readVaxData as vax_data
from toolset.BenchMark import Benchmark as Benchmark

import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=UserWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=RuntimeWarning) #surpress various warnings for charts if you want to see the warnings comment these lines
warnings.simplefilter(action='ignore', category=FutureWarning) #surpress various warnings to do with dataframes if you want to see the warnings comment these lines

nation = "England" #If this is set to anything else Age profiled data will always be for England as it is not available for the other nations

chart = CovidChart()
vData = vax_data("England")
govData = govDataClass(True, "England")
funcs = functions()

date_lag = (281) #Date lag between 2nd March 2020 and 8th December 2020, 281 days
vax_rate = 15
colour = "green"

#We must align the age groups as he vax data has different age groups to the case/death data

'''
age_groups = ['00_04', '05_09','10_14', '15_19', '20_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']
                0          1        2       3       4       5          6       7        8       9       10      11          12      13      14      15          16      17      18

vax_age_groups =               ['12_15', '16_17', '18_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']
                                   0          1        2       3       4       5           6       7       8       9       10          11      12      13       14      15      16

merge age_group 3 & 4
merge vax age groups 2 & 3
'''


def create_vax_chart(data):
    chart.clear_chart()



chart.set_chart_params(False, False, False, True)
for ii in range(0, len(vData.get_vax_age_groups())):
    chart.clear_chart()

    df = vData.get_vax_aged_data(vData.get_vax_age_groups()[ii])
    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedFirstDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())

    
    #Find out when more than 0.1% of each age group received the 1st vax
    crit_vax_date = 0
    for iii in range(0, len(ratio_df)):
        if ratio_df[iii] > vax_rate:
            crit_vax_date = iii
            crit_vax_date = crit_vax_date + date_lag # 281 days since 2 March to 8 December
            chart.add_vline_day_no(crit_vax_date, "After Vax Cutoff Date", colour)
            break
    

    #Now total the deaths before and after vaccination
    deaths_before_vax = 0
    deaths_after_vax = 0
    deaths = govData.get_aged_death_data(ii + 2)
    for iii in range(0 , len(deaths)):
        if iii < crit_vax_date or iii == crit_vax_date:
            deaths_before_vax = deaths_before_vax + deaths[iii]
        else:
            deaths_after_vax = deaths_after_vax + deaths[iii]
    
    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "firebrick", "1st Dose", True, True)

    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedSecondDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "darkgoldenrod", "2nd Dose", True, True)

    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedThirdInjectionByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "darkgreen", "3rd Dose", True, True)

    per_day_before = 0
    per_day_after = 0
    try:
        per_day_before = deaths_before_vax / crit_vax_date
        per_day_after = deaths_after_vax / (len(deaths) - crit_vax_date)
    except:
        pass

    per_day_before =  "{:.3f}".format(per_day_before)
    per_day_after =  "{:.3f}".format(per_day_after)

    chart.add_bar_chart(govData.get_aged_gov_date_series(), govData.get_aged_death_data(ii + 2), "pink", "Deaths (Before Vax: " + str(deaths_before_vax) + " (" + str(per_day_before) + " per day) , After Vax: " + str(deaths_after_vax) + " (" + str(per_day_after) + " per day)", display_vals= False, to_bar_over=False)

    chart.draw_chart("",""," " + vData.get_vax_age_groups()[ii],"test" + str(ii),True)






#------------------------------------------------------------------------------------------------
#           DEATHS



for ii in range(0, len(vData.get_vax_age_groups())):
    chart.clear_chart()
    df = vData.get_vax_aged_data(vData.get_vax_age_groups()[ii])
    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedFirstDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())

    #Find out when more than 0.1% of each age group received the 1st vax
    crit_vax_date = 0
    for iii in range(0, len(ratio_df)):
        if ratio_df[iii] > vax_rate:
            crit_vax_date = iii
            crit_vax_date = crit_vax_date + date_lag # 281 days since 2 March to 8 December
            chart.add_vline_day_no(crit_vax_date, "After Vax Cutoff Date", colour)
            break

    #Now total the deaths before and after vaccination
    deaths_before_vax = 0
    deaths_after_vax = 0
    deaths = govData.get_aged_case_data(ii + 2)
    for iii in range(0 , len(deaths)):
        if iii < crit_vax_date or iii == crit_vax_date:
            deaths_before_vax = deaths_before_vax + deaths[iii]
        else:
            deaths_after_vax = deaths_after_vax + deaths[iii]

    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "firebrick", "1st Dose", True, True)

    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedSecondDoseByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "darkgoldenrod", "2nd Dose", True, True)

    
    ratio_df = funcs.calc_ratio_as_int(df["cumPeopleVaccinatedThirdInjectionByVaccinationDate"].tolist(), df["VaccineRegisterPopulationByVaccinationDate"].tolist())
    chart.add_scatter_plot(df["date"].tolist(), ratio_df, "darkgreen", "3rd Dose", True, True)

    per_day_before = 0
    per_day_after = 0
    try:
        per_day_before = deaths_before_vax / crit_vax_date
        per_day_after = deaths_after_vax / (len(deaths) - crit_vax_date)
    except:
        pass

    per_day_before =  "{:.3f}".format(per_day_before)
    per_day_after =  "{:.3f}".format(per_day_after)

    chart.add_bar_chart(govData.get_aged_gov_date_series(), govData.get_aged_case_data(ii + 2), "pink", "Deaths (Before Vax: " + str(deaths_before_vax) + " (" + str(per_day_before) + " per day) , After Vax: " + str(deaths_after_vax) + " (" + str(per_day_after) + " per day)", display_vals= False, to_bar_over=False)

    chart.draw_chart("",""," " + vData.get_vax_age_groups()[ii],"test_cases" + str(ii),True)