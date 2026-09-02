output "instance_public_ip" {
  value       = aws_instance.tradeguard.public_ip
  description = "The public IP address of the EC2 instance"
}

output "db_endpoint" {
  value       = aws_db_instance.database.endpoint
  description = "The connection endpoint for the RDS database"
}