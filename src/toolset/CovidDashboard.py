class Dashboard:
    '''
    Used to create dashboards and tables from COVID data. 

    This class can be used to create dashboards from a list of images and to create tables from Lists that can be added to dashbaords or graphs. An example is included below.
    '''
    from PIL import ImageFont, ImageDraw, Image, ImageOps
    from .CovidChart import CovidChart as chartBENCH


    def __init__(self):
        self.globalMaxWidth = 0 #Max width for each column in a table, this ensures that all coluns are the same width
        self.globalHeight = 0
        pass


    def create_dashboard(self, title, images, file_name):
        '''
        Takes a list of PNG images and creates a dashboard. Images will be displayed in order

        Args:
            title: String Value, this is the title of the dashboard
            images: List, this will be a list of images to be used for the dashboard
            file_name: String Value, this is the name of the image file for the dashbaord, do not include the file extension

        .. Note:: Do not include the file extension for the file_name argument

        .. Note:: Only give 2 sizes of images to this function all portrait images should be the same size and all landscape images should be the same size

        .. Note:: If you give portrait images they should be in an even number as these are laid side by side
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

        img.save('reports/images/' + file_name + '.png')

        xPos = imageWidth - 700
        yPos = imageHeight - 25

        chart = self.chartBENCH()
        chart.create_time_stamp("reports/images/" + file_name + ".png",  xPos, yPos, 20, False)
        print("--DASHBOARD CLASS -- Dashboard Saved as reports/images/" + file_name + ".png")
   

    def create_table(self, x_start, y_start, x_padding, y_padding, data, fill_colour, line_colour, label, to_total, image_path, fontsize, title_row, table_title):
        '''
        Create a table and saves to PNG image, this method uses the create_row method in a loop to create tables.

        Args:
            x_start: Integer Value, start location on the x-axis 
            y_start: Integer Value, start location on the y-axis
            x_padding: Integer Value, the amount of padding to have in the x-axis in pixels
            y_padding: Integer Value, the amount of padding to have in the y-axis in pixels
            data: List[][], data that will be used in the tables row, this is multidimensional List[row][column]
            fill_colour: String Value, background colour of the cells
            line_colour: String Value, Line colour of the table lines
            label: List, title for each column
            to_total: Boolean Value, this will be true if the values are to be added and a totals column inserted
            image_path: String Value, locaiton of the image that the table row will be inserted into, this must already exist
            fonstsize: Integer Value, size of the fonts to be used when generating the table
            title_row: List, title of each row, there must be a title for each row and a blank title for the top row if your using title_row
            table_title: String Value, title of the table

        .. Note:: Data is a multidimenstional list data[row][column]

        .. Note:: Please note that len(label) must be equal to the number of rows, this is the title for each row, 
        
        .. Note:: If title_row is used then a blank label must be included in the label List i.e label = ['','20 -24', '25 - 29', '30 - 34']

        .. Note:: If to_total is true then ensure that all data apart from the title header is numeric, for non numeric data set to_total to False

        Example:

            from toolset.CovidDashboard import Dashboard as chart

            chart = chart()

            label = ['', 'Cases', 'Deaths', 'CFR']
            title_row = ['0-4', '5-9', '10-14']
            data = [title_row,[20156,22514,30145],[0,1,2],['0%','0%','0%']]

            chart.create_table(500, 200, 15, 15, data, "white", "black", label, False, "reports/images/test_Table.png", 30, True, "Just a test table")

            +------------------------+------------+----------+----------+
            |                        |    0-4     |   5-9    |   10-14  |
            |                        |            |          |          |
            +========================+============+==========+==========+
            | Cases                  |   20,156   |  22,514  |  30,145  |
            +------------------------+------------+----------+----------+
            | Deaths                 |     0      |    1     |    2     |
            +------------------------+------------+----------+----------+
            | CFR                    |     0%     |     0%   |   0%     |
            +------------------------+------------+----------+----------+


        '''
        self.globalMaxWidth = 0 #Reset this value when creating a new table
        #Before doing anything lets find what our column widths will be
        for record in data:
            self._get_max_widths(record, image_path, to_total, x_padding, fontsize)
        
        if (table_title != ''): #If a table title is used
            img = self.Image.open(image_path)
            d = self.ImageDraw.Draw(img)
            font = self.ImageFont.truetype("arial.ttf", (fontsize * 2)) #Title will be twice the size of the table text
            draw = self.ImageDraw.Draw(img)
            titleWidth, titleHeight =  draw.textsize(table_title, font=font)

            #Now we have the size of the title we now need to place it
            #calc table width
            tableWidth = (self.globalMaxWidth * len(data[0]))
            if (to_total == True): tableWidth = tableWidth + self.globalMaxWidth #add an extra column to the calculaiton for the totals

            #Calc the middle of the table to centre align the text
            tableStart = x_start + (      (tableWidth / 2) - (titleWidth / 4)           )

            d.text((tableStart,  (y_start + y_padding)), table_title, fill=(100,8,58), font=font)
            y_start = y_start + (titleHeight + (y_padding * 2))

            img.save(image_path)

        if (title_row == True):
            #Add a title Row, use element 1 for column headings
            tmpData = data[0]
            self.create_row(x_start, y_start, x_padding, y_padding, tmpData, 'lightgrey', line_colour, '', False, image_path, fontsize)
            y_start = y_start + (self.globalHeight + (y_padding * 2)) #Increment Y-Coords
     
        cntr = 0
        for record in data:
            if (title_row == True and cntr == 0):
                pass #do nothing
            else: #add the rows
                self.create_row(x_start, y_start, x_padding, y_padding, record, fill_colour, line_colour, label[cntr], to_total, image_path, fontsize)
                y_start = y_start + (self.globalHeight + (y_padding * 2)) #Increment Y-Coords
            cntr = cntr + 1


    def create_row(self, x_start, y_start, x_padding, y_padding, data, fill_colour, line_colour, label, to_total, image_path, fontsize):
        '''
        Creates a row of a table from a list of data

        Args,
            x_start: Integer Value, start location on the x-axis 
            y_start: Integer Value, start location on the y-axis
            x_padding: Integer Value, the amount of padding to have in the x-axis in pixels
            y_padding: Integer Value, the amount of padding to have in the y-axis in pixels
            data: List, data that will be used in the tables row
            fill_colour: String Value, background colour of the cells
            line_colour: String Value, Line colour of the table lines
            label: String Value, title for the row
            to_total: Boolean Value, this will be true if the values are to be added and a totals column inserted
            image_path: String Value, locaiton of the image that the table row will be inserted into, this must already exist
            fonstsize: Integer Value, size of the fonts to be used when generating the table
        
        .. Note:: give this funciton one row of data at a time
        '''
        total = 0

        img = self.Image.open(image_path)
        d = self.ImageDraw.Draw(img)
        font = self.ImageFont.truetype("arial.ttf", fontsize)
        draw = self.ImageDraw.Draw(img)

        width = [0] * len(data)
        height = [0] * len(data)

        for ii in range(len(data)): #Calculate the width and height of the text
            width[ii], height[ii] = draw.textsize(str(data[ii]), font=font)
            width[ii] = width[ii] + (x_padding * 2) #Add padding to the calculations
            height[ii] = height[ii] + (y_padding * 2)

        #Find the maxwidth so all colums are the same size
        maxWidth = max(width)

        if (self.globalMaxWidth > 0): #if the global max width is being used
            maxWidth = self.globalMaxWidth

        maxHeight = max(height)

        if (self.globalHeight > 0): #if the global ax width is being used
            maxHeight = (self.globalHeight + (y_padding * 2))

        #Now write the label
        lblWidth, lblHeight =  draw.textsize(str(label), font=font)

        d.text((x_start - (lblWidth + (x_padding)),  y_start + (lblHeight - (y_padding))), label, fill=(100,8,58), font=font)

        for ii in range(len(data)):
            if(to_total == True):
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
            
            draw.rectangle((x_start, y_start, x_start + (maxWidth + x_padding * 2), y_start + maxHeight), fill=(fill_colour), outline=(line_colour))
            d.text((x_start  + (((maxWidth / 2) + (x_padding * 2)) - ((width[ii]) / 2)),  (y_start + y_padding)), data[ii], fill=(100,8,58), font=font)
            
            x_start = x_start + (maxWidth + x_padding * 2)

        if(to_total == True):
            try:
                total = f'{total:,}' #Use a try incase the total is a string value
            except:
                pass
            totWidth, totHeight =  draw.textsize(str(total), font=font)

            draw.rectangle((x_start, y_start, x_start + (maxWidth + x_padding * 2), y_start + maxHeight), fill=(fill_colour), outline=(line_colour))
            d.text((x_start  + (((maxWidth / 2) + ((x_padding)) - ((totWidth) / 2))),  (y_start + y_padding)), total, fill=(100,8,58), font=font)
            
        img.save(image_path)


    def create_PNG(self, width, height, file_name, fontsize):
        '''
        Creates a png file with specified dimensions and pink boarder

        Args:
            width: Integer Value, width of the image in pixels
            height: Integer Value, height of the image in pixels
            file_name: String Value, the loaction where the file will be saved, do not include file extension or file path just the file_name
            fontsize: Integer Value, not used at this time
        '''

        img = self.Image.new('RGB', (width, height), color = 'white')
        img = self.ImageOps.expand(img, border=2,fill='pink')
        d = self.ImageDraw.Draw(img)

        img.save('reports/images/' + file_name + '.png')
        img.close()


    def _get_max_widths(self, data, image_path, to_total, x_padding, fontsize):
        '''
        Used to calulate cell widths when creating tables

        Args:
            data: List, data that will be used to create the table
            image_path: String Value, location where the image resides that the table will be inserted into
            to_total: Boolean Value, this will be true if the values are to be added and a totals column inserted
            x_padding: Integer Value, the amount of padding to have in the x axis in pixels
            fontsize: Integer Value, size of the fonts to be used when generating the table

        '''
        img = self.Image.open(image_path)
        draw = self.ImageDraw.Draw(img)
        font = self.ImageFont.truetype("arial.ttf", fontsize)

        width = [0] * len(data)
        height = [0] * len(data)

        for ii in range (len(data)):
            width[ii], height[ii] =  draw.textsize(str(data[ii]), font=font)

        if(max(width) > self.globalMaxWidth):
            self.globalMaxWidth = max(width)

        self.globalHeight = max(height) #This will be the sae for all rows 

        if (to_total == True):
            try: #Put this in a try incase we have string values
                tmpVal = sum(data)
                x, y =  draw.textsize(str(tmpVal), font=font)
                if ((x + (x_padding * 2)) > self.globalMaxWidth):
                    self.globalMaxWidth = x + (x_padding * 2)
            except:
                pass