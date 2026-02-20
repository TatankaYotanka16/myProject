<< ////
Last update: November 9th, 2019
Author: Roberto Patrizi

This script launch bachup, drop
and initial load of mbda MariaDB database

this script needs to be run from its own directory
by the command ./mbda_DB_drop_load.sh
after have made the script executable by
the command chmod +x mbda_DB_drop_load.sh
////

root="/home/studentbda/myProject"
pythonDir=$root'/python/modules/'
scriptDir=$root"/python/scripts"
scriptDbLoad=$scriptDir"/create_mbda_DB.sql"
backupDir=$root"/Data/Backup"

prog1='load_mbda_DB.py'
log1=$root"/Logs/load_mbda_DB.log"

masterUrl="spark://127.0.0.1:7077"

echo "#-----------------------------------------#"
echo "#     start script mbda_DB_drop_load    #"
echo "#-----------------------------------------#"

dayTime=$(date +"%Y-%m-%d-%T")
echo "current system dayTime is "$dayTime

# make sure to declare the right hostname, 
# depending on the environment where the script is run 
dbHost="127.0.0.1"
dbPort="3306"
dbUser="studentbda"
dbPassword="studentbda"
#dbName="mbda_01_00"
dbName="mbda_01_00"

destDB="$backupDir/$dbName-DB-backup-$dayTime.sql"

#  ask user to indicate whether he wants to drop or not
#  and recreate delphi database
read -p "Do you want to backup, drop and recreate MBDA DB? : (yes / no) > " ans1
if [ $ans1 == "yes" ]; then
	echo "#-----------------------------------------------------------#"
	echo "  start database "$dbName" backup at "$dayTime

	mysqldump \
		--user=$dbUser \
		--password=$dbPassword \
		--host=$dbHost \
		--port=$dbPort \
		--lock-tables \
		$dbName \
			> $destDB

	if [ $? -eq 0 ]; then
		echo " DB backup successfully completed at "$dayTime
	else
    	echo "Error found during backup"
	    exit 1
	fi

	echo "#----------------------------------------#"
	echo "  start drop and create "
	echo "  database "$dbName" at "$dayTime

	mysql \
		--user=$dbUser \
		--password=$dbPassword \
		--host=$dbHost \
		--port=$dbPort \
<<my_sql
    source $scriptDbLoad;
	select concat ("#--------------------------#") as '';
    show tables;
my_sql

fi

#  ask user to indicate whether he wants to stop and restart
#  spark master and workers
read -p "Do you want to stop and restart spark master/slaves session ? : (yes / no) > " ans2

if [ $ans2 == "yes" ]; then

	# stopping pre existing spark sessions
	$SPARK_HOME"/sbin/stop-master.sh"
	$SPARK_HOME"/sbin/stop-worker.sh"

	# launching new spark session
	$SPARK_HOME"/sbin/start-master.sh" 
	$SPARK_HOME"/sbin/start-worker.sh"  $masterUrl --memory 2g
fi

# ask user to indicate whether he wants to make
# initial load of MBDA database or not
echo "#------------------------------------------------#"
echo "before you start DB loading, make sure"
echo "spark master and worker are already running"
read -p "Do you want to perform MBDA DB initial load? : (yes / no) > " ans3

# stdout and stderr are both redirected to log1
if [ $ans3 == "yes" ]; then
	$SPARK_HOME"/bin/spark-submit" --master $masterUrl \
		  $pythonDir$prog1 \
                 > $log1 2>&1 &

fi


echo "#---------------------------------------#"
echo "#       end script mbda_DB_drop_load  #"
echo "#---------------------------------------#"
