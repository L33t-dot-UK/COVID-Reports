import pages_01_Overview as page1
import pages_02_Cases_Deaths as page2
import pages_03_Dashboard as page3
import pages_04_Testing as page4
import pages_05_Lockdown as page5
import pages_06_Vaccinations as page6

import functions_get_Data as getData
import functions_Chart as chart

print("------------------ COVID REPORTS JOB STARTED ------------------")

getData.get_Data()
getData.get_Aged_Data()

page1.draw_Overview("false", "true")
page1.draw_DeathsVdeaths("false", "true")

page2.draw_Scatter_Aged_Cases_per_Million(0,19)
page2.draw_Bar_Aged_Cases_per_Million()
page2.draw_Scatter_Aged_Cases(0, 19)
page2.draw_Age_Cases_Treemap()
page2.draw_Scatter_Aged_Deaths_per_Million(0,19)
page2.draw_Bar_Aged_Deaths_per_Million()
page2.draw_Age_Deaths_Treemap()
page2.draw_Age_Deaths_Bar_Under_vs_Over(12, "Under 60's", "Over 60's", "COVID 19 - Age Profile of Deaths Under 60's Vs Over 60's","images/ageUnder60VSover.png")
page2.draw_Age_Deaths_Bar_Under_vs_Over(10, "Under 50's", "Over 50's", "COVID 19 - Age Profile of Deaths Under 50's Vs Over 50's","images/ageUnder50VSover.png")
page2.draw_Bar_Aged_Cases()
page2.draw_Scatter_Aged_Deaths(0,19)
page2.draw_Bar_Aged_Deaths()

page4.draw_Scatter_Cases_LFFT_PCR()
page4.draw_Scatter_PositivityRate()
page4.draw_Scatter_pRate_Cases_deaths()
page4.draw_Scatter_Tests_Conducted()

page5.draw_Daily_Growth_Rate()

page6.draw_Comp_Graphs()
chart.put_Side_By_Side("images/yearlyCompCases.png", "images/yearlyCompDeaths.png", "images/yearCompCasesDeaths.png")
chart.put_Side_By_Side("images/yearlyCompHospital_Admissions.png", "images/yearlyCompPeople_in_Hospital_With_C19.png", "images/YearCompHospital.png")
page2.draw_Scatter_Aged_Cases_Grouped()
page2.draw_Scatter_Aged_Death_Grouped()
chart.put_Side_By_Side("images/ageGroupCases.png", "images/ageGroupDeaths.png", "images/agedGroupedData.png")

page3.createDashboard() #Do this last so we don't need to reload data

print("------------------ COVID REPORTS JOB COMPLETE ----------- -------")