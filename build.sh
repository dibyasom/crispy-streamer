#!/bin/bash

if (docker volume ls | grep "crispy-streamer_shared-source-code")
then
    echo "Found, removing." 
    docker rm $(docker ps -aq) 
    docker volume rm $(docker volume ls -q)
else
    echo "Not Found"
fi

docker-compose build gcs-celery-worker stream-handle