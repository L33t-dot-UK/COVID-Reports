class readHospitalData():
    '''
    This class is designed to help wrangle data from the monthly hospital spreadsheets found at

    https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/

    This version of the class will allow you to get regonal total data from any worksheet 
    the excel files must in be date order where the first excel file should be the earliest
    '''
    import pandas as pd
    import os

    def __init__(self):
        pass

    def readinTotals(self, excel_file, ws):
        '''
        This will read the Hospitals worksheet from 

        https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/

        and turn the top of the worksheet into a dataframe, this only reads the totals from each worksheet for ENGLAND and the regions

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

    def readinAllTotals(self, directory):
        '''
        This will read in totals from all worksheets, takes around 7 seconds for each worksheet
        it will also merge files from the directory so ensure you just have your hospital data in
        there!
        '''

        #iterate through the directory
        excelFiles = self.os.listdir(directory)

        for ii in range(len(excelFiles)): #for each excel file
            print("Processing file " + excelFiles[ii])
            dataLocation = self.os.path.join(directory, excelFiles[ii]) #create the path to the excel file
            excel_file = self.pd.ExcelFile(dataLocation, engine='openpyxl') #open the excel file
            sheetNames = excel_file.sheet_names #get a list of sheet names

            df = [0] * len(sheetNames)
            for iii in range(len(sheetNames)):
                print("Processing worksheet " + sheetNames[iii])
                df[iii] = self.readinTotals(excel_file, sheetNames[iii])

        return df, sheetNames #return an array of dataframes and the sheet names

    def joinTotalsDataSets(self, directory, ws):
        '''
        This will scan the directory open each excel file and
        join the dataframes for totals for a specific worksheet
        '''
        #iterate through the directory
        excelFiles = self.os.listdir(directory)

        excel_file = [0] * len(excelFiles)
        for ii in range(len(excelFiles)): #load each excel file
            print("Processing file " + excelFiles[ii])
            dataLocation = self.os.path.join(directory, excelFiles[ii]) #create the path to the excel file
            excel_file[ii] = self.pd.ExcelFile(dataLocation, engine='openpyxl') #open the excel file

        df = [0] * len(excelFiles)
        for ii in range(len(excelFiles)): #Read the worksheet from each excel file
            df[ii] = self.readinTotals(excel_file[ii], ws)

        if (ws == "MV Beds Occupied Covid-19") or (ws == "MV Beds Occupied") or (ws == "Total HospAdm From Care Nursing") or (ws == "Reported Admissions & Diagnoses"):
            df[0].drop(df[0].tail(1).index,inplace=True) # drop last n rows, these worksheets contain extra number of rows

        #now merge the dataframes
        final_df = self.pd.concat(df)

        return final_df #return an array of dataframes and the sheet names