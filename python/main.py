# -*. coding: UTF-8 -*-
'''
Written on: October 8th, 2019
Author: Roberto Patrizi This program checks if MariaDB Server is
correctly accessed by PySpark environment. It read the user table in mysql
DB, reading name, host, plugin and password for each user.
'''
programName = 'try_mariadb'
import time
#import pyspark packages
from   pyspark.sql   import SparkSession

from   pyspark.sql   import  DataFrame
print('\n#------------------------------------------------------------#'
                 , '\n  program ', programName, ' starts at '
                 , time.strftime('%Y-%m-%d %H:%M:%S')
                 ,   '\n#------------------------------------------------------------#')
#---------------------------------------------#
#         database parameters                 #
#---------------------------------------------#
dbName = 'mysql'
dbHost   = 'localhost'
dbPort    =  '3306'
dbUrl = 'jdbc:mariadb://' + dbHost + ':' + dbPort + '/' + dbName + "?sessionVariables=sql_mode='ANSI_QUOTES'"
dbUser = 'studentbda'
dbPassword = 'studentbda'

# create a local Spark session
spark = SparkSession \
       .builder       \
       .appName(programName) \
       .config("spark.jars", "/usr/share/java/mariadb-java-client-3.5.7.jar") \
       .getOrCreate()
print('\nspark version = ' + spark.version, '\n')
#read data from mariadb table mysql.user
jdbcDF =  spark \
          .read \
          .format("jdbc") \
          .option('url', dbUrl) \
          .option("dbtable", 'tabellatest') \
           .option("user", dbUser) \
          .option("password", dbPassword) \
          .option("driver", "org.mariadb.jdbc.Driver") \
          .load()

jdbcDF.printSchema()
jdbcDF.show(truncate=False)

#select several columns from jdbc dataframe
jdbcDF \
         .select('col1'
                    , 'col2') \
         .show()
#stop spark core
spark.stop()
print('#------------------------------------------------------------#'
              , '\n      program  ', programName, ' ends at '
              , time.strftime('%Y-%m-%d %H:%M:%S')
              ,   '\n#------------------------------------------------------------#')
