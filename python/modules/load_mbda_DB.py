# -*- coding: UTF-8 -*-

''' 
Last update on: November 9th, 2019
Author: Roberto Patrizi

This program perform initial upload of line structure into delphi
MariaDB database. Tables that will be loaded:
- machine,
- compnenent
- measure
- item
- measure_component
- item_measure_component

TABLES ARE REQUIRED BE EMPTED BEFORE PERFORMING UPLOAD
therefore, ensure you have reset data base
'''
programName = 'load_mbda_DB'

import time

print(' #-----------------------------------------------------------------#\n'
      , 'program ', programName, ' starts at  '
      , time.strftime('%Y-%m-%d %H:%M:%S'), '\n'
      , '#-----------------------------------------------------------------#')

# import application libraries
from mbda_library import *

# create a local Spark session
spark = SparkSession \
    .builder \
    .appName(programName) \
    .getOrCreate()
 
print( '\nspatk version = ' + spark.version)

# instancing spark classe
mySpark = sparkClass(spark)

#-----------------------------------------------------------------#
# reading measure dataset
measureDF, exitCode = mySpark.readCsv(measureDir, measureSchema)
# writing measure table
exitCode = mySpark.writeTable(measureDF, 'measure')
# reading measure table
measureDB, exitCode = mySpark.readTable('measure')

#-----------------------------------------------------------------#
# reading item dataset
itemDF, exitCode = mySpark.readCsv(itemDir, itemSchema)

itemDF2 = itemDF \
            .join(measureDB
                , ['measure'], 'inner') \
            .select('itemID'
                    , 'measure_id'
                    , 'cycleTime')

# writing item table
exitCode = mySpark.writeTable(itemDF2, 'item')
# reading item table
itemDB, exitCode = mySpark.readTable('item')

# reading linestructure dataset
lineStructureDF, exitCode = mySpark.readCsv(
                            lineStructureDir
                            , lineStructureSchema)

#-----------------------------------------------------------------#
# dealing with area
areaDF = lineStructureDF \
            .select('area', 'areaID') \
            .distinct()

# writing area table
exitCode = mySpark.writeTable(areaDF, 'area')
# reading item table
areaDB, exitCode = mySpark.readTable('area')

#-----------------------------------------------------------------#
#AB Occhio che il campo measure su measure.csv per mtt* sia definito come hour altrimenti la query estrae 0
# dealing with machine
print( '\n##STARTING MACHINEDF' )
machineDF = lineStructureDF \
            .filter((F.col('componentClass') == 'NA') &
                    (F.col('componentID') == 'NA') & 
                    (F.col('deactivationTime').isNull())) \
            .persist() \
            .join(areaDB
                , ['areaID'], 'inner') \
            .drop('measure') \
            .withColumn('measure', F.lit(mttf_measure)) \
            .persist() \
            .join(measureDB
                , ['measure'], 'inner') \
            .withColumnRenamed('mttf', 'machine_mttf') \
            .withColumnRenamed('mtbf', 'machine_mtbf') \
            .withColumnRenamed('mttr', 'machine_mttr') \
            .select('area_id'
                    , 'machineClass'
                    , 'machineID'
                    , 'measure_id'
                    , 'machine_mttf'
                    , 'machine_mtbf'
                    , 'machine_mttr'
                    , 'activationTime'
                    , 'deactivationTime')

# writing machine table
exitCode = mySpark.writeTable(machineDF, 'machine')
# reading machine table
machineDB, exitCode = mySpark.readTable('machine')
print( '\n####ENDED MACHINEDF' )
#-----------------------------------------------------------------#
# dealing with component
print( '\n##STARTING componentDF' )
componentDF = lineStructureDF \
            .filter((F.col('componentClass') != 'NA') &
                    (F.col('componentID') != 'NA') & 
                    (F.col('deactivationTime').isNull())) \
            .dropDuplicates(['componentID']) \
            .persist() \
            .join(areaDB
                , ['areaID'], 'inner') \
            .withColumnRenamed('mttf', 'component_mttf') \
            .withColumnRenamed('mtbf', 'component_mtbf') \
            .withColumnRenamed('mttr', 'component_mttr') \
            .persist() \
            .join(machineDB \
                    .select('machine_id', 'machineID'
                            , 'measure_id')
                , ['machineID'], 'inner') \
            .withColumnRenamed('mttf', 'component_mttf') \
            .withColumnRenamed('mtbf', 'component_mtbf') \
            .withColumnRenamed('mttr', 'component_mttr') \
            .select('machine_id'
                    , 'componentClass'
                    , 'componentID'
                    , 'measure_id'
                    , 'component_mttf'
                    , 'component_mtbf'
                    , 'component_mttr'
                    , 'activationTime'
                    , 'deactivationTime')

# writing component table
exitCode = mySpark.writeTable(componentDF, 'component')
# reading component table
componentDB, exitCode = mySpark.readTable('component')
print( '\n####ENDING componentDF' )

#-----------------------------------------------------------------#
# dealing with measure_component
print( '\n##START measure_componentDF' )
measure_componentDF = lineStructureDF \
                        .select('componentID', 'measure') \
                        .distinct() \
                        .persist() \
                        .join(componentDB
                                .select('component_id', 'componentID')
                            , ['componentID'], 'inner') \
                        .persist() \
                        .join(measureDB
                            , ['measure'], 'inner') \
                        .select('component_id', 'measure_id')

# writing measure_component table
exitCode = mySpark.writeTable(measure_componentDF, 'measure_component')
# reading measure_component table
measure_componentDB, exitCode = mySpark.readTable('measure_component')
print( '\n####ENDING measure_componentDF' )

#-----------------------------------------------------------------#
# dealing with item_measure_component
item_measure_componentDF, exitCode = mySpark.readCsv(
                                item_measure_componentDir
                                , item_measure_componentSchema)
print( '\n##STARTING item_measure_componentDF2' )
item_measure_componentDF2 = item_measure_componentDF \
                        .persist() \
                        .join(componentDB
                        .select('component_id', 'componentID')
                            , ['componentID'], 'inner') \
                        .persist() \
                        .join(measureDB
                            , ['measure'], 'inner') \
                        .persist() \
                        .join(measure_componentDB
                            , ['measure_id', 'component_id'], 'inner') \
                        .persist() \
                        .join(itemDB
                            , ['itemID'], 'inner') \
                        .select('item_id', 'measure_component_id'
                                , 'min_value', 'avg_value', 'max_value')

# writing item_measure_component table
exitCode = mySpark.writeTable(item_measure_componentDF2
                    , 'item_measure_component')
# reading item_measure_component table
item_measure_componentDB, exitCode = \
                mySpark.readTable('item_measure_component')
print( '\n####END item_measure_componentDF2' )
print(' #-----------------------------------------------------------------#\n'
      , 'program ', programName, ' ends at  '
      , time.strftime('%Y-%m-%d %H:%M:%S'), '\n'
      , '#-----------------------------------------------------------------#')

