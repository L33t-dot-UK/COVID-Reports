class LoadDataSets:
    '''
    This class will load datasets from the data CSV files, clean the datasets
    and make them accessable through callable functions.

    This class will offer the datasets up in two formats; 

        1. As a list
        2. In a dataframe

    Data is converted into a list is to make it accessable to non data scientists who haven't worked with
    dataframes before. I offer it up in dataframes for data scientists and to allow for easier analysis/incoroporation 
    into computer models.

    For usage examples view the examples scripts in the root folder of the github repo.
    '''

    
    import sys
    sys.path.append('./src/toolset')

    import pandas as pd
    import numpy as np
    from BenchMark import Benchmark as Benchmark
    import ast

    BENCH = Benchmark()

    BENCH.set_bench(False) #Bechmark output will be printed if this is set to true
    

    def __init__(self, to_load, nation):
        '''
        Sets up various variables used in the function contained in this class.

        Args:
            :to_load: Boolean Value, this tells the clas whether it should load the dataset, when set to false you can use this class to access the population data, colours and age groups.
            :nations: String Value, this is the nation that your dataset is for.

        .. Note:: Age profiled data is only available for England.
        '''

        self.nation = nation
        print("--LOAD DATA SETS CLASS--: LoadDataSets Object Created")

        #All variables below will be used in this class and accessible outside of this class
        #All variables that should be accessed outside of this class should be accessed using the GET helper
        #functions included in the class
        
        #Hard coded population stats from the ONS
        self.population = [3299637,
                            3538206,3354246,3090232,
                            3487863,3801409,3807954,3733642,3414297,3715812,3907461,3670651,3111835,
                            2796740,2779326,1940686,1439913,
                            879778,517273] # 2019 Population Data for England

        self.population_nation = [56286961, 5454000, 3136000, 1885000] #Population figures for the nations england, scotland, wales and NI

        #Line colour and age cats are used when creating the graphs to keep things the same. If you change these here it will affect all graphs
        #self.line_colour = ['black', 'gray', 'rosybrown', 'maroon', 'salmon', 'sienna', 'sandybrown', 'goldenrod', 'olive', 'lawngreen', 'darkseagreen', 'green', 'lightseagreen', 'darkcyan', 'steelblue', 'navy', 'indigo', 'purple', 'crimson']
        self.line_colour = ['#800000', '#9A6324', '#808000', '#469990', '#000075', '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6', '#fabed4', '#ffd8b1', '#aaffc3', '#dcbeff']
        self.line_colour.reverse()

        self.ageCategoriesString = ['Under 5', '05-09', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

        self.age_groups = ['00_04', '05_09','10_14', '15_19', '20_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']

        self.hospitalCases = ""
        self.newAdmssions = ""
        self.newCases = ""
        self.newDeaths = ""
        self.pillarTwoTests = ""
        self.deathsByReportDate = ""
        self.newPillarOneTestsByPublishDate = ""

        self.positivePCRtests = ""
        self.positiveLFDconfirmedByPCR = ""
        self.newLFDCases = ""

        self.newPCRTests = ""
        self.newLFDTests = ""

        self.cumSecondDose = ""
        
        self.GOVdateSeries = ""
        self.GOVdataset = ""

        self.agedGOVdataset = ""
        self.agedGOVdateSeries = ""

        self.caseDataByAge = ""
        self.deathDataByAge = ""

        self.yearDatesDataSet = ""
        self.yearDates = ""

        self.newCasesByReportDate = ""

        self.fullDataFrame = self.pd.DataFrame()
        self.fullDataFrameAgeCases = self.pd.DataFrame()
        self.fullDataFrameAgeDeaths = self.pd.DataFrame()

        if (to_load == True):
            self._load_data_from_file() #Populate variables in the class

    def _unpack_aged_data(self, data_to_unpack):
        '''
        Takes the aged data and unpacks it so we can use it in the graphs
        At various stages the government has reordered this data, if this happens
        this is the function that will be changed to make sure that the data is in
        the correct order for our graphs.

        Args:
            :data_to_unpack, Nested List, this will reorder the aged data and unnest the list.
        
        Returns:
            List of unpacked rearranged data.
        '''

        self.BENCH.bench_start()

        #Unpack the Data
        for ii in range(len(data_to_unpack)):
            data_to_unpack[ii] = eval(data_to_unpack[ii]) #convert the list from a list of strings to a dicitonary list

        TMPunPackedData = [0]*len(data_to_unpack)
        for ii in range(len(data_to_unpack)):
            TMPunPackedData[ii] = data_to_unpack[ii].copy()

        #Re-Order the list so we can use loops when creating aged profiled graphs
        for ii in range(0, len(data_to_unpack)):
            data_to_unpack[ii][1] = TMPunPackedData[ii][2]
            data_to_unpack[ii][2] = TMPunPackedData[ii][3]
            data_to_unpack[ii][3] = TMPunPackedData[ii][4]
            data_to_unpack[ii][4] = TMPunPackedData[ii][5]
            data_to_unpack[ii][5] = TMPunPackedData[ii][6]
            data_to_unpack[ii][6] = TMPunPackedData[ii][7]
            data_to_unpack[ii][7] = TMPunPackedData[ii][8]
            data_to_unpack[ii][8] = TMPunPackedData[ii][9]
            data_to_unpack[ii][9] = TMPunPackedData[ii][10]
            data_to_unpack[ii][10] = TMPunPackedData[ii][11]
            data_to_unpack[ii][11] = TMPunPackedData[ii][12]
            data_to_unpack[ii][12] = TMPunPackedData[ii][14]
            data_to_unpack[ii][13] = TMPunPackedData[ii][15]
            data_to_unpack[ii][14] = TMPunPackedData[ii][16]
            data_to_unpack[ii][15] = TMPunPackedData[ii][17]
            data_to_unpack[ii][16] = TMPunPackedData[ii][18]
            data_to_unpack[ii][17] = TMPunPackedData[ii][19]
            data_to_unpack[ii][18] = TMPunPackedData[ii][20] #Unassigned
            data_to_unpack[ii][19] = TMPunPackedData[ii][1]  #00-59
            data_to_unpack[ii][20] = TMPunPackedData[ii][13] #60+

        print("--LOAD DATA SETS CLASS--: Aged data unpacked")
        self.BENCH.bench_end("LOADDATASETS UnpackingAgedData")
        return data_to_unpack

    def unpack_data(self, field):
        '''
        Unpacks the aged data in to a dataframe.

        Args:
            :field: String Value, this is the column name in the dataframe that you want to access. Values for this can be either newCasesBySpecimenDateAgeDemographics or newDeaths28DaysByDeathDateAgeDemographics.

        Returns:
            Aged data in a dataframe that can be accessed using dataframe functions, for either cases or deaths using the above column names as the field.
        '''
        df = self.pd.read_csv('data/autoimport/dataAge.csv') #load the aged dataset from the CSV file
        df.drop(df.tail(32).index,inplace=True) #Remove the first days_to_sub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
        #Full DF
        new_df = self.pd.DataFrame(df[["date", field]])

        #do a first run to get column names
        dicTMP = new_df[field][0] #this is a single row
        dicTMP  = self.ast.literal_eval(dicTMP)
        TMPunPacked_df = self.pd.DataFrame(dicTMP )
        TMPunPacked_df["date"] = new_df["date"][0]

        fullUnPacked_df = self.pd.DataFrame(columns=TMPunPacked_df.columns)


        for ii in range(0 , len(new_df)):
            #iterate through each row and build an unpacked dataframe
            #This will allow filtering by age later on
            dic = new_df[field][ii] #this is a single row
            dic = self.ast.literal_eval(dic)
            unPacked_df = self.pd.DataFrame(dic)
            #unPacked_df["date"] = new_df["date"][ii]
            unPacked_df["date"] = self.np.array(new_df["date"][ii], dtype='datetime64')

            fullUnPacked_df = fullUnPacked_df.append(unPacked_df)

        fullUnPacked_df  = fullUnPacked_df.iloc[::-1] #Reverse the DataFrame

        return fullUnPacked_df 

    def _load_data_from_file(self):
        '''
        Loads data from the CSV file into lists that can be accessed via this class through helper methods. This will be called automatically when the object is created if to_load == True

        .. Note:: This is only called is to_load == True when creating the LoadDatasets object. If you want to create a LoadDatasets object to access static variable such as population or line_colour you can set to_load to False
        '''
        print("--LOAD DATA SETS CLASS--: Loading data from CSV files")
        self.BENCH.bench_start()
        try:
            self.yearDatesDataSet = self.pd.read_csv('data/static/dates.csv') #This will be used for yearly comparisons
            self.yearDates = self.yearDatesDataSet.iloc[0:,0].values

            self.GOVdataset =  self.pd.read_csv('data/autoimport/data' + self.nation + '.csv') #load the dataset from the CSV file

            if (self.nation == "England"):
                self.GOVdataset.drop(self.GOVdataset.tail(32).index,inplace=True) #Remove the first 32 rows so the data starts on the 02/03/20
            else:
                self.GOVdataset.drop(self.GOVdataset.tail(4).index,inplace=True) #Remove the first 32 rows so the data starts on the 02/03/20

            self.fullDataFrame = self.GOVdataset.copy()
            self.fullDataFrame = self.fullDataFrame.fillna(0)
            self.fullDataFrame = self.fullDataFrame[::-1]

            self.startDayOfYear = 62 #Day 62 is the 2nd March - If start date is changed this date should also change
        
            self.GOVdataset.fillna(0, inplace=True) #replace all null values with 0

            self.agedGOVdataset =  self.pd.read_csv('data/autoimport/dataAge.csv') #load the aged dataset from the CSV file
            
            print("--LOAD DATA SETS CLASS--: CSV Files Loaded & Flipped")
            
        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Loading CSV Files; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)
        
        #Now the files are loaded into memory we need to process the dataframe and assign it to some lists
        try:
            '''
            ----------------------------- Data from data.csv -----------------------------
            '''
            print("--LOAD DATA SETS CLASS--: Assigning Values From data.csv")
            self.hospitalCases = self.GOVdataset.iloc[0:,3].values
            self.newAdmssions = self.GOVdataset.iloc[0:,4].values
            
            self.newCases = self.GOVdataset.iloc[0:,5].values
            
            self.newDeaths = self.GOVdataset.iloc[0:,6].values
            self.pillarTwoTests = self.GOVdataset.iloc[0:,7].values
            self.deathsByReportDate = self.GOVdataset.iloc[0:,8].values
            self.newPillarOneTestsByPublishDate = self.GOVdataset.iloc[0:,9].values

            self.positiveLFDconfirmedByPCR = self.GOVdataset.iloc[0:,10].values
            self.positivePCRtests = self.GOVdataset.iloc[0:,11].values

            self.newPCRTests = self.GOVdataset.iloc[0:,12].values
            self.newLFDTests = self.GOVdataset.iloc[0:,13].values
            self.newLFDCases = self.GOVdataset.iloc[0:,14].values

            self.cumSecondDose = self.GOVdataset.iloc[0:,15].values

            self.newCasesByReportDate = self.GOVdataset.iloc[0:,16].values
            self.hospMVbeds = self.GOVdataset.iloc[0:,17].values

            self.GOVdateSeries = self.GOVdataset.iloc[0:,0].values
            
            #Now lets flip the list so index 0 will be the oldest value
            self.hospitalCases = self.hospitalCases[::-1]
            self.newAdmssions = self.newAdmssions[::-1]
            self.newCases = self.newCases[::-1]
            self.newDeaths = self.newDeaths[::-1]
            self.pillarTwoTests = self.pillarTwoTests[::-1]
            self.deathsByReportDate = self.deathsByReportDate[::-1]
            self.newPillarOneTestsByPublishDate = self.newPillarOneTestsByPublishDate[::-1]
            self.positiveLFDconfirmedByPCR = self.positiveLFDconfirmedByPCR[::-1]
            self.positivePCRtests = self.positivePCRtests[::-1]
            self.newPCRTests = self.newPCRTests[::-1]
            self.newLFDTests = self.newLFDTests[::-1]
            self.newLFDCases = self.newLFDCases[::-1]
            self.cumSecondDose = self.cumSecondDose[::-1]
            self.newCasesByReportDate = self.newCasesByReportDate[::-1]
            self.hospMVbeds = self.hospMVbeds[::-1]
            
            self.GOVdateSeries = self.GOVdateSeries[::-1]

        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Processing the Data Frame From data.csv; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)

        '''
        ----------------------------- Data from dataAge.csv -----------------------------
        '''
        print("--LOAD DATA SETS CLASS--: Assigning Values From dataAge.csv")

        try:
            self.agedGOVdataset.drop(self.agedGOVdataset.tail(32).index,inplace=True) #Remove the first days_to_sub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
            #go through the deaths array and check for null values, if you find them replace with zero values
            replacementString = "[{'age': '00_04', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '00_59', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0}, {'age': '05_09', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '10_14', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '15_19', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '20_24', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '25_29', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '30_34', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '35_39', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '40_44', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '45_49', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '50_54', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0}, {'age': '55_59', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '60+', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '60_64', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '65_69', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '70_74', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '75_79', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '80_84', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0.0}, {'age': '85_89', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0}, {'age': '90+', 'deaths': 0, 'rollingSum': 0, 'rollingRate': 0}]"
        
            self.agedGOVdataset = self.agedGOVdataset.replace("[]", replacementString) #Replace null values
            
            self.caseDataByAge = self.agedGOVdataset.iloc[0:,3].values
            self.deathDataByAge = self.agedGOVdataset.iloc[0:,4].values
            
            self.agedGOVdateSeries = self.agedGOVdataset.iloc[0:,0].values

            self.caseDataByAge = self.caseDataByAge[::-1] #Reorder the data
            self.deathDataByAge = self.deathDataByAge[::-1] #Reorder the data
            self.agedGOVdateSeries = self.agedGOVdateSeries[::-1]#Reorder the data

            print("--LOAD DATA SETS CLASS--: Reordering Values From dataAge.csv")
            #We need to reorder these values and thats what _unpack_aged_data does
            self.caseDataByAge = self._unpack_aged_data(self.caseDataByAge)
            self.deathDataByAge = self._unpack_aged_data(self.deathDataByAge)

            print("--LOAD DATA SETS CLASS--: The object is ready to use, please use getter methods to access data from this object.")

            #put back here            
            
        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Processing the Data Frame From ageData.csv; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)
        
        self.BENCH.bench_end("LOADDATASETS DATA loadDataFromFile")

            #Now we will create a dataframe enabling us to access this data using dataframe functions
        self.fullDataFrameAgeCases = self.unpack_data("newCasesBySpecimenDateAgeDemographics")
        self.fullDataFrameAgeDeaths = self.unpack_data("newDeaths28DaysByDeathDateAgeDemographics")
    
    '''
    ----------------------------- All getter functions are below -----------------------------
    .. Note:: These functions will return a copy of the list so it can be changed without changing the
    data within the object. This is important if the object is used to create multiple graphs
    where the data is manipulated in some way. By calling the getter methods you will always
    get the unmanipulated data. If you access the variables directly through assignment, data
    in the object will change when manipulated causing issues if the same object is used for
    multiple graphs. Always use these getter methods to access the data contained within this
    class.
    ------------------------------------------------------------------------------------------
    '''

    '''
    ----------------------------------------------------
    GETTER METHODS FOR THE NON-AGED DATASET FROM DATA.CSV
    ----------------------------------------------------
    '''
    

    def get_full_data_frame(self):
        '''
        Returns the full dataframe from the non-age profiled csv file.

        Returns:
            Dataframe representing the csv file data + nation.csv e.g. dataEngland.csv, this data is not age profiled.
        '''
        return self.fullDataFrame.copy() 
    

    def get_aged_data_frames(self):
        '''
        Returns full dataframes for aged cases and aged deaths.

        Returns:
            Dataframe representing the csv file dataAge.csv for cases and age deaths.
        '''
        return self.fullDataFrameAgeCases.copy(), self.fullDataFrameAgeDeaths.copy()


    def get_aged_data_cases(self, age_group):
        '''
        returns aged case data for a given age group as a dataframe.
        
        Args:
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

            .. Note:: To calculate the age group divide the target age by 5 and round down

        Returns:
            Dataframe representing the csv file dataAge.csv for cases.
        '''
        df = self.fullDataFrameAgeCases[self.fullDataFrameAgeCases['age'] == age_group]
        return df["cases"].copy()


    def get_aged_data_deaths(self, age_group):
        '''
        returns aged death data for a given age group as a dataframe.

        Args:
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

            .. Note:: To calculate the age group divide the target age by 5 and round down

        Returns:
            Dataframe representing the csv file dataAge.csv for age deaths.
        '''
        df = self.fullDataFrameAgeDeaths[self.fullDataFrameAgeDeaths['age'] == age_group]
        return df["deaths"].copy()


    def get_population_number_list(self):
        '''
        Returns the population list giving populaiton figures for each age group

        Returns:
            List of population figures from the ONS for each age group, i.e. populaiton[0] will be for 0_4 year olds, population[4] will be for 15_19 year olds, etc.
        '''
        return self.population.copy()

    def get_population_nation_list(self):

        return self.population_nation.copy()
    

    def get_line_colour_list(self):
        '''
        Returns line colours for graphs making all graphs look the same, used for age profiled graphs.

        Returns:
            List of colours used the age profiled graphs. If you want different colours change the line_colour list.
        '''
        return self.line_colour.copy()
    

    def get_age_cat_string_list(self):
        '''
        Returns age strings for each age categories used to label graphs.

        Returns:
            List of strings used for age profiled charts, these are the string descriptions of each age groups used in the legends of charts.
        '''
        return self.ageCategoriesString.copy()


    def get_hospital_cases(self):
        '''
        Returns an list with all detailing total people in hospital with COVID

        Returns:
            List of hospital cases for all age groups, hospital cases are people in hosiptal with a positive COVID test. These are not necessarily people being treated for COVID. This data is not released. 
        '''
        return self.hospitalCases


    def get_new_admssions(self):
        '''
        Returns an list with all hospital admissions.

        Returns:
            List of hosiptal admissions, these are people going into hospital per day. The hospital data accessed through the ReadHospitalData class splits these admissions into admissions and diagnoses.
        '''
        return self.newAdmssions.copy()
    

    def get_new_cases(self):
        '''
        Returns an list detailing all new COVID cases found by PCR and LFD.

        Returns:
            List of new COVID cases found by PCR and LFD by specimen date.
        '''
        return self.newCases.copy()
    

    def get_new_deaths(self):
        '''
        Returns an list with daily COVID deaths; these are deaths by death date and could be out of date for up to a week.

        Returns:
            List of deaths from people with COVID. These are deaths by death date and not reported date.
        '''
        return self.newDeaths.copy()
    

    def get_pillar_two_tests(self):
        '''
        Returns all pillar 2 tests that have been conducted.

        Returns:
            List of how many pillar 2 tests have been conducted per day.
        '''
        return self.pillarTwoTests.copy()
    

    def get_deaths_by_report_date(self):
        '''
        Returns all deaths by reported date.

        Returns:
            List of daily deaths by reported date.
        '''
        return self.deathsByReportDate.copy()
    

    def get_new_pillar_one_tests_by_publish_date(self):
        '''
        Returns all pillar 1 tests.

        Returns:
            List of how many pillar one tests have been conducted per day.
        '''
        return self.newPillarOneTestsByPublishDate.copy()
    

    def get_positive_PCR_tests(self):
        '''
        Returns all positive PCR tests.

        Returns:
            List of positive PCR tests per day.
        '''
        return self.positivePCRtests.copy()
    

    def get_positive_LFD_confirmed_by_PCR(self):
        '''
        Returns all positive LFD confirmed by PCR.

        Returns:
            List of positive LFD tests that have been confirmed by PCR.
        '''
        return self.positiveLFDconfirmedByPCR.copy()
    

    def get_new_LFD_cases(self):
        '''
        Retuturns all positive LFD tests.

        Returns:
            List of cases found by LFD tests.
        '''
        return self.newLFDCases.copy() 


    def get_new_PCR_tests(self):
        '''
        Returns all PCR test conducted.

        Returns:
            List of how many PCR test have been conducted.
        '''
        return self.newPCRTests.copy()


    def get_new_LFD_tests(self):
        '''
        Returns all LFD tests conducted.

        Returns:
            List of how many LFD tests have been conducted.
        '''
        return self.newLFDTests.copy()


    def get_cum_second_dose(self):
        '''
        Returns the amount of 2nd doses administered

        Returns:
            List of second vaccine doses administered.
        '''
        return self.cumSecondDose.copy()
    

    def get_new_cases_by_report_date(self):
        '''
        Return new cases by report date.

        Returns:
            List of new cases by reported date for both PCR and LFD.
        '''
        return self.newCasesByReportDate


    def get_gov_date_Series(self):
        '''
        Returns a date arra to be used for the xAxis on charts.

        Returns:
            list of dates to be used with non age profiled graphs.

        .. Note:: Use this when creating time series graphs that use non-age profiled data.
        '''
        return self.np.array(self.GOVdateSeries, dtype='datetime64')


    def get_year_dates(self):
        '''
        Returns dates in a year for use with the year comparrisons and requres the CSV file dates.csv.

        Returns:
            list of days in the year, these are used for yearly comparisons.
        '''
        
        return self.yearDates.copy()
        #return self.np.array(self.yearDates.copy(), dtype='datetime64')

    def get_mv_beds(self):
        '''
        Returns number of people in mechanical ventalation beds

        Returns:
            list of number of people in mechanical ventalation beds
        '''

        return self.hospMVbeds

    '''
    ----------------------------------------------------
    GETTER METHODS FOR THE AGED DATASET FROM DATAAGE.CSV
    ----------------------------------------------------
    '''


    def get_aged_gov_date_series(self):
        '''
        Returns a date list to be used for the xAxis on charts when using age separated data.

        Returns:
            List of dates to be used with age profiled graphs.

        .. Note:: Use this when creating time series graphs that use age profiled data.
        '''

        #return self.agedGOVdateSeries.copy()
        return self.np.array(self.agedGOVdateSeries.copy(), dtype='datetime64')
    

    def get_death_data_by_age_all(self):
        '''
        Returns a multidimensional list with all death data by date.

        Returns:
            List[dayOfYear][age_group][deaths] list of all deaths spilt into age groups.
        '''
        return self.deathDataByAge
        

    def get_death_data_by_age(self, dayOfYear, age_group):
        '''
        This will return the number of deaths for a given day and a given age group. Age groups go from 0 to 18 and days go from 0 to len(n).

        Args:
            :dayOfYear: Integer Value, this will be from 0 to how many days you have in your dataset.
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

            .. Note:: To calculate the age group divide the target age by 5 and round down.

        Returns:
            Integer Value of the amount of deaths on a given day for a given age group.
        '''
        return self.deathDataByAge[dayOfYear][age_group]['deaths']


    def get_aged_death_data(self, age_group):
        '''
        Returns an list of death values ready to plot, age groups from 0-18.

        Args:
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

            .. Note:: To calculate the age group divide the target age by 5 and round down.

        Returns:
            List of deaths by death date for the given age group.
        '''
        returnedData = [0]*len(self.deathDataByAge)
        for ii in range(0, len(self.deathDataByAge)):
            returnedData[ii] = self.deathDataByAge[ii][age_group]['deaths']
        return returnedData.copy()


    def get_case_data_by_age(self, dayOfYear, age_group):
        '''
        This will return the number of cases for a given day and a given age group. Age groups go from 0 to 18 and days go from 0 to len(n)

        Args:
            :dayOfYear: Integer Value, this will be from 0 to how many days you have in your dataset.
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

        .. Note:: To calculate the age group divide the target age by 5 and round down.

        Returns:
            Integer Value of the amount of cases on a given day for a given age group.

        '''
        return self.caseDataByAge[dayOfYear][age_group]['cases']


    def get_aged_case_data(self, age_group):
        '''
        Returns an list of case values ready to plot, age groups from 0-18

        Args:
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.

            .. Note:: To calculate the age group divide the target age by 5 and round down.

        Returns:
            List of cases by specimen date for the given age group.

        '''

        returnedData = [0]*len(self.caseDataByAge)
        for ii in range(0, len(self.caseDataByAge)):
            returnedData[ii] = self.caseDataByAge[ii][age_group]['cases']
        return returnedData.copy()
    

    def get_age_groups(self, age_group):
        '''
        Returns a given age group for a given age_group index, age groups from 0-18

        Args:
            :age_group: Integer Value, This will be from 0 to 18 and increases in 5 year increments.
        
        Returns:
            Integer Value corresponding to the age group that you assigned to age_group. For instance::

                get_age_groups(0)
            
            will return 00_04::

                get_age_groups(12)

            will return 60_64

        '''
        return self.caseDataByAge[0][age_group]['age']


    def get_age_groups_literal(self):
        '''
        Returns a list of age groups used in the aged data dataframe.

        Returns:
            List of labels that represent each age group within the dataframe.
        '''
        return self.age_groups