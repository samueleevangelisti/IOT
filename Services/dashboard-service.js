const axios = require('axios').default;
const ip = require('ip');

let [command, value] = process.argv.slice(2);

switch(command) {
  case 'iotfind':
    let count = 0;
    for(let i = 1; i < 255; i++) {
      axios.get(`http://192.168.1.${i}/iotfind`)
        .then((response) => {
          console.log(`[OK  ] ${JSON.stringify(response.data)} ${++count}`);
        })
        .catch((error) => {
          console.log(`[ERR ] ${error.message} ${++count}`);
        });
    }
    break;
  case 'subscribe':
    axios.post('http://192.168.1.4/subscribe', {
      url: `http://${ip.address()}:8080/send`
    })
      .then((response) => {
        console.log('[RESPONSE] ', response.data);
      })
      .catch((error) => {
        console.log(`[ERROR] ${error}`);
      });
    break;
  case 'protocol':
    axios.post('http://192.168.1.4/protocol', {
      protocol: value
    })
      .then((response) => {
        console.log('[RESPONSE] ', response.data);
      })
      .catch((error) => {
        console.log(`[ERROR] ${error}`);
      });
    break;
}
