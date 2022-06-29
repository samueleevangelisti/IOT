const fs = require('fs');
const path = require('path');
const mqtt = require('mqtt');
const influx = require('./influx');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, '../MQTT/mqtt-service-config.json'), 'utf-8'));

const client  = mqtt.connect(config.url, {
  username: config.user,
  password: config.password,
  clientId: config.id,
  reconnectPeriod: 2000
});

client.on('connect', (response) => {
  console.log('[OK  ] connection')
  console.log('[WAIT] subscribe');
  client.subscribe(config.topic, (err) => {
    if(err) {
      console.log('[ERR ] subscribe');
    } else {
      console.log('[OK  ] subscribe');
    }
  });
});

client.on('message', (topic, message) => {
  let dataStr = message.toString();
  console.log(`[LOG ] ${dataStr}`);
  influx.writeSensor(dataStr);
});

client.on('error', (error) => {
  console.log(`[ERR ] connection -> ${error.message}`);
});

console.log('[WAIT] connection');
