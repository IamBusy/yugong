#!/usr/bin/env bash
contName=$1
docker stop ${contName};
docker rm ${contName};
docker build -t yugong-${contName} .
docker run --name ${contName} -d -e "app=${contName}"  yugong-${contName}