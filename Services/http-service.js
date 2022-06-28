const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');
const influx = require('./influx');

const  config = JSON.parse(fs.readFileSync(path.join(__dirname, '../HTTP/http-service.json'), 'utf-8'));

app.use(express.json());

app.post('/send', (req, res) => {
  console.log(`[LOG ]\n${JSON.stringify(req.body, null, 2)}`);
  influx.writeSensor(req.body);
  res.send({
    success: true
  });
});

app.listen(config.port, () => {
  console.log(`[LOG ] port ${config.port}`);
});
