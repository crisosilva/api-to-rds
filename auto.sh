#!/bin/bash

#kubectl apply -f k8s/api-to-rds-job.yml

kubectl delete job fetch-api

kubectl apply -f k8s/api-to-rds-job.yml