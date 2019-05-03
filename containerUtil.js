var Docker = require("dockerode");
const axios = require('axios');
var fs = require('fs');

var docker = new Docker({socketPath: '/var/run/docker.sock'});
var list = require("./containers.json");

var ONE_SEC_IN_MS = 1000;
var g_containersList = {};

var f_counter = 0;


function listContainerCB(containersInfo) {
    var containersList =  containersInfo;
    g_containersList = containersInfo;
    if(containersList){
       var containers = containersList.container;
       if(containers){
           containers.forEach(function (containerInfo) {
                var url = "http://127.0.0.1:"+containerInfo.port+"/api/v1/_health";
                axios.get(url)
                    .then(resp =>{
                        console.log("host: http://127.0.0.1:"+containerInfo.port+" | health resp: "+resp.status);
                        //donot do anything
                    })
                    .catch(err => {

                       // console.log("port: ",containerInfo.port," resp:",err.response.status);
                        if(err && err.response && err.response.status === 500){
                            // restart container
                            console.log("host: http://127.0.0.1:"+containerInfo.port+ " | health resp: "+err.response.status);
                            stopContainer(containerInfo.id,containerInfo.port);
                            //docker.getContainer(containerInfo.id).stop(dummyCB);
                        }
                    });
            });
        }
    }
}

function healthCheck(){
    f_counter++;
    listContainers(listContainerCB);
    if(f_counter == 10){
        let port = 8002;
        runContainer(port.toString());
    }
}


/*
*
*   Public Functions
* */
function init() {
    setInterval(healthCheck,ONE_SEC_IN_MS);
}

function stopContainer(id,port) {
    var that = this;
    this.containerStopCB = function () {
        runContainer(port.toString());
    };

    docker.getContainer(id).stop(this.containerStopCB);
}

function runContainer(port){
	var createOptions = {
    			Image:"acts",
    			Tty:true,
   			 ExposedPorts: {
        			"5000/tcp:": {},
    				},
    		HostConfig:{
        		PortBindings: {
            			"5000/tcp": [{
                			"HostIP":"0.0.0.0",
                			"HostPort": port
            			}],
        		},
    		},
	};

	docker.createContainer(createOptions, function(err, result){
		var container = docker.getContainer(result.id);

		container.start(function(err, data){
			if(err) console.log(err);
		});

	});
}

function getContainers(){
    return containersList;
}

function formContainersList(dataJson){
    g_containersList = dataJson;
}

function listContainers(callback){
    var dataJson = {
        container:[]
    };
	docker.listContainers(function (err, containers) {
	    containers.forEach(function (containerInfo) {
	        //console.log("containerInfo: ",containerInfo);
            let contObj = {
                "id":containerInfo.Id,
                "port":containerInfo.Ports[1].PublicPort ? containerInfo.Ports[1].PublicPort : containerInfo.Ports[0].PublicPort,
                "isRunning":true
            };
            //console.log("publicPort: ",containerInfo.Ports[1].PublicPort);
            dataJson.container.push(contObj);
		});
	    if(typeof callback == "function")
	        callback(dataJson);
	    else
	        formContainersList(dataJson);
  });

}

module.exports.init = init;
module.exports.runContainer = runContainer;
module.exports.listContainers = listContainers;
module.exports.getContainers = getContainers;
