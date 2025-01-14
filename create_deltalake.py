import pandas as pd
from deltalake import DeltaTable, write_deltalake
import numpy as np
from datetime import datetime, timedelta

# Create sample data
np.random.seed(42)
dates = [datetime.now() - timedelta(days=x) for x in range(100)]
data = {
    'date': dates,
    'value': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'quantity': np.random.randint(1, 100, 100)
}

# Create pandas DataFrame
df = pd.DataFrame(data)

# Define the path where you want to save the Delta table
delta_table_path = "sample_delta_table"

# Write DataFrame to Delta table
write_deltalake(
    delta_table_path,
    df,
    mode="overwrite",  # or "append" if you want to add to existing table
    partition_by=["category"]  # optional: partition the data by category
)

# Read the Delta table to verify
dt = DeltaTable(delta_table_path)
print("\nDelta Table Schema:")
print(dt.schema())

print("\nDelta Table History:")
print(dt.history())

# Read back as pandas DataFrame
df_read = dt.to_pandas()
print("\nFirst few rows of the Delta table:")
print(df_read.head())

print("\nTotal number of records:", len(df_read))