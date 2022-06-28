
const coap = require('coap')
const req = coap.request('coap://'+'192.168.1.213'+'/DATA')

req.on('response', (res) => {
    res.pipe(process.stdout)
})

req.end()