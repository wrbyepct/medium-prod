
##
# ECS cluster for running app on Fargate.
#
resource "aws_ecs_cluster" "main" {
  name = "${local.prefix}-ecs-cluster"
}

##
# Create one-time service linked role resources for ECS
# To perform registering your container IP in a target group
# Creating ENIs in your VPC/subnets
# Sending health check data to CloudWatch
##

resource "aws_iam_service_linked_role" "ecs" {
  aws_service_name = "ecs.amazonaws.com"
}

##
# Fargate gets permission role from IAM
##
resource "aws_iam_role" "ecs_execution_role" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = file("${path.module}/template/ecs/task-assume-role-policy.json")

}

##
# Fargate Task execution policy - Allow Fargate to pull images and run container
##
resource "aws_iam_role_policy" "ecs_execution_policy" {
  name   = "TaskExecutionPolicy"
  role   = aws_iam_role.ecs_execution_role.name
  policy = file("${path.module}/template/ecs/task-execution-policy.json")
}


##
# App task gets permission role from IAM
##
resource "aws_iam_role" "app_task" {
  name               = "ecsAPPTaskRole"
  assume_role_policy = file("${path.module}/template/ecs/task-assume-role-policy.json")

}

##
# Fargate Task Role Policy - Allow ECS task to use SES to sen mails
##

resource "aws_iam_role_policy" "ses_policy" {
  name = "SESPolicy"
  role = aws_iam_role.app_task.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "*"
      }
    ]
  })
}

##
# Fargate Task role policy - Allow connect to System Service Manager 
##
resource "aws_iam_role_policy" "ssm_policy" {
  name   = "SSMSessionPolicy"
  role   = aws_iam_role.app_task.name
  policy = file("${path.module}/template/ecs/ssm-role-policy.json")
}

resource "aws_iam_role_policy" "opensearch_access" {
  name = "OpenSearchAccess"
  role = aws_iam_role.app_task.name
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "es:ESHttpPut",
          "es:ESHttpPost",
          "es:ESHttpGet"
        ],
        Resource = "arn:aws:es:ap-northeast-1:${data.aws_caller_identity.current.account_id}:domain/${local.prefix}-es/*"
      }
    ]
  })
}


##
# CloudWatch log Group 
##
resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name = "${local.prefix}-log-group"

}

##
#  ECS Task definition
## 

