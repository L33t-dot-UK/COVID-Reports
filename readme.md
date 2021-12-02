# COVID-19 Toolset

This code allows you to download COVID-19 data from the UK Governments COVID dashboard and create graphs with the data or use it in ML/AI systems

An example is shown at the start of the chart class in COVIDTOOLSET.py and runWebsite.py contains the code that I used to create the graphs for the website http://www.COVIDreports.uk

This is a WIP and I will add to it as time goes on, when i'm trying new stuff out the code could have no documentation and could change.

Once data is loaded from the dataframe it is put into arrays of lists, this was done to allow people to use the data with little dataframe knowlegde

I have added readHospitalData class to the toolset enabling manual download of NHS data to be used for graph production. For this data I have kept the data as dataframes to make it easier to manipulate.

-runWebsite.py is used to create graphs for COVIDreports
-visualisations.py is used for the YT videos found at https://www.youtube.com/channel/UCNcBT9HlCxl9HaK-LC--gSA

The code has been written to enable amature programmers to use. I take data from dataframes and put that data into lists then iterate over the data using for loops. I know that this is bad practice and I should be using dataframe methods however, I decided to do things this way to allow people to understand my code who do not have background knowledge of dataframes.

For a list of all methods in the 4 classes from COVIDTOOLSET.py open the COVIDTOOLSET.html file which has been created using pyDoc.
