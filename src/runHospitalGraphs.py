import numpy as np

from toolset.CovidChart import CovidChart as COVIDCHART
from toolset.ReadHospitalData import readHospitalData as HOSPITALDATA
from toolset.LoadDatasets import LoadDataSets as govData

hospitalData = HOSPITALDATA()

nation = "England"
govData = govData(True, nation)
chart = COVIDCHART()

population = govData.get_population_number_list()

adjustedPop = [0] * 5

adjustedPop[0] = population[0]
adjustedPop[1] = sum(population[1:4])
adjustedPop[2] = sum(population[4:13])
adjustedPop[3] = sum(population[13:17])
adjustedPop[4] = sum(population[17:19])

#for pop in adjustedPop:
#    print(f'{pop:,}')

def addEnglandToChart(df, colour, label, to_dash):
    df = df.reset_index() #remove dates as the index
    chart.add_scatter_plot(df["Dates"].tolist(), df["ENGLAND"].tolist(), colour, label, to_dash, False)

def calcPerMillion(age_group, df):
    df = df.apply(lambda x: (x / float(adjustedPop[age_group]) * 1000000), axis=1)
    return(df)


def addRegionsToChart(df):
    df = df.reset_index() #remove dates as the index
    chart.add_scatter_plot(df["Dates"].tolist(), df["East of England"].tolist(), "red", "East of England", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["London"].tolist(), "blue", "London", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["Midlands"].tolist(), "black", "Midlands", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["North East and Yorkshire"].tolist(), "green", "North East and Yorkshire", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["North West"].tolist(), "indigo", "North West", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["South East"].tolist(), "orange", "South East", False, False)
    chart.add_scatter_plot(df["Dates"].tolist(), df["South West"].tolist(), "pink", "South West", False, False)

def drawBedsvsBeds():

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)

    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Total Beds Occupied")
    df2= hospitalData.join_totals_datasets("data/hospitalData", "Total Beds Occupied Covid")

    df1 = df1.reset_index() #remove dates as the index
    chart.add_bar_plot(df1["Dates"].tolist(), df1["ENGLAND"].tolist(), "green", "Number of Total Occupied Beds")

    df2 = df2.reset_index() #remove dates as the index
    chart.add_bar_plot(df2["Dates"].tolist(), df2["ENGLAND"].tolist(), "red", "Number of Beds Used by COVID-19 Patients")


    bedCap = 124000
    bedCapArr = [0] * len(df2["Dates"].tolist())
    for ii in range(0, len(df2["Dates"].tolist())):
        bedCapArr[ii] = bedCap

    chart.add_scatter_plot(df2["Dates"].tolist(), bedCapArr, 'grey', 'Estimated Bed Capacity', True, False) 

    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Covid Absences")
    addEnglandToChart(df1, "indigo", "COVID19 NHS Staff Absences", True)

    chart.draw_chart("Date", "Percentage of Beds Used / Total Beds Occupied (Scaled, in thousands)", "COVID-19: Number of Occupied Beds Used by COVID Patients (England)", "HOSDATA_PercentBedsUsed", True)

def drawMechBeds():

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)

    df1 = hospitalData.join_totals_datasets("data/hospitalData", "MV Beds Occupied")
    df2= hospitalData.join_totals_datasets("data/hospitalData", "MV Beds Occupied Covid-19")

    df1 = df1.reset_index() #remove dates as the index
    chart.add_bar_plot(df1["Dates"].tolist(), df1["ENGLAND"].tolist(), "green", "Number of Total Occupied Mechanical Ventalation Beds")

    df2 = df2.reset_index() #remove dates as the index
    chart.add_bar_plot(df2["Dates"].tolist(), df2["ENGLAND"].tolist(), "red", "Number of Mechanical Ventalation Beds Used by COVID-19 Patients")

    bedCap = 4000
    bedCapArr = [0] * len(df2["Dates"].tolist())
    for ii in range(0, len(df2["Dates"].tolist())):
        bedCapArr[ii] = bedCap

    chart.add_scatter_plot(df2["Dates"].tolist(), bedCapArr, 'grey', 'Estimated Critcal Care Bed Capacity', True, False) 

    chart.draw_chart("Date", "Percentage of MV Beds Used / Total MV Beds Occupied (Scaled, in Hundreds)", "COVID-19: Number of Occupied Mechanical Ventalation Beds Used by COVID Patients (England)", "HOSDATA_MechBeds", True)

def drawAdsDiagsActual():

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total")
    df2= hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total")

    addEnglandToChart(df2, "purple", "Daily Hospital Diagnoses (People Tested in Hospital with +ve PCR)", False)
    addEnglandToChart(df1, "darkgoldenrod", "Daily Hospital Admissions (People going in to Hospital with +ve PCR)", False)

    chart.draw_chart("Date", "Beds Used", "COVID-19: Daily Hospital Admissions and Diagnoses (England)", "HOSDATA_AdsDiagnoses", True)

