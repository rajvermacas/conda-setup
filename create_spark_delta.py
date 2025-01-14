import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, rand, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

# Set environment variables for local Spark cluster
os.environ['SPARK_LOCAL_IP'] = 'localhost'
os.environ['HADOOP_HOME'] = os.path.abspath('.')

# Initialize Spark with Delta Lake support and local cluster configuration
spark = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0") \
    .config("spark.sql.warehouse.dir", "spark-warehouse") \
    .config("spark.driver.extraJavaOptions", "-Dderby.system.home=./derby") \
    .enableHiveSupport() \
    .getOrCreate()

# Set log level to reduce verbosity
spark.sparkContext.setLogLevel("WARN")

print("Spark Web UI available at:", spark.sparkContext.uiWebUrl)
print("Number of cores in local cluster:", spark.sparkContext.defaultParallelism)

# Define schema for our data
schema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("value", DoubleType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True)
])

# Create sample data
num_rows = 100
df = spark.range(0, num_rows) \
    .withColumn("timestamp", current_timestamp()) \
    .withColumn("value", rand()) \
    .withColumn("category", expr("case when rand() < 0.33 then 'A' when rand() < 0.66 then 'B' else 'C' end")) \
    .withColumn("quantity", expr("cast(rand() * 100 as int)")) \
    .select("timestamp", "value", "category", "quantity")

# Define the path for Delta table
delta_table_path = "/root/projects/conda-setup/spark_delta_table"

# Write the DataFrame as a Delta table
df.write \
    .format("delta") \
    .mode("overwrite") \
    .partitionBy("category") \
    .save(delta_table_path)

# Read the Delta table back
df_read = spark.read.format("delta").load(delta_table_path)

# Show some sample data
print("\nSample data from Delta table:")
df_read.show(5)

# Show table statistics
print("\nTable Statistics:")
print(f"Total number of records: {df_read.count()}")
print("\nRecords per category:")
df_read.groupBy("category").count().show()

# Show Delta table history
print("\nDelta Table History:")
spark.sql(f"DESCRIBE HISTORY delta.`{delta_table_path}`").show(truncate=False)

# Print cluster information
print("\nSpark Cluster Information:")
print(f"Spark version: {spark.version}")
print(f"Master: {spark.sparkContext.master}")
print(f"Application ID: {spark.sparkContext.applicationId}")
print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")

# Clean up
spark.stop()
