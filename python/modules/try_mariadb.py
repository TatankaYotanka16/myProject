# -*. coding: UTF-8 -*-
'''
Written on: October 8th, 2019
Autohr: ROberto Patrizi This program checks if MariaDB Server is 
correctly accessed by PySpark enviroment. It read the user table in mysql
DB, reading name, host, plugin and password for each user.
'''
programName = 'try_mariadb'
import time
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
#import pyspark packages
from   pyspark.sql   import SparkSession
from   pyspark.sql   import  DataFrame
# create a local Spark session
spark = SparkSession \
       .builder       \
       .appName(programName) \
       .getOrCreate()
#      .config("spark.jars", "/usr/share/java/mariadb-java-client-3.5.7.jar") \ da mettere dopo appName ora non serve perchè il jar è sotto $SPARK_HOME/jar

print('\nspark version = ' + spark.version, '\n')
#read data from mariadb table mysql.user
jdbcDF =  spark \
          .read \
          .format("jdbc") \
          .option('url', dbUrl) \
          .option("dbtable", 'user') \
          .option("user", dbUser) \
          .option("password", dbPassword) \
          .option("driver", "org.mariadb.jdbc.Driver") \
          .load()
#select several columns from jdbc dataframe

print("=== Schema effettivo ===")
jdbcDF \
        .select('User'
                    , 'Host'
                    , 'plugin'
                    , 'Password') \
         .show()
#stop spark core
spark.stop()
print('#---------------------------------------------#'
              , '\n      program  ', programName, ' ends at '
              , time.strftime('%Y-%m-%d %H:%M:%S')
              ,   '\n#------------------------------------------------------------#')
