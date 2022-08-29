const express = require('express');
const app = express();
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const axios = require('axios').default;
const chromeLauncher = require('chrome-launcher');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, '../Dashboard/dashboard-service-config.json'), 'utf-8'));

app.use(express.static(path.join(__dirname, config.client)));
app.use(cors());
app.use(express.json());

app.post('/proxy', (req, res) => {
  console.log(`[LOG ] POST /proxy\n${JSON.stringify(req.body, null, 2)}`);
  switch(req.body.method) {
    case 'GET':
      axios.get(req.body.url)
        .then((response) => {
          console.log(`[OK  ]\n${JSON.stringify(response.data, null, 2)}`);
          res.send(response.data);
        })
        .catch((error) => {
          console.log(`[ERR ]\n${error.message}`);
          res.send(error);
        });
      break;
    case 'POST':
      axios.post(req.body.url, req.body.body)
        .then((response) => {
          console.log(`[OK  ]\n${JSON.stringify(response.data, null, 2)}`);
          res.send(response.data);
        })
        .catch((error) => {
          console.log(`[ERR ]\n${error.message}`);
          res.send(error);
        });
      break;
    default:
      break;
  }
});

app.listen(config.port, () => {
  console.log(`[LOG ] listen on port ${config.port}`);
  if(process.argv[2] != 'no-autostart') {
    chromeLauncher.launch({
      startingUrl: '--app=http://localhost:8081',
      chromeFlags: ['--start-maximized']
    })
      .then((chrome) => {
        chrome.process.on('exit', () => {
          process.exit(0);
        });
      });
  }
});
