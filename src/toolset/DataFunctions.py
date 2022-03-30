class Functions:
    '''
    Provides various functions when manipulating COVID data. These functions are mainly to be used with List data and will help you to do certain things. Any functions that will be reused should be put here.

    '''
    
    import sys
    sys.path.append('./src/toolset')

    
    import numpy as np

    from LoadDatasets import LoadDataSets as loadDataSets
    

    def __init__(self): #set toLoad to true of you need to load data from CSV files
        print("--FUNCITONS CLASS--: Functions Class Created")
        self.dataSetLoader = self.loadDataSets(False, "NULL ")
        self.dataSetLoader = self.loadDataSets(False, "NULL")  #We don't need to reload CSV data as we're only using this object to get population data, 


    def calc_total_per_million(self, data, age_group):
        '''
        Pass in a list of data and this will calculate the total per million for that list
        the data list should just be a list of time series numbers. You also need to pass in
        the age group 0 to 18.

        Args:
            :data: List, timseries data that contain the numbers such as case or death figures.
            :age_group: Integer Value, age group from 0 to 18, the method will get population data from toolset.LoadDatasets.

        Returns:
            A single integer value that will be the amount per million for the selected age group.
        '''
        population = self.dataSetLoader.get_population_number_list() #Load population data

        perMillionData = self.np.sum(data) / float(population[age_group])
        perMillionData = perMillionData * 1000000

        perMillionData = int(perMillionData) #cast to an int to remove the decimal place
        return perMillionData


    def calc_time_series_per_million(self, data, age_group):
        '''
        Pass in an list of data and this will calculate the per million for that time series list
        the data list should just be a list of time series numbers. You also need toLoad pass in
        the age group 0 toLoad 18.

        Args:
            >data: List, timseries data that contain the numbers such as case or death figures.
            >age_group: Integer Value, age group from 0 to 18, the method will get population data from toolset.LoadDatasets.

        Returns:
            A time series list with per million amounts for the selected age group.
        '''
        population = self.dataSetLoader.get_population_number_list() #Load populaiton data

        perMillionData = [0] * len(data)
        for ii in range(len(data)):
            perMillionData[ii] = float(data[ii] / population[age_group])
            perMillionData[ii] = perMillionData[ii] * 1000000

        return perMillionData


    def get_last_records(self, days_to_sub, data):
        '''
        Will return n amount of last records, so for instance if you want the last 90 days of cases
        you would pass the arguments 90 and govData.get_new_cases().

        Args:
            :days_to_sub: Integer Value, amount of days to return from the end of the dataset.
            :data: List, this is the full dataset as a list.
        
        Returns:
            A List of the last n values from the original dataset.
        '''
        tmpData = [0] * days_to_sub
        cntr = 0
        for ii in range(len(data) - days_to_sub, len(data)):
            tmpData[cntr] = data[ii]
            cntr = cntr + 1

        return tmpData


    def get_first_records(self, days_to_sub, data):
        '''
        Returns the first n amount of records

        Args:
            :days_to_sub: Integer Value, amount of days to return from the start of the dataset.
            :data: List, this is the full dataset as a list.
        
        Returns:
            A List of the first n values from the original dataset.
        '''
        tmpData = [0] * days_to_sub
        for ii in range(0, days_to_sub):
            tmpData[ii] = data[ii]

        return tmpData


    def calc_ratio_as_percentage(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as a string percentage
        Can be use to calculate CFR or other ratios, use this when wanting percentages for a table that are formatted.

        Args:
            >data1: Integer Value, this value will be divided by the next.
            >data2: Integer Value, this value will divide the above value; data1/data2.

        Returns:
            A string value with the percentage follows by % sign.
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2[ii]

            calcRatio[ii]  = calcRatio[ii] * 100
            calcRatio[ii] = "{:.3f}".format(calcRatio[ii])
            calcRatio[ii] = str(calcRatio[ii]) + "%"
        return calcRatio
    
    
    def calc_ratio_as_int(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as an integer 
        Can be use to calculate CFR or other ratios, use this when wnating data to plot on a graph.

        
        Args:
            :data1: Integer Value, this value will be divided by the next.
            :data2: Integer Value, this value will divide the above value; data1/data2.

        Returns:
            An Integer value representing the percentage.
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2[ii]

            calcRatio[ii]  = calcRatio[ii] * 100
        return calcRatio
    

    def scale_data(self, data, scale_factor):
        '''
        Uae this when you want to scale data in a list.

        Args: 
            :data: List, the data to be scaled.
            :scale_factor: Float Value, by how much to scale the data for a 25% increase use 1.25, etc.

        Returns:
            A List with the scaled values.
        '''
        for ii in range(len(data)):
            data[ii] = data[ii] * scale_factor

        return data


    def calc_ratio_as_int_noList(self, data1, data2):
        '''
        Used to divide one number by another and returning the result as an integer 
        Can be use to calculate CFR or other ratios, use this when wanting data to plot on a graph
        Use this when data1 is a list but data2 is a single value.

        Args:
            :data1: List, the values to be used to calculate the ratio.
            :data2: Integer Value, a single value to be use as the denominator for the calculation.

        Returns:
            A list of calulated values.
        '''
        calcRatio = [0] * len(data1)
        for ii in range(len(data1)):
            calcRatio[ii] = data1[ii] / data2

            calcRatio[ii]  = calcRatio[ii] * 100
        return calcRatio
    

    def add_datasets(self, set1, set2):
        '''
        Adds 2 datasets, both datasets must be of the same length
        This can be used to add deaths from different age groups together for instance
        O/P will be newSet[1] = data1[1] + data2[1], newSet[2] = data1[2] + data2[2],
        newSet[n] = data1[n] + data2[n], etc.

        Args:
            :set1: List, the first list to add to the next list.
            :set2: List, the second list to add to the first list.

        Returns:
            A List that contains both lists set1 + set2.

        '''
        newSet = set1.copy()
        for ii in range(len(set1)):
            newSet[ii] = set1[ii] + set2[ii]
        return newSet
    

    def Calc_CFR(self, lag, deaths, cases):
        '''
        Calculates the CFR with a specified lag in days.

        Args:
            :lag: Integer Value, the amount of lag in days to have between the cases and deaths.
            :deaths: List, a list of deaths.
            :cases: List, a list of cases.

        Returns:
            A List of values that is the ((deaths + lag) / cases) given as a percentage.

        '''
        CFR = [0] * (len(cases) - lag)

        for ii in range((len(cases) - lag)):
            try:
                CFR[ii] = float((deaths[ii + lag] / cases[ii])) * 100
                if CFR[ii] > 100: CFR[ii] = 100 #limit the CFR to 100 
            except: #Catch any 0 division errors
                CFR[ii] = 0
        return CFR
    

    def add_aged_data(self, cat, L_Limit, h_Limit, govData):
        '''
        This method will iterate through age cats and add the data together
        using the add_datasets Method.

        Args:
            :cat: String Value, this will be either deaths or cases.
            :L_Limit: Integer Value, this is the lower age limit 0 - 18.
            :h_Limit: Integer Value, this is the upper age limit 0 - 18.
            :govData: toolset.LoadDataSets object, this is the LoadDataSets object thats passed to this class.
        '''
        aggData = [0] * len(govData.get_aged_gov_date_series())

        for ii in range(L_Limit, h_Limit):
            if cat == 'deaths':
                data = govData.get_aged_death_data(ii)
            elif cat == 'cases':
                data = govData.get_aged_case_data(ii)

            aggData = self.add_datasets(aggData, data)

        aggDataStr = self.np.sum(aggData)
        aggDataStr = f'{aggDataStr:,}'
        return aggData, aggDataStr
