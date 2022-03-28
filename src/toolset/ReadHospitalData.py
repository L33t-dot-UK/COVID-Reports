class readHospitalData():
    '''
    This class is designed to help wrangle data from the monthly hospital spreadsheets found at

    https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/

    This version of the class will allow you to get regonal data from any worksheet. 
    
    .. Note:  The excel files must in be date order where the first excel file should be the earliest

    '''

    import pandas as pd
    import os


    def __init__(self):
        pass


    def read_in_totals(self, excel_file, ws):
        '''
        This will read the selected owrksheet form a given excel file.
        Then turn the top of the worksheet into a dataframe, this only reads the totals from each worksheet for ENGLAND and the english regions, it does not read in data for each trust.

        Args:
            excel_file: String Value, location of the excel file to be used.
            es: String Value, worksheet name within the excel file to read.

        Returns:
            A dataframe with all data from the totals part of any given worksheet.

        '''
        master_df = self.pd.read_excel(excel_file, sheet_name=ws, engine='openpyxl')
        #now we need to create a df for just to total data
        column_names = master_df.iloc[12:21, 3].tolist() #These will be our column names
        dates = master_df.iloc[11, 4:len(master_df.columns) - 3]
        dates = dates.tolist() #get the dates as list

        '''
        #THIS WAS AN ATTEMPT TO REMOVE NAT VALUES FROM THE DATES LIST IT DOES NOT WORK AS IT MAKES THE LIST TOO SHORT, 1 ELEMENT SHORTER THAN THE REST!

        cntr = 0
        try:
            for ii in range(0, len(dates) - 1):
                if self.pd.isnull(dates[ii]):
                    print(ws)
                    dates.pop(ii) #Remove the nan value 
                    cntr = cntr + 1
                    #pass
        except:
            #dates.append('nan')
            pass
        
        for ii in range (0, cntr):
            dates.append('CUNT') #Put some nan values at the end of the date list, these will be dealt with later
        '''
        column_values = master_df.iloc[12:21, 4:len(master_df.columns) - 3].copy() #read in the values excluding the dates

        #Now we need to create a df with the trusts as column names, dates as row indexes and the values as values

        values_dict = { "Dates" : dates} #Add the dates, these will be used as the index
        for ii in range(0, len(column_names)):
            values_dict[column_names[ii]] = column_values.iloc[ii, 0:len(column_values.columns)].tolist()  #create a list of dictionaries with values for each row
 
        totals_df = self.pd.DataFrame(values_dict)
        totals_df = totals_df.drop(index=2)
        totals_df = totals_df.set_index('Dates')
    
        print(totals_df.isna().sum())

        return totals_df.copy()


    def read_in_all_totals(self, directory):
        '''
        This will read in totals from all worksheets, takes around 7 seconds for each worksheet
        it will also merge files from the directory so ensure you just have your hospital data in
        there!

        Args:
            directory: String Value, the directory that contains hospital data.

        Returns:
            A dataframe that contains totals data from all files within the directory and for all worksheets. This function will merge the excel files.

        .. Note:: This method is very slow and can take up to 7 seconds per worksheet.
        '''

        #iterate through the directory
        excel_files = self.os.listdir(directory)

        for ii in range(len(excel_files)): #for each excel file
            print("Processing file " + excel_files[ii])
            data_location = self.os.path.join(directory, excel_files[ii]) #create the path to the excel file
            excel_file = self.pd.ExcelFile(data_location, engine='openpyxl') #open the excel file
            sheet_names = excel_file.sheet_names #get a list of sheet names

            df = [0] * len(sheet_names)
            for iii in range(len(sheet_names)):
                print("Processing worksheet " + sheet_names[iii])
                df[iii] = self.read_in_totals(excel_file, sheet_names[iii])

        return df, sheet_names #return an array of dataframes and the sheet names


    def join_totals_datasets(self, directory, ws):
        '''
        This will scan the directory open each excel file and
        join the dataframes for totals for a specific worksheet.

        This methods similar to the above one however it will onlt merge data for the selected worksheet.

        Args:
            directory: String Value, this is the directory where the hospital data is.
            ws: String Value, this is the worksheet that you want to read.
        '''
        #iterate through the directory
        excel_files = self.os.listdir(directory)

        excel_file = [0] * len(excel_files)
        for ii in range(len(excel_files)): #load each excel file
            print("Processing file " + excel_files[ii])
            data_location = self.os.path.join(directory, excel_files[ii]) #create the path to the excel file
            excel_file[ii] = self.pd.ExcelFile(data_location, engine='openpyxl') #open the excel file

        df = [0] * len(excel_files)
        for ii in range(len(excel_files)): #Read the worksheet from each excel file
            df[ii] = self.read_in_totals(excel_file[ii], ws)

        if (ws == "MV Beds Occupied Covid-19") or (ws == "MV Beds Occupied") or (ws == "Total HospAdm From Care Nursing") or (ws == "Reported Admissions & Diagnoses"):
            df[0].drop(df[0].tail(1).index,inplace=True) # drop last n rows, these worksheets contain extra number of rows

        #now merge the dataframes
        final_df = self.pd.concat(df)

        return final_df #return an array of dataframes and the sheet names