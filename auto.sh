#!/bin/bash

docker build -t crisosilva88/api-to-rds:latest .

docker push crisosilva88/api-to-rds:latest

kubectl delete job fetch-api

kubectl apply -f k8s/api-to-rds-job.yml