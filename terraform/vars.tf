variable "AWS_REGION" {
  default = "ap-southeast-1"
}

## Lambda deployment package name
variable "lambda_deployment_package" {
  default = "empty-deployment-package.zip"
}

variable "lambda_stage" {
  default = "prod"
}




