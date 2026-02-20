# -*- coding: UTF-8 -*-

'''
This program gets data from a python TCP/IP server program
using pyspark SQL Structured Streaming API, performed
by readstream and writestream functions.
'''

programName = 'Streaming_Socket_Client'

import time

print('#---------------------------------------------------#')
print( 'program ' +
       programName + ' starts at  ' +
       time.strftime('%Y-%m-%d %H:%M:%S'))
print('#---------------------------------------------------#')

# application libraries
from  bda_library import *

# create a local Spark session
spark = SparkSession \
    .builder \
    .appName(programName) \
    .getOrCreate()

print('\n spatk version = ', spark.version, '\n')

#-----------------------------------------------#
#         main socket client program            #
#------------------------------s----------------#

# from socket import *
# s = socket(AF_INET,SOCK_STREAM)

# hostname and port number
host_1 = '127.0.0.1'
port_1 = 7502

outDir = ['/home/studentbda/myProject/Data/Lake/Raw/measurements'
        , '/home/studentbda/myProject/Data/Lake/Raw/states']

dsType = ['1', '2']

chkDir = ['/home/studentbda/myProject/Checkpoint/measurements'
        , '/home/studentbda/myProject/Checkpoint/states']

inDF = spark \
           .readStream \
           .format('socket') \
           .option('host', host_1) \
           .option('port', port_1) \
           .option("maxFilesPerTrigger", 1) \
           .load()

#--------------------------------------------------#
#  write streaming raw dataser R-01 plateMeasures  #
#--------------------------------------------------#

# during writestream process, it will be filtering
# records not starting with expected record types
q0 = inDF \
        .filter(
            (F.split(
                inDF.value, ',') \
                .getItem(0) == dsType[0]) |
            (F.split(
                inDF.value, ',') \
                .getItem(0) == dsType[1])
                ) \
        .writeStream \
        .format('text') \
        .outputMode('append') \
        .queryName(programName) \
        .start(path = outDir[0]
            , checkpointLocation = chkDir[0])

# following statement tell Spark to perform indefinetely
spark.streams.awaitAnyTermination()

print('#---------------------------------------------#')
print( 'program ' +
       programName + ' ends at  ' +
       time.strftime('%Y-%m-%d %H:%M:%S'))
print('#---------------------------------------------#')
