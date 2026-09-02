terraform {
  backend "s3" {
    bucket       = "tradeguardcicdv"
    key          = "tradeguard/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}