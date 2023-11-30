class readVaxData:
    '''
    This class is used to read vaccination data from vax_data.csv
    for this we will use dataframes similar to how we dealt with hospital data
    '''

    
    import ast
    import numpy as np
    import pandas as pd
    import os
    import re
    from datetime import datetime
    

    def __init__(self, nation):

        self.nation = nation
        self.unpacked = self.unpack_data() #loads and unpacks vaccination data
        self.vax_age_groups = ['05_11', '12_15', '16_17', '18_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']

        self.vax_age_groups_4th = ['05-11', '12-15', '16-17', '18-24','25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'] #Age groupings are different for 4th dose as this comes from NHS and not UKHSA

        self.vax_age_groups_string = ['5 to 11', '12 to 15', '16 to 17', '18 to 24','25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64', 
                                        '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90+']
        
        self.plus_80_pop = []
        self.calc_80_plus_population() #Calculates population for 80+ age group for use with NHS data

    def get_vax_data(self):
        '''
        Loads the data into a dataframe.

        Returns:
            Vaccination dataframe in the nested list format.
        '''
        vax_df = self.pd.read_csv("data/autoimport/vax_data" + self.nation + ".csv")
        return vax_df
    
    def unpack_data(self):
        '''
        unpacks the vaccination data as each day is in a nested list.

        Returns:
            The full unpacked dataframe .
        '''
        df = self.get_vax_data()

        #Full DF
        new_df = self.pd.DataFrame(df[["date", "vaccinationsAgeDemographics"]])

        #do a first run to get column names
        dicTMP = new_df["vaccinationsAgeDemographics"][0] #this is a single row
        dicTMP  = self.ast.literal_eval(dicTMP)
        TMPunPacked_df = self.pd.DataFrame(dicTMP )
        TMPunPacked_df["date"] = new_df["date"][0]

        fullUnPacked_df = self.pd.DataFrame(columns=TMPunPacked_df.columns)


        for ii in range(0 , len(new_df)):
            #iterate through each row and build an unpacked dataframe
            #This will allow filtering by age later on
            dic = new_df["vaccinationsAgeDemographics"][ii] #this is a single row
            dic = self.ast.literal_eval(dic)
            unPacked_df = self.pd.DataFrame(dic)
            #unPacked_df["date"] = new_df["date"][ii]
            unPacked_df["date"] = self.np.array(new_df["date"][ii], dtype='datetime64')

            fullUnPacked_df = fullUnPacked_df.append(unPacked_df)

        fullUnPacked_df  = fullUnPacked_df.iloc[::-1] #Reverse the DataFrame

        return fullUnPacked_df 


    def get_vax_aged_data(self, age_group):
        '''
        returns vaccination data for a given age group as a dataframe. This makes it easier to navigate the dataframe.

        Args:
            :age_group: Integer Value, these age groups can be seen at the start of this class under self.vax_age_groups.

        Returns:
            A dataframe with vaccinaiton data for the selected age group.
        '''
        df = self.unpacked[self.unpacked['age'] == age_group]
        return df

    
    def get_packed_data(self):
        '''
        Returns all vaccinaiton data in the nested list format.
        '''
        return self.unpacked


    def get_vax_age_groups(self):
        '''
        Returns the age groups as they are in the dataframe.
        '''
        return self.vax_age_groups.copy()


    def get_vax_age_groups_string(self):
        '''
        Returns the age groups for use in a graph or report.
        '''
        return self.vax_age_groups_string.copy()


    #-----------------------------------------------------------------------------------
    #THIS CODE DOES NOT USE AUTO IMPORTED DATA


    #CODE UNDER HERE IS UNDOCUMENTED



    #The below functions will read the date, 4th dose and age range fields from daily spreadsheets released by the NHS stats service found at;
    #https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-vaccinations/

    #This data can not be used with other vaccinaiton data as the age categories are different in order to use it with the other datasets you must call normalise_vax_data

    def read_spreadsheet(self, file_path):
        spreadsheet = self.pd.read_excel(file_path, sheet_name = "Total Vaccinations by Age", engine = "openpyxl")

        #EXTRACT THE DATE FROM THE WORKSHEET AND SAVE IT AS A DATETIME OBJECT
        temp_date = spreadsheet.iloc[2,2] #This is the cell with the date range
        temp_date = temp_date.split('to ')
        date = temp_date[1]
        pattern = r'(?<=[0-9])(?:st|nd|rd|th)' #regex expression to remove date ordinal
        date =  self.re.sub(pattern, '',date) #apply regex
        date =  self.datetime.strptime(date, '%d %B %Y') #convert the string date to a datetime object

        if date < self.datetime(2022, 4, 27): #New age group added on the 27th April 2022 5 - 11 year olds
            #Now get the age ranges
            age_ranges = spreadsheet.iloc[14:29,1] 
            #Now get the figures
            jabs = spreadsheet.iloc[14:29,6]

            first_dose = spreadsheet.iloc[14:29,3]
            second_dose = spreadsheet.iloc[14:29,4]
            third_dose = spreadsheet.iloc[14:29,5]

            age_ranges = self.pd.concat([self.pd.Series(["05-11"]), age_ranges])
            jabs = self.pd.concat([self.pd.Series([0]), jabs])
            first_dose = self.pd.concat([self.pd.Series([0]), first_dose])
            second_dose = self.pd.concat([self.pd.Series([0]), second_dose])
            third_dose = self.pd.concat([self.pd.Series([0]), third_dose])
        else:
            #Now get the age ranges
            age_ranges = spreadsheet.iloc[14:30,1] #An extra age group needs to be accounted for
            #Now get the figures
            jabs = spreadsheet.iloc[14:30,6] #An extra age group needs to be accounted for

            first_dose = spreadsheet.iloc[14:30,3]
            second_dose = spreadsheet.iloc[14:30,4]
            third_dose = spreadsheet.iloc[14:30,5]

        #Now package all the data up as a dataframe
        values_dict = { "Dates" : date, "age": age_ranges, "4th Dose": jabs, "1st Dose": first_dose, "2nd Dose": second_dose, "3rd Dose": third_dose} #Add the dates, these will be used as the index

        vax_df =  self.pd.DataFrame(values_dict)

        
        vax_df = vax_df.replace("5-11", "05-11") #This needs to be done or the sorting method won't work properly

        return vax_df


    #This function will open every spreadsheet in a directory adding the data to a data frame using the read_spreadsheet function
    def get_vax_dataframe_4th_dose(self, directory):

        master_df =  self.pd.DataFrame()
        excel_files =  self.os.listdir(directory)
        
        for ii in range(len(excel_files)):
            data_location =  self.os.path.join(directory, excel_files[ii])
            if (data_location.split(".")[1] == "xlsx"):
                master_df =  self.pd.concat([master_df,  self.read_spreadsheet(data_location)])
            else:
                pass #ignore the file as it is not a spreadsheet

        master_df = master_df.sort_values(by=['Dates', "age"]) #sort the dataframe by date and age
        #master_df = master_df.sort_values(by=['Dates']) #sort the dataframe by date and age

        #Create a column with actual values rather than cumalative

        values = master_df["4th Dose"].tolist()
        actual_jabs = [0] * len(values)
        for ii in range(16, len(values)): #16 will need changing if new age ranges are added
            if isinstance(values[ii], str):
                values[ii] = 0
            actual_jabs[ii] =  values[ii] - values[ii - 16] #16 will need changing if new age ranges are added

        master_df["daily_doses"] = actual_jabs #Add the actual jabs to the dataframe
        master_df = master_df.reset_index(drop=True)
            
        return master_df

    def calc_80_plus_population(self):
        tot_population = 0

        df = self.get_vax_aged_data(self.vax_age_groups[15])
        tot_population = tot_population + df["VaccineRegisterPopulationByVaccinationDate"].tolist()[1]
        df = self.get_vax_aged_data(self.vax_age_groups[16])
        tot_population = tot_population + df["VaccineRegisterPopulationByVaccinationDate"].tolist()[1]
        df = self.get_vax_aged_data(self.vax_age_groups[17])
        tot_population = tot_population + df["VaccineRegisterPopulationByVaccinationDate"].tolist()[1]

        #Create a population list so we can use it with the calc_ratio method
        self.plus_80_pop = [0] * len(df["VaccineRegisterPopulationByVaccinationDate"].tolist())

        for iii in range (0, len(self.plus_80_pop)):
            self.plus_80_pop[iii] = tot_population

    def get_80_plus_pop_list(self):
        return  self.plus_80_pop.copy()
