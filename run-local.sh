#!/bin/bash

APPTABLE_NAME=$(aws dynamodb list-tables --query TableNames[0] --output text)
AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}
echo "Table Name: $APPTABLE_NAME"
echo "Region: $AWS_DEFAULT_REGION"
cd src
docker build -t cli-workshop-svc .
docker run -e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION -e APPTABLE_NAME=$APPTABLE_NAME -p 8080:5000 cli-workshop-svc
