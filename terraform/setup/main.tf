terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.23.0"
    }
  }

  backend "s3" {
    bucket         = "devops-medium-api-tf-state-bucket"
    region         = "ap-northeast-1"
    key            = "tf-state-setup"
    encrypt        = true
    dynamodb_table = "devops-medium-api-tf-lock-table"
  }

}

provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = {
      Environment = terraform.workspace
      Project     = var.project
      Contact     = var.contact
      ManageBy    = "Terraform/setup"
    }
  }

}