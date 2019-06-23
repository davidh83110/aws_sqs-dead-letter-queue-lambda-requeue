terraform {
  backend "s3" {
    bucket = "terraform.default.bucket"
    key    = "dead-letter-queue-lambda/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = "${var.AWS_REGION}"
}