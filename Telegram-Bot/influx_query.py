from datetime import tzinfo
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

org = 'IoT'
token = 'WOqKy-gIeRs9U-IlbEzZdLZcTZHpwPsx2NpibTGWbYFq_IuDZVEAcMZ1VtrYKnjFEjs2vsQJl6H2vvXvfClfPw=='
url='http://localhost:8086'

client = influxdb_client.InfluxDBClient(
   url=url,
   token=token,
   org=org
)

def fun_report(bucket):
  fun_query = 'from(bucket: {bucket})\
    |> range(start: -24h, stop: now())\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> aggregateWindow(every: 24h, fn: mean, createEmpty: false)\
    |> yield(name: "mean")'.format(bucket = bucket)

  fun_result = client.query_api().query(org=org, query=fun_query)

  df = []
  for table in fun_result:
      for record in table.records:
        if('00:00:00+00:00' not in str(record['_time'])): #La query influx ha un problema col fuso orario e salva i dati sia alle 00:00 che all'orario in cui la query è stata lanciata
          df.append(record.get_value())
  return df




def fun_sensor_filter(bucket, field):
  fun_query = 'from(bucket: {bucket})\
    |> range(start: -5m, stop: now())\
    |> filter(fn: (r) => r["_measurement"] == "sensor")\
    |> filter(fn: (r) => r["_field"] == {field})\
    |> aggregateWindow(every: 1w, fn: last, createEmpty: false)\
    |> yield(name: "last")'.format(bucket = bucket, field = field)

  fun_result = client.query_api().query(org=org, query=fun_query)

  for table in fun_result:
      for record in table.records:
        return record.get_value()
