const express = require('express');
const app = express();
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const axios = require('axios').default;
const ip = require('ip');

const sse = require('./sse');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, '../Dashboard/dashboard-service-config.json'), 'utf-8'));

app.use(express.static(config.client));
app.use(cors());
app.use(express.json());

// let [isCommand, command, value] = process.argv.slice(2);

// if(isCommand == 'cmd') {
//   switch(command) {
//     case 'iotfind':
//       let count = 0;
//       for(let i = 1; i < 255; i++) {
//         axios.get(`http://192.168.1.${i}/iotfind`)
//           .then((response) => {
//             console.log(`[OK  ] ${JSON.stringify(response.data)} ${++count}`);
//             if(count == 254) {
//               process.exit(0);
//             }
//           })
//           .catch((error) => {
//             console.log(`[ERR ] ${error.message} ${++count}`);
//             if(count == 254) {
//               process.exit(0);
//             }
//           });
//       }
//       break;
//     case 'subscribe':
//       axios.post('http://192.168.1.4/subscribe', {
//         url: `http://${ip.address()}:8080/send`
//       })
//         .then((response) => {
//           console.log('[RESPONSE] ', response.data);
//         })
//         .catch((error) => {
//           console.log(`[ERROR] ${error}`);
//         })
//         .finally(() => {
//           process.exit(0);
//         });
//       break;
//     case 'protocol':
//       axios.post('http://192.168.1.4/protocol', {
//         protocol: value
//       })
//         .then((response) => {
//           console.log('[RESPONSE] ', response.data);
//         })
//         .catch((error) => {
//           console.log(`[ERROR] ${error}`);
//         })
//         .finally(() => {
//           process.exit(0);
//         });
//       break;
//   }
// }

app.get('/sse', (req, res) => {
  console.log('[LOG ] GET /sse');
  sse.init(res);
  sse.sendEvent('connect', true);
});

app.post('/iotfind', (req, res) => {
  console.log(`[LOG ] POST /iotfind\n${req.body}`);
  sse.sendEvent('iotfind-request', true);
  let count = 0;
  let maxCount = req.body.addressArr.length;
  req.body.addressArr.forEach((address) => {
    if(address != ip.address()) {
      axios.get(`http://${address}/iotfind`)
        .then((response) => {
          count++;
          if(response.data.success) {
            console.log(`[OK  ] ${JSON.stringify(response.data)} ${count}/${maxCount}`);
            sse.sendEvent('iotfind-data', {
              success: true,
              count: count,
              maxCount: maxCount,
              data: {
                ip: response.data.ip,
                port: response.data.port
              }
            });
          } else {
            console.log(`[ERR ] ${JSON.stringify(response.data)} ${count}/${maxCount}`);
            sse.sendEvent('iotfind-data', {
              success: false,
              count: count,
              maxCount: maxCount,
              data: {
                ip: response.data.ip,
                port: response.data.port
              }
            });
          }
          if(count == maxCount) {
            sse.sendEvent('iotfind-request', false);
          }
        })
        .catch((error) => {
          count++;
          console.log(`[ERR ] ${error.message} ${count}/${maxCount}`);
          sse.sendEvent('iotfind-data', {
            success: false,
            count: count,
            maxCount: maxCount
          });
          if(count == maxCount) {
            sse.sendEvent('iotfind-request', false);
          }
        });
    } else {
      maxCount--;
      sse.sendEvent('iotfind-data', {
        success: false,
        count: count,
        maxCount: maxCount
      });
    }
  });
  res.send({
    success: true
  });
});

app.post('/getdashboard', (req, res) => {
  console.log(`[LOG ] POST /getdashboard\n${JSON.stringify(req.body, null, 2)}`)
  axios.get(req.body.url)
    .then((response) => {
      console.log(`[OK  ]\n${JSON.stringify(response.data, null, 2)}`);
      res.send(response.data);
    })
    .catch((error) => {
      console.log(`[ERR ]\n${error.message}`);
      res.send(error.error);
    })
});

app.post('/subscribe', (req, res) => {
  axios.post(req.body.deviceUrl, {
    url: req.body.subscribeUrl
  })
    .then((response) => {
      res.send(response.data);
    })
    .catch((error) => {
      res.send(error.message);
    });
});

app.listen(config.port, () => {
  console.log(`[LOG ] listen on port ${config.port}`);
});
