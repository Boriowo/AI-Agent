resource "aws_s3_bucket" "cloudful001" {
  bucket = "${var.name}-${var.environment}-cai-001"

  website {
    index_document = "index.html"
    error_document = "index.html"
  }
  tags = {
    Name        = "${var.name}-${var.environment}"
    Environment = "${var.environment}"
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-role-tst-statefile"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole" 
        Principal = {
          Service = "lambda.amazonaws.com" 
        }
      }
    ]
  })
}

resource "aws_lambda_function" "CAI001" {
  function_name = "${var.name}-${var.environment}-Ibd-01"
  s3_bucket     = aws_s3_bucket.CAI.bucket
  s3_key        = aws_s3_bucket_object.lambda_package.key
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_role.arn
  memory_size   = 5120

  ephemeral_storage {
    size = 5024
  }

  timeout = 900
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
  backend "s3" {
    bucket = "cloudful-statefile-test-s3-01"
    key    = "terraform.tfstate"
    region = "us-east-2"
  }
}

provider "aws" {
  region = var.region
}

variable "name" {
  type        = string
  description = "The Name of the VPC Tag"
  default     = "cloudful-statefile"
}

variable "environment" {
  type        = string
  description = "The Environmnet of the Resource"
  default     = "test"
}
ccc
variable "region" {
  type        = string
  description = "Region of Deployment"
  default     = "us-east-2"
}