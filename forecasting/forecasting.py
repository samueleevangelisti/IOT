from datetime import tzinfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = 'IoT-sensor'
org = 'IoT'
token = '5XSTceUB8mbuFxUkS5RgqZiQ2nStsdyPiFSX5pbxBNxUS5COqT-t5bhxTxk7v6cDzvRMvH6P1a0ywgVIr31M_g=='
# Store the URL of your InfluxDB instance
url='http://localhost:8086'
client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)
query_api = client.query_api()
query = 'from(bucket: "IoT-sensor")\
  |> range(start:-10m)\
  |> filter(fn: (r) => r["_measurement"] == "sensor")\
  |> filter(fn: (r) => r["_field"] == "temperature")'

result = client.query_api().query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        results.append((record.get_time(), record.get_field(), record.get_value()))

print(results)