#DRAWING THE CHART ------------------------------------------------------------------------------------------------------------------

#Draw the chart
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime

from PIL import ImageFont, ImageDraw, Image, ImageOps
from datetime import datetime

import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter

#DRAWING LINES, LEGENDS ETC ON THE CHART ------------------------------------------------------------------------------------------

globalLegendFontSize = 18

def drawChart(xAxisTitle, yAxisTitle, title, fileName, toShow, showLeg, ax1, toAdd, toStamp):

    if (toAdd == 'true'):
        #Draw verticle lines on the chart
        startDatasetDate = date(2020, 3,2)
        LD1 = date(2020,3,23)
        LD1_2Weeks = date(2020,4,6)
        LD1_S = date(2020,6,23)
        LD1_SchoolsBack = date(2020,6,1)
        FM = date(2020,7,24)
        FFM_2Weeks = date(2020,8,7)
        LD2 = date(2020,11,5)
        LD2_2Weeks = date(2020,11,19)
        LD2_S = date(2020,12,2)
        LD3 = date(2021,1,6)
        LD3_2Weeks = date(2021,1,20)
        LD3_S = date(2021,7,19)
        
        VAC = date(2020,12,8)
        P2T = date(2020,7,13)
        SLFT = date(2021,3,8)

        plt.axvline(x=(LD1 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 1.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD1_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD1_SchoolsBack - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) LD1 Schools Back')
        plt.axvline(x=(LD1_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        #Shade in lockdown 1 region
        for i in range((LD1 - startDatasetDate).days, (LD1_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(P2T - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Large Scale P2 Tests Introduced', color = 'red')
        
        plt.axvline(x=(FM - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Mandatory Face Masks', color = 'deepskyblue')
        plt.axvline(x=(FFM_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'deepskyblue' , linestyle='-.')

        plt.axvline(x=(LD2 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 2.0', color = 'cadetblue')
        plt.axvline(x=(LD2_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'cadetblue', linestyle='-.')
        plt.axvline(x=(LD2_S - startDatasetDate).days, alpha = 0.2, color = 'cadetblue')

        #Shade in lockdown 2 region
        for i in range((LD2 - startDatasetDate).days, (LD2_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(VAC - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) Vaccine Rollout Starts')

        plt.axvline(x=(LD3 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 3.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD3_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD3_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        plt.axvline(x=(SLFT - startDatasetDate).days, alpha = 0.2, label = '(VLINE) LD3 Schools Back with LFTs', color = 'red')
        
        #Shade in lockdown 3 region
        for i in range((LD3 - startDatasetDate).days, (LD3_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

    plt.ylim(ymin=0)

    plt.title(title)
    plt.xlabel(xAxisTitle)
    plt.ylabel(yAxisTitle)

    #Add the legend

    if(showLeg == "true"):
        plt.legend(loc='best')

    #Rotate the x plts labels and change bg colour
    plt.xticks(rotation = 90)

    ax1.set_facecolor("white")
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(75))

    plt.title(title, fontsize=20)
    plt.xlabel(xAxisTitle, fontsize=18)
    plt.ylabel(yAxisTitle, fontsize=18)
    if(showLeg == "true"):
        plt.legend(loc='upper left', fontsize = 18)
    plt.xticks(rotation = 90, fontsize = 16)
    plt.yticks(fontsize = 16)

    figure = plt.gcf()
    figure.set_size_inches(28, 20)
    plt.savefig("images/" + fileName + '.png')

    if(toStamp == 'true'):
        createTimeStamp("images/" + fileName + '.png', 1740, 1930, 24)

    print ("Graph saved as " + "images/" + fileName + ".png")

    plt.title(title, fontsize=12)
    plt.xlabel(xAxisTitle, fontsize=10)
    plt.ylabel(yAxisTitle, fontsize=10)
    if(showLeg == "true"):
        plt.legend(loc='upper left', fontsize = 8)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.yticks(fontsize = 8)

    if (toShow == "true"):
        plt.show() #Show the plot
    else:
        plt.close() #If we don't show the plot we close it

def drawWideChart(xAxisTitle, yAxisTitle, title, fileName, toShow, showLeg, ax1, toAdd, toStamp):

    if (toAdd == 'true'):
        #Draw verticle lines on the chart
        startDatasetDate = date(2020, 3,2)
        LD1 = date(2020,3,23)
        LD1_2Weeks = date(2020,4,6)
        LD1_S = date(2020,6,23)
        LD1_SchoolsBack = date(2020,6,1)
        FM = date(2020,7,24)
        FFM_2Weeks = date(2020,8,7)
        LD2 = date(2020,11,5)
        LD2_2Weeks = date(2020,11,19)
        LD2_S = date(2020,12,2)
        LD3 = date(2021,1,6)
        LD3_2Weeks = date(2021,1,20)
        LD3_S = date(2021,7,19)
        
        VAC = date(2020,12,8)
        P2T = date(2020,7,13)
        SLFT = date(2021,3,8)

        plt.axvline(x=(LD1 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 1.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD1_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD1_SchoolsBack - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) LD1 Schools Back')
        plt.axvline(x=(LD1_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        #Shade in lockdown 1 region
        for i in range((LD1 - startDatasetDate).days, (LD1_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(P2T - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Large Scale P2 Tests Introduced', color = 'red')
        
        plt.axvline(x=(FM - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Mandatory Face Masks', color = 'deepskyblue')
        plt.axvline(x=(FFM_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'deepskyblue' , linestyle='-.')

        plt.axvline(x=(LD2 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 2.0', color = 'cadetblue')
        plt.axvline(x=(LD2_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'cadetblue', linestyle='-.')
        plt.axvline(x=(LD2_S - startDatasetDate).days, alpha = 0.2, color = 'cadetblue')

        #Shade in lockdown 2 region
        for i in range((LD2 - startDatasetDate).days, (LD2_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(VAC - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) Vaccine Rollout Starts')

        plt.axvline(x=(LD3 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 3.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD3_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD3_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        plt.axvline(x=(SLFT - startDatasetDate).days, alpha = 0.2, label = '(VLINE) LD3 Schools Back with LFTs', color = 'red')
        
        #Shade in lockdown 3 region
        for i in range((LD3 - startDatasetDate).days, (LD3_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

    plt.ylim(ymin=0)

    plt.title(title)
    plt.xlabel(xAxisTitle)
    plt.ylabel(yAxisTitle)

    #Add the legend

    if(showLeg == "true"):
        plt.legend(loc='best')

    #Rotate the x plts labels and change bg colour
    plt.xticks(rotation = 90)

    ax1.set_facecolor("white")
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(75))

    plt.title(title, fontsize=20)
    plt.xlabel(xAxisTitle, fontsize=18)
    plt.ylabel(yAxisTitle, fontsize=18)
    if(showLeg == "true"):
        plt.legend(loc='upper left', fontsize = 18)
    plt.xticks(rotation = 90, fontsize = 16)
    plt.yticks(fontsize = 16)

    figure = plt.gcf()
    figure.set_size_inches(56, 20)
    plt.savefig("images/" + fileName + '.png')

    if(toStamp == 'true'):
        createTimeStamp("images/" + fileName + '.png', 4200, 1930, 24)

    print ("Graph saved as " + "images/" + fileName + ".png")

    plt.title(title, fontsize=12)
    plt.xlabel(xAxisTitle, fontsize=10)
    plt.ylabel(yAxisTitle, fontsize=10)
    if(showLeg == "true"):
        plt.legend(loc='upper left', fontsize = 8)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.yticks(fontsize = 8)

    if (toShow == "true"):
        plt.show() #Show the plot
    else:
        plt.close() #If we don't show the plot we close it

def drawChartHR(xAxisTitle, yAxisTitle, title, fileName, toShow, showLeg, ax1, toAdd, toStamp):

    if (toAdd == 'true'):
        #Draw verticle lines on the chart
        startDatasetDate = date(2020, 3,2)
        LD1 = date(2020,3,23)
        LD1_2Weeks = date(2020,4,6)
        LD1_S = date(2020,6,23)
        LD1_SchoolsBack = date(2020,6,1)
        FM = date(2020,7,24)
        FFM_2Weeks = date(2020,8,7)
        LD2 = date(2020,11,5)
        LD2_2Weeks = date(2020,11,19)
        LD2_S = date(2020,12,2)
        LD3 = date(2021,1,6)
        LD3_2Weeks = date(2021,1,20)
        LD3_S = date(2021,7,19)
        
        VAC = date(2020,12,8)
        P2T = date(2020,7,13)
        SLFT = date(2021,3,8)

        plt.axvline(x=(LD1 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 1.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD1_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD1_SchoolsBack - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) LD1 Schools Back')
        plt.axvline(x=(LD1_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        #Shade in lockdown 1 region
        for i in range((LD1 - startDatasetDate).days, (LD1_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(P2T - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Large Scale P2 Tests Introduced', color = 'red')
        
        plt.axvline(x=(FM - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Mandatory Face Masks', color = 'deepskyblue')
        plt.axvline(x=(FFM_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'deepskyblue' , linestyle='-.')

        plt.axvline(x=(LD2 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 2.0', color = 'cadetblue')
        plt.axvline(x=(LD2_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'cadetblue', linestyle='-.')
        plt.axvline(x=(LD2_S - startDatasetDate).days, alpha = 0.2, color = 'cadetblue')

        #Shade in lockdown 2 region
        for i in range((LD2 - startDatasetDate).days, (LD2_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

        plt.axvline(x=(VAC - startDatasetDate).days, alpha = 0.2, color = 'red', label = '(VLINE) Vaccine Rollout Starts')

        plt.axvline(x=(LD3 - startDatasetDate).days, alpha = 0.2, label = '(VLINE) Lockdown 3.0 & Schools Closed', color = 'steelblue')
        plt.axvline(x=(LD3_2Weeks - startDatasetDate).days, alpha = 0.2,  color = 'steelblue', linestyle='-.')
        plt.axvline(x=(LD3_S - startDatasetDate).days, alpha = 0.2, color = 'steelblue')

        plt.axvline(x=(SLFT - startDatasetDate).days, alpha = 0.2, label = '(VLINE) LD3 Schools Back with LFTs', color = 'red')
        


        #Shade in lockdown 3 region
        for i in range((LD3 - startDatasetDate).days, (LD3_S - startDatasetDate).days):
            plt.axvspan(i, i+1, facecolor='grey', alpha=0.1)

    plt.ylim(ymin=0)

    plt.title(title, fontsize = 50)
    plt.xlabel(xAxisTitle, fontsize = 40)
    plt.ylabel(yAxisTitle, fontsize = 40)
    plt.xticks(fontsize = 35)
    plt.yticks(fontsize = 35)

    #Add the legend

    if(showLeg == "true"):
        plt.legend(loc='best', fontsize= 30)

    #Rotate the x plts labels and change bg colour
    plt.xticks(rotation = 90)

    ax1.set_facecolor("white")
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(75))
    
    figure = plt.gcf()
    figure. set_size_inches(56, 40)
    plt.savefig("images/" + fileName + '.png')

    if(toStamp == 'true'):
        createTimeStamp("images/" + fileName + '.png', 3880, 3940, 48)

    print ("Graph saved as " + "images/" + fileName + ".png")

    plt.title(title, fontsize=12)
    plt.xlabel(xAxisTitle, fontsize=10)
    plt.ylabel(yAxisTitle, fontsize=10)
    if(showLeg == "true"):
        plt.legend(loc='best', fontsize = 8)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.yticks(fontsize = 8)

    if (toShow == "true"):
        plt.show()
    else:
        plt.close() #If we don't show the plot we close it


def drawChartDash(xAxisTitle, yAxisTitle, title, fileName, toShow, ax1):
    #Rotate the x plts labels and change bg colour
    plt.xticks(rotation = 90)

    ax1.set_facecolor("whitesmoke")
    ax1.xaxis.set_major_locator(ticker.MaxNLocator(75))

    plt.ylim(ymin=0)

    plt.title(title)
    plt.xlabel(xAxisTitle)
    plt.ylabel(yAxisTitle)

    #Display the chart
    figure = plt.gcf()
    figure. set_size_inches(28, 20)
    plt.savefig("images/" + fileName + '.png')

    if (toShow == "true"):
        plt.show()
    else:
        plt.close() #If we don't show the plot we close it

'''
#Use this to average values where the dataset is complete such as age profiled data
def averagedValuesCompleteData(values, time):
    pointer = 0
    tmpVal = 0
    newValues = [0] * len(values)
    
    if(time % 2 != 0): # Not even
        time = time + 1 # make the number even

    #Now average the last half of the selected time frame using n + 1 and n - 1
    newValues[0] = values[0]
    for ii in range(1, int(time / 2)):
        tmpVal = 0
        tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
        newValues[ii] = tmpVal / 3

    #calculate averages for the rest of the values apart from the last n / 2 values
    for ii in range(int(time / 2) , (len(values) - int(time / 2))):
        tmpVal = 0
        #print(ii)
        #getting values from after the datapoint
        for iv in range(0, int(time / 2)):
            pointer = ii - int(iv)
            tmpVal = tmpVal + values[pointer]
            #print(iv)

        #getting values from before
        for iv in range(0, int(time / 2)):
            pointer = (ii) + int(iv)
            tmpVal = tmpVal + values[pointer]
            #print(iv)
        tmpVal = tmpVal / time
        newValues[ii] = tmpVal

    tmpVal = 0

    #Now average the last half of the selected time frame using n + 1 and n - 1
    for ii in range(int((len(values) - ((time / 2)))), len(values) - 1):
        tmpVal = 0
        tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
        newValues[ii] = tmpVal / 3

    #Do this so the line doesnt fall off the end of the chart due to nill values
    if (values[len(values)- 1] == 0):
        values[len(values)- 1] = values[len(values)- 2]

    newValues[len(values)- 1] = (values[len(values) - 1] + values[len(values) - 2] / 2)

    return newValues
'''
#Averages values for a line of best fit
def averagedValues(nValues, time):
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
        #print(ii)
        #getting values from after the datapoint
        for iv in range(0, int(time / 2)):
            pointer = ii - int(iv)
            tmpVal = tmpVal + values[pointer]
            #print(iv)

        #getting values from before
        for iv in range(0, int(time / 2)):
            pointer = (ii) + int(iv)
            tmpVal = tmpVal + values[pointer]
            #print(iv)
        tmpVal = tmpVal / time
        newValues[ii] = tmpVal

    tmpVal = 0

    #Now average the last half of the selected time frame using n + 1 and n - 1
    #If the data is incomplete of varies too much the LOBF could look a little strange
    for ii in range(int((len(values) - ((time / 2)))), len(values) - 1):
        tmpVal = 0
        tmpVal = values[ii] + values[ii + 1] + values[ii - 1]
        newValues[ii] = tmpVal / 3

    #Do this so the line doesnt fall off the end of the chart due to nill values
    if (values[len(values)- 1] == 0):
        values[len(values)- 1] = values[len(values)- 2]

    newValues[len(values)- 1] = (values[len(values) - 1] + values[len(values) - 2]) / 2

    return newValues

def calcRatios(value1, value2, offset):
    calcedVal = value1.copy()
    for ii in range(len(value1)):
        calcedVal[ii] = 0

    for ii in range(len(value1) - offset):
        try:
            calcedVal[ii] = (float(value1[ii + offset] / value2[ii])* 100)
        except:
            calcedVal[ii] = 0
    return calcedVal

def calcRatioslimit(value1, value2, offset, upperLimit):
    calcedVal = value1.copy()
    for ii in range(len(value1)):
        calcedVal[ii] = 0

    for ii in range(len(value1) - offset):
        try:
            calcedVal[ii] = (float(value1[ii + offset] / value2[ii])* 100)
            if calcedVal[ii] > upperLimit:
                calcedVal[ii] = upperLimit
        except:
            calcedVal[ii] = 0
    return calcedVal

#total up values within an array
def totalValues(values):
    totalVal = 0
    for ii in range(len(values)):
        totalVal = totalVal + values[ii]
    return totalVal
    
def createTimeStamp(imgPath, xPos, yPos, fontSize):
    img = Image.open(imgPath)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    font = ImageFont.truetype("arial.ttf", fontSize)
    d = ImageDraw.Draw(img)
    d.text((xPos,yPos), "https://www.COVIDreports.uk   Last Updated " + dt_string, fill=(100,8,58), font=font)

    img.save(imgPath)

def drawRow(xStart, yStart, width, height, data, fillColour, lineColour, label, toTotal, imagePath, fontsize):
    total = 0

    img = Image.open(imagePath)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", fontsize)
    draw = ImageDraw.Draw(img)

    d.text((xStart - 130,  yStart + 25), label, fill=(100,8,58), font=font)
    
    for ii in range(19):
        
        if(toTotal == "true"):
            total = int(total)  + int(data[ii])
        try:
            data[ii] = f'{data[ii]:,}'
        except:
            print("Number format error")
        
        draw.rectangle((xStart, yStart, xStart + width, yStart + height), fill=(fillColour), outline=(lineColour))
        d.text((20 + xStart,  yStart + 25), data[ii] , fill=(100,8,58), font=font)
        xStart = xStart + width

    if(toTotal == "true"):
        total = f'{total:,}'
        draw.rectangle((xStart, yStart, xStart + width + int((width/2)), yStart + height), fill=(fillColour), outline=(lineColour))
        d.text((20 + xStart,  yStart + 25), str(total), fill=(100,8,58), font=font)

    img.save(imagePath)

def addScatterplot(xData, yData, colour, label):
    LOBF_Data = averagedValues(yData.copy(),7)

    #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
    #will make our LOBF look a little funny if we include it.
    values = [0]*(len(xData) - 7)
    for ii in range (0 , len(values)):
        values[ii] = xData[ii]

    nData = [0]* (len(LOBF_Data) - 7)
    for ii in range (0 , len(nData)):
        nData[ii] = LOBF_Data[ii]

    plt.plot(values, nData,  color = colour, alpha = 1, label = label)
    plt.scatter(xData, yData,  color = colour, alpha = 0.2, s =5)

def addScatterplotSubbed(xData, yData, colour, label, LOBFsub):
    LOBF_Data = averagedValues(yData.copy(),7)

    #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
    #will make our LOBF look a little funny if we include it.
    values = [0]*(len(xData) - LOBFsub)
    for ii in range (0 , len(values)):
        values[ii] = xData[ii]

    nData = [0]* (len(LOBF_Data) - LOBFsub)
    for ii in range (0 , len(nData)):
        nData[ii] = LOBF_Data[ii]

    plt.plot(values, nData,  color = colour, alpha = 1, label = label)
    plt.scatter(xData, yData,  color = colour, alpha = 0.2, s =5)

def addDashedLine(xData, yData, colour, label):
    plt.plot(xData, yData, '--', color = colour, alpha = 0.5, label = label)

def addBarplot(xData, yData, colour, label):
    LOBF_Data = averagedValues(yData.copy(),7)

    #Now we will chop the last 4 days worth of data as this data is probably incomplete and 
    #will make our LOBF look a little funny of we include it. However we will draw the scatter plots for this data.
    values = [0]*(len(xData) - 7)
    for ii in range (0 , len(values)):
        values[ii] = xData[ii]

    nData = [0]* (len(LOBF_Data) - 7)
    for ii in range (0 , len(nData)):
        nData[ii] = LOBF_Data[ii]

    plt.plot(values, nData,  color = colour, alpha = 1, label = label)
    plt.bar(xData, yData,  color = colour, alpha = 0.5)

def put_Side_By_Side(filename1, filename2, saveName):
    img = Image.new('RGB', (5600, 2000), color = 'white')
    d = ImageDraw.Draw(img)

    im1 = Image.open(filename1)
    im2 = Image.open(filename2)

    img.paste(im1, (0, 0))
    img.paste(im2, (2800, 0))

    img.save(saveName)



