
resource "aws_security_group" "redis" {
  name   = "${local.prefix}-redis-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service.id]
  }
}


resource "aws_elasticache_subnet_group" "redis" {
  name = "${local.prefix}-redis-subnet-group"
  subnet_ids = [
    aws_subnet.private[0].id,
    aws_subnet.private[1].id,
  ]
}

resource "aws_elasticache_replication_group" "redis" {
  replication_group_id = "my-redis"
  description          = "Redis for Django + Celery"
  node_type            = "cache.t3.small"
  num_node_groups      = 1

  replicas_per_node_group    = 0
  automatic_failover_enabled = false # set true if multi-AZ

  engine         = "redis"
  engine_version = "7.1"
  port           = 6379

  subnet_group_name  = aws_elasticache_subnet_group.redis.name
  security_group_ids = [aws_security_group.redis.id]
}