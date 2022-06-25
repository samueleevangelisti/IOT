from os import path
import json
from datetime import datetime
from time import sleep
import paho.mqtt.client as mqtt
from influx import Influx

influx = Influx()

f = open(path.abspath(path.join(path.dirname(__file__), '../MQTT/mqtt-service-config.json')), 'r')
config = json.load(f)
f.close()

def on_connect(client, userdata, flags, rc):
  print('[OK  ] connected with result code {:d}'.format(rc))
  client.subscribe(config['topic'])

def on_message(client, userdata, msg):
  data_dict = json.loads(msg.payload.decode())
  print('[LOG ]\n{:s}'.format(json.dumps(data_dict, indent=2)))
  influx.write_sensor(data_dict)

client = mqtt.Client(client_id="mqtt_service_eva")
client.username_pw_set(config['user'], config['password'])
client.on_connect = on_connect
client.on_message = on_message

connected = False
while not connected:
  try:
    print('[WAIT] connecting')
    client.connect(config['server'], 1883, 60)
    connected = True
  except:
    pass
  sleep(1)

client.loop_forever()
