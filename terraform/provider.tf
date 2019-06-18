terraform {
  backend "s3" {
    region = "ap-southeast-1"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = "${var.AWS_REGION}"
}