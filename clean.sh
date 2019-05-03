#! /bin/bash

docker stop $(docker ps)
docker rm $(docker ps)
