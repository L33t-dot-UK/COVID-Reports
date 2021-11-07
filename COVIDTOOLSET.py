#[COMPLETED V1.0.0]
from matplotlib.pyplot import table


class CovidChart:
    '''

    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    This class is used toLoad create covid charts
    it will automatically add lines of best fit and add vertical lines denoting important dates
    it will also add a timestamp and save the graph as a png image formatting fonts, etc

    Example;

        from COVIDTOOLSET import LoadDataSets as govDataClass
        from COVIDTOOLSET import CovidChart as CovidChart
        from COVIDTOOLSET import GetCOVIDData as getData

        pullData = getData("England") #get the latest data and save toLoad data.csv and ageData.csv

        govData = govDataClass() #Create a govDataClass
        dates = govData.getGOVdateSeries() #get dates from the class
        data = govData.getNewCases() #get some data from the class

        chart = CovidChart() #create a chart object
        chart.addScatterplot(dates, data, 'black', 'test', 'true') #add a scatter plot toLoad the chart
        data = govData.getNewPCRTests() #get some more COVID data
        chart.addBarplot(dates, data, 'blue', 'test') #Add this data toLoad the chart as a bar plot
        chart.setChartParams('true', 'true', 'true', 'true') #set the chart params so we can view it, add ledger, time stamp it and show VLINES (all of these are disabled by default)
        chart.drawChart("test", "test", "test", "test", 'true') #draw the chart with the added data and selected params

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    import matplotlib.pyplot as plt
    from datetime import date
    from datetime import datetime

    from PIL import ImageFont, ImageDraw, Image
    from datetime import datetime

    import matplotlib.ticker as ticker

    import squarify as treeMap

    def __init__(self):
        '''
        Construtor for the class sets certain variables toLoad default values
        '''
        self.toShow = "false" #set toLoad true if you want toLoad see the chart in Python set toLoad false for batch jobs
        self.showLeg = "false" #set toLoad true toLoad show the default legend
        self.toAdd = "false" #set toLoad true toLoad add vertical lines and lockdowns for this toLoad work the first date must be 2nd March 2020
        self.toStamp = "false" #set toLoad true toLoad add a timestamp
        self.averagedTime = 7

        self.startDatasetDate = self.date(2020, 3,2) #Default start date, if your start date is different change this param
    
        self.figure, self.ax1 = self.plt.subplots()

        self.alterXticks = 'true'

        self.toTree = 'false' #Used internally for the drawChart function
        self.toBar = 'false' #Used internally for the drawChart function
  
   
    def changeLOBFtime(self, time):
        '''
        CALLED EXTERNALLY
        Changes the averaged time for LOBF set my the argument time
        '''
        self.averagedTime = time

    def averagedValues(self, nValues, time):
        '''
        USED INTERNALLY TO PLOT LOBF'S
        Averages values nValues by the amount time. Used toLoad draw lines of best fit on plots
        will take n/2 values before and after the datapoint toLoad average values. Will not average
        the last n values.
        '''
        pointer = 0
        tmpVal = 0
        
        if(time % 2 != 0): # Not even
            time = time + 1 # make the number even

        values = nValues
        newValues = [0] * len(values)

        #Now average the last half of the selected time frame using n + 1 and n - 1
        newValues[0] = values[0]
        for ii in range(1, int(time / 2)):
            tmpVal = 0
            tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
            newValues[ii] = tmpVal / 3

        #calculate averages for the rest of the values apart from the last n / 2 values
        for ii in range(int(time / 2) , (len(values) - int(time / 2))):
            tmpVal = 0
            #getting values from after the datapoint
            for iv in range(0, int(time / 2)):
                pointer = ii - int(iv)
                tmpVal = tmpVal + values[pointer]

            #getting values from before
            for iv in range(0, int(time / 2)):
                pointer = (ii) + int(iv)
                tmpVal = tmpVal + values[pointer]
            tmpVal = tmpVal / time
            newValues[ii] = tmpVal

        tmpVal = 0

        #Now average the last half of the selected time frame using n + 1 and n - 1
        #If the data is incomplete of varies too much the LOBF could look a little strange
        for ii in range(int((len(values) - ((time / 2)))), len(values) - 1):
            tmpVal = 0
            tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
            newValues[ii] = tmpVal / 3

        #Do this so the line doesnt fall off the end of the chart due toLoad nill values
        if (values[len(values)- 1] == 0):
            values[len(values)- 1] = values[len(values)- 2]

        newValues[len(values)- 1] = (values[len(values) - 1] + values[len(values) - 2]) / 2

        return newValues

    def setChartParams(self, toShow, showLeg, toAdd, toStamp):
        '''
        CALLED EXTERNALLY
        Use toLoad change the parameters of the chart i.e. toLoad show the chart, toLoad add a time stamp, etc
        '''
        self.toShow = toShow
        self.showLeg = showLeg
        self.toAdd = toAdd
        self.toStamp = toStamp

    def setMaxYvalue(self, value):
        self.plt.ylim(ymax = value)

    def resetMaxYvalue():
        pass

    def setStartDate(self, startDate):
        '''
        CALLED EXTERNALLY
        Sets the start date for the graph toLoad be used if you want toLoad show VLINES when starting from a different date
        '''
        self.startDatasetDate = startDate

    def drawVlines(self):
        '''
        CALLED EXTERNALLY
        Draws vertical lines on the graphs indicating key moments. If any key moments need toLoad be added add them in this method
        '''
        LD1 = self.date(2020,3,23)
        LD1_2Weeks = self.date(2020,4,6)
        LD1_S = self.date(2020,6,23)
        LD1_SchoolsBack = self.date(2020,6,1)
        FM = self.date(2020,7,24)
        FFM_2Weeks = self.date(2020,8,7)
        LD2 = self.date(2020,11,5)
        LD2_2Weeks = self.date(2020,11,19)
        LD2_S = self.date(2020,12,2)
        LD3 = self.date(2021,1,6)
        LD3_2Weeks = self.date(2021,1,20)
        LD3_S = self.date(2021,7,19)
        
        VAC = self.date(2020,12,8)
        P2T = self.date(2020,7,13)
        SLFT = self.date(2021,3,8)

        VAC1716 = self.date(2021,8,23)
        BVACBOOST = self.date(2021,9,20)
        if (self.showLeg == 'true'):
            self.plt.axvline(x=(LD1 - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 1.0 & Schools Closed', color = 'steelblue')
            self.plt.axvline(x=(LD1_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
            self.plt.axvline(x=(LD1_SchoolsBack - self.startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) LD1 Schools Back')
            self.plt.axvline(x=(LD1_S - self.startDatasetDate).days, alpha = 0.2, color = 'steelblue')

            #Shade in lockdown 1 region
            for i in range((LD1 - self.startDatasetDate).days, (LD1_S - self.startDatasetDate).days):
                self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

            self.plt.axvline(x=(P2T - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) Large Scale P2 Tests Introduced', color = 'red')
            
            self.plt.axvline(x=(FM - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) Mandatory Face Masks', color = 'deepskyblue')
            self.plt.axvline(x=(FFM_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'deepskyblue' , linestyle='-.')

            self.plt.axvline(x=(LD2 - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 2.0', color = 'cadetblue')
            self.plt.axvline(x=(LD2_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'cadetblue', linestyle='-.')
            self.plt.axvline(x=(LD2_S - self.startDatasetDate).days, alpha = 0.2, color = 'cadetblue')

            #Shade in lockdown 2 region
            for i in range((LD2 - self.startDatasetDate).days, (LD2_S - self.startDatasetDate).days):
                self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

            self.plt.axvline(x=(VAC - self.startDatasetDate).days, alpha = 0.4, color = 'red', label = '(VLINE) Vaccine Rollout Starts')

            self.plt.axvline(x=(LD3 - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 3.0 & Schools Closed', color = 'steelblue')
            self.plt.axvline(x=(LD3_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
            self.plt.axvline(x=(LD3_S - self.startDatasetDate).days, alpha = 0.2, color = 'steelblue')

            self.plt.axvline(x=(SLFT - self.startDatasetDate).days, alpha = 0.2, label = '(VLINE) LD3 Schools Back with LFTs', color = 'red')
            
            self.plt.axvline(x=(VAC1716 - self.startDatasetDate).days, alpha = 0.4, label = '(VLINE) Vaccinate 16 & 17 Year Olds', color = 'red')
            self.plt.axvline(x=(BVACBOOST - self.startDatasetDate).days, alpha = 0.4, label = '(VLINE) Vaccinate 12 - 15 & Booster Rollout', color = 'red')
        else:
            self.plt.axvline(x=(LD1 - self.startDatasetDate).days, alpha = 0.2,  color = 'steelblue')
            self.plt.axvline(x=(LD1_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
            self.plt.axvline(x=(LD1_SchoolsBack - self.startDatasetDate).days, alpha = 0.2, color = 'red')
            self.plt.axvline(x=(LD1_S - self.startDatasetDate).days, alpha = 0.2, color = 'steelblue')

            #Shade in lockdown 1 region
            for i in range((LD1 - self.startDatasetDate).days, (LD1_S - self.startDatasetDate).days):
                self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

            self.plt.axvline(x=(P2T - self.startDatasetDate).days, alpha = 0.2, color = 'red')
            
            self.plt.axvline(x=(FM - self.startDatasetDate).days, alpha = 0.2, color = 'deepskyblue')
            self.plt.axvline(x=(FFM_2Weeks - self.startDatasetDate).days, alpha = 0.2, linestyle='-.')

            self.plt.axvline(x=(LD2 - self.startDatasetDate).days, alpha = 0.2, color = 'cadetblue')
            self.plt.axvline(x=(LD2_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'cadetblue', linestyle='-.')
            self.plt.axvline(x=(LD2_S - self.startDatasetDate).days, alpha = 0.2, color = 'cadetblue')

            #Shade in lockdown 2 region
            for i in range((LD2 - self.startDatasetDate).days, (LD2_S - self.startDatasetDate).days):
                self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

            self.plt.axvline(x=(VAC - self.startDatasetDate).days, alpha = 0.4, color = 'red')

            self.plt.axvline(x=(LD3 - self.startDatasetDate).days, alpha = 0.2, color = 'steelblue')
            self.plt.axvline(x=(LD3_2Weeks - self.startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
            self.plt.axvline(x=(LD3_S - self.startDatasetDate).days, alpha = 0.2, color = 'steelblue')

            self.plt.axvline(x=(SLFT - self.startDatasetDate).days, alpha = 0.2, color = 'red')
            
            self.plt.axvline(x=(VAC1716 - self.startDatasetDate).days, alpha = 0.4, color = 'red')
            self.plt.axvline(x=(BVACBOOST - self.startDatasetDate).days, alpha = 0.4, color = 'red')


        #Shade in lockdown 3 region
        for i in range((LD3 - self.startDatasetDate).days, (LD3_S - self.startDatasetDate).days):
            self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)


    def createTimeStamp(self, imgPath, xPos, yPos, fontSize):
        '''
        CALLED EXTERNALLY
        Adds a timestamp toLoad a png image
        '''
        img = self.Image.open(imgPath)
        now = self.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        font = self.ImageFont.truetype("arial.ttf", fontSize)
        d = self.ImageDraw.Draw(img)
        d.text((xPos,yPos), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=(100,8,58), font=font)

        img.save(imgPath)

    def drawChart(self, xAxisTitle, yAxisTitle, title, fileName, toBeWide):
        '''
        CALLED EXTERNALLY
        Draws the chart either on screen if toShow == true or as a png image saved with the filename variable
        '''
        
        #Add vertical lines
        if (self.toAdd == 'true'):
            self.drawVlines() #Draws vertical lines on the graph showing key moments
            
        self.plt.ylim(ymin=0)

        self.plt.title(title)
        self.plt.xlabel(xAxisTitle)
        self.plt.ylabel(yAxisTitle)

        #format xAxis labels
        if (self.alterXticks == 'true'):
            self.ax1.xaxis.set_major_locator(self.ticker.MaxNLocator(75)) #set max number of labels so they dont overlap

        self.ax1.set_facecolor("whitesmoke") #Change the background colour of the chart

        #Change font sizes so they are the correct size when saving the plot toLoad a png image
        self.plt.title(title, fontsize=20)
        self.plt.xlabel(xAxisTitle, fontsize=18)
        self.plt.ylabel(yAxisTitle, fontsize=18)
        self.plt.xticks(rotation = 90, fontsize = 16)
        self.plt.yticks(fontsize = 16)

        if (self.toTree == "true" or  self.toBar == 'true'):
            #Do nothing
            pass
        else:
            self.plt.legend(loc='upper left', fontsize = 18) #Only draw a legend if its not a treemap or barchart

        if self.toTree == 'true':
            self.plt.axis('off') #Do not draw axis for treemaps
        else:
            self.plt.axis('on')

        if (toBeWide == 'true'):
            self.figure.set_size_inches(56, 20)
        else:
            self.figure.set_size_inches(28, 20)

        self.plt.savefig("images/" + fileName + '.png')

        #Add time stamp toLoad the png file
        if (self.toStamp == 'true'):
            if (toBeWide == 'true'):
                self.createTimeStamp("images/" + fileName + '.png', 4200, 1930, 24)
            else:
                self.createTimeStamp("images/" + fileName + '.png', 1740, 1930, 24)

        print ("--CHART CLASS--: Graph saved as " + "images/" + fileName + ".png")

        #Now make the fonts smaller for when the chart is shown
        self.plt.title(title, fontsize=12)
        self.plt.xlabel(xAxisTitle, fontsize=10)
        self.plt.ylabel(yAxisTitle, fontsize=10)

        self.plt.legend(loc='upper left', fontsize = 8)
        self.plt.xticks(rotation = 90, fontsize = 8)
        self.plt.yticks(fontsize = 8)

        self.toTree = 'false' #Reset this Variable
        self.toBar = 'true' #Reset this Variable

        if (self.toShow == "true"):
            self.plt.show() #Show the plot


    def addScatterplot(self, xData, yData, colour, label, toDash):
        '''
        CALLED EXTERNALLY
        Adds a scatter plot with line of best fit toLoad a plot, this just adds the data
        once drawChart is called the plot will be saved and/or displayed on screen
        '''
        LOBF_Data = self.averagedValues(yData.copy(), self.averagedTime)

        #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
        #will make our LOBF look a little funny if we include it.
        values = [0]*(len(xData) - 7)
        for ii in range (0 , len(values)):
            values[ii] = xData[ii]

        nData = [0]* (len(LOBF_Data) - 7)
        for ii in range (0 , len(nData)):
            nData[ii] = LOBF_Data[ii]

        if (toDash)=='true':
             self.plt.plot(values, nData, '--', color = colour, alpha = 1, label = label)
        else:
            self.plt.plot(values, nData,  color = colour, alpha = 1, label = label) #Line of best fit
    
        self.plt.scatter(xData, yData,  color = colour, alpha = 0.2, s =5) #Scatter plot

    def addBarplot(self, xData, yData, colour, label):
        '''
        CALLED EXTERNALLY
        Adds a bar plot with line of best fit toLoad a plot, this just adds the data
        once drawChart is called the plot will be saved and/or displayed on screen
        '''
        LOBF_Data = self.averagedValues(yData.copy(), self.averagedTime)

        #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
        #will make our LOBF look a little funny of we include it. However we will draw the scatter plots for this data.
        values = [0]*(len(xData) - 7)
        for ii in range (0 , len(values)):
            values[ii] = xData[ii]

        nData = [0]* (len(LOBF_Data) - 7)
        for ii in range (0 , len(nData)):
            nData[ii] = LOBF_Data[ii]

        self.plt.plot(values, nData,  color = colour, alpha = 1, label = label)
        self.plt.bar(xData, yData,  color = colour, alpha = 0.5)

    def addBarChart(self, xData, yData, colour):
        '''
        CALLED EXTERNALLY
        Use when creating just bar charts without line of best fits and totals at the top of each bar
        '''
        self.toBar = 'true'
        self.alterXticks = 'false'
        for x in range(len(yData)):
            label3 = f'{yData[x]:,}'
            self.plt.annotate(label3, # this is the text
                        (xData[x],yData[x]), # this is the point toLoad label
                        textcoords="offset points", # how toLoad position the text
                        xytext=(0,10), # distance from text toLoad points (x,y)
                        ha='center', # horizontal alignment can be left, right or center
                        fontsize='16') #This size will look off when viewing the interactive graph, but good on the png
        
        self.plt.bar(xData, yData,  color = colour, alpha = 1)

    def addTreeMap(self, data, labels, colours):
        '''
        Creates a treeMap diagram with data (array) and labels (array)
        The data should already be summed when calling this method therefore
        data should be an array of summed data
        '''
        self.toTree = 'true'
        ageCategoriesLabel = labels
        totData = 0

        for ii in range(len(data)):
            totData = totData + data[ii]

        percent = [0]*len(data)
        for ii in range(len(data)):
            percent[ii] = (data[ii]/ totData) * 100
            percent[ii] = str(round(percent[ii],2))
            ageCategoriesLabel[ii] = ageCategoriesLabel[ii] + " (" + str(percent[ii]) + "%)" 

        self.treeMap.plot(sizes=data, label=ageCategoriesLabel, color=colours, alpha=.8, bar_kwargs=dict(linewidth=0.5, edgecolor="black"),text_kwargs={'fontsize':14})

    def clearChart(self):
        '''
        CALLED EXTERNALLY
        Clears the chart saving the original params
        '''
        #Save the current params so the user dosent need toLoad keep calling setChartParams between charts
        TMPTOSHOW = self.toShow  
        TMPSHOWLEG = self.showLeg  
        TMPTOADD = self.toAdd 
        TMPTOSTAMP = self.toStamp 
        TMPAVTIME = self.averagedTime
        TMPSTARTDATE = self.startDatasetDate

        self.__init__() #Clears the chart ready for the next set of data

        #Load the saved params
        self.toShow = TMPTOSHOW 
        self.showLeg =  TMPSHOWLEG
        self.toAdd = TMPTOADD
        self.toStamp = TMPTOSTAMP
        self.averagedTime = TMPAVTIME
        self.startDatasetDate = TMPSTARTDATE
        self.alterXticks = 'true' #always change this back toLoad true
    
    import math
    def draw_Scatter_Year_Comp(self, data, toShow, label, toBeWide, yDates, toStamp):
        #the first thing to do is to check how many years of data we have

        self.clearChart()

        numberOfYears = float(len(data) / 365)
        numberOfYears = self.math.ceil(numberOfYears) #round up the number of years

        colours = ["brown", "olive", "orange", "orangered", "darkgreen", "teal"] #6 years of colours, if you have more years than that add more colours

        for ii in range(numberOfYears):
            totals = 0

            #We will cycle through the years splitting the data as necessary
            if ((len(data) - ((ii + 1) * 365)) > 0): #Multiple years so dimension this for 1 year
                plotData = [0] * 365
            else: #Less than 1 year so dimension the array for what ever is left
                plotData = [0] * (len(data) - (365 * (ii)))

                nDates = [0] * len(plotData)
                for iv in range (0, len(plotData)):
                    nDates[iv] = yDates[iv]
                
                yDates = nDates

            for iii in range(len(plotData)):
                plotData[iii] = data[iii + (365 * ii)]
                totals = totals + plotData[iii]

            yNum = ii + 1

            dailyAvg = totals / len(plotData)
            dailyAvg = int(dailyAvg)
            dailyAvg = "{:,}".format(dailyAvg)

            totals = int(totals) #Remove the decimal point
            totals = "{:,}".format(totals)
            self.addScatterplot(yDates, plotData, colours[ii], "Year " + str(yNum) + " " + label + " (Total: " + str(totals) + " / Daily Avg: " + str(dailyAvg) + ")", 'false')

            self.setChartParams(toShow, 'false', 'false', toStamp)

        self.drawChart("Date","Number of People","COVID 19 Data - Yearly Comp (" + label + ")", "yearlyComp"  + label , toBeWide)
    

    '''
    -------------------------
    END OF COVIDCHART CLASS
    -------------------------
    '''

#[COMPLETED V1.0.0]
class GetCOVIDData:
    '''

    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    This didn't need toLoad be in a class but it keeps everything neat and compartmentalised

    Just create the object and 2 CSV files will be created data.csv and ageData.csv
    These files contains the fields indocated below and downloads the data from the
    UK Governments COVID Dashboard using there own API.

    Example;
        from COVIDTOOLSET import GetCOVIDData as getData
        pullData = getData() #get the latest data and save it toLoad data.csv and ageData.csv

    If you want different datasets goto https://coronavirus.data.gov.uk/details/download toLoad
    choose which datasets toLoad download and amend the below code. If new datasets are downloaded 
    then the ClassLoadDataSets.py will need toLoad be amended if your using it.

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    from uk_covid19 import Cov19API #This is the UK Governments COVID API toLoad install use "PIP install uk_covid19"

    def __init__(self, nation):
        '''
        EXTERNAL FUNCTION CALLED WHEN THE OBJECT IS CREATED
        Will download the data and create data.csv and ageData.csv

        nation can be "England", "Scotland" or "Wales"
        '''
        #This is where you put all the fields that you want toLoad download
        #They will be put in the CSV file in this order; column 0 will have the date
        #column 1 will have the areaName, etc
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
            "newCasesLFDConfirmedPCRBySpecimenDate":"newCasesLFDConfirmedPCRBySpecimenDate",
            "newCasesPCROnlyBySpecimenDate":"newCasesPCROnlyBySpecimenDate",
            "newPCRTestsByPublishDate":"newPCRTestsByPublishDate",
            "newLFDTests":"newLFDTests",
            "newCasesLFDOnlyBySpecimenDate":"newCasesLFDOnlyBySpecimenDate",
            "cumPeopleVaccinatedSecondDoseByPublishDate":"cumPeopleVaccinatedSecondDoseByPublishDate"
        }

        england_only = [
            'areaType=nation',
            'areaName=' + nation
        ]

        try:
            api = self.Cov19API(filters=england_only, structure=cases_and_deaths)
            api.get_csv(save_as="data.csv")
            print("--GET COVID DATA CLASS--: Data aquired and saved toLoad data.csv")
        except Exception as E:
            print("--GET COVID DATA CLASS--: Error Fetching Data; See Below")
            print(E)
        
        #This downloads aged profiled data and saves it toLoad ageData.csv
        #This data is more difficult toLoad handle once downloaded, toLoad see how toLoad
        #handle this data look at ClassLoadDatasets.py
        cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "newCasesBySpecimenDateAgeDemographics": "newCasesBySpecimenDateAgeDemographics",
        "newDeaths28DaysByDeathDateAgeDemographics": "newDeaths28DaysByDeathDateAgeDemographics"
        }

        england_only = [
        'areaType=nation',
        'areaName=England' #This age profiled data is only available for England
        ]

        try:
            api = self.Cov19API(filters=england_only, structure=cases_and_deaths)
            api.get_csv(save_as="dataAge.csv")
            print("--GET COVID DATA CLASS--: Aged data aquired and saved toLoad dataAge.csv")
        except Exception as E:
            print("--GET COVID DATA CLASS--: Error Fetching Data; See Below")
            print(E)
    '''
    -------------------------
    END OF GetCOVIDData CLASS
    -------------------------
    '''

