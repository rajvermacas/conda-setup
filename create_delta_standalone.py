import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from deltalake import write_deltalake
import pyarrow as pa

# Create sample data
np.random.seed(42)
dates = [datetime.now() - timedelta(days=x) for x in range(100)]
data = {
    'timestamp': dates,
    'value': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'quantity': np.random.randint(1, 100, 100)
}

# Create pandas DataFrame
df = pd.DataFrame(data)

# Convert to PyArrow Table
table = pa.Table.from_pandas(df)

# Define the path for Delta table
delta_table_path = "standalone_delta_table"

# Write as Delta table
write_deltalake(
    delta_table_path,
    table,
    mode="overwrite",
    partition_by=["category"]
)

# Read and verify the data
from deltalake import DeltaTable
dt = DeltaTable(delta_table_path)

# Print schema
print("\nDelta Table Schema:")
print(dt.schema())

# Read as pandas DataFrame
df_read = dt.to_pandas()

# Show sample data
print("\nFirst few rows of data:")
print(df_read.head())

# Show statistics
print("\nTotal number of records:", len(df_read))
print("\nRecords per category:")
print(df_read.groupby('category').size())
