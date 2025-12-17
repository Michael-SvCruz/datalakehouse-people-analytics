variable "aws_region" {
  description = "The AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for S3 bucket names"
  type        = string
  default     = "rh-182399721888"
}

variable "env" {
  description = "Ambiente (dev, prod)"
  type        = string
  default     = "dev"
}