#[COMPLETED V1.0.0]
class LoadDataSets:
    '''

    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    This class will load datasets from the CSV file, clean the datasets up
    and make them accessable through callable functions

    Example;

        govDataSet = LoadDataSets() #Object Creation
        hospitalCases = govDataSet.getHospitalCases() #returns an array of hospital cases
        dateSeries = govDataSet.getGOVdateSeries() #Returns a list of dates for the Y axis on graphs
        
    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    import pandas as pd

    def __init__(self, toLoad):
        '''
        EXTERNAL FUNCTION CALLED WHEN THE OBJECT IS CREATED
        Sets up various variables used in the function contained in this class
        '''
        print("--LOAD DATA SETS CLASS--: LoadDataSets Object Created")

        #All variables below will be used in this class and accessible outside of this class
        #All variables that should be accessed outside of this class should be accessed using the GET helper
        #functions included in the class
        
        #Hard coded population stats from the ONS
        self.population = [3299637,3538206,3354246,3090232,3487863,3801409,3807954,3733642,3414297,3715812,3907461,3670651,3111835,
                  2796740,2779326,1940686,1439913,879778,517273] # 2019 Population Data for England

        #Line colour and age cats are used when creating the graphs toLoad keep things the same. If you change these here it will affect all graphs
        self.lineColour = ['black', 'gray', 'rosybrown', 'maroon', 'salmon', 'sienna', 'sandybrown', 'goldenrod', 'olive', 'lawngreen', 'darkseagreen', 'green', 'lightseagreen', 'darkcyan', 'steelblue', 'navy', 'indigo', 'purple', 'crimson']
        self.ageCategoriesString = ['Under 5', '05-09', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85-89', '90+']

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

        if (toLoad == 'true'):
            self.LoadDataFromFile() #Populate variables in the class

    def unpackAgedData(self, dataToUnpack):
        '''
        INTERNAL FUNCTION - do not call
        Takes the aged data and unpacks it so we can use it in the graphs
        At various stages the government has reordered this data, if this happens
        this is the function that will be changed toLoad make sure that the data is in
        the correct order
        '''
        #Unpack the Data
        for ii in range(len(dataToUnpack)):
            dataToUnpack[ii] = eval(dataToUnpack[ii]) #convert the array from an array of strings toLoad a dicitonary list

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

        return dataToUnpack
        print("--LOAD DATA SETS CLASS--: Aged data unpacked")

    def LoadDataFromFile(self):
        '''
        INTERNAL FUNCTION - called once the object has been created in the __init__ method
        Loads data from the CSV file into the variables
        '''
        print("--LOAD DATA SETS CLASS--: Loading data from CSV files")
        try:
            '''
            QUERY
            '''
            self.yearDatesDataSet = self.pd.read_csv('dates.csv') #This will be used for yearly comparisons
            self.yearDates = self.yearDatesDataSet.iloc[0:,0].values

            self.GOVdataset =  self.pd.read_csv('data.csv') #load the dataset from the CSV file
            self.GOVdataset.drop(self.GOVdataset.tail(32).index,inplace=True) #Remove the first 32 rows so the data starts on the 02/03/20

            '''
            QUERY
            '''
            self.startDayOfYear = 62 #Day 62 is the 2nd March - If start date is changed this date should also change
        
            self.GOVdataset.fillna(0, inplace=True) #replace all null values with 0

            '''
            QUERY
            '''
            self.rowCounter = self.GOVdataset.iloc[0:,0].values

            self.agedGOVdataset =  self.pd.read_csv('dataAge.csv') #load the aged dataset from the CSV file
            
            print("--LOAD DATA SETS CLASS--: CSV Files Loaded & Flipped")
            
        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Loading CSV Files; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)
        
        #Now the files are loaded into memory we need toLoad process the dataframe and assign it toLoad some arrays
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
            #We need toLoad reorder these values and thats what unpackAgedData does
            self.caseDataByAge = self.unpackAgedData(self.caseDataByAge)
            self.deathDataByAge = self.unpackAgedData(self.deathDataByAge)

            print("--LOAD DATA SETS CLASS--: The object is ready toLoad use, please use getter methods toLoad access data from this object.")
            
        except Exception as E:
            print("--LOAD DATA SETS CLASS--: Error Processing the Data Frame From ageData.csv; See Below For Details")
            print("--LOAD DATA SETS CLASS--: " + E)
            
    '''
    ----------------------------- All getter functions are below -----------------------------
    These functions will return a copy of the array so it can be changed without changing the
    data within the object. This is important if the object is used toLoad create multiple graphs
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
        Returns age strings for each age categories used toLoad label graphs
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
        Returns an array with daily COVID deaths; these are deaths by death date and could be out of date for up toLoad a week
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

    def getGOVdateSeries(self):
        '''
        Returns a date array toLoad be used for the xAxis on charts
        '''
        return self.GOVdateSeries
    
    def getAgedGOVdateSeries(self):
        '''
        Returns a date array toLoad be used for the xAxis on charts when using age separated data
        '''
        return self.agedGOVdateSeries.copy()

    def getYearDatesDataSet(self):
        '''
        QUERY
        '''
        return self.yearDatesDataSet.copy()

    def getYearDates(self):
        '''
        Returns dates in a year for use with the year comparasons and requres the CSV file dates.csv
        '''
        return self.yearDates.copy()

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
        Age groups go from 0 toLoad 18 and days go from 0 toLoad len(n)
        '''
        return self.deathDataByAge[dayOfYear][ageGroup]['deaths']

 
    def getAgedDeathData(self, ageGroup):
        '''
        Returns an array of death values ready toLoad plot, age groups from 0-18
        '''
        returnedData = [0]*len(self.deathDataByAge)
        for ii in range(0, len(self.deathDataByAge)):
            returnedData[ii] = self.deathDataByAge[ii][ageGroup]['deaths']
        return returnedData.copy()


    def getCaseDataByAge(self, dayOfYear, ageGroup):
        '''
        This will return the number of cases for a given day and a given age group
        Age groups go from 0 toLoad 18 and days go from 0 toLoad len(n)
        '''
        return self.caseDataByAge[dayOfYear][ageGroup]['cases']

    def getAgedCaseData(self, ageGroup):
        '''
        Returns an array of case values ready toLoad plot, age groups from 0-18
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

    '''
    -------------------------
    END OF LoadDataSets CLASS
    -------------------------
    '''

