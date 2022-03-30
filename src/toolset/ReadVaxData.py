class readVaxData:
    '''
    This class is used to read vaccination data from vax_data.csv
    for this we will use dataframes similar to how we dealt with hospital data
    '''

    
    import ast
    import numpy as np
    import pandas as pd
    

    def __init__(self, nation):

        self.nation = nation
        self.unpacked = self.unpack_data() #loads and unpacks vaccination data
        self.vax_age_groups = ['12_15', '16_17', '18_24','25_29', '30_34', '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_74', '75_79', '80_84', '85_89', '90+']
        self.vax_age_groups_string = ['12 to 15', '16 to 17', '18 to 24','25 to 29', '30 to 34', '35 to 39', '40 to 44', '45 to 49', '50 to 54', '55 to 59', '60 to 64', 
                                        '65 to 69', '70 to 74', '75 to 79', '80 to 84', '85 to 89', '90+']

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