resource "aws_ecs_task_definition" "api" {
  family                   = "${local.prefix}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([
    # API container
    {
      name              = "api"
      image             = var.ecr_repo_app_image
      essential         = true
      memoryReservation = 768
      command           = ["/start"]
      user              = "medium-api" # TODO: factor this out later

      environment = [
        {
          name  = "DJANGO_SECRET_KEY"
          value = var.django_secret_key
        },
        {
          name  = "DJANGO_ALLOWED_HOST"
          value = aws_route53_record.app.fqdn
        },
        {
          name  = "JWT_SIGNING_KEY"
          value = var.jwt_signing_key
        },
        {
          name  = "DJANGO_ADMIN_URL"
          value = var.django_admin_url
        },
        {
          name  = "DATABASE_URL"
          value = "postgresql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.address}:5432/${aws_db_instance.main.db_name}"
        },
        {
          name  = "CELERY_BROKER"
          value = "redis://${aws_elasticache_replication_group.redis.primary_endpoint_address}:6379/0"
        },
        {
          name  = "AWS_DEFAULT_REGION"
          value = data.aws_region.current.name
        },
        {
          name  = "ELASTICSEARCH_URL"
          value = aws_opensearch_domain.es.endpoint
        },
        {
          name  = "DOMAIN"
          value = aws_route53_record.app.fqdn
        },
        {
          name  = "ALB_HOST"
          value = aws_lb.api.dns_name
        },
        {
          name  = "CSRF_TRUSTED_ORIGINS"
          value = var.csrf_trusted_origins
        },
        {
          name  = "DJANGO_ALLOWED_HOSTS"
          value = var.django_allowed_hosts
        },
      ]
      mountPoints = [
        {
          readOnly      = false
          containerPath = "/vol/api/staticfiles"
          sourceVolume  = "static"
        },
        {
          readOnly      = false
          containerPath = "/vol/api/mediafiles"
          sourceVolume  = "efs-media"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "api"
        }
      }
    },
    # NGINX container
    {
      name              = "nginx"
      image             = var.ecr_repo_proxy_image
      essential         = true
      memoryReservation = 512
      user              = "nginx"

      portMappings = [
        {
          hostPort      = 8080
          containerPort = 8080
        }
      ]
      environment = [
        {
          name  = "API_HOST"
          value = "127.0.0.1"
        },
        {
          name  = "LISTEN_PORT"
          value = "8080"
        },
        {
          name  = "API_PORT"
          value = "8000"
        }
      ]
      mountPoints = [
        {
          readOnly      = true
          containerPath = "/vol/staticfiles/"
          sourceVolume  = "static"
        },
        {
          readOnly      = true
          containerPath = "/vol/mediafiles/"
          sourceVolume  = "efs-media"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "nginx"
        }

      }
    },
    # Celery
    {
      name              = "celery"
      image             = var.ecr_repo_app_image
      essential         = true
      memoryReservation = 768
      command           = ["celery", "-A", "core.celery", "worker", "--loglevel=info"]

      environment = [
        {
          name  = "DJANGO_SECRET_KEY"
          value = var.django_secret_key
        },
        {
          name  = "DJANGO_ALLOWED_HOST"
          value = aws_route53_record.app.fqdn
        },
        {
          name  = "JWT_SIGNING_KEY"
          value = var.jwt_signing_key
        },
        {
          name  = "DJANGO_ADMIN_URL"
          value = var.django_admin_url
        },
        {
          name  = "DATABASE_URL"
          value = "postgresql://${aws_db_instance.main.username}:${aws_db_instance.main.password}@${aws_db_instance.main.address}:5432/${aws_db_instance.main.db_name}"
        },
        {
          name  = "CELERY_BROKER"
          value = "redis://${aws_elasticache_replication_group.redis.primary_endpoint_address}:6379/0"
        },
        {
          name  = "AWS_DEFAULT_REGION"
          value = data.aws_region.current.name
        },
        {
          name  = "ELASTICSEARCH_URL"
          value = "https://${aws_opensearch_domain.es.endpoint}"
        },
        {
          name  = "DOMAIN"
          value = aws_route53_record.app.fqdn
        },
        {
          name  = "ALB_HOST"
          value = aws_lb.api.dns_name
        },
        {
          name  = "CSRF_TRUSTED_ORIGINS"
          value = var.csrf_trusted_origins
        },
        {
          name  = "DJANGO_ALLOWED_HOSTS"
          value = var.django_allowed_hosts
        },
      ]
      mountPoints = [
        {
          readOnly      = false
          containerPath = "/vol/api/staticfiles"
          sourceVolume  = "static"
        },
        {
          readOnly      = false
          containerPath = "/vol/api/mediafiles"
          sourceVolume  = "efs-media"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs.name
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "celery"
        }
      }
    },
  ])

  volume {
    name = "static"
  }

  volume {
    name = "efs-media"
    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.api.id
      transit_encryption = "ENABLED"

      authorization_config {
        access_point_id = aws_efs_access_point.media.id
        iam             = "DISABLED" # for kms decrypt in efs
      }
    }
  }


  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}


##
# ECs security group
##

resource "aws_security_group" "ecs_service" {
  description = "Access Rule for ECS"
  name        = "${local.prefix}-ecs-service"
  vpc_id      = aws_vpc.main.id

  # For client to connect into the api
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  # For ECS to access RDS
  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private[0].cidr_block,
      aws_subnet.private[1].cidr_block,
    ]
  }


  # For ECS to access EFS
  egress {
    from_port = 2049
    to_port   = 2049
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private[0].cidr_block,
      aws_subnet.private[1].cidr_block
    ]
  }

  # Egress for ElastiCache
  egress {
    from_port = 6379
    to_port   = 6379
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private[0].cidr_block,
      aws_subnet.private[1].cidr_block
    ]
  }

  # For ECS to access vpc endpoints
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # do we really need this many ips?
  }


}

##
# ECS Django API service 
##

resource "aws_ecs_service" "api" {
  name                   = "${local.prefix}-ecs-service-api"
  cluster                = aws_ecs_cluster.main.name
  task_definition        = aws_ecs_task_definition.api.arn
  desired_count          = 1
  enable_execute_command = true
  launch_type            = "FARGATE"
  platform_version       = "1.4.0"

  health_check_grace_period_seconds = 90

  network_configuration {
    subnets = [
      aws_subnet.private[0].id,
      aws_subnet.private[1].id
    ]
    security_groups = [aws_security_group.ecs_service.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "nginx"
    container_port   = 8080
  }
  depends_on = [
    aws_lb_listener.api_https,
    aws_db_instance.main,
    aws_elasticache_replication_group.redis
  ]
}





