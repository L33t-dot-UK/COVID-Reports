
from uk_covid19 import Cov19API #This is the UK Governments COVID API to install use "PIP install uk_covid19"

def get_Data():

    '''
    Gets data from the UK Governments COVID-19 Dashboard and saves it to data.csv

    This function will save 15 datasets starting at row 0 and ending at row 14
    '''

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "hospitalCases": "hospitalCases",
        "newAdmissions": "newAdmissions",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
        "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
        "newPillarTwoTestsByPublishDate": "newPillarTwoTestsByPublishDate",
        "newDeaths28DaysByPublishDate": "newDeaths28DaysByPublishDate",
        "newPillarOneTestsByPublishDate": "newPillarOneTestsByPublishDate",
        "newCasesLFDConfirmedPCRBySpecimenDate":"newCasesLFDConfirmedPCRBySpecimenDate",
        "newCasesPCROnlyBySpecimenDate":"newCasesPCROnlyBySpecimenDate",
        "newPCRTestsByPublishDate":"newPCRTestsByPublishDate",
        "newLFDTests":"newLFDTests",
        "newCasesLFDOnlyBySpecimenDate":"newCasesLFDOnlyBySpecimenDate",
        "cumPeopleVaccinatedSecondDoseByPublishDate":"cumPeopleVaccinatedSecondDoseByPublishDate"
    }

    england_only = [
        'areaType=nation',
        'areaName=England'
    ]

    try:
        api = Cov19API(filters=england_only, structure=cases_and_deaths)
        api.get_csv(save_as="data.csv")
        print("Data aquired and saved to data.csv")
    except Exception as E:
        print("Get data error!")
        print(E)

def get_Aged_Data():

    '''
    Gets data from the UK Governments COVID-19 Dashboard and saves it to dataAge.csv

    This function will save 5 datasets starting at row 0 and ending at row 4
    '''

    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesBySpecimenDateAgeDemographics": "newCasesBySpecimenDateAgeDemographics",
        "newDeaths28DaysByDeathDateAgeDemographics": "newDeaths28DaysByDeathDateAgeDemographics"
    }

    england_only = [
        'areaType=nation',
        'areaName=England'
    ]

    try:
        api = Cov19API(filters=england_only, structure=cases_and_deaths)
        api.get_csv(save_as="dataAge.csv")
        print("Aged data aquired and saved to dataAge.csv")
    except:
        print("Get data error!")