
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
  memory                   = 512
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.app_task.arn

  container_definitions = jsonencode([
    {
      name              = "medium"
      image             = var.ecr_repo_proxy_image
      essential         = true
      memoryReservation = 100
      user              = "nginx"
      portMappings = [
        {
          containerPort = 80
          hostPort      = 8080
        }

      ]
      environment = [
        {
          name  = "APP_HOST"
          value = "127.0.0.1"
        },
        {
          name  = "LISTEN_PORT"
          value = 80
        },
        {
          name  = "API_PORT"
          value = 8000
        }
      ]
      mountPoints = [
        {
          readOnly      = true
          containerPath = "/vol/staticfiles"
          sourceVolume  = "static"
        }
      ]
      logConfiguration = {
        logDriver = "awsvpc"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs
          awslogs-stream-prefix = "nginx"
          awslogs-region        = data.aws_region.current.name
        }

      }
    }
  ])

  volume {
    name = "static"
  }
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }
}
