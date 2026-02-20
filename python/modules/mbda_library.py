# -*- coding: UTF-8 -*-

'''
Written on: November 8th, 2019
Author: Roberto Patrizi

This python module contains the common library
shared by all the python programs developed
carrying out the course
'''

# getting mbda global variables set for python programs
# mbda_exec_mode can indicate either 'debug' or 'running' mode
import os
# print('os.environ type = ', type(os.environ)) 
# print('os.environ = ', os.environ) 
mbda_exec_mode    = os.environ['mbda_exec_mode']
if mbda_exec_mode == 'debug':
    print('os.environ[mbda_exec_mode] = '
            , os.environ['mbda_exec_mode']) 

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

#----------------------------------#
# import mathematical classes
#----------------------------------#
import math

# import scientific python library
import scipy
from scipy import *
import numpy as np

#----------------------------------#
# dataset / dataframe directories
#----------------------------------#
root = '/home/studentbda/myProject/Data/'
measureDir = root + 'Configuration/measure'
itemDir = root + 'Configuration/item'
lineStructureDir = root + 'Configuration/lineStructure'
item_measure_componentDir = root + 'Configuration/item_measure_component'

# mttf, mtbt and mttr measyre
mttf_measure = 'hour'

#---------------------------------------------#                 
#           database parameters               #
#---------------------------------------------#
#dbName = 'mbda_01_00'
dbName = 'mbda_01_00'
dbHost = '127.0.0.1'
dbPort = '3306'
#dbUrl = 'jdbc:mysql://' + dbHost + ':' + dbPort + '/' + dbName
dbUrl = 'jdbc:mariadb://' + dbHost + ':' + dbPort + '/' + dbName+ "?sessionVariables=sql_mode='ANSI_QUOTES'"
dbUser = 'studentbda'

# set this variable with your own password rather then 'xxxxxxxxxx'
dbPassword = 'studentbda'
#-----------------------------------------------------#
#    configuration tables schemas              #
#-----------------------------------------------------#
# measure 
measureSchema = StructType() \
        .add("unitID", "string") \
        .add("unit", "string") \
        .add("measure", "string") 

'''
# lineStructure 
# alternative syntax to define dataframe schema
lineStructureSchema = \
    StructType([
        StructField("area", StringType(), True)
        , StructField("areaID", StringType(), True)
        , StructField("machineClass", StringType(), True)
        , StructField("machineID", StringType(), True)
        , StructField("componentClass", StringType(), True)
        , StructField("componentID", StringType(), True)
        , StructField("activationTime", StringType(), True)
        , StructField("deactivationTime", StringType(), True)
        , StructField("mttf", DoubleType(), True)
        , StructField("mtbf", DoubleType(), True)
        , StructField("mttr", DoubleType(), True)
        , StructField("measure", StringType(), True)
    ])

'''
# lineStructure 
lineStructureSchema = \
    StructType() \
        .add("area", 'string') \
        .add("areaID", 'string') \
        .add("machineClass", 'string') \
        .add("machineID", 'string') \
        .add("componentClass", 'string') \
        .add("componentID", 'string') \
        .add("activationTime", 'string') \
        .add("deactivationTime", 'string') \
        .add("mttf", 'double') \
        .add("mtbf", 'integer') \
        .add("mttr", 'integer') \
        .add("measure", 'string')

# item 
itemSchema = StructType() \
        .add("itemID", "string") \
        .add("measure", "string") \
        .add("cycleTime", "double")
#AB     .add("cycleTime", "integer")


# item_measure_component 
item_measure_componentSchema = StructType() \
        .add("machineID", 'string') \
        .add("componentID", 'string') \
        .add("itemID", "string") \
        .add("measure", "string") \
        .add("min_value", "double") \
        .add("avg_value", "double") \
        .add("max_value", "double") 

#----------------------------------#
# dataset / dataframe schemas
#----------------------------------#
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


