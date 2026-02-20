# -*- coding: UTF-8 -*-

'''
Written on: October 16th, 2019
Author: Roberto Patrizi

This python module contains the common library
shared by all the python programs developed
carrying out the course
'''

#---------------------------------------------------------------------#
#                python overall library importing                     #
#---------------------------------------------------------------------#
import datetime
import time
import csv
# import random
import re
import copy as cp
import random as Random
import json

#------------------------------------------#
# importing sql module classes
#------------------------------------------#
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import *
from pyspark.sql import DataFrame, Row, Window
from pyspark.sql.types import *
from pyspark.sql.window import Window as W

#---------------------------------------------------------------------#
# import mathematical classes
#---------------------------------------------------------------------#
import math
# import scientific python library
#---------------------------------------------------------------------#
import scipy
from scipy import *
import numpy as np

# raw-data type = R-01
measurementSchema = StructType() \
        .add("recType", "string") \
        .add("event_time", "string") \
        .add("batchID", "string") \
        .add("recipeID", "string") \
        .add('machineID', 'string') \
        .add('componentID', 'string') \
        .add("itemNumber", 'string') \
        .add('measure', 'string') \
        .add('value', 'double') \
        .add('recording_time', 'string')

# raw-data type = R-02
stateSchema = StructType() \
        .add("recType", "string") \
        .add("event_time", "string") \
        .add('machineID', 'string') \
        .add('moduleID', 'string') \
        .add('componentID', 'string') \
        .add('stateCode', 'string')  \
        .add('recording_time', 'string')

#-----------------------------------------------------#
#    configuration tables schemas              #
#-----------------------------------------------------#
# lineStructure dataset LS-00
lineStructureSchema = StructType() \
        .add("machineClass", 'string') \
        .add("machineID", 'string') \
        .add("componentClass", 'string') \
        .add("componentID", 'string') \
        .add("activationTime", 'string') \
        .add("deactivationTime", 'string') \
        .add("mttf", 'double') \
        .add("mtbf", 'integer') \
        .add("mttr", 'integer')

# messages dataset MS-00
# msgSeverityLevel: 0 = OK, 1 = warning, 2 = severe
messageSchema = StructType() \
        .add("msgID", "string") \
        .add("msgSeverityLevel", "integer") \
        .add("msgText", 'string') \
        .add('msgExplanation', 'string')

# item RC-00
itemSchema = StructType() \
        .add("itemID", "string") \
        .add("itemTypeID", "string") 

# recipe RC-01
recipeSchema = StructType() \
        .add("recipeID", "string") \
        .add("recipe_descr", "string") 

#---------------------------------------------#                 
#           database parameters               #
#---------------------------------------------#
dbName = 'mysql'
dbHost = 'localhost'
dbPort = '3306'
dbUrl = 'jdbc:mysql://' + dbHost + ':' + dbPort + '/' + dbName
dbUser = 'studentbda'

# set this variable with your own password rather then 'xxxxxxxxxx'
dbPassword = 'xxxxxxxxxx'

