class CovidChart:
    '''

    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    This class is used to create charts using COVID data.
    I created the class so all charts have a consistent look and feel
    All formatting is carried out by this class with LOBF added by the 
    class when scatter graphs are created.

    CLASS COMPLETE AND DOCUMENTED
    VERSION 2.0.0 (March 22)
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from datetime import date
    from datetime import datetime

    import math

    from PIL import ImageFont, ImageDraw, Image

    import matplotlib.ticker as ticker

    import squarify as treeMap
    import pandas as pd
    import numpy as np

    from toolset.BenchMark import Benchmark as Benchmark

    BENCH = Benchmark() #Used for benchmarking
    BENCH.setBench(False) #Bechmark output will be printed if this is set to true

    def __init__(self):
        '''
        Construtor for the class sets certain variables to default values
        '''
        self.BENCH.benchStart()
        self.toShow = False #set to true if you want to see the chart in Python set to false for batch jobs when you just want to png image
        self.showLeg = False #set to true to show the default legend
        self.toAdd = False #set to true to add vertical lines and lockdowns for this to work the first date must be 2nd March 2020
        self.toStamp = False #set to true to add a timestamp
        self.averagedTime = 7 #sets the averge time for the line of best fit

        self.startDatasetDate = self.date(2020, 3,2) #Default start date, if your start date is different change this param

        self.figure, self.ax1 = self.plt.subplots()

        self.alterXticks = True

        self.toTree = False #Used internally for the drawChart function
        self.toBar = False #Used internally for the drawChart function

        self.columns = 14 #number of columns for the legend
        self.legendBottom = True #If you want the legend at the bottom set to true
        self.BENCH.benchEnd("CREATE COVIDCHART CLASS")
  
    def changeLOBFtime(self, time):
        '''
        CALLED EXTERNALLY
        Changes the averaged time for LOBF set my the argument time
        '''
        self.averagedTime = time

    def averagedValues(self, nValues, time):
        '''
        USED INTERNALLY TO PLOT LOBF'S
        Averages values nValues by the amount time. Used to draw lines of best fit on plots
        will take n/2 values before and after the datapoint to average values. Will not average
        the last n values.
        '''
        self.BENCH.benchStart()
        pointer = 0
        tmpVal = 0
        
        if(time % 2 != 0): # Not even
            time = time + 1 # make the number even

        values = nValues
        newValues = [0] * len(values)

        if len(nValues) > time:
            #Now average the first half of the selected time frame using n + 1 and n - 1
            newValues[0] = values[0] #The first value will not be averaged
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
            #If the data is incomplete or varies too much the LOBF could look a little strange
            for ii in range(int((len(values) - ((time / 2)))), len(values) - 1):
                tmpVal = 0
                tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
                newValues[ii] = tmpVal / 3

            #Do this so the line doesnt fall off the end of the chart due to nill values
            if (values[len(values)- 1] == 0):
                values[len(values)- 1] = values[len(values)- 2]

            newValues[len(values)- 1] = (values[len(values) - 1] + values[len(values) - 2]) / 2

        self.BENCH.benchEnd("COVIDCHART averagedValues")
        return newValues
    
    def setChartParams(self, toShow, showLeg, toAdd, toStamp):
        '''
        CALLED EXTERNALLY
        Use to change the parameters of the chart i.e. to show the chart, to add a time stamp, etc
        You should call this before you call drawChart
        '''
        self.toShow = toShow
        self.showLeg = showLeg
        self.toAdd = toAdd
        self.toStamp = toStamp

    def setMaxYvalue(self, value):
        '''
        sets the maximum Y valve
        '''
        self.plt.ylim(ymax = value)

    def resetMaxYvalue(self):
        '''
        Resets ylimit if it was explicitly set
        '''
        self.plt.autoscale()

    def setStartDate(self, startDate):
        '''
        CALLED EXTERNALLY
        Sets the start date for the graph to be used if you want to show VLINES when starting from a different date
        '''
        self.startDatasetDate = startDate

    def drawVlines(self):
        '''
        CALLED EXTERNALLY
        Draws vertical lines on the graphs indicating key moments. If any key moments need to be added add them in this method
        getGOVdateSeries() or govAgedDateSeries() should be used with this method and not dataframe["date"] as this will give an error
        '''
        LD1 = self.np.array(self.date(2020,3,23), dtype='datetime64')
        print(LD1)
        LD1_S = self.np.array(self.date(2020,6,23), dtype='datetime64')
        LD1_SchoolsBack = self.np.array(self.date(2020,6,1), dtype='datetime64')
        FM = self.np.array(self.date(2020,7,24), dtype='datetime64')
        FFM_2Weeks = self.np.array(self.date(2020,8,7), dtype='datetime64')
        LD2 = self.np.array(self.date(2020,11,5), dtype='datetime64')
        LD2_2Weeks = self.np.array(self.date(2020,11,19), dtype='datetime64')
        LD2_S = self.np.array(self.date(2020,12,2), dtype='datetime64')
        LD3 = self.np.array(self.date(2021,1,6), dtype='datetime64')
        LD3_2Weeks = self.np.array(self.date(2021,1,20), dtype='datetime64')
        LD3_S = self.np.array(self.date(2021,7,19), dtype='datetime64')
        
        VAC = self.np.array(self.date(2020,12,8), dtype='datetime64')
        P2T = self.np.array(self.date(2020,7,13), dtype='datetime64')
        SLFT = self.np.array(self.date(2021,3,8), dtype='datetime64')

        TODAY = self.np.array(self.date(2021,11,16), dtype='datetime64')

        VAC1716 = self.np.array(self.date(2021,8,23), dtype='datetime64')
        BVACBOOST = self.np.array(self.date(2021,9,20), dtype='datetime64')
        try:
            if (self.showLeg == True):
                
                self.plt.axvline(x=(LD1), alpha = 0.2, label = '(VLINE 1) Lockdown 1.0 & Schools Closed', color = 'steelblue')
                self.plt.axvline(x=(LD1_SchoolsBack), alpha = 0.2, color = 'red', label = '(VLINE 2) LD1 Schools Back')
                self.plt.axvline(x=(LD1_S), alpha = 0.2, color = 'steelblue')

                #Shade in lockdown 1 region
                #for i in range((LD1), (LD1_S)):
                #    self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

                self.plt.axvline(x=(P2T), alpha = 0.2, label = '(VLINE 3) Large Scale P2 Tests Introduced', color = 'red')
                
                self.plt.axvline(x=(FM), alpha = 0.2, label = '(VLINE 4) Mandatory Face Masks', color = 'deepskyblue')

                self.plt.axvline(x=(LD2), alpha = 0.2, label = '(VLINE 5) Lockdown 2.0', color = 'cadetblue')
                self.plt.axvline(x=(LD2_S), alpha = 0.2, color = 'cadetblue')

                #Shade in lockdown 2 region
                #for i in range((LD2), (LD2_S)):
                #    self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

                self.plt.axvline(x=(VAC), alpha = 0.4, color = 'red', label = '(VLINE 6) Vaccine Rollout Starts')

                self.plt.axvline(x=(LD3), alpha = 0.2, label = '(VLINE 7) Lockdown 3.0 & Schools Closed', color = 'steelblue')
                self.plt.axvline(x=(LD3_S), alpha = 0.2, color = 'steelblue')

                self.plt.axvline(x=(SLFT), alpha = 0.2, label = '(VLINE 8) LD3 Schools Back with LFTs', color = 'red')
                
                self.plt.axvline(x=(VAC1716), alpha = 0.4, label = '(VLINE 9) Vaccinate 16 & 17 Year Olds', color = 'red')
                self.plt.axvline(x=(BVACBOOST), alpha = 0.4, label = '(VLINE 10) Vaccinate 12 - 15 & Booster Rollout', color = 'red')
            else:
                self.plt.axvline(x=(LD1), alpha = 0.2,  color = 'steelblue')
                self.plt.axvline(x=(LD1_SchoolsBack), alpha = 0.2, color = 'red')
                self.plt.axvline(x=(LD1_S), alpha = 0.2, color = 'steelblue')

                #Shade in lockdown 1 region
                #for i in range((LD1), (LD1_S)):
                #    self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

                self.plt.axvline(x=(P2T), alpha = 0.2, color = 'red')
                
                self.plt.axvline(x=(FM), alpha = 0.2, color = 'deepskyblue')

                self.plt.axvline(x=(LD2), alpha = 0.2, color = 'cadetblue')
                self.plt.axvline(x=(LD2_S), alpha = 0.2, color = 'cadetblue')

                #Shade in lockdown 2 region
                #for i in range((LD2 - self.startDatasetDate).days, (LD2_S - self.startDatasetDate).days):
                #    self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

                self.plt.axvline(x=(VAC), alpha = 0.4, color = 'red')

                self.plt.axvline(x=(LD3), alpha = 0.2, color = 'steelblue')
                self.plt.axvline(x=(LD3_S), alpha = 0.2, color = 'steelblue')

                self.plt.axvline(x=(SLFT), alpha = 0.2, color = 'red')
                
                self.plt.axvline(x=(VAC1716), alpha = 0.4, color = 'red')
                self.plt.axvline(x=(BVACBOOST), alpha = 0.4, color = 'red')

                #self.plt.axvline(x=(TODAY - self.startDatasetDate).days, alpha = 0.4, color = 'red')

            #Shade in lockdown regions
            LD1 = self.date(2020,3,23)
            LD1_S = self.date(2020,6,23)
            startFill = (LD1 - self.startDatasetDate).days 
            endFill = (LD1_S - self.startDatasetDate).days
            startDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(startDate, endDate, facecolor='grey', alpha=0.1)

            LD2 = self.date(2020,11,5)
            LD2_S = self.date(2020,12,2)
            startFill = (LD2 - self.startDatasetDate).days 
            endFill = (LD2_S - self.startDatasetDate).days
            startDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(startDate, endDate, facecolor='grey', alpha=0.1)

            LD3 = self.date(2021,1,6)
            LD3_S = self.date(2021,7,19)
            startFill = (LD3 - self.startDatasetDate).days 
            endFill = (LD3_S - self.startDatasetDate).days
            startDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.startDatasetDate) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(startDate, endDate, facecolor='grey', alpha=0.1)
        except:
            print("--CHART CLASS--: Error drawing VLINES, use LoadDatasets.getGOVdateSeries() or govAgedDateSeries() instead of DataFrame['date'], Y axis canot be a dataframe it must be a list of dates.")

    def createTimeStamp(self, imgPath, xPos, yPos, fontSize, toBeWide):
        '''
        CALLED EXTERNALLY
        Adds a timestamp to a png image with the website URL
        '''
        img = self.Image.open(imgPath)
        now = self.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        font = self.ImageFont.truetype("arial.ttf", fontSize)
        d = self.ImageDraw.Draw(img)

        if (toBeWide == True): #put time stamps at the top
            d.text((xPos,yPos - 30), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((xPos,yPos),"GitHub Repo: https://github.com/L33t-dot-UK/COVID-Reports", fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((xPos,yPos + 30),"Data Source: https://coronavirus.data.gov.uk/details/download", fill=("#6D6D6D"), font=font, alpha = 0.7)
        else: #put the time stamps at the bottom
            d.text((xPos,yPos - 30), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((xPos,yPos),"GitHub Repo: https://github.com/L33t-dot-UK/COVID-Reports", fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((xPos - 1400,yPos),"Data Source: https://coronavirus.data.gov.uk/details/download", fill=("#6D6D6D"), font=font, alpha = 0.7)
            
        img.save(imgPath)

    def drawChart(self, xAxisTitle, yAxisTitle, title, fileName, toBeWide):
        '''
        CALLED EXTERNALLY
        Draws the chart either on screen if toShow == true (setChartParams) or as a png image saved with the filename variable
        These graphs use ONS guidelines for formatting
        '''

        if self.showLeg == True and self.columns == 14:
            self.columns = 7 #change the number of columns in the legend if were adding the VLINES

        #Add vertical lines
        if (self.toAdd == True):
            self.drawVlines() #Draws vertical lines on the graph showing key moments
            
        #Format the axis
        axes = self.plt.gca()

        if (toBeWide == True):
            self.figure.set_size_inches(56, 20) #dimensions if the graph is to be wide
        else:
            self.figure.set_size_inches(28, 20) #dimensions for a non wide graph :)

        self.plt.ylim(ymin=0)

        axes.margins(x=0)
        axes.margins(y=0)
        #axes.yaxis.grid(alpha=0.5)
        axes.tick_params(axis="x",colors="#6D6D6D")
        axes.tick_params(axis="y", colors="#6D6D6D")
        axes.margins(x=0)

        axes.spines["right"].set_visible(False)
        axes.spines["top"].set_visible(False)
        axes.spines["left"].set_visible(False)
        axes.spines["bottom"].set_position("zero")
        axes.set_axisbelow(True)

        # Gridlines
        axes.grid(b=False, which="both", axis="x", color="white", alpha = 0.0) 
        axes.grid(b=True, which="both", axis="y", color="#BEBEBE")

        self.plt.title(title, fontname="Arial", size=40, loc="center", color = "#6D6D6D")
        
        #self.plt.xlabel(xAxisTitle)
        self.plt.ylabel(yAxisTitle)

        #format xAxis labels
        if (self.alterXticks == True):
            self.ax1.xaxis.set_major_locator(self.ticker.MaxNLocator(75)) #set max number of labels so they dont overlap

        #self.ax1.set_facecolor("whitesmoke") #Change the background colour of the chart
        self.ax1.set_facecolor("white")

        #self.plt.xlabel(xAxisTitle, fontsize=18,  color = "#6D6D6D")
        self.plt.ylabel(yAxisTitle, fontsize=18,  color = "#6D6D6D")
        self.plt.xticks(rotation = 90, fontsize = 16)
        self.plt.yticks(fontsize = 16)

        if (self.toTree == True or  self.toBar == True):
            #Do nothing
            pass
        elif self.legendBottom == True:
            #self.plt.legend(loc='upper left', fontsize = 18) #Only draw a legend if its not a treemap or barchart
            #Set Legends
            legend = axes.legend(bbox_to_anchor=(0, -0.2, 1, .102), loc="upper left",
                            ncol=self.columns, mode="expand", borderaxespad=0,
                            prop={"family": "Arial", "size":16},
                            frameon=False);
        elif self.legendBottom == False:
            legend = axes.legend(loc="upper left",
                                ncol=1, borderaxespad=1,
                                prop={"family": "Arial", "size":16},
                                frameon=True);

        # Loop through each thing in the legend to change the text colour
        try:
            for text in legend.get_texts():
                text.set_color("#6D6D6D")
        except:
            pass

        if self.toTree == True:
            self.plt.axis('off') #Do not draw axis for treemaps
        else:
            self.plt.axis('on')

        self.plt.savefig("reports/images/" + fileName + '.png')

        #Add time stamp to the png file
        if (self.toStamp == True):
            if (toBeWide == True):
                self.createTimeStamp("reports/images/" + fileName + '.png', 4300, 200, 24, toBeWide)
            else:
                self.createTimeStamp("reports/images/" + fileName + '.png', 1795, 1930, 24, toBeWide)

        print ("--CHART CLASS--: Graph saved as " + "reports/images/" + fileName + ".png")

        #Now make the fonts smaller for when the chart is shown
        self.plt.title(title, fontsize=16)
        #self.plt.xlabel(xAxisTitle, fontsize=10)
        self.plt.ylabel(yAxisTitle, fontsize=10)

        #self.plt.legend(loc='upper left', fontsize = 8)
        # Set Legends
        if self.legendBottom == True:
            legend = axes.legend(bbox_to_anchor=(0, -0.2, 1, .102), loc="upper left",
                                ncol=self.columns, mode="expand", borderaxespad=0,
                                prop={"family": "Arial", "size":8},
                                frameon=False);
        else:
            legend = axes.legend(loc="upper left",
                                ncol=1, borderaxespad=1,
                                prop={"family": "Arial", "size":8},
                                frameon=True);


        # Loop through each thing in the legend to change the text colour
        for text in legend.get_texts():
            text.set_color("#6D6D6D")


        self.plt.xticks(rotation = 90, fontsize = 8)
        self.plt.yticks(fontsize = 8)

        self.toTree = False #Reset this Variable
        self.toBar = True #Reset this Variable
        
        if (self.toShow == True):
            self.plt.show() #Show the plot

        self.columns = 14 #Reset this value


    def addScatterplot(self, xData, yData, colour, label, toDash, dataComplete):
        '''
        CALLED EXTERNALLY
        Adds a scatter plot with line of best fit to a plot, this just adds the data
        once drawChart is called the plot will be saved and/or displayed on screen
        '''

        self.BENCH.benchStart()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(xData, list):
            pass
        else:
            xData = xData.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(yData, list):
            pass
        else:
            yData = yData.tolist()

        self.BENCH.benchStart()
        LOBF_Data = self.averagedValues(yData.copy(), self.averagedTime)

        if (dataComplete == False):
            #If the data is not complete don't add a line of best fit for the last 7 days

            #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
            #will make our LOBF look a little funny if we include it.
            values = [0]*(len(xData) - 7)
            for ii in range (0 , len(values)):
                values[ii] = xData[ii]


            nData = [0]* (len(LOBF_Data) - 7)
            for ii in range (0 , len(nData)):
                nData[ii] = LOBF_Data[ii]
        else:
            values = xData
            nData = LOBF_Data

        if (toDash)==True:
             self.plt.plot(values, nData, '--', color = colour, alpha = 1, label = label)
        else:
            self.plt.plot(values, nData,  color = colour, alpha = 1, label = label) #Line of best fit
    
        self.plt.scatter(xData, yData,  color = colour, alpha = 0.2, s =3) #Scatter plot
        self.BENCH.benchEnd("COVIDCHART addScatterPlot")

    def addBarplot(self, xData, yData, colour, label):
        '''
        CALLED EXTERNALLY
        Adds a bar plot with line of best fit to a plot, this just adds the data
        once drawChart is called the plot will be saved and/or displayed on screen
        '''

        self.BENCH.benchStart()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(xData, list):
            pass
        else:
            xData = xData.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(yData, list):
            pass
        else:
            yData = yData.tolist()
        
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
        self.BENCH.benchEnd("COVIDCHART addBarPlot")

    def addBarChart(self, xData, yData, colour):
        '''
        CALLED EXTERNALLY
        Use when creating just bar charts without line of best fits and totals at the top of each bar
        '''

        self.BENCH.benchStart()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(xData, list):
            pass
        else:
            xData = xData.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(yData, list):
            pass
        else:
            yData = yData.tolist()
        
        self.toBar = True
        self.alterXticks = False
        for x in range(len(yData)):
            yData[x] = int(yData[x])
            label3 = f'{yData[x]:,}'
            self.plt.annotate(label3, # this is the text
                        (xData[x],yData[x]), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        ha='center', # horizontal alignment can be left, right or center
                        fontsize='16', color="#6D6D6D") #This size will look off when viewing the interactive graph, but good on the png
        
        self.plt.bar(xData, yData,  color = colour, alpha = 0.7)
        self.BENCH.benchEnd("COVIDCHART addBarChart")

    def addTreeMap(self, data, labels, colours):
        '''
        CALLED EXTERNALLY
        Creates a treeMap diagram with data (array) and labels (array)
        The data should already be summed when calling this method therefore
        data should be an array of summed data
        '''

        self.BENCH.benchStart()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(data, list):
            pass
        else:
            data = data.tolist()

        self.toTree = True
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
        self.BENCH.benchEnd("COVIDCHART addTreeMap")

    def clearChart(self):
        '''
        CALLED EXTERNALLY
        Clears the chart saving the original params
        '''
        #Save the current params so the user dosent need to keep calling setChartParams between charts
        TMPTOSHOW = self.toShow  
        TMPSHOWLEG = self.showLeg  
        TMPTOADD = self.toAdd 
        TMPTOSTAMP = self.toStamp 
        TMPAVTIME = self.averagedTime
        TMPSTARTDATE = self.startDatasetDate
        TMPLEGBOT = self.legendBottom
        TMPCOLS = self.columns

        self.__init__() #Clears the chart ready for the next set of data

        #Load the saved params
        self.toShow = TMPTOSHOW 
        self.showLeg =  TMPSHOWLEG
        self.toAdd = TMPTOADD
        self.toStamp = TMPTOSTAMP
        self.averagedTime = TMPAVTIME
        self.startDatasetDate = TMPSTARTDATE
        self.alterXticks = True #always change this back to true
        self.legendBottom = TMPLEGBOT
        self.columns = TMPCOLS

    def draw_Scatter_Year_Comp(self, data, toShow, label, toBeWide, yDates, toStamp):
        '''
        Give this method some data and it will split it into years and plot a 
        year comparison with daily averages
        '''

        self.BENCH.benchStart()
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

            dailyAvg = float(totals / len(plotData))
            if dailyAvg > 10:
                dailyAvg = int(dailyAvg)
                dailyAvg = "{:,}".format(dailyAvg)
            else:
                dailyAvg = "{:.4f}".format(dailyAvg)


            totals = int(totals) #Remove the decimal point
            totals = "{:,}".format(totals)


            self.addScatterplot(yDates, plotData, colours[ii], "Year " + str(yNum) + " " + label + " (Total: " + str(totals) + " / Daily Avg: " + str(dailyAvg) + ")", False, False)

            self.setChartParams(toShow, False, False, toStamp)

        self.setLegendBottom(False)
        self.drawChart("Date","Number of People","COVID 19 Data - Yearly Comp (" + label + ")", "yearlyComp"  + label , toBeWide)
        self.BENCH.benchEnd("COVIDCHART draw_Scatter_Year_Comp")    

    def setLegendCols(self, value):
        '''
        Use this to change how many columns we have in the legend
        '''
        self.columns = value
    
    def setLegendBottom(self, value):
        '''
        Use this if you wnat to change the position of the legend
        '''
        self.legendBottom = value