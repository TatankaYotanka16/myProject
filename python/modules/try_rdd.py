# -*- coding: UTF-8 -*-
'''
Written on: October 12th, 2019
Author: Roberto Patrizi
This program:
- creates a new RDD from a texr file,
selecting only error messages
- performs several example functions
about RDD Actions nd Trnsformations
'''
programName = 'try_rdd'
import time
print('\n#------------------------------------------------------------# '
    , '\n program ', programName, ' starts at '
    , time.strftime('%Y-%m-%d %H:%M:%S')
    ,'\n#------------------------------------------------------------#')
# importing regular expressions package
import re

# import pyspark packages
from pyspark.sql import SparkSession

# create a local Spark session
spark = SparkSession \
    .builder \
    .appName(programName) \
    .getOrCreate()

print('\nspatk version = ' + spark.version, '\n')
file_location = '/home/studentbda/myProject/Logs/'
log_file = 'spark_out.log'
error_msg = 'error_spark_out.log'

# read data from log text file
log_rdd = spark.sparkContext \
    .textFile(file_location + log_file)

# filter log records for errors only
only_errors_rdd = log_rdd \
    .filter(lambda line: "ERROR" in line)

# print on console stdout error lines
print('\nfollowing lines are error caught in the log file')
only_errors_rdd \
            .foreach(lambda line: print(line))

# print type and content of the new rdd
print('\nonly_errors_rdd type = ', type(only_errors_rdd))
print('\nonly_errors_rdd = ', only_errors_rdd)

# .map function counts total number of lines
error_number = only_errors_rdd \
    .count()

# print type and content of the new object
print('\nerror_number type = ', type(error_number))
print('\nerror_number = ', error_number)

# .map function computs line character number for each line
error_size = only_errors_rdd \
             .map(lambda s: len(s))
# print type and content of the new object
print('\nerror size type = ', type(error_size))
print('\nerror size = ', error_size)

# .reduce function compute total size
total_error_size = error_size \
        .reduce(lambda a, b: a + b)

# print type and content of the new object
print('\ntotal_error size type = ', type(total_error_size))
print('\ntotal_error size = ', total_error_size)
# counting occurrences of each word in error messages
# and return the counts sorted by the most frequently
# occurring words
wordcounts = only_errors_rdd \
        .filter(lambda line: len(line) > 0) \
        .flatMap(lambda line: re.split('\W+', line)) \
        .filter(lambda word: len(word) > 0) \
        .map(lambda word:(word.lower(),1)) \
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .map(lambda x: (x[1],x[0])) \
        .sortByKey(ascending=False) \
        .persist()

# print number of distinct words in error messages without actionprint('\nwordcounts in error messages = ', wordcounts)
print('\nwordcounts in error messages = ', wordcounts)

# print number of distinct words in error messages
print('\nwordcounts in error messages ='
        , wordcounts \
        .collect())

# printing wordcounts again, making
# output more confortable
w = wordcounts \
        .collect()
for x in w:
    print(x)

# save only_errors_rdd as a file
only_errors_rdd \
            .saveAsTextFile(file_location + error_msg)

# stop spark core
spark.stop()

print('\n#------------------------------------------------------------#'
    , '\n program ', programName, ' ends at '
    , time.strftime('%Y-%m-%d %H:%M:%S')
    , '\n#------------------------------------------------------------#')