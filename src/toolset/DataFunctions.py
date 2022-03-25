class Functions:
    '''
    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    Provides various functions when manipulating COVID data

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    import numpy as np
    from toolset.LoadDatasets import LoadDataSets as loadDataSets
    
    def __init__(self): #set toLoad to true of you need to load data from CSV files
        print("--FUNCITONS CLASS--: Functions Class Created")
        self.dataSetLoader = self.loadDataSets(False, "NULL ")
        self.dataSetLoader = self.loadDataSets(False, "NULL")  #We don't need to reload CSV data as we're only using this object to get population data, 

    def calcTotalPerMillion(self, data, ageGroup):
        '''
        Pass in a n array of data and this will calculate the total per million for that array
        the data array should just be a list of time series numbers. You also need to pass in
        the age group 0 to 18.

        Returns a single value
        '''
        population = self.dataSetLoader.getPopulationNumberArray() #Load population data

        perMillionData = self.np.sum(data) / float(population[ageGroup])
        perMillionData = perMillionData * 1000000

        perMillionData = int(perMillionData) #cast to an int to remove the decimal place
        return perMillionData

    def calcTimeSeriesPerMillion(self, data, ageGroup):
        '''
        Pass in an array of data and this will calculate the per million for that time series array
        the data array should just be a list of time series numbers. You also need toLoad pass in
        the age group 0 toLoad 18.

        Returns time series array
        '''
        population = self.dataSetLoader.getPopulationNumberArray() #Load populaiton data

        perMillionData = [0] * len(data)
        for ii in range(len(data)):
            perMillionData[ii] = float(data[ii] / population[ageGroup])
            perMillionData[ii] = perMillionData[ii] * 1000000

        return perMillionData

    def getLastRecords(self, daysToSub, data):
        '''
        Will return n amount of last records, so for instance if you want the last 90 days of cases
        you would pass the arguments 90 and govData.getNewCases()
        '''
        tmpData = [0] * daysToSub
        cntr = 0
        for ii in range(len(data) - daysToSub, len(data)):
            tmpData[cntr] = data[ii]
            cntr = cntr + 1

        return tmpData


    def getFirstRecords(self, daysToSub, data):
        '''
        Returns the first n amount of records
        '''
        tmpData = [0] * daysToSub
        for ii in range(0, daysToSub):
            tmpData[ii] = data[ii]

        return tmpData

    def calcRatioAsPercentage(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as a string percentage
        Can be use to calculate CFR or other ratios, use this when wanting percentages for a table that are formatted
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2[ii]

            calcRatio[ii]  = calcRatio[ii] * 100
            calcRatio[ii] = "{:.3f}".format(calcRatio[ii])
            calcRatio[ii] = str(calcRatio[ii]) + "%"
        return calcRatio
    
    
    def calcRatioAsInt(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as an integer 
        Can be use to calculate CFR or other ratios, use this when wnating data to plot on a graph
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2[ii]

            calcRatio[ii]  = calcRatio[ii] * 100
        return calcRatio
    
    def scaleData(self, data, scaleFactor):
        '''
        Uae this when you want to scale data in a list
        '''
        for ii in range(len(data)):
            data[ii] = data[ii] * scaleFactor

        return data

    def calcRatioAsInt_noList(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as an integer 
        Can be use to calculate CFR or other ratios, use this when wnating data to plot on a graph
        Use this when data1 is a kist but data2 is a single value
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2

            calcRatio[ii]  = calcRatio[ii] * 100
        return calcRatio
    
    def addDatasets(self, set1, set2):
        '''
        Adds 2 datasets, both datasets must be of the same length
        This can be used to add deaths from different age groups together for instance
        O/P will be newSet[1] = data1[1] + data2[1], newSet[2] = data1[2] + data2[2],
        newSet[n] = data1[n] + data2[n], etc
        '''
        newSet = set1.copy()
        for ii in range(len(set1)):
            newSet[ii] = set1[ii] + set2[ii]
        return newSet
    
    def CalcCFR(self, lag, deaths, cases):
        '''
        Calculates the CFR with a specified lag in days
        '''
        CFR = [0] * (len(cases) - lag)

        for ii in range((len(cases) - lag)):
            try:
                CFR[ii] = float((deaths[ii + lag] / cases[ii])) * 100
                if CFR[ii] > 100: CFR[ii] = 100 #limit the CFR to 100 
            except: #Catch any 0 division errors
                CFR[ii] = 0
        return CFR
    
    def add_Aged_Data(self, cat, lLimit, hLimit, govData):
        '''
        This method will iterate through age cats and add the data together
        using the addDataSet Method
        '''
        aggData = [0] * len(govData.getAgedGOVdateSeries())

        for ii in range(lLimit, hLimit):
            if cat == 'deaths':
                data = govData.getAgedDeathData(ii)
            elif cat == 'cases':
                data = govData.getAgedCaseData(ii)

            aggData = self.addDatasets(aggData, data)

        aggDataStr = self.np.sum(aggData)
        aggDataStr = f'{aggDataStr:,}'
        return aggData, aggDataStr
