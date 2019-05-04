var Docker = require("dockerode");
var docker = new Docker({socketPath: '/var/run/docker.sock'});
const axios = require('axios');
var ONE_SEC_IN_MS = 1000;
var g_containersList = {};
var g_number_of_active_containers = 0;

var g_host_ip = "http://127.0.0.1";

var next_request_handler_index = 0;

var f_counter = 0;
function listContainerCB(containersInfo) {
    var containersList =  containersInfo;

    if(containersList){
       var containers = containersList.container;
       if(containers){
           g_containersList = containersInfo;
           g_number_of_active_containers = containers.length;
           containers.forEach(function (containerInfo, index) {
                var url = "http://127.0.0.1:"+containerInfo.port+"/api/v1/_health";
                axios.get(url)
                    .then(resp =>{
                        //console.log("host: http://127.0.0.1:"+containerInfo.port+" | health resp: "+resp.status);
                        //donot do anything
                    })
                    .catch(err => {

                       // console.log("port: ",containerInfo.port," resp:",err.response.status);
                        if(err && err.response && err.response.status === 500){
                            // restart container
                         //   console.log("host: http://127.0.0.1:"+containerInfo.port+ " | health resp: "+err.response.status);
                            g_containersList.container.splice(index,1);
                            g_number_of_active_containers = containers.length;
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
    // if(f_counter == 10){
    //      let port = 8002;
    //      runContainer(port.toString());
    //  }
    // if(f_counter == 20){
    //      let port = 8003;
    //      runContainer(port.toString());
    //  }
    //
    //  if(f_counter == 25){
    //     console.log("containerslist : ",JSON.stringify(g_containersList));
    //  }
}


/*
*
*   Public Functions
* */
function init(debug_value) {
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
    return g_containersList;
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
            dataJson.container.unshift(contObj);
		});
	    if(typeof callback == "function")
	        callback(dataJson);
	    else
	        formContainersList(dataJson);
  });

}

function getHostUrl(){
    if(next_request_handler_index > (g_number_of_active_containers - 1))
        next_request_handler_index = 0;

    if(g_number_of_active_containers){
        let host = g_host_ip + ":" + g_containersList.container[next_request_handler_index].port;
        next_request_handler_index++;

        return host;
    }

}

module.exports.init = init;
module.exports.runContainer = runContainer;
module.exports.listContainers = listContainers;
module.exports.getContainers = getContainers;
module.exports.getHostUrl = getHostUrl;
