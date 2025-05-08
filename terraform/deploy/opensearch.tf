resource "aws_security_group" "es" {
  name   = "${local.prefix}-es-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 9200
    to_port         = 9200
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs_service.id] # allow ECS only
  }

}


resource "aws_opensearch_domain" "es" {
  domain_name    = "${local.prefix}-es"
  engine_version = "OpenSearch_2.11"
  cluster_config {
    instance_type          = "t3.small.search"
    instance_count         = 1
    zone_awareness_enabled = false # Set true for real production
  }
  # Storage
  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp3"
  }

  vpc_options {
    subnet_ids = [
      aws_subnet.private[0].id,
      aws_subnet.private[1].id,
    ]
    security_group_ids = [aws_security_group.es.id]
  }

  access_policies = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          AWS = aws_iam_role.app_task.arn
        },
        Action   = "es:*",
        Resource = "arn:aws:es:${data.aws_region.current}:${data.aws_caller_identity.current.account_id}:domain/${local.prefix}-es/*"
      }
    ]
  })
}