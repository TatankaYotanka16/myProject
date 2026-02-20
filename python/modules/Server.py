# -*- coding: UTF-8 -*-

# -*- coding: UTF-8 -*-

'''
Written on: October 19th, 2019
Author: Roberto Patrizi
This program:
- open a TCP/IP socket connection
- reads pre existing sample daya from an 
  external text dataset in which variables
  are separated by comma
- arranges timestamp thet refers to event time
- sends the whole data to client
'''

programName = 'Server'

import time
import csv

print(' #----------------------------------------------------------#\n'
      , 'program ', programName, ' starts at  '
      , time.strftime('%Y-%m-%d %H:%M:%S'), '\n'
      , '#----------------------------------------------------------#')

# application libraries
from  bda_library import *

#------------------------------------------#
#      main socket server program          #
#------------------------------------------#
from socket import *
s = socket(AF_INET,SOCK_STREAM)

host = '127.0.0.1'
port = 7502

inputSocketDir = '/home/studentbda/myProject/Data/Lake/Raw/events/'
datasetName = 'events.txt'
s.bind((host, port))
s.listen(1)

rawData = open(inputSocketDir + datasetName 
          , newline = '\n')
lines = rawData.read()
rawData.close()
rows = lines.split('\n')

#------------------------------------------------#
#    socket connection management
#------------------------------------------------#
print('waiting for connection at time '
      , time.strftime('%Y-%m-%d %H:%M:%S'))
c,a = s.accept()
print('#-----------------------------------------------#')
print("Received connection from ", a, ' - at time '
              , time.strftime('%Y-%m-%d %H:%M:%S'), '\n')

h = 1
while True:
    time.sleep(10)
    timeStamp = datetime.datetime.now()
    time_to_write = timeStamp \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
    msg = []
    for row in rows:
        # print('row = ', row)
        if row != '':
            # convert record sting into list
            x = row.split(',')
            # print('\nx before = ', x)
            # overwriting timestamp to this record
            x[1] = time_to_write
            x.append('#')
            # print('x after = ', x)
            # convert list into record string
            y = ','.join(x)
            # print('y = ', y)
            msg.append(y)
            # adding 1 second to current timestamp
            # figured out earlier
            timeStamp = timeStamp + \
                    datetime.timedelta(seconds=1)
            time_to_write = timeStamp \
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            break

    # add line feed to each record string
    msgString = '\n'.join(msg) + '\n'
    # print(msgString.encode())
    print('#----------------------------------------#')
    print('iteration = ', h, ' - at time '
              , time.strftime('%Y-%m-%d %H:%M:%S'), '\n')
    msgLength = len(msgString)
    print('sending ', msgLength, ' bytes')
    c.sendall(msgString.encode())
    print('send executed')
    h = h + 1

c.close()

print('#-----------------------------------#')
print( 'program ' +
       programName + ' ends at  ' +
       time.strftime('%Y-%m-%d %H:%M:%S'))
print('#-----------------------------------#')




''''
# java connector 2.4.0 for MariaDB 10.3 through Spark 2.4.0
spark.driver.extraClassPath=/usr/share/java/mariadb-java-client-2.4.4.jar
spark.executor.extraClassPath=/usr/share/java/mariadb-java-client-2.4.4.jar

# spark job scheduling policy
spark.scheduler.mode=FAIR

# maximum memory reserved 
spark.driver.memory=1g
spark.executor.memory=1g

# number of worker to launch
export SPARK_WORKER_INSTANCES=3
# maximum number of cores to allocate for each worker    
export SPARK_WORKER_CORES=2

# number of cores for each executor: 
spark.executor.cores=1

# Default maximum number of cores to allow per application.
# Applications can override this by setting the 
# spark.cores.max parameter. If it isn’t set, applications 
# take all available cores on the machine
spark.deploy.defaultCores=1

# it turns out spark will run a number 
# of executors for each worker given by:
# SPARK_WORKER_CORES / spark.executor.cores

# Whether the standalone cluster manager should spread applications out 
# across nodes or try to consolidate them onto as few nodes as possible
spark.deploy.spreadOut=false

# setting up console progress bar
spark.ui.showConsoleProgress=False


# Bind the master to a specific hostname or IP address
# dellphi version for Oroshaza = 192.168.1.100
export SPARK_MASTER_HOST=127.0.0.1
# start the master on a different port (default: 7077)
export SPARK_MASTER_PORT=7077
# Port for the master web UI (default: 8080).
export SPARK_MASTER_WEBUI_PORT=8080

'''
