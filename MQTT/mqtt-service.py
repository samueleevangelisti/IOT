import json
import paho.mqtt.client as mqtt

config = json.load('./mqtt-service-config.json')

def on_connect(client, userdata, flags, rc):
  print('Connected with result code ' + str(rc))
  client.subscribe(config['topic'])

def on_message(client, userdata, msg):
  print('{:s} {}'.format(msg.topic, msg.payload.decode()))

client = mqtt.Client()
client.username_pw_set(config['user'], config['password'])
client.on_connect = on_connect
client.on_message = on_message

client.connect(config['server'], 1883, 60)

client.loop_forever()
