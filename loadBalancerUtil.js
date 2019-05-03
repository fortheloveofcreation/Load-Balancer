var containerUtil = require('./containerUtil');
var apiCounter = 0;



function init() {
  setInterval(healthCheck, ONE_SEC_IN_MS);
}

module.exports.init = init;
