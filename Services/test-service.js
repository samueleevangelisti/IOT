const axios = require('axios').default;
const ip = require('ip');

axios.post('http://192.168.1.4/subscribe', {
  url: `https://${ip.address()}:8080/observe`
})
  .then((response) => {
    console.log('[RESPONSE] ', response);
    debugger;
  })
  .catch((error) => {
    console.log(`[ERROR] ${error}`);
  });
