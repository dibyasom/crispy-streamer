#!/bin/bash

if (docker volume ls | grep "crispy-streamer_shared-source-code")
then
    echo "Found, removing." 
    docker rm $(docker ps -aq) 
    docker volume rm crispy-streamer_shared-source-code
else
    echo "Not Found"
fi

docker-compose up