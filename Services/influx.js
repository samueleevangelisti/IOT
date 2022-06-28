const fs = require('fs');
const {InfluxDB, Point} = require('@influxdata/influxdb-client');

const config = JSON.parse(fs.readFileSync('../Influx/influx-config.json', 'utf-8'));

module.exports = {
  _config: config,
  _influxdb: new InfluxDB({
    url: config.url,
    token: config.token
  }),
  writeSensor: function(pointObj) {
    return new Promise((resolve, reject) => {
      console.log('INFLUX -> [WAIT] write sensor')
      let point = new Point(pointObj.measurement)
        .tag('id', pointObj.tags.id)
        .tag('latitude', pointObj.tags.latitude)
        .tag('longitude', pointObj.tags.longitude)
        .intField('rssi', pointObj.fields.rssi)
        .floatField('temperature', pointObj.fields.temperature)
        .floatField('humidity', pointObj.fields.humidity)
        .intField('gas', pointObj.fields.gas)
        .intField('aqi', pointObj.fields.aqi);
      const writeApi = this._influxdb.getWriteApi(config.organization, this._config.bucket.sensor);
      writeApi.writePoint(point);
      writeApi.close()
        .then((result) => {
          console.log('INFLUX -> [OK  ] write sensor');
          resolve(result);
        })
        .catch((error) => {
          console.log('INFLUX -> [ERR ] write sensor');
          reject(error);
        });
      });
  }
};
