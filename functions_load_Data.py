import pandas as pd

#Populaiton stats saved here to make it easy to update them
population = [3299637,3538206,3354246,3090232,3487863,3801409,3807954,3733642,3414297,3715812,3907461,3670651,3111835,
                  2796740,2779326,1940686,1439913,879778,517273] # 2019 Population Data for England

    #https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/bulletins/annualmidyearpopulationestimates/mid2019estimates

lineColour = ['black', 'gray', 'rosybrown', 'maroon', 'salmon', 'sienna', 'sandybrown', 'goldenrod', 'olive', 'lawngreen', 'darkseagreen', 'green', 'lightseagreen', 'darkcyan', 'steelblue', 'navy', 'indigo', 'purple', 'crimson']
ageCategoriesString = ['Under 5', '05-09', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']
   
def assignValues():
    '''
    Assigns values from the Pandas dataframe GOVdataset to various global variables, it will also flip the array so the oldest variable is at
    the end of the array rather than the front enabling us to plot the data correctly
    
    '''
    global hospitalCases
    global newAdmssions
    global newCases
    global newDeaths
    global pillarTwoTests
    global deathsByReportDate
    global newPillarOneTestsByPublishDate

    global positivePCRtests
    global positiveLFDconfirmedByPCR
    global newLFDCases

    global newPCRTests
    global newLFDTests
    
    global GOVdateSeries

    hospitalCases = GOVdataset.iloc[0:,3].values
    newAdmssions = GOVdataset.iloc[0:,4].values
    
    newCases = GOVdataset.iloc[0:,5].values
    
    newDeaths = GOVdataset.iloc[0:,6].values
    pillarTwoTests = GOVdataset.iloc[0:,7].values
    deathsByReportDate = GOVdataset.iloc[0:,8].values
    newPillarOneTestsByPublishDate = GOVdataset.iloc[0:,9].values

    positiveLFDconfirmedByPCR = GOVdataset.iloc[0:,10].values
    positivePCRtests = GOVdataset.iloc[0:,11].values

    newPCRTests = GOVdataset.iloc[0:,12].values
    newLFDTests = GOVdataset.iloc[0:,13].values
    newLFDCases = GOVdataset.iloc[0:,14].values

    GOVdateSeries = GOVdataset.iloc[0:,0].values
    
    #Now lets flip the array so index 0 will be the oldest value
    hospitalCases = hospitalCases[::-1]
    newAdmssions = newAdmssions[::-1]
    newCases = newCases[::-1]
    newDeaths = newDeaths[::-1]
    pillarTwoTests = pillarTwoTests[::-1]
    deathsByReportDate = deathsByReportDate[::-1]
    newPillarOneTestsByPublishDate = newPillarOneTestsByPublishDate[::-1]
    positiveLFDconfirmedByPCR = positiveLFDconfirmedByPCR[::-1]
    positivePCRtests = positivePCRtests[::-1]
    newPCRTests = newPCRTests[::-1]
    newLFDTests = newLFDTests[::-1]
    newLFDCases = newLFDCases[::-1]
    
    GOVdateSeries = GOVdateSeries[::-1]


def reSizeDataSet(size):
    '''
    
    '''
    GOVdataset.drop(GOVdataset.tail(size).index,inplace=True)
    assignValues()
    
def get_Data():
    '''
    Loads the dataset into a pandas frame called GOVdataset
    '''
    try:
        global yearDatesDataSet
        global yearDates
        yearDatesDataSet = pd.read_csv('dates.csv') #This will be used for yearly comparisons
        yearDates = yearDatesDataSet.iloc[0:,0].values


        global GOVdataset

        GOVdataset =  pd.read_csv('data.csv') #load the dataset from the CSV file
        GOVdataset.drop(GOVdataset.tail(32).index,inplace=True) #Remove the first 32 rows so the data starts on the 02/03/20

        global startDayOfYear
        startDayOfYear = 62 #Day 62 is the 2nd March - If start date is changed this date should also change
        
        GOVdataset.fillna(0, inplace=True) #replace all null values with 0
        rowCounter = GOVdataset.iloc[0:,0].values
        assignValues() #Now assign values to various arrays
        
    except Exception as E:
        print("Government dataset error on load!")
        print(E)



#----------------------------------------- START OF AGED DATA -------------------------------------------
def loadData(category, toReOrder, daysToSub):
    CSVcol = 0
    if(category == 'cases'):
        CSVcol = 3
    elif (category == 'deaths'):
        CSVcol = 4

    #Load the Data
    try:
        GOVdataset =  pd.read_csv('dataAge.csv') #load the dataset from the CSV file
        #Please note that the death data starts on the 2/03/21 if we don't drop the first 32 rows we get errors this is done just for death data
        #We also do this for time series graphs as it is pointless to show data before 02/03/21 as there were very little cases
        GOVdataset.drop(GOVdataset.tail(daysToSub).index,inplace=True) #Remove the first daysToSub rows, for time series chart drop the first 32 rows 32 the data starts on the 02/03/20
        GOVdataset.fillna(0, inplace=True) #replace all null values with 0

        global GOVdateSeries

        dataByAge = GOVdataset.iloc[0:,CSVcol].values
        GOVdateSeries = GOVdataset.iloc[0:,0].values

        if(toReOrder == 'true'):
            dataByAge = dataByAge[::-1] #Reorder the data
            GOVdateSeries = GOVdateSeries[::-1]#Reorder the data

    except:
        print("Government Aged dataset error!")

    global unPackedData
    unPackedData = [0]*len(dataByAge) #Create an empty Array of the correct size

    #Unpack the Data
    for ii in range(len(unPackedData)):
        unPackedData[ii] = dataByAge[ii] #Take each day and assign all values to the array
        unPackedData[ii] = eval(unPackedData[ii]) #convert the array from an array of strings to a dicitonary list

    TMPunPackedData = [0]*len(unPackedData)
    for ii in range(len(unPackedData)):
        TMPunPackedData[ii] = unPackedData[ii].copy()

    for ii in range(0, len(unPackedData)):
        try:
            unPackedData[ii][1] = TMPunPackedData[ii][2]
            unPackedData[ii][2] = TMPunPackedData[ii][3]
            unPackedData[ii][3] = TMPunPackedData[ii][4]
            unPackedData[ii][4] = TMPunPackedData[ii][5]
            unPackedData[ii][5] = TMPunPackedData[ii][6]
            unPackedData[ii][6] = TMPunPackedData[ii][7]
            unPackedData[ii][7] = TMPunPackedData[ii][8]
            unPackedData[ii][8] = TMPunPackedData[ii][9]
            unPackedData[ii][9] = TMPunPackedData[ii][10]
            unPackedData[ii][10] = TMPunPackedData[ii][11]
            unPackedData[ii][11] = TMPunPackedData[ii][12]
            unPackedData[ii][12] = TMPunPackedData[ii][14]
            unPackedData[ii][13] = TMPunPackedData[ii][15]
            unPackedData[ii][14] = TMPunPackedData[ii][16]
            unPackedData[ii][15] = TMPunPackedData[ii][17]
            unPackedData[ii][16] = TMPunPackedData[ii][18]
            unPackedData[ii][17] = TMPunPackedData[ii][19]
            unPackedData[ii][18] = TMPunPackedData[ii][20] #Unassigned
            unPackedData[ii][19] = TMPunPackedData[ii][1]  #00-59
            unPackedData[ii][20] = TMPunPackedData[ii][13] #60+
        except Exception as e:
            print("Error Data")
            print(e)
            
def getUnPackedData(toReOrder, daysToSub):
    loadData('cases', toReOrder, daysToSub) #Load the data so we can get age groups
    return unPackedData

def getDataLength():
    loadData('cases', 'false', 0)
    return len(GOVdateSeries)
    

def getSubData(dataIndex, category, toReOrder, daysToSub):
    #Data index will be the age category i.e. 0-4.etc and the category will be the string value of what you want i.e. cases or deaths
    loadData(category, toReOrder, daysToSub) #Always drop the first 32 dates as this will always be used for time series graphs
    returnedData = [0]*len(unPackedData)
    try:
        for ii in range(len(unPackedData)):
            returnedData[ii] = unPackedData[ii][dataIndex][category]
    except Exception as e:
        print("Data Error (getData) - This error can be ignored")
        print(e)
        
    return returnedData
    
def getData(dataIndex, category, toReOrder):
    #Data index will be the age category i.e. 0-4.etc and the category will be the string value of what you want i.e. cases or deaths
    loadData(category, toReOrder, 32) #Always drop the first 32 dates as this will always be used for time series graphs
    returnedData = [0]*len(unPackedData)
    try:
        for ii in range(len(unPackedData)):
            returnedData[ii] = unPackedData[ii][dataIndex][category]
    except Exception as e:
        print("Data Error (getData) - This error can be ignored")
        print(e)
        
    return returnedData
    
def getTotals(dataIndex, category, toReOrder):
    if(category == 'deaths'):
        loadData(category, toReOrder, 32) #If we are totaling deaths drop first 32 rows as these contain no data anyway
    elif(category == 'cases'):
        loadData(category, toReOrder, 0) #if were totaling cases keep all rows
    
    returnedData = 0
    try:
        for ii in range(len(unPackedData)): #Calculate the total number of cases in each age group
            returnedData = returnedData + int(unPackedData[ii][dataIndex][category])
    except Exception as e:
        print("Data Error (getTotals) - This error can be ignored")
        print(e)

    loadData(category, toReOrder, 32) #This will stop certain errors if you wanted to plot data after totalling it
    return returnedData