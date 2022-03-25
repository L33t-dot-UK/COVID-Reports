#[COMPLETED V1.0.0]


#NEED TO ADD DATA FRAME FUNCTIONALITY

class LoadDataSets:
    '''

    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    This class will load datasets from the CSV file, clean the datasets
    and make them accessable through callable functions.

    This class will offer the dataset up in two formats; 

        1. As a list
        2. In a dataframe

    The reason why I convert the data into a list is to make it accessable to non data scientists who haven't worked with
    dataframes before. I offer it up in dataframes for data scientists and to allow for easier analysis/incoroporation 
    into computer models.

    Example;

        govDataSet = LoadDataSets(true, "England") #Object Creation
        hospitalCases = govDataSet.getHospitalCases() #returns a list of hospital cases
        dateSeries = govDataSet.getGOVdateSeries() #Returns a list of dates for the Y axis on graphs
        
    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    import pandas as pd
    import numpy as np
    from toolset.BenchMark import Benchmark as Benchmark
    import ast

    BENCH = Benchmark()
    BENCH.setBench(False) #Bechmark output will be printed if this is set to true

    def __init__(self, toLoad, NATION):
        '''
        EXTERNAL FUNCTION CALLED WHEN THE OBJECT IS CREATED
        Sets up various variables used in the function contained in this class
        '''

        self.nation = NATION
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

        #Line colour and age cats are used when creating the graphs to keep things the same. If you change these here it will affect all graphs
        #self.lineColour = ['black', 'gray', 'rosybrown', 'maroon', 'salmon', 'sienna', 'sandybrown', 'goldenrod', 'olive', 'lawngreen', 'darkseagreen', 'green', 'lightseagreen', 'darkcyan', 'steelblue', 'navy', 'indigo', 'purple', 'crimson']
        self.lineColour = ['#800000', '#9A6324', '#808000', '#469990', '#000075', '#000000', '#e6194B', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6', '#fabed4', '#ffd8b1', '#aaffc3', '#dcbeff']
        self.lineColour.reverse()

        self.ageCategoriesString = ['Under 5', '05-09', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

        self.AgeGroups = ['00_04', '05_09','10_14', '15_19', '20_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']

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

        if (toLoad == True):
            self.LoadDataFromFile() #Populate variables in the class

    def unpackAgedData(self, dataToUnpack):
        '''
        INTERNAL FUNCTION - do not call
        Takes the aged data and unpacks it so we can use it in the graphs
        At various stages the government has reordered this data, if this happens
        this is the function that will be changed to make sure that the data is in
        the correct order for our graphs
        '''

        self.BENCH.benchStart()

        #Unpack the Data
        for ii in range(len(dataToUnpack)):
            dataToUnpack[ii] = eval(dataToUnpack[ii]) #convert the array from an array of strings to a dicitonary list

        TMPunPackedData = [0]*len(dataToUnpack)
        for ii in range(len(dataToUnpack)):
            TMPunPackedData[ii] = dataToUnpack[ii].copy()

        #Re-Order the array so we can use loops when creating aged profiled graphs
        for ii in range(0, len(dataToUnpack)):
            dataToUnpack[ii][1] = TMPunPackedData[ii][2]
            dataToUnpack[ii][2] = TMPunPackedData[ii][3]
            dataToUnpack[ii][3] = TMPunPackedData[ii][4]
            dataToUnpack[ii][4] = TMPunPackedData[ii][5]
            dataToUnpack[ii][5] = TMPunPackedData[ii][6]
            dataToUnpack[ii][6] = TMPunPackedData[ii][7]
            dataToUnpack[ii][7] = TMPunPackedData[ii][8]
            dataToUnpack[ii][8] = TMPunPackedData[ii][9]
            dataToUnpack[ii][9] = TMPunPackedData[ii][10]
            dataToUnpack[ii][10] = TMPunPackedData[ii][11]
            dataToUnpack[ii][11] = TMPunPackedData[ii][12]
            dataToUnpack[ii][12] = TMPunPackedData[ii][14]
            dataToUnpack[ii][13] = TMPunPackedData[ii][15]
            dataToUnpack[ii][14] = TMPunPackedData[ii][16]
            dataToUnpack[ii][15] = TMPunPackedData[ii][17]
            dataToUnpack[ii][16] = TMPunPackedData[ii][18]
            dataToUnpack[ii][17] = TMPunPackedData[ii][19]
            dataToUnpack[ii][18] = TMPunPackedData[ii][20] #Unassigned
            dataToUnpack[ii][19] = TMPunPackedData[ii][1]  #00-59
            dataToUnpack[ii][20] = TMPunPackedData[ii][13] #60+

        print("--LOAD DATA SETS CLASS--: Aged data unpacked")
        self.BENCH.benchEnd("LOADDATASETS UnpackingAgedData")
        return dataToUnpack
        
    def unpackData(self, field):
        '''
        unpacks the aged data in to a dataframe
        '''
        df = self.pd.read_csv('data/autoimport/dataAge.csv') #load the aged dataset from the CSV file
        df.drop(df.tail(32).index,inplace=True) #Remove the first daysToSub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
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

    def LoadDataFromFile(self):
        '''
        INTERNAL FUNCTION - called once the object has been created in the __init__ method
        Loads data from the CSV file into the variables
        '''
        print("--LOAD DATA SETS CLASS--: Loading data from CSV files")
        self.BENCH.benchStart()
        try:
            self.yearDatesDataSet = self.pd.read_csv('data/static/dates.csv') #This will be used for yearly comparisons
            self.yearDates = self.yearDatesDataSet.iloc[0:,0].values

            self.GOVdataset =  self.pd.read_csv('data/autoimport/data' + self.nation + '.csv') #load the dataset from the CSV file
            self.GOVdataset.drop(self.GOVdataset.tail(32).index,inplace=True) #Remove the first 32 rows so the data starts on the 02/03/20

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
        
        #Now the files are loaded into memory we need to process the dataframe and assign it to some arrays
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

            self.GOVdateSeries = self.GOVdataset.iloc[0:,0].values
            
            #Now lets flip the array so index 0 will be the oldest value
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
            
            self.GOVdateSeries = self.GOVdateSeries[::-1]

        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Processing the Data Frame From data.csv; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)

        '''
        ----------------------------- Data from dataAge.csv -----------------------------
        '''
        print("--LOAD DATA SETS CLASS--: Assigning Values From dataAge.csv")

        try:
            self.agedGOVdataset.drop(self.agedGOVdataset.tail(32).index,inplace=True) #Remove the first daysToSub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
            self.agedGOVdataset.fillna(0, inplace=True) #replace all null values with 0
            
            self.caseDataByAge = self.agedGOVdataset.iloc[0:,3].values
            self.deathDataByAge = self.agedGOVdataset.iloc[0:,4].values
            
            self.agedGOVdateSeries = self.agedGOVdataset.iloc[0:,0].values

            self.caseDataByAge = self.caseDataByAge[::-1] #Reorder the data
            self.deathDataByAge = self.deathDataByAge[::-1] #Reorder the data
            self.agedGOVdateSeries = self.agedGOVdateSeries[::-1]#Reorder the data

            print("--LOAD DATA SETS CLASS--: Reordering Values From dataAge.csv")
            #We need to reorder these values and thats what unpackAgedData does
            self.caseDataByAge = self.unpackAgedData(self.caseDataByAge)
            self.deathDataByAge = self.unpackAgedData(self.deathDataByAge)

            print("--LOAD DATA SETS CLASS--: The object is ready to use, please use getter methods to access data from this object.")

            #put back here            
            
        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Processing the Data Frame From ageData.csv; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)
        
        self.BENCH.benchEnd("LOADDATASETS DATA loadDataFromFile")

            #Now we will create a dataframe enabling us to access this data using dataframe functions
        self.fullDataFrameAgeCases = self.unpackData("newCasesBySpecimenDateAgeDemographics")
        self.fullDataFrameAgeDeaths = self.unpackData("newDeaths28DaysByDeathDateAgeDemographics")
    
    '''
    ----------------------------- All getter functions are below -----------------------------
    These functions will return a copy of the array so it can be changed without changing the
    data within the object. This is important if the object is used to create multiple graphs
    where the data is manipulated in some way. By calling the getter methods you will always
    get the unmanipulated data. If you access the variables directly through assignment, data
    in the object will change when manipulated causing issues if the same object is used for
    multiple graphs
    ------------------------------------------------------------------------------------------
    '''

    '''
    ----------------------------------------------------
    GETTER METHODS FOR THE NON-AGED DATASET FROM DATA.CSV
    ----------------------------------------------------
    '''
    
    def getFullDataFrame(self):
        '''
        Returns the full dataframe from the CSV file data.csv
        '''
        return self.fullDataFrame.copy() 
    
    def getAgedDataFrames(self):
        '''
        Returns full dataframes for aged cases and aged deaths
        '''
        return self.fullDataFrameAgeCases.copy(), self.fullDataFrameAgeDeaths.copy()

    def getAgedDataCases(self, ageGroup):
        '''
        returns aged case data for a given age group as a dataframe
        '''
        df = self.fullDataFrameAgeCases[self.fullDataFrameAgeCases['age'] == ageGroup]
        return df["cases"].copy()

    def getAgedDataDeaths(self, ageGroup):
        '''
        returns aged death data for a given age group as a dataframe
        '''
        df = self.fullDataFrameAgeDeaths[self.fullDataFrameAgeDeaths['age'] == ageGroup]
        return df["deaths"].copy()

    def getPopulationNumberArray(self):
        '''
        Returns the population array giving populaiton figures for each age group
        '''
        return self.population.copy()
    
    def getLineColourArray(self):
        '''
        Returns line colours for graphs making all graphs look the same, used for age profiled graphs
        '''
        return self.lineColour.copy()
    
    def getAgeCatStringArray(self):
        '''
        Returns age strings for each age categories used to label graphs
        '''
        return self.ageCategoriesString.copy()

    def getHospitalCases(self):
        '''
        Returns an array with all detailing total people in hospital with COVID
        '''
        return self.hospitalCases

    def getnewAdmssions(self):
        '''
        Returns an array with all hospital admissions
        '''
        return self.newAdmssions.copy()
    
    def getNewCases(self):
        '''
        Returns an array detailing all new COVID cases found by PCR and LFD
        '''
        return self.newCases.copy()
    
    def getNewDeaths(self):
        '''
        Returns an array with daily COVID deaths; these are deaths by death date and could be out of date for up to a week
        '''
        return self.newDeaths.copy()
    
    def getPillarTwoTests(self):
        '''
        Returns all pillar 2 tests that have been conducted
        '''
        return self.pillarTwoTests.copy()
    
    def getDeathsByReportDate(self):
        '''
        Returns all deaths by reported date
        '''
        return self.deathsByReportDate.copy()
    
    def getNewPillarOneTestsByPublishDate(self):
        '''
        Returns all pillar 1 tests
        '''
        return self.newPillarOneTestsByPublishDate.copy()
    
    def getPositivePCRtests(self):
        '''
        Returns all positive PCR tests
        '''
        return self.positivePCRtests.copy()
    
    def getPositiveLFDconfirmedByPCR(self):
        '''
        Returns all positive LFD confirmed by PCR
        '''
        return self.positiveLFDconfirmedByPCR.copy()
    
    def getNewLFDCases(self):
        '''
        retuturns all positive LFD tests
        '''
        return self.newLFDCases.copy() 

    def getNewPCRTests(self):
        '''
        Returns all PCR test conducted
        '''
        return self.newPCRTests.copy()

    def getNewLFDTests(self):
        '''
        Returns all LFD tests conducted
        '''
        return self.newLFDTests.copy()

    def getCumSecondDose(self):
        '''
        Returns the amount of 2nd doses administered
        '''
        return self.cumSecondDose.copy()
    
    def getnewCasesByReportDate(self):
        '''
        Return new cases by report date
        '''
        return self.newCasesByReportDate

    def getGOVdateSeries(self):
        '''
        Returns a date arra to be used for the xAxis on charts
        '''
        #return self.GOVdateSeries
        return self.np.array(self.GOVdateSeries, dtype='datetime64')


    def getAgedGOVdateSeries(self):
        '''
        Returns a date array to be used for the xAxis on charts when using age separated data
        '''
        #return self.agedGOVdateSeries.copy()
        return self.np.array(self.agedGOVdateSeries, dtype='datetime64')
    
    def getAgedGOVdateSeriesNPDTG(self):
        '''
        Returns a list of numpy datetime64 dates
        use these dates instead of the list if you need to plot misaligned data
        '''
        
        return self.np.array(self.agedGOVdateSeries.copy(), dtype='datetime64')

    def getYearDatesDataSet(self):
        '''
        QUERY
        '''
        #return self.yearDatesDataSet.copy()
        return self.np.array(self.yearDatesDataSet.copy(), dtype='datetime64')

    def getYearDates(self):
        '''
        Returns dates in a year for use with the year comparasons and requres the CSV file dates.csv
        '''
        return self.yearDates.copy()
        #return self.np.array(self.yearDates.copy(), dtype='datetime64')

    '''
    ----------------------------------------------------
    GETTER METHODS FOR THE AGED DATASET FROM DATAAGE.CSV
    ----------------------------------------------------
    '''
    def getDeathDataByAgeAll(self):
        return self.deathDataByAge
        
    def getDeathDataByAge(self, dayOfYear, ageGroup):
        '''
        This will return the number of deaths for a given day and a given age group
        Age groups go from 0 to 18 and days go from 0 to len(n)
        '''
        return self.deathDataByAge[dayOfYear][ageGroup]['deaths']

    def getRawDeathData(self):
        return self.deathDataByAge
 
    def getAgedDeathData(self, ageGroup):
        '''
        Returns an array of death values ready to plot, age groups from 0-18
        '''
        returnedData = [0]*len(self.deathDataByAge)
        for ii in range(0, len(self.deathDataByAge)):
            returnedData[ii] = self.deathDataByAge[ii][ageGroup]['deaths']
        return returnedData.copy()


    def getCaseDataByAge(self, dayOfYear, ageGroup):
        '''
        This will return the number of cases for a given day and a given age group
        Age groups go from 0 to 18 and days go from 0 to len(n)
        '''
        return self.caseDataByAge[dayOfYear][ageGroup]['cases']

    def getAgedCaseData(self, ageGroup):
        '''
        Returns an array of case values ready to plot, age groups from 0-18
        '''
        returnedData = [0]*len(self.caseDataByAge)
        for ii in range(0, len(self.caseDataByAge)):
            returnedData[ii] = self.caseDataByAge[ii][ageGroup]['cases']
        return returnedData.copy()
    

    def getAgeGroups(self, ageGroup):
        '''
        Returns a given age group for a givn agegroup index, age groups from 0-18
        '''
        return self.caseDataByAge[0][ageGroup]['age']

    def getAgeGroupsLiteral(self):
        '''
        Returns a list of age groups used in the aged data dataframe
        '''
        return self.AgeGroups