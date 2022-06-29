const coap = require('coap');
const server = coap.createServer();
const influx = require('./influx');

server.on('request', (req, res) => {
  let dataStr = req.payload.toString();
  console.log(`[LOG ] ${dataStr}`);
  influx.writeSensor(dataStr);
});

server.listen(() => {
  console.log('[LOG ] listening on port 5683');
});