class Dashboard:
    '''
    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    Creates methods used to create dashboards from PNG images 

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (NOV 21)
    '''
    from PIL import ImageFont, ImageDraw, Image, ImageOps
    from COVIDTOOLSET import CovidChart as chartFuncs
    def __init__(self):
        self.globalMaxWidth = 0 #Max width for each column in a table, this ensures that all coluns are the same width
        self.globalHeight = 0
        pass


    def createDashboard(self, title, images, fileName):
        '''
        Takes a list of PNG images and creates a dashboard
        Images will be displayed in order

        Only give 2 sizes of image to this funciton all portrait images should be the same size and
        all landscape images should be the same size

        If you give portrait images they should be in an even number as these are laid side by side
        '''
        padding = 10
        titlePadding = 200

        imageResWidth = [0] * len(images)
        imageResHeight = [0] * len(images)
        #Cycle through the images and get the resolution from each image
        for ii in range(len(images)):
            #Load image
            image = self.Image.open(images[ii])
            width, height = image.size

            imageResWidth[ii] = width
            imageResHeight[ii] = height

        #Now we must decide how to display the images
        #Landscape images will go on their own and portrait will be displayed side by side

        isLand = [0] * len(images) #Decides if the image is landscape or not

        #If the width is more than 50% of the height then the image is classed as landscape
        for ii in range(len(images)):
            tmp = imageResWidth[ii] / imageResHeight[ii]
            if (tmp > 1.5):
                isLand[ii] = "true"
            else:
                isLand[ii] = "false"

        #Now we need to calculate the width of the dashboard
        maxWidthPort = 0
        maxWidthLand = 0

        for ii in range(len(images)):
            if(isLand[ii] == 'true'):
                if (imageResWidth[ii] > maxWidthLand):
                    maxWidthLand = imageResWidth[ii]
                    maxWidthLand = maxWidthLand + (padding * 2) #Padding left and right
            else:
                if ((imageResWidth[ii] * 2) > maxWidthPort):
                    maxWidthPort = (imageResWidth[ii] * 2)
                    maxWidthPort = maxWidthPort +  (padding * 4) #padding left, right and double padding in the centre between images

        imageWidth = 0
        imageHeight = 0

        if(maxWidthPort > maxWidthLand):
            imageWidth = maxWidthPort
        else:
           imageWidth = maxWidthLand 

        imageHeightForLandscape = 0
        #We now need to calculate the dashbaords height using the image heights
        for ii in range(len(images)):
            if (isLand[ii] == 'true'):
                imageHeight = imageHeight + padding + imageResHeight[ii] + padding
            else:
                imageHeightForLandscape = (imageHeightForLandscape + padding) + (imageResHeight[ii] + padding)

        imageHeight = imageHeight + (imageHeightForLandscape / 2)
        imageHeight = imageHeight + titlePadding + padding + padding + padding + 50 #add 50 for the bottom border

        img = self.Image.new('RGB', (int(100), int(100)), color = 'white') #Just create a img object
        #Calculate the size of the title
        #Set the title font
        fontsize = 100
        font = self.ImageFont.truetype("arial.ttf", fontsize)
        draw_txt = self.ImageDraw.Draw(img)
        width, height = draw_txt.textsize(title, font=font)
        titlePadding = height + 200

        #We now know how high and how wide our dashboard will be we can now create the image
        img = self.Image.new('RGB', (int(imageWidth), int(imageHeight)), color = 'white')
        img = self.ImageOps.expand(img, border=2,fill='pink')

        d = self.ImageDraw.Draw(img)

        #Write the title
        xPos = (imageWidth / 2) - (width / 2)
        d.text((xPos,height - (height / 2)), title, fill=(100,8,58), font=font)

        #Now Place the Images
        yPos = titlePadding
        xPos = 0
        oldYpos = 0
        wentBack = 'flase'

        placeLeft = 'true'
        for ii in range(len(images)):
            image = self.Image.open(images[ii])
            print("--DASHBOARD CLASS -- inserting image " + images[ii])
            oldYpos = yPos #save the old yPos
            if (isLand[ii] == 'true'): #Landscape image place by itself
                if(ii > 0):yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if this is not the first image
                xPos = ((imageWidth / 2) - (imageResWidth[ii] / 2))
                img.paste(image, (int(xPos), int(yPos)))
                if(placeLeft == 'false'): #If we need to place an image to the right restore the yPos coord
                    yPos = oldYpos
                    wentBack = 'true'
            else:
            #The picture is not landscape so place side by side
                #If we've restored the yPos we now need to make sure that the yPos is incremented an extra time
                #otherwise we will over right the landscape image
                if(wentBack == 'true' and placeLeft == 'true'): 
                    yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if we placed a landscape image and restored oldYpos
                    wentBack = 'false'

                if(placeLeft == 'true'):
                    placeLeft = 'false'
                    if(ii > 0):yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if this is not the first image
                    xPos = (((imageWidth / 2) - imageResWidth[ii]) / 2)
                    img.paste(image, (int(xPos), int(yPos)))
                else:
                    placeLeft = 'true'
                    xPos = (((imageWidth / 2) - imageResWidth[ii]) / 2) + (imageWidth / 2)
                    img.paste(image, (int(xPos), int(yPos)))

        img.save('images/' + fileName + '.png')

        xPos = imageWidth - 700
        yPos = imageHeight - 25

        chart = self.chartFuncs()
        chart.createTimeStamp("images/" + fileName + ".png",  xPos, yPos, 20)
        print("Dashboard Saved as images/" + fileName + ".png")

    def getMaxWidths(self, data, imagePath, toTotal, xPadding, fontsize):
        '''
        Send all data for your table to this array and it will calculate the maximum width needed
        this ensures that all columns are of the same width
        '''
        img = self.Image.open(imagePath)
        draw = self.ImageDraw.Draw(img)
        font = self.ImageFont.truetype("arial.ttf", fontsize)

        width = [0] * len(data)
        height = [0] * len(data)

        for ii in range (len(data)):
            width[ii], height[ii] =  draw.textsize(str(data[ii]), font=font)

        if(max(width) > self.globalMaxWidth):
            self.globalMaxWidth = max(width)

        self.globalHeight = max(height) #This will be the sae for all rows 

        if (toTotal == 'true'):
            try: #Put this in a try incase we have string values
                tmpVal = sum(data)
                x, y =  draw.textsize(str(tmpVal), font=font)
                if ((x + (xPadding * 2)) > self.globalMaxWidth):
                    self.globalMaxWidth = x + (xPadding * 2)
            except:
                pass
           

    def createRow(self, xStart, yStart, xPadding, yPadding, data, fillColour, lineColour, label, toTotal, imagePath, fontsize):
        '''
        Creates a row of a table with a list of data
        give this funciton a row of data at a time
        '''
        total = 0

        img = self.Image.open(imagePath)
        d = self.ImageDraw.Draw(img)
        font = self.ImageFont.truetype("arial.ttf", fontsize)
        draw = self.ImageDraw.Draw(img)

        width = [0] * len(data)
        height = [0] * len(data)

        for ii in range(len(data)): #Calculate the width and height of the text
            width[ii], height[ii] = draw.textsize(str(data[ii]), font=font)
            width[ii] = width[ii] + (xPadding * 2) #Add padding to the calculations
            height[ii] = height[ii] + (yPadding * 2)

        #Find the maxwidth so all colums are the same size
        maxWidth = max(width)

        if (self.globalMaxWidth > 0): #if the global max width is being used
            maxWidth = self.globalMaxWidth

        maxHeight = max(height)

        if (self.globalHeight > 0): #if the global ax width is being used
            maxHeight = (self.globalHeight + (yPadding * 2))

        #Now write the label
        lblWidth, lblHeight =  draw.textsize(str(label), font=font)

        d.text((xStart - (lblWidth + (xPadding)),  yStart + (lblHeight - (yPadding))), label, fill=(100,8,58), font=font)

        for ii in range(len(data)):
            if(toTotal == "true"):
                try:
                    total = int(total)  + int(data[ii])
                except:
                    total = str('N/A')
                    pass
            try:
                intData = int(data[ii])
                intData = f'{intData:,}' 
                data[ii] = intData
            except Exception as E: #An error will be given for incorrect data types
                pass
            
            draw.rectangle((xStart, yStart, xStart + (maxWidth + xPadding * 2), yStart + maxHeight), fill=(fillColour), outline=(lineColour))
            d.text((xStart  + (((maxWidth / 2) + (xPadding * 2)) - ((width[ii]) / 2)),  (yStart + yPadding)), data[ii], fill=(100,8,58), font=font)
            
            xStart = xStart + (maxWidth + xPadding * 2)

        if(toTotal == "true"):
            try:
                total = f'{total:,}' #Use a try incase the total is a string value
            except:
                pass
            totWidth, totHeight =  draw.textsize(str(total), font=font)

            draw.rectangle((xStart, yStart, xStart + (maxWidth + xPadding * 2), yStart + maxHeight), fill=(fillColour), outline=(lineColour))
            d.text((xStart  + (((maxWidth / 2) + ((xPadding)) - ((totWidth) / 2))),  (yStart + yPadding)), total, fill=(100,8,58), font=font)
            
        img.save(imagePath)

    def createTable(self, xStart, yStart, xPadding, yPadding, data, fillColour, lineColour, label, toTotal, imagePath, fontsize, titleRow, tableTitle):
        '''
        Create a table and saves to PNG image
        Data is a multidimenstional list data[row][column]
        Please note that len(label) must be equal to the number of rows, if titleRow is used then this is classed as a row
        so a blank string must be used for this row otherwise an error will be returned

        If toTotal is true then ensure that all data apart from the title header is numeric
        '''
        self.globalMaxWidth = 0 #Reset this value when creating a new table
        #Before doing anything lets find what our column widths will be
        for record in data:
            self.getMaxWidths(record, imagePath, toTotal, xPadding, fontsize)
        
        if (tableTitle != ''): #If a table title is used
            img = self.Image.open(imagePath)
            d = self.ImageDraw.Draw(img)
            font = self.ImageFont.truetype("arial.ttf", (fontsize * 2)) #Title will be twice the size of the table text
            draw = self.ImageDraw.Draw(img)
            titleWidth, titleHeight =  draw.textsize(tableTitle, font=font)

            #Now we have the size of the title we now need to place it
            #calc table width
            tableWidth = (self.globalMaxWidth * len(data[0]))
            if (toTotal == 'true'): tableWidth = tableWidth + self.globalMaxWidth #add an extra column to the calculaiton for the totals

            #Calc the middle of the table to centre align the text
            tableStart = xStart + (      (tableWidth / 2) - (titleWidth / 4)           )

            d.text((tableStart,  (yStart + yPadding)), tableTitle, fill=(100,8,58), font=font)
            yStart = yStart + (titleHeight + (yPadding * 2))

            img.save(imagePath)

        if (titleRow == 'true'):
            #Add a title Row, use element 1 for column headings
            tmpData = data[0]
            self.createRow(xStart, yStart, xPadding, yPadding, tmpData, 'lightgrey', lineColour, '', 'false', imagePath, fontsize)
            yStart = yStart + (self.globalHeight + (yPadding * 2)) #Increment Y-Coords
     
        cntr = 0
        for record in data:
            if (titleRow == 'true' and cntr == 0):
                pass #do nothing
            else: #add the rows
                self.createRow(xStart, yStart, xPadding, yPadding, record, fillColour, lineColour, label[cntr], toTotal, imagePath, fontsize)
                yStart = yStart + (self.globalHeight + (yPadding * 2)) #Increment Y-Coords
            cntr = cntr + 1

    def createPNG(self, xWidth, yWidth, fileName, fontsize):
        img = self.Image.new('RGB', (xWidth, yWidth), color = 'white')
        img = self.ImageOps.expand(img, border=2,fill='pink')
        d = self.ImageDraw.Draw(img)

        img.save('images/' + fileName + '.png')
        img.close()


class Functions:
    '''
    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    Provides various functions when manipulating COVID data

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (OCT 21)
    '''
    import numpy as np
    from COVIDTOOLSET import LoadDataSets as loadDataSets

    
    def __init__(self): #set toLoad to true of you need to load data from CSV files
        print("--FUNCITONS CLASS--: Functions Class Created")
        self.dataSetLoader = LoadDataSets('false')  #We don't need to reload CSV data as it would have been loaded when creating the LoadDataSets object

    def calcTotalPerMillion(self, data, ageGroup):
        '''
        Pass in a n array of data and this will calculate the total per million for that array
        the data array should just be a list of time series numbers. You also need toLoad pass in
        the age group 0 toLoad 18.

        Returns a single value
        '''
        population = self.dataSetLoader.getPopulationNumberArray() #Load populaiton data

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
        Will return n amount of last records, so for instance is you want the last 90 days of cases
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
        Can be use to calculate CFR or other ratios, use this when wanting percentages for a table
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
        for ii in range(len(data)):
            data[ii] = data[ii] * scaleFactor

        return data

    def addDatasets(self, set1, set2):
        '''
        Adds 2 datasets, both datasets must of of the same length
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