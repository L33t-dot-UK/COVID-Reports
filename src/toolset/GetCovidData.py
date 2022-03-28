class GetCOVIDData:
    '''
    Create the object and 2 CSV files will be created data.csv and ageData.csv.
    These files contain the fields indicated below and downloads, data from the
    UK Governments COVID Dashboard using their own API version 1.

    This class has not methods everything is done in the constructor.

    If you want different datasets goto https://coronavirus.data.gov.uk/details/download to
    choose which datasets to download and amend the below code. If new datasets are downloaded 
    then the Class LoadDataSets.py will need to be amended if your using it.

    .. Note:: Age profiled data for Scotland, Wales and NI is not available. If you select one of these nations the age profiled data will not be downloaded. You will only download non-age specific data saved in data.csv
    '''
    from uk_covid19 import Cov19API #This is the UK Governments COVID API to install use "PIP install uk_covid19"
    from .BenchMark import Benchmark as Benchmark
    BENCH = Benchmark()
    BENCH.set_bench(False) #Bechmark output will be printed if this is set to true
    
    def __init__(self, nation):
        '''
        Will download the data, create data.csv and ageData.csv

        Args:
            nations: String Value, can be "England", "Scotland" or "Wales"
        '''

        #This is where you put all the fields that you want to download
        #They will be put in the CSV file in this order; column 0 will have the date
        #column 1 will have the areaName, etc

        self.BENCH.bench_start()
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
            "newCasesLFDConfirmedPCRBySpecimenDate": "newCasesLFDConfirmedPCRBySpecimenDate",
            "newCasesPCROnlyBySpecimenDate": "newCasesPCROnlyBySpecimenDate",
            "newPCRTestsByPublishDate": "newPCRTestsByPublishDate",
            "newLFDTests": "newLFDTestsBySpecimenDate",
            "newCasesLFDOnlyBySpecimenDate": "newCasesLFDOnlyBySpecimenDate",
            "cumPeopleVaccinatedSecondDoseByPublishDate": "cumPeopleVaccinatedSecondDoseByPublishDate",
            "newCasesByPublishDate": "newCasesByPublishDate"
        }

        england_only = [
            "areaType=nation",
            "areaName=" + nation
        ]

        try:
            api = self.Cov19API(filters=england_only, structure=cases_and_deaths)
            api.get_csv(save_as="data/autoimport/data" + nation + ".csv")
            print("--GET COVID DATA CLASS--: Data aquired and saved to data.csv")

        except Exception as E:
            print("--GET COVID DATA CLASS--: Error Fetching Data; See Below")
            print(E)
        
        self.BENCH.bench_end("GETCOVID DATA Downloaded data.csv")
        
        #Download the vaccine data
        self.BENCH.bench_start()
        cases_and_deaths = {
            "date": "date",
            "areaName": "areaName",
            "areaCode": "areaCode",
            "vaccinationsAgeDemographics": "vaccinationsAgeDemographics",
        }

        england_only = [
            "areaType=nation",
            "areaName=" + nation
        ]

        try:
            api = self.Cov19API(filters=england_only, structure=cases_and_deaths)
            api.get_csv(save_as="data/autoimport/vax_data" + nation + ".csv")
            print("--GET COVID DATA CLASS--: Data aquired and saved to vax_data.csv")

        except Exception as E:
            print("--GET COVID DATA CLASS--: Error Fetching Data; See Below")
            print(E)
        
        self.BENCH.bench_end("GETCOVID DATA Downloaded vax_data.csv")


        #This downloads aged profiled data and saves it to ageData.csv
        #This data is more difficult to handle once downloaded, to see how to
        #handle this data look at Class LoadDatasets.py
        self.BENCH.bench_start()

        print("--GET COVID DATA CLASS--: Aged profiled data is only available for England, Data saved in agedData.csv will be for England only")
        cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesBySpecimenDateAgeDemographics": "newCasesBySpecimenDateAgeDemographics",
        "newDeaths28DaysByDeathDateAgeDemographics": "newDeaths28DaysByDeathDateAgeDemographics"
        }

        england_only = [
        "areaType=nation",
        "areaName=England" #This age profiled data is only available for England
        ]

        try:
            api = self.Cov19API(filters=england_only, structure=cases_and_deaths)
            api.get_csv(save_as="data/autoimport/dataAge.csv")
            print("--GET COVID DATA CLASS--: Aged data aquired and saved to dataAge.csv")
        except Exception as E:
            print("--GET COVID DATA CLASS--: Error Aged Fetching Data; See Below")
            print(E)
        self.BENCH.bench_end("GETCOVID DATA Downloaded dataAge.csv")