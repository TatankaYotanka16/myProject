# Setup Sistemi MBDA
## Università Unimarconi - Esercitazione caricamento dati su MariaDB tramite PySpark

Aim of this repository is to share the involved files used during the test of PySpark for MBDA systems. 
The environment used for the tests was the following:

1. Virtual Machine KVM su Host Ubuntu 24.04 i7 16GB RAM 30GB qcow virtual disk
2. Guest Machine
   a. Ubuntu 24.04 Kernel 6.17
   b. PySpark 4.1.1
   c. JVM 17.0.18
   d. MariaDB 15.1
   e. JDBC connector `mariadb-java-client-3.5.7.jar` da inserire in `$SPARK_HOME/jars/`

### Note e modifiche rispetto agli appunti del corso

Due to different software version between course (2019) and current available, the following changes were needed:

* **JDBC connection string**: cambiato da `jdbc:mysql://` a `jdbc:mariadb://`
* **JDBC force quote setup**: aggiunto `"?sessionVariables=sql_mode='ANSI_QUOTES'"` alla definizione di `dbUrl` per evitare conflitti con colonne/dati nel DB
* **File `/etc/hosts`**: ridefinito l'hostname `studentbda` da `127.0.1.1` a `127.0.0.1` per evitare errori durante l'avvio delle istanze PySpark (Workers vs Master)
* **Metodo `readcsv`**: impostato `header=true` per identificare automaticamente i nomi delle colonne nei file CSV
