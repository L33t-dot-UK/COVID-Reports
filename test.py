
'''
THIS IS WHERE I TEST SOME OF THE CODE IN THE COVIDTOOLSET CLASS

THIS CODE CAN BE IGNORED!!!!!
'''

#Import COVID Data with our COVIDTOOLSET
from numpy.core.shape_base import block
from numpy.lib import function_base
from COVIDTOOLSET import LoadDataSets as govDataClass
from COVIDTOOLSET import CovidChart as CovidChart
from COVIDTOOLSET import GetCOVIDData as getData
from COVIDTOOLSET import Functions as functions
from COVIDTOOLSET import Dashboard as DASH

import numpy as np

nation = "England" #If this is set to anything else Age profiled data will always be for England as it is not available for the other nations

pullData = getData(nation) #get the latest data