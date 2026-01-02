from config import get_datasource

ds = get_datasource()

print("data source loaded:", ds['class'])
print("base URL", ds['base_url'])
print("api key", ds['api_key'][:4] + "..." )
print("coverage keys:", list(ds['coverage'].keys()))