
from COVIDTOOLSET import CovidChart, readHospitalData as HOSPITALDATA
from COVIDTOOLSET import CovidChart as COVIDCHART
from COVIDTOOLSET import LoadDataSets as govData
import numpy as np

hospitalData = HOSPITALDATA()
govData = govData("true")
chart = COVIDCHART()

population = govData.getPopulationNumberArray()

adjustedPop = [0] * 5

adjustedPop[0] = population[0]
adjustedPop[1] = sum(population[1:4])
adjustedPop[2] = sum(population[4:13])
adjustedPop[3] = sum(population[13:17])
adjustedPop[4] = sum(population[17:19])

for pop in adjustedPop:
    print(f'{pop:,}')

def addEnglandToChart(df, colour, label, toDash):
    df = df.reset_index() #remove dates as the index
    chart.addScatterplot(df["Dates"].tolist(), df["ENGLAND"].tolist(), colour, label, toDash)

def calcPerMillion(ageGroup, df):
    df = df.apply(lambda x: (x / float(adjustedPop[ageGroup]) * 1000000), axis=1)
    return(df)


def addRegionsToChart(df):
    df = df.reset_index() #remove dates as the index
    chart.addScatterplot(df["Dates"].tolist(), df["East of England"].tolist(), "red", "East of England", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["London"].tolist(), "blue", "London", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["Midlands"].tolist(), "black", "Midlands", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["North East and Yorkshire"].tolist(), "green", "North East and Yorkshire", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["North West"].tolist(), "indigo", "North West", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["South East"].tolist(), "orange", "South East", "false")
    chart.addScatterplot(df["Dates"].tolist(), df["South West"].tolist(), "pink", "South West", "false")

def drawBedsvsBeds():

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")

    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Total Beds Occupied")
    df2= hospitalData.joinTotalsDataSets("hospitalData", "Total Beds Occupied Covid")

    df1 = df1.reset_index() #remove dates as the index
    chart.addBarplot(df1["Dates"].tolist(), df1["ENGLAND"].tolist(), "green", "Number of Total Occupied Beds")

    df2 = df2.reset_index() #remove dates as the index
    chart.addBarplot(df2["Dates"].tolist(), df2["ENGLAND"].tolist(), "red", "Number of Beds Used by COVID-19 Patients")


    bedCap = 124000
    bedCapArr = [0] * len(df2["Dates"].tolist())
    for ii in range(0, len(df2["Dates"].tolist())):
        bedCapArr[ii] = bedCap

    chart.addScatterplot(df2["Dates"].tolist(), bedCapArr, 'grey', 'Estimated Bed Capacity', 'true') 

    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Covid Absences")
    addEnglandToChart(df1, "indigo", "COVID19 NHS Staff Absences", "true")

    chart.drawChart("Date", "Percentage of Beds Used / Total Beds Occupied (Scaled, in thousands)", "COVID-19: Percentage of Occupied Beds Used by COVID Patients (England)", "HOSDATA_PercentBedsUsed", "true")

def drawMechBeds():

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")

    df1 = hospitalData.joinTotalsDataSets("hospitalData", "MV Beds Occupied")
    df2= hospitalData.joinTotalsDataSets("hospitalData", "MV Beds Occupied Covid-19")

    df1 = df1.reset_index() #remove dates as the index
    chart.addBarplot(df1["Dates"].tolist(), df1["ENGLAND"].tolist(), "green", "Number of Total Occupied Mechanical Ventalation Beds")

    df2 = df2.reset_index() #remove dates as the index
    chart.addBarplot(df2["Dates"].tolist(), df2["ENGLAND"].tolist(), "red", "Number of Mechanical Ventalation Beds Used by COVID-19 Patients")

    bedCap = 5500
    bedCapArr = [0] * len(df2["Dates"].tolist())
    for ii in range(0, len(df2["Dates"].tolist())):
        bedCapArr[ii] = bedCap

    chart.addScatterplot(df2["Dates"].tolist(), bedCapArr, 'grey', 'Estimated Critcal Care Bed Capacity', 'true') 

    chart.drawChart("Date", "Percentage of MV Beds Used / Total MV Beds Occupied (Scaled, in Hundreds)", "COVID-19: Percentage of Occupied Mechanical Ventalation Beds Used by COVID Patients (England)", "HOSDATA_MechBeds", "true")



def drawAdsDiagsActual():

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions Total")
    df2= hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses Total")

    addEnglandToChart(df2, "purple", "Daily Hospital Diagnoses (People Tested in Hospital with +ve PCR)", "false")
    addEnglandToChart(df1, "darkgoldenrod", "Daily Hospital Admissions (People going in to Hospital with +ve PCR)", "false")

    chart.drawChart("Date", "Beds Used", "COVID-19: Daily Hospital Admissions and Diagnoses (England)", "HOSDATA_AdsDiagnoses", "true")

