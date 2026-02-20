# Esegui in spark-shell o nel tuo script
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()

# Prova a caricare la classe del driver
try:
    spark._jvm.java.lang.Class.forName("org.mariadb.jdbc.Driver")
    print("✅ Driver MariaDB caricato correttamente")
except Exception as e:
    print(f"❌ Errore: {e}")