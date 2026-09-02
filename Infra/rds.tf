resource "aws_db_instance" "database" {
  identifier             = "tradeguard"
  engine                 = "mysql"
  instance_class         = "db.t3.micro"
  allocated_storage      = 20
  storage_encrypted      = false
  db_name                = "tradeguard"
  username               = var.db_username
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  publicly_accessible    = false
  skip_final_snapshot    = true

  tags = { Name = "TradeGuard" }
}