def drawAdsDiagsPerCap():
    #------------------------ HOSPITAL ADMISSIONS PER CAP ------------------------

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 0-5")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(0, df), "green", "Age Group: 0 - 5", "false")
    #addEnglandToChart(df, "green", "0 - 5", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 6-17")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(1, df), "blue", "Age Group: 6 - 17", "false")
    #addEnglandToChart(df, "blue", "0 - 5", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 18-64")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(2, df), "orange", "Age Group: 18 - 64", "false")
    #addEnglandToChart(df, "orange", "0 - 5", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 65-84")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(3, df), "indigo", "Age Group: 65 - 84", "false")
    #addEnglandToChart(df, "indigo", "0 - 5", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 85+")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(calcPerMillion(4, df), "red", "Age Group: 85+", "false")


    chart.drawChart("Date", "Beds Used Per Capita (Per 1,000,000 People)", "COVID-19: Daily Hospital Admissions (Diagnoses + Admissions) Per Capita (England)", "HOSDATA_AdmissionsByAge", "true")

def drawAdsDiags():

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 0-5")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "green", "Age Group: 0 - 5", "false")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 6-17")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "blue", "Age Group: 6 - 17", "false")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 18-64")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "orange", "Age Group: 18 - 64", "false")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 65-84")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "indigo", "Age Group: 65 - 84", "false")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 85+")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    addEnglandToChart(df, "red", "Age Group: 85+", "false")


    chart.drawChart("Date", "Beds Used", "COVID-19: Daily Hospital Admissions (Diagnoses + Admissions) Actual (England)", "HOSDATA_AdmissionsByAgeActual", "true")


def drawC19Abs():
    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")

    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Covid Absences")

    df1 = df1.reset_index() #remove dates as the index
    chart.addBarplot(df1["Dates"], df1["ENGLAND"], "pink", "COVID-19 NHS Absences")
    chart.addScatterplot(govData.getGOVdateSeries(), govData.getHospitalCases(), "indigo", "People in Hospital with COVID-19", "false")

    #df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses Total")
    #df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions Total")
    #df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    #addEnglandToChart(df, "indigo", "Daily Hospital Cases", "true")

    chart.addScatterplot(govData.getGOVdateSeries(), govData.getNewCases(), "orange", "COVID-19 Cases", "false")
    chart.drawChart("Date", "Staff Absences", "COVID-19: C19 Related NHS Staff Absenses (England)", "HOSDATA_Absences", "true")

def drawPopulaitonChart():

    nChart = CovidChart()
    nChart.clearChart()

    nChart.addBarChart(["0 - 5","6 - 17","18 - 64","65 - 84", "85+"], adjustedPop, "teal")
    nChart.drawChart("Age Group", "Number of Poeple", "Number of People in Each Age Group - ONS Population Estimates (England)", "HOSDATA_AgeGroups", "false")

def drawRecovery():
    chart.clearChart()

    df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 0-5")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 0-5")
    df2 = hospitalData.joinTotalsDataSets("hospitalData", "Discharges 0-5")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "green", "Age Group: 0 - 5", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 6-17")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 6-17")
    df2 = hospitalData.joinTotalsDataSets("hospitalData", "Discharges 6-17")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "blue", "Age Group: 6 - 17", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 18-64")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 18-64")
    df2 = hospitalData.joinTotalsDataSets("hospitalData", "Discharges 18-64")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "orange", "Age Group: 18 - 64", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 65-84")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 65-84")
    df2 = hospitalData.joinTotalsDataSets("hospitalData", "Discharges 65-84")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "indigo", "Age Group: 65 - 84", "true")

    df = hospitalData.joinTotalsDataSets("hospitalData", "Diagnoses 85+")
    df1 = hospitalData.joinTotalsDataSets("hospitalData", "Admissions 85+")
    df2 = hospitalData.joinTotalsDataSets("hospitalData", "Discharges 85+")
    df["ENGLAND"] = df["ENGLAND"] + df1["ENGLAND"]
    df1["ENGLAND"] = df["ENGLAND"] - df2["ENGLAND"]
    addEnglandToChart(df, "red", "Age Group: 85+", "true")

    chart.drawChart("Date", "Number of People", "COVID-19: Gross Number of People Admitted to Hospital ((Admissions + Diagnoses) - Discharges) (England)", "HOSDATA_Recovered", "true")

def drawFromNursing():

    chart.clearChart()
    chart.setChartParams("false", "false", "true", "true")
    df = hospitalData.joinTotalsDataSets("hospitalData", "Total HospAdm From Care Nursing")
    addEnglandToChart(df, "red", "Total HospAdm From Care Nursing", "true")

    chart.drawChart("Date", "Number of People", "COVID-19: TEST", "HOSDATA_TEST", "true")

    

'''
drawBedsvsBeds()
drawAdsDiagsActual()
drawAdsDiagsPerCap()
drawAdsDiags()
drawC19Abs()
drawPopulaitonChart()
drawRecovery()
drawMechBeds()
drawFromNursing()
'''

drawC19Abs()


