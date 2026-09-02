resource "aws_security_group" "app_sg" {
  name        = "tradeguard-app-sg"
  description = "Security group for TradeGuard EC2 instance and RDS access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH from trusted CIDR only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  ingress {
    description = "Postgres from within this security group"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "tradeguard-app-sg" }
}