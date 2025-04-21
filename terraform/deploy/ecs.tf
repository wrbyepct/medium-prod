
##
# ECS cluster for running app on Fargate.
#
resource "aws_ecs_cluster" "main" {
  name = "${local.prefix}-ecs-cluster"
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
# Fargate Task role policy - Allow connect to System Service Manager 
##
resource "aws_iam_role_policy" "ssm_policy" {
  name   = "SSMSessionPolicy"
  role   = aws_iam_role.app_task.name
  policy = file("${path.module}/template/ecs/ssm-role-policy.json")
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
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([
    # API container
    {
      name              = "api"
      image             = var.ecr_repo_app_image
      essential         = true
      memoryReservation = 256
      user              = "medium-api"
      environment = [
        {
          name  = "DJANGO_SECRET_KEY"
          value = var.django_secret_key
        },
        {
          name  = "DJANGO_ALLOWED_HOST"
          value = "*"
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
        }
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
        logDriver = "awsvpc"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs
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
      memoryReservation = 256
      user              = "nginx"
      portMappings = [
        {
          hostPort      = 8080
          containerPort = 8080
        }
      ]
      environment = [
        {
          name  = "APP_HOST"
          value = "127.0.0.1"
        },
        {
          name  = "LISTEN_PORT"
          value = 8080
        },
        {
          name  = "API_PORT"
          value = 8000
        }
      ]
      mountPoints = [
        {
          readOnly      = true
          containerPath = "/vol/staticfiles/"
          sourceVolume  = "static"
        },
        {
          readOnly = true
          containerPath = "/vol/mediafiles/"
          sourceVolume = "efs-media"
        }
      ]
      logConfiguration = {
        logDriver = "awsvpc"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs
          awslogs-region        = data.aws_region.current.name
          awslogs-stream-prefix = "nginx"
        }

      }
    }
  ])

  volume {
    name = "static"
  }

  volume {
    name = "efs-media"
    efs_volume_configuration {
      file_system_id = aws_efs_file_system.media.id
      transit_encryption = "ENABLED"

      authorization_config {
        access_point_id = aws_efs_access_point.media.id
        iam = "DISABLED"
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
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    security_groups = [aws_security_group.lb.id]
  }

  # For ECS to access RDS
  egress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    cidr_blocks = [
      aws_subnet.private[0].cidr_block,
      aws_subnet.private[1].cidr_block
    ]
  }

  # For ECS to access EFS
  egress {
    from_port = 2049
    to_port = 2049
    protocol = "tcp"
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
# ECS service 
##

resource "aws_ecs_service" "api" {
  name = "${local.prefix}-ecs-service-api"
  cluster = aws_ecs_cluster.main.name 
  task_definition = aws_ecs_task_definition.api.family
  desired_count = 1 
  enable_execute_command = true
  launch_type = "FARGATE"
  platform_version = "1.4.0"
  
  network_configuration {
    subnets = [
      aws_subnet.private[0].id, 
      aws_subnet.private[1].id
    ]
    security_groups = [aws_security_group.ecs_service.id]
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name = "nginx"
    container_port = 8080
  }
}

