terraform {
  backend "s3" {
    region = "ap-southeast-1"
  }
}

provider "aws" {
  version = "~> 2.0"
  region  = "${var.AWS_REGION}"
}


data "terraform_remote_state" "remote" {
  backend = "s3"

  config {
    bucket = "david-terraform-bucket"
    key    = "vpc-terraform/terraform.tfstate"
    region = "${var.AWS_REGION}"
  }
}