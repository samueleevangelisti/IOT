from os import path
import json
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class Influx:
    def __init__(self):
        f = open(path.abspath(path.join(path.dirname(__file__), '../Influx/influx-config.json')), 'r')
        self.influx_config = json.load(f)
        f.close()
        f = open(path.abspath(path.join(path.dirname(__file__), '../Weather/weather-service-config.json')), 'r')
        self.weather_config = json.load(f)
        f.close()
        f = open(path.abspath(path.join(path.dirname(__file__), '../Forecasting/forecasting-service-config.json')), 'r')
        self.forecasting_config = json.load(f)
        f.close()
        self.client = InfluxDBClient(url=self.influx_config['url'], token=self.influx_config['token'], org=self.influx_config['organization'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()

    def write_weather(self, point_dict):
        print('INFLUX -> [WAIT] write weather')
        try:
            point_dict['measurement'] = self.influx_config['measurement']['weather']
            point_dict['tags'] = self.weather_config
            self.write_api.write(bucket=self.influx_config['bucket']['weather'], org=self.influx_config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write weather')
        except:
            print('INFLUX -> [ERR ] write weather')

    def write_forecasting_arima(self, point_dict):
        print('INFLUX -> [WAIT] write forecasting arima')
        try:
            point_dict['measurement'] = self.influx_config['measurement']['forecasting']['arima']
            point_dict['tags'] = self.forecasting_config
            self.write_api.write(bucket=self.influx_config['bucket']['sensor'], org=self.influx_config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write forecasting arima')
        except:
            print('INFLUX -> [ERR ] write forecasting arima')

    def write_forecasting_prophet(self, point_dict):
        print('INFLUX -> [WAIT] write forecasting prophet')
        try:
            point_dict['measurement'] = self.influx_config['measurement']['forecasting']['prophet']
            point_dict['tags'] = self.forecasting_config
            self.write_api.write(bucket=self.influx_config['bucket']['sensor'], org=self.influx_config['organization'], record=point_dict)
            print('INFLUX -> [OK  ] write forecasting prophet')
        except:
            print('INFLUX -> [ERR ] write forecasting prophet')

    def delete_forecasting_arima_all(self):
        print('INFLUX -> [WAIT] delete forecasting arima')
        try:
            self.delete_api.delete('1970-01-01T00:00:00Z', (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ'), '_measurement="{:s}"'.format(self.influx_config['measurement']['forecasting']['arima']), bucket=self.influx_config['bucket']['sensor'], org=self.influx_config['organization'])
            print('INFLUX -> [OK  ] delete forecasting arima')
        except Exception as e:
            print('INFLUX -> [ERR ] delete forecasting arima')
            print(e)

    def delete_forecasting_prophet_all(self):
        print('INFLUX -> [WAIT] delete forecasting prophet')
        try:
            self.delete_api.delete('1970-01-01T00:00:00Z', (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%dT%H:%M:%SZ'), '_measurement="{:s}"'.format(self.influx_config['measurement']['forecasting']['prophet']), bucket=self.influx_config['bucket']['sensor'], org=self.influx_config['organization'])
            print('INFLUX -> [OK  ] delete forecasting prophet')
        except Exception as e:
            print('INFLUX -> [ERR ] delete forecasting prophet')
            print(e)
        