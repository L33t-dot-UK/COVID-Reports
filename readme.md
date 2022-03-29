<h1> COVID Reports Toolset </h1>

<p>This toolset was designed to create charts found at http://www.COVIDreports.uk. It takes data from the government dashboard using version 1 of their API, cleans and processes it ready for use within Python</p>

<p>Depending on how you want to use the data you can get it in list form or as dataframes apart from vaccine and hospital data that can only be returned as a dataframe.</p>

<p>I have also included some funcitons to take hospital data that can be downloaded from https://www.england.nhs.uk/statistics/statistical-work-areas/covid-19-hospital-activity/ Monthly returns and put into graphs helping people to understand the data in better ways. The hospital data functions are a work in progress and are likely to change over time as this version of the code is slow and hard to use</p>

<p>runWebsite.py is an example script that shows you how to use the toolset and is what I use to create my graphs, runHospitalGraphs.py shows you how to use the ReadHospitalData class</p>

<p>All code can be found in the src folder and the complete toolset can be found in /src/toolset. data used for the graphs can be found in the data folder.</p>

<p>Easy to understand examples can be found in the examples folder allowing you to create graphs quickly.</p>

<h2>Graphical User Interface</h2>

<p>I'm currently working on a GUI that will allow users who do not know how to code to use the toolset to produce graphs. Due to my current workload beyond this project this may take some time.</p>

<p>The /docs/sphinx folder contains somme sphinx setup files that will be used later on for documentation purposes, this is still a WIP, fo now you will have to use the comments in the code and the examples to understand how to use the code</p>

<p>Happy Coding</p>

