const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');
const influx = require('./influx');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, '../HTTP/http-service-config.json'), 'utf-8'));

app.use(express.json());

app.post('/send', (req, res) => {
  let dataStr = req.body.data;
  console.log(`[LOG ] ${dataStr}`);
  influx.writeSensor(dataStr);
  res.send({
    success: true
  });
});

app.listen(config.port, () => {
  console.log(`[LOG ] listening on port ${config.port}`);
});
