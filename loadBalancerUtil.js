const axios = require('axios');
var containerUtil = require('./containerUtil');
var http_util = require('./util/http_util');
var timerHandler = undefined;
var apiCounter = 0;
var firstRequest = true;
var TWO_MIN_IN_MSEC = 2 * 60 * 1000;


function httpCallBack(responseObj, requestObj,apiResp){

      if(requestObj.method === "GET"){
          //console.log("resp ",apiResp.data);
          responseObj.send(apiResp.data);
      }
}

function loadBalancer() {
    console.log("loadbalancer called after every 2 min");
    firstRequest = true;
    let numberOfContainersTobeRun = Math.ceil(apiCounter/20);
    apiCounter = 0;
    containerUtil.runXnumberOfContainers(numberOfContainersTobeRun);
}

function handleRequest(request, response) {
    apiCounter++;
    console.log("handleRequest | apiCounter ",apiCounter);
    if(firstRequest){
        firstRequest = false;
        if(timerHandler)
            clearTimeout(timerHandler);
        console.log("handleRequest | firstReq made after 2/0 min");
        timerHandler = setTimeout(loadBalancer, TWO_MIN_IN_MSEC);// start timer for 2 min
    }

    var hostUrl = containerUtil.getHostUrl();
    //console.log("<loadBalancerUtil> url: "+url);
    http_util.makeRequest(hostUrl, request, response, httpCallBack);
    console.log("<loadBalancerUtil> url: "+hostUrl);
}


module.exports.handleRequest = handleRequest;
