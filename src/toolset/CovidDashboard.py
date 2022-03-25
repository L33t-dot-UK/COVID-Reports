class Dashboard:
    '''
    COPYRIGHT DAVID BRADSHAW, L33T.UK AND COVIDREPORTS.UK, CREDIT MUST BE GIVEN IF THIS CODE IS USED

    Creates methods used to create dashboards from PNG images 

    CLASS COMPLETE AND DOCUMENTED
    VERSION 1.0.0 (NOV 21)
    '''
    from PIL import ImageFont, ImageDraw, Image, ImageOps
    from toolset.CovidChart import CovidChart as chartBENCH

    def __init__(self):
        self.globalMaxWidth = 0 #Max width for each column in a table, this ensures that all coluns are the same width
        self.globalHeight = 0
        pass


    def createDashboard(self, title, images, fileName):
        '''
        Takes a list of PNG images and creates a dashboard
        Images will be displayed in order

        Only give 2 sizes of image to this function all portrait images should be the same size and
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
                isLand[ii] = True
            else:
                isLand[ii] = False

        #Now we need to calculate the width of the dashboard
        maxWidthPort = 0
        maxWidthLand = 0

        for ii in range(len(images)):
            if(isLand[ii] == True):
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
            if (isLand[ii] == True):
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

        placeLeft = True
        for ii in range(len(images)):
            image = self.Image.open(images[ii])
            print("--DASHBOARD CLASS -- inserting image " + images[ii])
            oldYpos = yPos #save the old yPos
            if (isLand[ii] == True): #Landscape image place by itself
                if(ii > 0):yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if this is not the first image
                xPos = ((imageWidth / 2) - (imageResWidth[ii] / 2))
                img.paste(image, (int(xPos), int(yPos)))
                if(placeLeft == False): #If we need to place an image to the right restore the yPos coord
                    yPos = oldYpos
                    wentBack = True
            else:
            #The picture is not landscape so place side by side
                #If we've restored the yPos we now need to make sure that the yPos is incremented an extra time
                #otherwise we will over right the landscape image
                if(wentBack == True and placeLeft == True): 
                    yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if we placed a landscape image and restored oldYpos
                    wentBack = False

                if(placeLeft == True):
                    placeLeft = False
                    if(ii > 0):yPos = yPos + imageResHeight[ii - 1] + padding #increment yPos by the height of the previous image if this is not the first image
                    xPos = (((imageWidth / 2) - imageResWidth[ii]) / 2)
                    img.paste(image, (int(xPos), int(yPos)))
                else:
                    placeLeft = True
                    xPos = (((imageWidth / 2) - imageResWidth[ii]) / 2) + (imageWidth / 2)
                    img.paste(image, (int(xPos), int(yPos)))

        img.save('reports/images/' + fileName + '.png')

        xPos = imageWidth - 700
        yPos = imageHeight - 25

        chart = self.chartBENCH()
        chart.createTimeStamp("reports/images/" + fileName + ".png",  xPos, yPos, 20, False)
        print("Dashboard Saved as reports/images/" + fileName + ".png")

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

        if (toTotal == True):
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
            if(toTotal == True):
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

        if(toTotal == True):
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
            if (toTotal == True): tableWidth = tableWidth + self.globalMaxWidth #add an extra column to the calculaiton for the totals

            #Calc the middle of the table to centre align the text
            tableStart = xStart + (      (tableWidth / 2) - (titleWidth / 4)           )

            d.text((tableStart,  (yStart + yPadding)), tableTitle, fill=(100,8,58), font=font)
            yStart = yStart + (titleHeight + (yPadding * 2))

            img.save(imagePath)

        if (titleRow == True):
            #Add a title Row, use element 1 for column headings
            tmpData = data[0]
            self.createRow(xStart, yStart, xPadding, yPadding, tmpData, 'lightgrey', lineColour, '', False, imagePath, fontsize)
            yStart = yStart + (self.globalHeight + (yPadding * 2)) #Increment Y-Coords
     
        cntr = 0
        for record in data:
            if (titleRow == True and cntr == 0):
                pass #do nothing
            else: #add the rows
                self.createRow(xStart, yStart, xPadding, yPadding, record, fillColour, lineColour, label[cntr], toTotal, imagePath, fontsize)
                yStart = yStart + (self.globalHeight + (yPadding * 2)) #Increment Y-Coords
            cntr = cntr + 1

    def createPNG(self, xWidth, yWidth, fileName, fontsize):
        img = self.Image.new('RGB', (xWidth, yWidth), color = 'white')
        img = self.ImageOps.expand(img, border=2,fill='pink')
        d = self.ImageDraw.Draw(img)

        img.save('reports/images/' + fileName + '.png')
        img.close()