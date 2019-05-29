variable "AWS_ACCOUNT" {
  default = "00000000"
}

variable "AWS_REGION" {
  default = "us-east-1"
}

## For Put Lambda deployment package
variable "lambda_s3_bucket_name" {
  default = "default-bucket"
}

## Lambda deployment package name
variable "lambda_deployment_package" {
  default = "empty-deployment-package.zip"
}

variable "lambda_stage" {
  default = "prod"
}

variable "sqs_name" {
  default = "default-queue"
}



