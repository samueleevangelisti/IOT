const fs = require('fs');
const path = require('path');
const {InfluxDB, Point} = require('@influxdata/influxdb-client');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, '../Influx/influx-config.json'), 'utf-8'));

module.exports = {
  _config: config,
  _influxdb: new InfluxDB({
    url: config.url,
    token: config.token
  }),
  writeSensor: function(dataStr) {
    console.log('INFLUX -> [WAIT] write sensor');
    try {
      let dataArr = dataStr.split('|');
      let point = new Point('sensor')
        .tag('id', dataArr[0])
        .tag('latitude', dataArr[1])
        .tag('longitude', dataArr[2])
        .intField('rssi', dataArr[3])
        .floatField('temperature', dataArr[4])
        .floatField('humidity', dataArr[5])
        .intField('gas', dataArr[6])
        .intField('aqi', dataArr[7]);
      const writeApi = this._influxdb.getWriteApi(config.organization, this._config.bucket.sensor);
      writeApi.writePoint(point);
      writeApi.close()
        .then((result) => {
          console.log('INFLUX -> [OK  ] write sensor');
        })
        .catch((error) => {
          console.log('INFLUX -> [ERR ] write sensor');
        });
    } catch(error) {
      console.log('INFLUX -> [ERR ] write sensor');
    }
  }
};
