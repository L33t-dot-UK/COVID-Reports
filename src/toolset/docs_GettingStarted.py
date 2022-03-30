#DO NOT USE THIS IS PART OF THE DOCUMENTATION SYSTEM

'''
To use the COVID Reports Python Toolset go tou our Git hub Repo, download, fork or clone it.

All toolset classes are stored in the /src/toolset folder. These are the classes that are used to create charts and import data using the Goverments API.

Example code can be viewed in the Examples folder and in this documentation. All of your code should be put in the src folder.

For imports to work always include the below line at the top of your code:

.. code-block:: python

    import sys
    sys.path.append('./src/toolset')

Once this is added you can import the modules in 2 ways the first way is shown below:

.. code-block:: python

    from toolset.LoadDatasets import LoadDataSets as govDataClass
    from toolset.CovidChart import CovidChart as CovidChart
    from toolset.GetCovidData import GetCOVIDData as getData
    from toolset.DataFunctions import Functions as functions
    from toolset.CovidDashboard import Dashboard as DASH
    from toolset.ReadVaxData import readVaxData as vax_data
    from toolset.ReadHospitalData import readHospitalData as HOSPITALDATA
    from toolset.BenchMark import Benchmark as Benchmark

.. Note:: The above way is to be used when putting you code in the src folder.

Another way to import the functions is shown here:

.. code-block:: python

    from LoadDatasets import LoadDataSets as govDataClass
    from CovidChart import CovidChart as CovidChart
    from GetCovidData import GetCOVIDData as getData
    from DataFunctions import Functions as functions
    from CovidDashboard import Dashboard as DASH
    from ReadVaxData import readVaxData as vax_data
    from ReadHospitalData import readHospitalData as HOSPITALDATA
    from BenchMark import Benchmark as Benchmark

.. Note:: If you use the above import with the toolset folder ommitted you might get syntax error highlighting however the code should still run. Use this method if your code is going in a different folder under root such as the examples folder.

Once the libaries are imported you will be able to access all methods within the classes. I recomend using Visual Studio Code with this project as it will automatically detect the virtual
environment that is stored in the venv folder. All dependecies have been added to this virtual environment. The dependcies are listed below incase you have any issues:

    | uk_coivd19
    | pandas
    | Matplotlib
    | Squarify
    | PIL
    | openpyxl

A summary of what each class does is shown below;

:GetCovidData: Used to download datasets from the UK Governments COVID API.
:LoadDatasets: Used to load the datasets into memory and offers easy to use methods to access the data in lists and as dataframes.
:ReadHospitalData: Reads hospital data from xlsx files downloaded manually from the NHS statistical service with detailed hsopital stats for England. Retruns data as a dataframe.
:ReadVaxData: Reads vaccination data that was downloaded with GetCovidData. Returns data as a dataframe.
:CovidChart: Used to create charts with a consistent look and feel. Allows the creation of bar charts, plot, scatter plots and tree maps.
:CovidDashboard: Used to create tables and dashboards from data and charts created by the CovidChart method.
:DataFunctions: Contains functions used to manipulate lists making it easier to create charts.
:Benchmark: Used to benchmark various methods.

If you want to change the time stamp i.e. change the URL to your own, you need to edit::

    CovidChart.create_time_stamp()

If you want to change how the charts looks you need to edit::

    CovidChart.draw_chart()

Documentation for this toolset can be viewed at https://covidreports.l33t.uk/API

Github Repo https://github.com/L33t-dot-UK/COVID-Reports

For support or bugs you can find me at Dave at L33T dot uk

'''