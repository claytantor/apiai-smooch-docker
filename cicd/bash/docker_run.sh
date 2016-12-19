#!/bin/bash

# where the application config dir should be mounted
export CONFIG_DIR=$1

#docker run -p host:exposed my-image
docker run -t -d --name apiai-smooch-docker -v ${CONFIG_DIR}:/mnt/config -p 8079:8079 claytantor/apiai-smooch-docker:latest