def drawAdsDiagsPerCap():
    #------------------------ HOSPITAL ADMISSIONS PER CAP ------------------------

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 0-5")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(0, df), "green", "Age Group: 0 - 5", False)
    #addEnglandToChart(df, "green", "0 - 5", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 6-17")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(1, df), "blue", "Age Group: 6 - 17", False)
    #addEnglandToChart(df, "blue", "0 - 5", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 18-64")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(2, df), "orange", "Age Group: 18 - 64", False)
    #addEnglandToChart(df, "orange", "0 - 5", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 65-84")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(3, df), "indigo", "Age Group: 65 - 84", False)
    #addEnglandToChart(df, "indigo", "0 - 5", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 85+")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(4, df), "red", "Age Group: 85+", False)

    chart.draw_chart("Date", "Beds Used Per Capita (Per 1,000,000 People)", "COVID-19: Daily Hospital Admissions (Diagnoses + Admissions) Per Capita (England)", "HOSDATA_AdmissionsByAge", True)

def drawAdsDiags():

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 0-5")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "green", "Age Group: 0 - 5", False)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 6-17")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "blue", "Age Group: 6 - 17", False)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 18-64")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "orange", "Age Group: 18 - 64", False)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 65-84")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "indigo", "Age Group: 65 - 84", False)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 85+")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "red", "Age Group: 85+", False)


    chart.draw_chart("Date", "Beds Used", "COVID-19: Daily Hospital Admissions (Diagnoses + Admissions) Actual (England)", "HOSDATA_AdmissionsByAgeActual", True)


def drawC19Abs():
    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)

    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Covid Absences")

    df1 = df1.reset_index() #remove dates as the index
    chart.add_bar_plot(df1["Dates"], df1["ENGLAND"], "pink", "COVID-19 NHS Absences")
    chart.add_scatter_plot(govData.get_gov_date_Series(), govData.get_hospital_cases(), "indigo", "People in Hospital with COVID-19", False, False)

    #df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses Total")
    #df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions Total")
    #df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    #addEnglandToChart(df, "indigo", "Daily Hospital Cases", True)

    chart.add_scatter_plot(govData.get_gov_date_Series(), govData.get_new_cases(), "orange", "COVID-19 Cases", False, False)
    chart.draw_chart("Date", "Staff Absences", "COVID-19: C19 Related NHS Staff Absenses (England)", "HOSDATA_Absences", True)

def drawPopulaitonChart():

    nChart = COVIDCHART()
    nChart.clear_chart()

    nChart.add_bar_chart(["0 - 5","6 - 17","18 - 64","65 - 84", "85+"], adjustedPop, "teal")
    nChart.draw_chart("Age Group", "Number of Poeple", "Number of People in Each Age Group - ONS Population Estimates (England)", "HOSDATA_age_groups", False)

def drawRecovery():
    chart.clear_chart()

    df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 0-5")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 0-5")
    df2 = hospitalData.join_totals_datasets("data/hospitalData", "Discharges 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "green", "Age Group: 0 - 5", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 6-17")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 6-17")
    df2 = hospitalData.join_totals_datasets("data/hospitalData", "Discharges 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "blue", "Age Group: 6 - 17", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 18-64")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 18-64")
    df2 = hospitalData.join_totals_datasets("data/hospitalData", "Discharges 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "orange", "Age Group: 18 - 64", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 65-84")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 65-84")
    df2 = hospitalData.join_totals_datasets("data/hospitalData", "Discharges 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "indigo", "Age Group: 65 - 84", True)

    df = hospitalData.join_totals_datasets("data/hospitalData", "Diagnoses 85+")
    df1 = hospitalData.join_totals_datasets("data/hospitalData", "Admissions 85+")
    df2 = hospitalData.join_totals_datasets("data/hospitalData", "Discharges 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "red", "Age Group: 85+", True)

    chart.draw_chart("Date", "Number of People", "COVID-19: Gross Number of People Admitted to Hospital ((Admissions + Diagnoses) - Discharges) (England)", "HOSDATA_Recovered", True)

def drawFromNursing():

    chart.clear_chart()
    chart.set_chart_params(False, False, True, True)
    df = hospitalData.join_totals_datasets("data/hospitalData", "Total HospAdm From Care Nursing")
    addEnglandToChart(df, "red", "Total HospAdm From Care Nursing", True)

    chart.draw_chart("Date", "Number of People", "COVID-19: TEST", "HOSDATA_TEST", True)

def bedCom():

#
#   WIP FOR YEARLY COMP DOES NOT WORK YET
#
#

    df2 = hospitalData.join_totals_datasets("data/hospitalData", "MV Beds Occupied Covid-19")
    
    chart.clear_chart()
    df2 = df2.reset_index()

    subset = df2[df2['Dates'].dt.year == 2020]
    subset1 = df2[df2['Dates'].dt.year == 2021]

    subset['Dates'] = subset['Dates'].dt.strftime('%m-%d') #Remove the year from the date
    chart.add_scatter_plot(subset["Dates"], subset["ENGLAND"], "black", "test 1", False, False)

    #subset1['Dates'] = subset1['Dates'].dt.strftime('%m-%d')
    #chart.add_scatter_plot(subset1["Dates"], subset1["ENGLAND"], "black", "test 1", False, True)

    chart.draw_chart("Date", "Number of People", "COVID-19: TEST", "HOSDATA_TESTA", True)




drawBedsvsBeds()
drawAdsDiagsActual()
drawAdsDiagsPerCap()
drawAdsDiags()
drawC19Abs()
drawPopulaitonChart()
drawRecovery()
#drawFromNursing()
#drawMechBeds()
#bedCom()





