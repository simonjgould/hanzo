#!/usr/bin/env bash
image_tag=$1
account_id=$2

echo "for image ${image_tag} to account ${account_id}"

echo "this doesnt actually deploy anything but is a description of the process"
echo "determine the account to deploy to: e.g. the AWS account ID number, this will be a param and set by the orchestration pipeline, default is always dev account"
echo "first get the existing infrastructure: e.g. RDS and VPC via reading stack outputs"
echo "deploy the infrastructure: Terraform/Cloudformation by preference as these are more atomic than config managemnt tools such as ansible"
echo "micro-services should register with service mesh or be accessed via LB or serverless mechanisms that allow for appropriate horizontal scaling"
