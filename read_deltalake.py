# dataset_id = "abcd"
# url = f"abfss://<account_name>@<storage_account_name>.dfs.core.windows.net/{dataset_id}"
# storage_options = {
#     "account_url": f"https://<storage_account_name>.dfs.core.windows.net/",
#     "client_id": "client_id"
# }

# from deltalake import DeltaTable
# from deltalake.exceptions import DeltaError

# try:
#     # First attempt with default settings
#     dataframe = DeltaTable(url, storage_options=storage_options)
#     df = dataframe.to_pandas()
# except DeltaError as e:
#     if "deletionVectors" in str(e):
#         # If error is about deletionVectors, try with without_deletion_vectors=True
#         dataframe = DeltaTable(url, storage_options=storage_options, without_deletion_vectors=True)
#         df = dataframe.to_pandas()
#     else:
#         raise e


from deltalake import DeltaTable
dt = DeltaTable("/root/projects/conda-setup/spark_delta_table")

# df = dt.to_pandas()
# print(df)
metadata = dt.metadata()
configuration = metadata.configuration

print("configuration")
print(configuration)

print("metadata")
print(metadata)

df = dt.to_pandas()
print(df)