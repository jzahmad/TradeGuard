resource "aws_instance" "tradeguard" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = data.aws_subnets.default.ids[0]
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  key_name               = var.key_name

  user_data              = file("${path.module}/deploy.sh")
  tags = { Name = "TradeGuard" }
}