class sparkClass:
    'dinamic class with Spark functions calling'
    spark = None

    def __init__(self, mySpark):
        self.spark = mySpark 
        pass

    # function for reading txt dataset by spark
    def readTxt(self, inDs):
        try:
            df = self.spark \
                .read \
                .format('text') \
                .load(inDs)
            if mbda_exec_mode == 'debug':
                print('\ntext dataset ', inDs, ' row numer = '
                                , df.count())
                df.show(10, truncate = False)

            return df, True

        except Exception as ex:
            print('\n# Exception while reading txt dataset ', inDs, ' #')   
            print('***** excetion is:\n', ex)
            return None, False

    # function for reading csv dataset by spark
    # AB             .option('header', 'false') \
    def readCsv(self, inDs, schema):
        try:
            df = self.spark \
                .read \
                .format('csv') \
                .schema(schema) \
                .option('header', 'true') \
                .option('sep', ',') \
                .load(inDs)
            if mbda_exec_mode == 'debug':
                print('\ncsv dataset ',inDs, ' row numer = '
                                , df.count())
                df.show(10, truncate = False)

            return df, True

        except Exception as ex:
            print('\n# Exception while reading csv dataset ', inDs, ' #')   
            print('\n***** excetion is:\n', ex)
            return None, False

    # function for reading db table by spark
    def readTable(self, inTable):
        try:
            tb = self.spark \
                .read \
                .format("jdbc") \
                .option("url", dbUrl) \
                .option("dbtable", inTable) \
                .option("user", dbUser) \
                .option("password", dbPassword) \
                .load()
            if mbda_exec_mode == 'debug':
                print('\ntable ', inTable, ' row numer = '
                                , tb.count())
                tb.show(10, truncate = False)

            return tb, True

        except Exception as ex:
            print('\n# Exception while reading db table ', inTable, ' #')   
            print('\n***** excetion is:\n', ex)
            return None, False

    # function for reading JSON dataset by spark
    def readJson(self, inJson):
        try:
            df = self.spark \
                .read \
                .format('json') \
                .option("multiline", "true") \
                .load(inJson)
            if mbda_exec_mode == 'debug':
                df.show(10, truncate = False)

            return df, True

        except Exception as ex:
            print('\n# Exception while reading json dataset ', inJson, ' #')   
            print('\n***** excetion is:\n', ex)
            return None, False

    # function for writing txt dataset by spark
    def writeTxt(self, df, dsDir, mode):
        try:
            df \
                .write \
                .format('text') \
                .option('quoteAll', 'false') \
                .mode('append') \
                .save(dsDir)

            return True

        except Exception as ex:
            print('\n# Exception while writing txt dataset ', dsDir, ' #')   
            print('\n***** excetion is:\n', ex)
            return False

    # function for writing csv dataset by spark
    def writeCsv(self, df, dsDir, mode):
        try:
            df \
                .write \
                .option('delimiter', ',') \
                .option('header', 'false') \
                .csv(dsDir, mode = mode)

            return True

        except Exception as ex:
            print('\n# Exception while writing csv dataset ', dsDir, ' #')   
            print('\n***** excetion is:\n', ex)
            return False

    # function for writing JSON dataset by spark
    def writeJson(self, df, dsDir, mode):
        try:
            df \
                .write \
                .format('json') \
                .mode(mode) \
                .save(dsDir)

            return True

        except Exception as ex:
            print('\n# Exception while writing JSON dataset ', dsDir, ' #')   
            print('\n***** excetion is:\n', ex)
            return False

    # function for writing db table by spark
    def writeTable(self, tb, tbName):
        try:
            tb \
                .write \
                .format("jdbc") \
                .option("url", dbUrl) \
                .option("dbtable", tbName) \
                .option("user", dbUser) \
                .option("password", dbPassword) \
                .mode('append') \
                .save()

            return True

        except Exception as ex:
            print('\n# Exception while writing db table ', tbName, ' #')   
            print('\n***** excetion is:\n', ex)
            return False
