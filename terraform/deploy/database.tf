##
# Database
##

# DB subnet group
resource "aws_db_subnet_group" "main" {
  name = "${local.prefix}-main"
  subnet_ids = [
    aws_subnet.private[0].id,
    aws_subnet.private[1].id
  ]
  tags = {
    Name = "${local.prefix}-db-subnet-group"
  }
}

# Security group
resource "aws_security_group" "rds" {
  description = "Allow access to the database instance"
  name        = "${local.prefix}-rds-inbound-access"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol  = "tcp"
    from_port = 5432
    to_port   = 5432

    security_groups = [
      aws_security_group.ecs_service.id
    ]
  }

  tags = {
    Name = "${local.prefix}-db-security-group"
  }
}

resource "aws_db_instance" "main" {
  instance_class = "db.t4g.micro" # Server size, smallest

  identifier = "${local.prefix}-db"

  db_name  = "medium"
  username = var.db_username
  password = var.db_password

  allocated_storage = 20 # GB
  storage_type      = "gp3"

  engine                     = "postgres"
  engine_version             = "15.5"
  auto_minor_version_upgrade = true

  skip_final_snapshot     = true  # in real project, we do want a bakcup when destroy the db
  backup_retention_period = 0     # in real project, we want to a backup for a period of time
  multi_az                = false # in real project, enable this for resilence, but here we try to keep the cost low 
  # deletion_protection = true    # Uncommen it in produciton
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  tags = {
    Name = "${local.prefix}-rds-instance"
  }

}
