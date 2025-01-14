import org.apache.spark.sql.SparkSession
import io.delta.tables._
import org.apache.hadoop.fs.{FileSystem, Path}

// Initialize Spark Session with Delta Lake support
val spark = SparkSession.builder()
  .appName("Recreate Delta Lake")
  .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
  .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
  .getOrCreate()

// Replace this with your ADLS path
val deltaTablePath = "adls://your-storage-account.dfs.core.windows.net/path/to/your/delta/table"
val tempDeltaPath = deltaTablePath + "_temp_backup"

// Read existing Delta table
val existingData = spark.read.format("delta").load(deltaTablePath)

// Create a temporary backup Delta table
println("Creating temporary backup Delta table...")
existingData.write
  .format("delta")
  .mode("overwrite")
  .save(tempDeltaPath)

// Verify the temporary backup was created successfully
val backupData = spark.read.format("delta").load(tempDeltaPath)
val originalCount = existingData.count()
val backupCount = backupData.count()

if (originalCount != backupCount) {
  throw new Exception(s"Backup verification failed! Original count: $originalCount, Backup count: $backupCount")
}

println(s"Backup verification successful. Records count: $backupCount")

// Delete the existing Delta table location
println("Deleting original Delta table...")
val fs = FileSystem.get(spark.sparkContext.hadoopConfiguration)
fs.delete(new Path(deltaTablePath), true)

// Write the data back to create a fresh Delta table
println("Creating fresh Delta table from backup...")
backupData.write
  .format("delta")
  .mode("overwrite")
  .save(deltaTablePath)

// Verify the new table was created successfully
val newTableCount = spark.read.format("delta").load(deltaTablePath).count()
if (newTableCount != originalCount) {
  throw new Exception(s"New table verification failed! Original count: $originalCount, New table count: $newTableCount")
}

println(s"New table creation successful. Records count: $newTableCount")

// Clean up the temporary backup
println("Cleaning up temporary backup...")
fs.delete(new Path(tempDeltaPath), true)

// Clean up
spark.stop()