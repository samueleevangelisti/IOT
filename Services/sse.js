module.exports = {
  res: null,
  init: function(res) {
    this.res = res;
    this.res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });
  },
  send: function(object) {
    if(this.res != null) {
      this.res.write(`data: ${JSON.stringify(object)}\n\n`);
    }
  },
  sendEvent: function(event, data) {
    this.send({
      event: event,
      data: data
    });
  },
  close: function() {
    this.res = null;
  }
};
