/* External Libraries */
const express = require('express');

const http = require('http');
const app = express();
var bodyParser = require('body-parser');
var DEBUG = true;
/* Internal Libraries */
var containerUtil = require('./containerUtil');
var loadBalancerUtil = require('./loadBalancerUtil');

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded
/* Globals */
const ecExposedPort = 80;

/*
*
*  FUNCTIONS
*
*/

/* Run a intial/first container on port 8000 */
function init(){
    var port = 8000;
    containerUtil.runContainer(port.toString());
    containerUtil.init();

    setTimeout(containerUtil.listContainers, 2000);
}


function routeToContainer(request, response){
   // console.log("<request> ",request.method, "url: ",request.body);
    loadBalancerUtil.handleRequest(request, response);
}

app.get('/', function (req, res) {
   res.sendFile( __dirname+"/index.html");
});

app.get('/api/v1/users/',routeToContainer);
app.post('/api/v1/users/*',routeToContainer);
app.post('/api/v1/users',routeToContainer);

app.get('/api/v1/acts/*',routeToContainer);
app.post('/api/v1/acts',routeToContainer);

app.get('/api/v1/categories/*',routeToContainer);
app.post('/api/v1/categories/*',routeToContainer);
app.post('/api/v1/categories',routeToContainer);

app.listen(ecExposedPort, function () {
    init();
    console.log('Server Running on port '+ ecExposedPort);
});

process.argv.forEach(function (val, index, array) {
  console.log(index + ': ' + val);
});

process.env.NODE_DEBUG = 'net';

