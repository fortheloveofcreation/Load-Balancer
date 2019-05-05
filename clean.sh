#! /bin/bash

docker stop $(docker ps -a)
docker rm $(docker ps -a)
rm -fr db/*

