from pyspark.sql import SparkSession

# --- Configurazione Spark ---
spark = SparkSession.builder \
    .appName("test_mariadb") \
    .getOrCreate()

# --- Parametri connessione MySQL ---
jdbc_url = "jdbc:mysql://localhost:3306/testdb"  # cambia 'testdb' con il nome del tuo database
table_name = "prova"                       # cambia con il nome della tabella che vuoi leggere
user = "studentbda"                               # il tuo utente
password = "studentbda"                      # la tua password

# --- Lettura tabella MySQL in DataFrame Spark ---
try:
    df = spark.read.format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", table_name) \
        .option("user", user) \
        .option("password", password) \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .load()
    df.show()
except Exception as e:
    print("Errore nella connessione:", e)

# --- Stop Spark ---
spark.stop()

