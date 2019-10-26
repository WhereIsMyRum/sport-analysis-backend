#!/bin/bash

docker-compose up -d

sleep 20

./mc.exe config host add s3 http://s3.docker admin password
./mc.exe mb s3/tennis-video-bucket-1

SQS=$(./mc.exe admin info server s3 | grep SQS | cut -c12-)

while [ -z "$SQS" ]
do 
    docker-compose stop s3.docker
    docker-compose stop msgdispatcher.internal
    docker-compose stop videoanalyzer.internal
    docker-compose stop videoformatter.internal
    docker-compose stop nginx
    docker-compose up -d s3.docker
    docker-compose up -d msgdispatcher.internal
    docker-compose up -d videoanalyzer.internal
    docker-compose up -d videoformatter.internal
    docker-compose up -d nginx
    sleep 5
    SQS=$(./mc.exe admin info server s3 | grep SQS | cut -c12-)
done

./mc.exe event add s3/tennis-video-bucket-1 $SQS

./mc.exe event list s3/tennis-video-bucket-1