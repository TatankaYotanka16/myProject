from pyspark.sql import SparkSession

# 1. Inizializzare la SparkSession
spark = SparkSession.builder \
    .appName("Esempio PySpark SQL") \
    .getOrCreate()

# 2. Creare un DataFrame di esempio
data = [("Alice", "Sales", 5000),
        ("Bob", "Sales", 3000),
        ("Charlie", "IT", 4000),
        ("David", "IT", 6000)]
columns = ["Name", "Department", "Salary"]
df = spark.createDataFrame(data, schema=columns)

# 3. Registrare il DataFrame come vista SQL temporanea
df.createOrReplaceTempView("employees")

# 4. Eseguire query SQL
result = spark.sql("""
    SELECT Department, AVG(Salary) as AvgSalary
    FROM employees
    GROUP BY Department
    HAVING AVG(Salary) > 3500
""")

# 5. Mostrare il risultato
result.show()
