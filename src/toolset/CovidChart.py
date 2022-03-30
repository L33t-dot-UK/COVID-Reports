class CovidChart:
    '''
    This class is used to create charts using COVID-19 data.
    All formatting is carried out by this class with lines of best fit added for scatter graphs.
    To change graph formatting amend the method draw_chart()
    '''

    
    import sys
    sys.path.append('./src/toolset')

    
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

    from BenchMark import Benchmark as Benchmark

    BENCH = Benchmark() #Used for benchmarking
    BENCH.set_bench(False) #Bechmark output will be printed if this is set to true
    

    def __init__(self):
        '''
        Construtor for the class sets certain variables to default values
        '''
        self.BENCH.bench_start()
        self.to_show = False #set to true if you want to see the chart in Python set to false for batch jobs when you just want to png image
        self.show_leg = False #set to true to show the default legend
        self.to_add = False #set to true to add vertical lines and lockdowns for this to work the first date must be 2nd March 2020
        self.to_stamp = False #set to true to add a timestamp
        self.averaged_time = 7 #sets the averge time for the line of best fit

        self.start_dataset_date = self.date(2020, 3,2) #Default start date, if your start date is different change this param

        self.figure, self.ax1 = self.plt.subplots()

        self.alter_x_ticks = True

        self.to_tree = False #Used internally for the draw_chart function
        self.to_bar = False #Used internally for the draw_chart function

        self.columns = 14 #number of columns for the legend
        self.legend_bottom = True #If you want the legend at the bottom set to true
        self.BENCH.bench_end("CREATE COVIDCHART CLASS")
  

    def add_scatter_plot(self, x_data, y_data, colour, label, to_dash, data_complete):
        '''
        Adds a scatter plot with line of best fit to a plot, this just adds the data
        once draw_chart is called the plot will be saved and/or displayed on screen

        Args:
            :x_data: List or DataFrame, data for the x-axis of your scatter chart
            :y_data: List or DataFrame, data for the y-axis of your chart
            :colour: String Value, color of the plot, can be a word such as "red" or a hex value
            :label: String Value, The label for the plot, this will be used in the legend
            :to_dash: Boolean Value, decides if the plot should have a solid or dashed line of best fit
            :data_complete: Boolean value, if set to true the LOBF will go to the end, if set to False the LOBF will go to (values - (time/2)), set to False if data is incomplete
        '''

        self.BENCH.bench_start()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(x_data, list):
            pass
        else:
            x_data = x_data.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(y_data, list):
            pass
        else:
            y_data = y_data.tolist()

        self.BENCH.bench_start()
        LOBF_Data = self._averaged_values(y_data.copy(), self.averaged_time)

        if (data_complete == False):
            #If the data is not complete don't add a line of best fit for the last 7 days

            #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
            #will make our LOBF look a little funny if we include it.
            values = [0]*(len(x_data) - 7)
            for ii in range (0 , len(values)):
                values[ii] = x_data[ii]


            nData = [0]* (len(LOBF_Data) - 7)
            for ii in range (0 , len(nData)):
                nData[ii] = LOBF_Data[ii]
        else:
            values = x_data
            nData = LOBF_Data

        if (to_dash)==True:
             self.plt.plot(values, nData, '--', color = colour, alpha = 1, label = label)
        else:
            self.plt.plot(values, nData,  color = colour, alpha = 1, label = label) #Line of best fit
    
        self.plt.scatter(x_data, y_data,  color = colour, alpha = 0.2, s =3) #Scatter plot
        self.BENCH.bench_end("COVIDCHART add_scatter_plot")


    def add_bar_plot(self, x_data, y_data, colour, label):
        '''
        Adds a bar plot with line of best fit to a plot, this just adds the data
        once draw_chart is called the plot will be saved and/or displayed on screen

        Args:
            :x_data: List or DataFrame, data for the x-axis of your bar plot 
            :y_data: List or DataFrame, data for the y-axis of your bar plot
            :colour: String Value, color of the plot, can be a word such as "red" or a hex value
            :label: String Value, The label for the plot, this will be used in the legend
        '''

        self.BENCH.bench_start()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(x_data, list):
            pass
        else:
            x_data = x_data.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(y_data, list):
            pass
        else:
            y_data = y_data.tolist()
        
        LOBF_Data = self._averaged_values(y_data.copy(), self.averaged_time)

        #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
        #will make our LOBF look a little funny of we include it. However we will draw the scatter plots for this data.
        values = [0]*(len(x_data) - 7)
        for ii in range (0 , len(values)):
            values[ii] = x_data[ii]

        nData = [0]* (len(LOBF_Data) - 7)
        for ii in range (0 , len(nData)):
            nData[ii] = LOBF_Data[ii]

        self.plt.plot(values, nData,  color = colour, alpha = 1, label = label)
        self.plt.bar(x_data, y_data,  color = colour, alpha = 0.5)
        self.BENCH.bench_end("COVIDCHART add_bar_plot")


    def add_bar_chart(self, x_data, y_data, colour, label="", display_vals = True, to_bar_over = True):
        '''
        Use when creating just bar charts without a line of best fit and totals at the top of each bar

        Args:
            :x_data: List or DataFrame, data for the x-axis of your bar plot 
            :y_data: List or DataFrame, data for the y-axis of your bar plot
            :colour: String Value, color of the plot, can be a word such as "red" or a hex value
            :label: String Value optional, This is the label used for the legend, to_bar_over must be set to False for the legend to be displayed 
            :display_vals: Boolean Value optional, set to true to display numbers above the bars
            :to_bar_over: Boolean Value optional, set to true if you don't want a legend, set to false for a legend
        '''

        self.BENCH.bench_start()

        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(x_data, list):
            pass
        else:
            x_data = x_data.tolist()
        #Make sure that the data is a list otherwiae the data could be reversed
        if isinstance(y_data, list):
            pass
        else:
            y_data = y_data.tolist()
        
        self.to_bar = to_bar_over

        if self.to_bar == True:
            self.alter_x_ticks = False
        
        if display_vals:
            for x in range(len(y_data)):
                y_data[x] = int(y_data[x])
                label3 = f'{y_data[x]:,}'
                self.plt.annotate(label3, # this is the text
                            (x_data[x],y_data[x]), # this is the point to label
                            textcoords="offset points", # how to position the text
                            xytext=(0,10), # distance from text to points (x,y)
                            ha='center', # horizontal alignment can be left, right or center
                            fontsize='16', color="#6D6D6D") #This size will look off when viewing the interactive graph, but good on the png
        
        self.plt.bar(x_data, y_data,  color = colour, alpha = 0.7,  label = label)
        self.BENCH.bench_end("COVIDCHART add_bar_chart")


    def add_treemap(self, data, labels, colours):
        '''
        Creates a treeMap diagram with data (list) and labels (list)
        The data should already be summed when calling this method therefore
        data should be an list of summed data

        Args:
            :data: List or DataFrame, data for the treemap. This data should not be timeseries, see the example in example.py
            :labels: List or DataFrame, The label for the plot, this will be used in the legend
            :colours: List or DataFrame, color of the plot, can be a word such as "red" or a hex value
        '''

        self.BENCH.bench_start()

        #Make sure that the data is a list otherwise the data could be reversed
        if isinstance(data, list):
            pass
        else:
            data = data.tolist()

        self.to_tree = True
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
        self.BENCH.bench_end("COVIDCHART add_treemap")


    def draw_chart(self, x_axis_title, y_axis_title, title, file_name, to_be_wide, hos_data=False):
        '''
        Draws the chart either on screen if to_show == true (set_chart_params) or as a png image saved with the file_name variable
        These graphs use ONS guidelines for formatting

        Args:
            :x_axis_title: String Value, Title for the x-axis
            :y_axis_title: String Value, Title for the y-axis
            :title: String Value, Title for the chart
            :file_name: String Value, file name of the chart (DO NOT INCLUDE FILE EXTENSION; this is added by this method)
            :to_be_wide: Boolean value, decides the aspect ratio of the chart, wide or portrait

            .. Note:: Do not add the file extension for the file name argument, this extension will always be .png and is added by this method
        '''

        if self.show_leg == True and self.columns == 14:
            self.columns = 7 #change the number of columns in the legend if were adding the VLINES

        #Add vertical lines
        if (self.to_add == True):
            self.draw_v_lines() #Draws vertical lines on the graph showing key moments
            
        #Format the axis
        axes = self.plt.gca()

        if (to_be_wide == True):
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
        
        #self.plt.xlabel(x_axis_title)
        self.plt.ylabel(y_axis_title)

        #format xAxis labels
        if (self.alter_x_ticks == True):
            self.ax1.xaxis.set_major_locator(self.ticker.MaxNLocator(75)) #set max number of labels so they dont overlap

        #self.ax1.set_facecolor("whitesmoke") #Change the background colour of the chart
        self.ax1.set_facecolor("white")

        #self.plt.xlabel(x_axis_title, fontsize=18,  color = "#6D6D6D")
        self.plt.ylabel(y_axis_title, fontsize=18,  color = "#6D6D6D")
        self.plt.xticks(rotation = 90, fontsize = 16)
        self.plt.yticks(fontsize = 16)

        if (self.to_tree == True or self.to_bar == True):
            #Do nothing
            pass
        elif self.legend_bottom == True:
            #self.plt.legend(loc='upper left', fontsize = 18) #Only draw a legend if its not a treemap or barchart
            #Set Legends
            legend = axes.legend(bbox_to_anchor=(0, -0.2, 1, .102), loc="upper left",
                            ncol=self.columns, mode="expand", borderaxespad=0,
                            prop={"family": "Arial", "size":16},
                            frameon=False);
        elif self.legend_bottom == False:
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

        if self.to_tree == True:
            self.plt.axis('off') #Do not draw axis for treemaps
        else:
            self.plt.axis('on')

        self.plt.savefig("reports/images/" + file_name + '.png')

        #Add time stamp to the png file
        if (self.to_stamp == True):
            if (to_be_wide == True):
                self.create_time_stamp("reports/images/" + file_name + '.png', 4300, 200, 24, to_be_wide, hos_data)
            else:
                self.create_time_stamp("reports/images/" + file_name + '.png', 1795, 1930, 24, to_be_wide, hos_data)

        print ("--CHART CLASS--: Graph saved as " + "reports/images/" + file_name + ".png")

        #Now make the fonts smaller for when the chart is shown
        self.plt.title(title, fontsize=16)
        #self.plt.xlabel(x_axis_title, fontsize=10)
        self.plt.ylabel(y_axis_title, fontsize=10)

        #self.plt.legend(loc='upper left', fontsize = 8)
        # Set Legends
        if self.legend_bottom == True:
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

        self.to_tree = False #Reset this Variable
        self.to_bar = True #Reset this Variable
        
        if (self.to_show == True):
            self.plt.show() #Show the plot

        self.columns = 14 #Reset this value
    

    def draw_v_lines(self):
        '''
        Draws vertical lines on charts indicating key moments. If any key moments need to be added add them in this method
        get_gov_date_Series() or govAgedDateSeries() should be used with this method and not dataframe["date"] as this will give an error
        '''
        LD1 = self.np.array(self.date(2020,3,23), dtype='datetime64')
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
            if (self.show_leg == True):
                
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
                #for i in range((LD2 - self.start_dataset_date).days, (LD2_S - self.start_dataset_date).days):
                #    self.plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

                self.plt.axvline(x=(VAC), alpha = 0.4, color = 'red')

                self.plt.axvline(x=(LD3), alpha = 0.2, color = 'steelblue')
                self.plt.axvline(x=(LD3_S), alpha = 0.2, color = 'steelblue')

                self.plt.axvline(x=(SLFT), alpha = 0.2, color = 'red')
                
                self.plt.axvline(x=(VAC1716), alpha = 0.4, color = 'red')
                self.plt.axvline(x=(BVACBOOST), alpha = 0.4, color = 'red')

                #self.plt.axvline(x=(TODAY - self.start_dataset_date).days, alpha = 0.4, color = 'red')

            #Shade in lockdown regions
            LD1 = self.date(2020,3,23)
            LD1_S = self.date(2020,6,23)
            startFill = (LD1 - self.start_dataset_date).days 
            endFill = (LD1_S - self.start_dataset_date).days
            start_date = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(start_date, endDate, facecolor='grey', alpha=0.1)

            LD2 = self.date(2020,11,5)
            LD2_S = self.date(2020,12,2)
            startFill = (LD2 - self.start_dataset_date).days 
            endFill = (LD2_S - self.start_dataset_date).days
            start_date = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(start_date, endDate, facecolor='grey', alpha=0.1)

            LD3 = self.date(2021,1,6)
            LD3_S = self.date(2021,7,19)
            startFill = (LD3 - self.start_dataset_date).days 
            endFill = (LD3_S - self.start_dataset_date).days
            start_date = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(startFill,'D')
            endDate = self.np.datetime64(self.start_dataset_date) + self.np.timedelta64(endFill,'D')
            self.plt.axvspan(start_date, endDate, facecolor='grey', alpha=0.1)
        except:
            print("--CHART CLASS--: Error drawing VLINES, use LoadDatasets.get_gov_date_Series() or govAgedDateSeries() instead of DataFrame['date'], Y axis canot be a dataframe it must be a list of dates.")


    def create_time_stamp(self, img_path, x_pos, y_pos, fontsize, to_be_wide, hos_data = False):
        '''
        Adds a timestamp to the chart with the website URL

        Args:
            :img_path: String Value, image path of where the chart is saved
            :x_pos: Integer Value, start position of the timestamp for the x-axis
            :y_pos: Integer Value, start position of the timestamp for the y-axis
            :fontsize: Integer Value, size of the fonts to be used
            :to_be_wide: Boolean value, is the charts aspect ratio wide or portait - decides if the stamp is to go at the top or bottom of the chart

            .. Note:: image_path is the path to the image including the file name extension, this will be .png for charts created by this class
        '''
        img = self.Image.open(img_path)
        now = self.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        font = self.ImageFont.truetype("arial.ttf", fontsize)
        d = self.ImageDraw.Draw(img)

        if (to_be_wide == True): #put time stamps at the top
            d.text((x_pos,y_pos - 30), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((x_pos,y_pos),"GitHub Repo: https://github.com/L33t-dot-UK/COVID-Reports", fill=("#6D6D6D"), font=font, alpha = 0.7)
            if(hos_data):
                d.text((x_pos,y_pos + 30),"Data Source: https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/", fill=("#6D6D6D"), font=font, alpha = 0.7)
            else:
                d.text((x_pos,y_pos + 30),"Data Source: https://coronavirus.data.gov.uk/details/download", fill=("#6D6D6D"), font=font, alpha = 0.7)
        else: #put the time stamps at the bottom
            d.text((x_pos,y_pos - 30), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=("#6D6D6D"), font=font, alpha = 0.7)
            d.text((x_pos,y_pos),"GitHub Repo: https://github.com/L33t-dot-UK/COVID-Reports", fill=("#6D6D6D"), font=font, alpha = 0.7)
            if (hos_data):
                d.text((x_pos - 1400,y_pos),"Data Source:  https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/", fill=("#6D6D6D"), font=font, alpha = 0.7)
            else:
                d.text((x_pos - 1400,y_pos),"Data Source: https://coronavirus.data.gov.uk/details/download", fill=("#6D6D6D"), font=font, alpha = 0.7)
            
        img.save(img_path)
   

    def clear_chart(self):
        '''
        Clears the chart saving the original params

        ..Note:: This should be called before creating another chart
        '''
        #Save the current params so the user dosent need to keep calling set_chart_params between charts
        TMPto_show = self.to_show  
        TMPshow_leg = self.show_leg  
        TMPto_add = self.to_add 
        TMPto_stamp = self.to_stamp 
        TMPAVTIME = self.averaged_time
        TMPstart_date = self.start_dataset_date
        TMPLEGBOT = self.legend_bottom
        TMPCOLS = self.columns

        self.__init__() #Clears the chart ready for the next set of data

        #Load the saved params
        self.to_show = TMPto_show 
        self.show_leg =  TMPshow_leg
        self.to_add = TMPto_add
        self.to_stamp = TMPto_stamp
        self.averaged_time = TMPAVTIME
        self.start_dataset_date = TMPstart_date
        self.alter_x_ticks = True #always change this back to true
        self.legend_bottom = TMPLEGBOT
        self.columns = TMPCOLS


    def draw_Scatter_Year_Comp(self, data, to_show, label, to_be_wide, y_dates, to_stamp):
        '''
        Give this method some data and it will split it into years and plot a 
        year comparison with daily averages

        Args:
            :data: List, data be to plotted on the y-axis
            :to_show: Boolean Value, deicdes if the chart should be shown
            :label: String Value, sets the label for the plots also used in the file name and title
            :to_be_wide: Boolean Value, sets aspect ratio to either landscape or portrait
            :y_dates: List, list of dates for the y-axis by default I used data/static/dates.csv, this will give you comparison charts starting and ending at March of each year
            :to_stamp: Boolean Value, decides if a time stamp should be added to the chart
        '''

        self.BENCH.bench_start()
        self.clear_chart()

        numberOfYears = float(len(data) / 365)
        numberOfYears = self.math.ceil(numberOfYears) #round up the number of years

        colours = ["brown", "olive", "orange", "orangered", "darkgreen", "teal"] #6 years of colours, if you have more years than that add more colours

        for ii in range(numberOfYears):
            totals = 0

            #We will cycle through the years splitting the data as necessary
            if ((len(data) - ((ii + 1) * 365)) > 0): #Multiple years so dimension this for 1 year
                plotData = [0] * 365
            else: #Less than 1 year so dimension the list for what ever is left
                plotData = [0] * (len(data) - (365 * (ii)))

                nDates = [0] * len(plotData)
                for iv in range (0, len(plotData)):
                    nDates[iv] = y_dates[iv]
                
                y_dates = nDates

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


            self.add_scatter_plot(y_dates, plotData, colours[ii], "Year " + str(yNum) + " " + label + " (Total: " + str(totals) + " / Daily Avg: " + str(dailyAvg) + ")", False, False)

            self.set_chart_params(to_show, False, False, to_stamp)

        self.set_legend_bottom(False)
        self.draw_chart("Date","Number of People","COVID 19 Data - Yearly Comp (" + label + ")", "yearlyComp"  + label , to_be_wide)
        self.BENCH.bench_end("COVIDCHART draw_Scatter_Year_Comp")    


    def _averaged_values(self, n_values, time):

        '''
        Averages values by the amount time. Used to draw lines of best fit on plots
        will take n/2 values before and after the datapoint to average values.

        Args:
            :n_values: A list of values to average
            :time: AMount of time to average the values over in days
        '''
        self.BENCH.bench_start()
        pointer = 0
        tmpVal = 0
        
        if(time % 2 != 0): # Not even
            time = time + 1 # make the number even

        values = n_values
        newValues = [0] * len(values)

        if len(n_values) > time:
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

        self.BENCH.bench_end("COVIDCHART averagedValues")
        return newValues
    

    def set_LOBF_time(self, time):
        '''
        Changes the averaged time in days for LOBF set my the argument time

        Args:
            :time: This is the amount of time in days for averaging the data

        '''
        self.averaged_time = time


    def set_chart_params(self, to_show, show_leg, to_add, to_stamp):
        '''
        Use to change the parameters of the COVID chart i.e. to show the chart, to add a time stamp, etc
        
        Args:
            :to_show: Boolean Value, decides whether to show the plot in python
            :show_leg:  Boolean Value, decides if the default COVID legend should be displayed with VLINES. You might want to show the VLINES without the legend
            :to_add: Boolean Value,  Boolean Value, decides if the VLINES should be added to the chart
            :to_stamp: Boolean Value, decides if the time stamp should be added to the chart
        ..Note:: 
        '''
        self.to_show = to_show
        self.show_leg = show_leg
        self.to_add = to_add
        self.to_stamp = to_stamp


    def set_legend_cols(self, value):
        '''
        Use this to change how many columns we have in the legend

        Args:
            :value: Integer Value, this will be the number of columns in the legend when its at the botton of the chart
        '''
        self.columns = value


    def set_legend_bottom(self, value):
        '''
        Use this if you wnat to change the position of the legend

        Args:
            :value: Boolean Value, if set to True the legend will be at the bottom of the chart otherwise it will be at the top left of the chart
        '''
        self.legend_bottom = value


    def set_max_y_value(self, value):
        '''
        sets the maximum Y valve

        Args:
            :value: Integer Value, sets the maxmum value for the Y-axis
        '''
        self.plt.ylim(ymax = value)


    def reset_max_y_value(self):
        '''
        Resets ylimit if it was explicitly set
        '''
        self.plt.autoscale()


    def set_start_date(self, start_date):
        '''
        Sets the start date for the graph to be used if you want to show VLINES when starting from a different date to the default one

        Args:
            :start_date: Date Value, used to set a different start date when to_add == True (set_chart_params). By default the start date is 20nd March 2020. This can be changed if required 
        '''
        self.start_dataset_date = start_date