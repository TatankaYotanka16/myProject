# Setup Sistemi MBDA
## Università Unimarconi - Esercitazione caricamento dati su MariaDB tramite pSpark

Aim of this repository is to share the involved files used during the test of pSpark for MBDA systems. 
The enviroment used for the tests was the following:
1. Virtual Machine KVM su Host Ubuntu 24.04 i7 16GB RAM 30GB qcow virtual disk
2. Guest Machine
  a. Ubuntu 24.04 Kernel 6.17
  b. Pspark 4.1.1
  c. JVM 17.0.18
  d. MariaDB 15.1
  e. jdbc connector mariadb-java-client-3.5.7.jar to place under $SPARK_HOME/jars/

### Note e modifiche rispetto agli appunti del corso
Due to different software version between course (2019) and current available, the following changes were needed:
* JDBC change to allow DB connection: old jdbc:mysql://new jdbc:mariadb://
* JDBC force quote setup: "?sessionVariables=sql_mode='ANSI_QUOTES'" on dbUrl definition to avoid wrong column/data interaction with DB
* file /etc/hosts redefined host name studentbda from old 127.0.1.1 to 127.0.0.1 to avoid error during pSpark instances of Workers vs Master
* method readcsv set to true the header identification in order to identify quickly the column names inside the csv files
