variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "ami" {
  type        = string
  default     = "ami-081b0a6eac00b4f53"
  description = "The Linux Machine for EC2"
}

variable "instance_type" {
  type        = string
  default     = "t3.micro"
  description = "The type of EC2 instance"
}

data "http" "my_ip" {
  url = "https://api.ipify.org"
}

variable "ssh_allowed_cidr" {
  type        = string
  description = "CIDR block allowed to SSH into the EC2 instance"
  default     = null
}

locals {
  ssh_allowed_cidr = coalesce(var.ssh_allowed_cidr, "${chomp(data.http.my_ip.response_body)}/32")
}

variable "key_name" {
  type        = string
  description = "Existing AWS EC2 key pair name"

  default = "temp_12"
}

variable "db_username" {
  type        = string
  default     = "admin1"
  description = "RDS mysql master username"
}

variable "db_password" {
  sensitive = true
}