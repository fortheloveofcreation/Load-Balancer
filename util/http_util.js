const axios = require('axios');
const qs = require('qs');

function makeGetReq(hostUrl,requestObj, responseObj, callback) {
    let url = hostUrl + request.url;
    axios.get(url)
    .then(resp =>{
        callback(responseObj,requestObj, resp);
    })
    .catch(err => {
        console.log("err",err);
        responseObj.sendStatus(404);
    });
}

function makePostReq(hostUrl,request, responseObj, callback) {
    let url = hostUrl + request.url;
    console.log("url",request.body);
    axios.post(url, qs.stringify(request.body))
    .then(resp =>{
       responseObj.sendStatus(201);
    })
    .catch(err => {
        console.log("err",err);
        responseObj.sendStatus(400);
    });
}

function makeDelReq(hostUrl,request, responseObj, callback) {
    let url = hostUrl + request.url;
    axios.delete(url)
    .then(resp =>{
       responseObj.sendStatus(200);
    })
    .catch(err => {
        console.log("err",err);
        responseObj.sendStatus(400);
    });
}

function makeRequest(hostUrl,request, responseObj, callback) {
    if(request.method === "GET") {
        makeGetReq(hostUrl,request,responseObj, callback)
    }
    else if(request.method === "POST")
        makePostReq(hostUrl,request,responseObj, callback);
    else if(request.method === "DELETE")
        makeDelReq();
    else
        console.log("options req ?");
}


module.exports.makeRequest = makeRequest;
