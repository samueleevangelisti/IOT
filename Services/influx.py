from os import path
import json
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class Influx:
    def __init__(self):
        f = open(path.abspath(path.join(path.dirname(__file__), '../Influx/influx-config.json')), 'r')
        self.config = json.load(f)
        f.close()
        self.client = InfluxDBClient(url=self.config['url'], token=self.config['token'], org=self.config['organization'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()

    def write_weather(self, point_dict):
        print('INFLUX -> [WAIT] write weather')
        try:
            self.write_api.write(bucket=self.config['bucket']['weather'], org=self.config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write weather')
        except:
            print('INFLUX -> [ERR ] write weather')

    def write_forecasting_arima(self, point_dict):
        print('INFLUX -> [WAIT] write forecasting arima')
        try:
            self.write_api.write(bucket=self.config['bucket']['forecasting']['arima'], org=self.config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write forecasting arima')
        except:
            print('INFLUX -> [ERR ] write forecasting arima')

    def write_forecasting_prohpet(self, point_dict):
        print('INFLUX -> [WAIT] write forecasting prophet')
        try:
            self.write_api.write(bucket=self.config['bucket']['forecasting']['prophet'], org=self.config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write forecasting prophet')
        except:
            print('INFLUX -> [ERR ] write forecasting prophet')

    def delete_forecasting_arima_all(self):
        print('INFLUX -> [WAIT] delete forecasting arima')
        try:
            self.delete_api.delete('1970-01-01T00:00:00Z', (datetime.now() + timedelta(days=365)).timestamp() * 1000000000, bucket=self.config['bucket']['forecasting']['arima'], org=self.config['organization'])
            print('INFLUX -> [OK  ] delete forecasting arima')
        except Exception as e:
            print('INFLUX -> [ERR ] delete forecasting arima')
            print(e)
        