const axios = require('axios');

function makeRequest(hostUrl,request, response, callback) {
    console.log("re method",request.method," reqUrl ",hostUrl+request.url);
    axios({
        method:request.method,
        url: hostUrl+request.url,
        responseType:'text/json'
    })
    .then(function(apiResp) {
        console.log("apiResp ",apiResp);
        if(typeof callback === 'function')
            callback(response,apiResp);
    })
    .catch(err => {

    // console.log("port: ",containerInfo.port," resp:",err.response.status);
    if(err && err.response && err.response.status === 500){
        // restart container
     //   console.log("host: http://127.0.0.1:"+containerInfo.port+ " | health resp: "+err.response.status);
       console.log("internal server error");
       callback(response,err);
    }
    });
}


module.exports.makeRequest = makeRequest;
