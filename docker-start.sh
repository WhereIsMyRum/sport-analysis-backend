#!/bin/bash

docker-compose up -d

sleep 20

./mc config host add s3 http://s3.docker admin password
./mc mb s3/tennis-video-bucket-1

SQS=$(./mc admin info server s3 | grep SQS | cut -c12-)

while [ -z "$SQS" ]
do 
    docker-compose stop s3.docker
    docker-compose stop vidapp.internal
    docker-compose up -d s3.docker
    docker-compose up -d vidapp.internal
    sleep 5
    SQS=$(./mc admin info server s3 | grep SQS | cut -c12-)
done

./mc event add s3/tennis-video-bucket-1 $SQS

./mc event list s3/tennis-video-bucket-1