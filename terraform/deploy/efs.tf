##
# KMS key for fine-grained EFS access
##
resource "aws_kms_key" "efs" {
  description = "KMS Key for EFS"

  enable_key_rotation = true

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid : "Allow account users to manage key",
        Effect : "Allow",
        Principal : {
          AWS : "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        Action : "kms:*",
        Resource : "*"
      },
      {
        Sid : "Allow ECS task roles to use the key",
        Effect : "Allow",
        Principal : {
          AWS : aws_iam_role.app_task.arn
        },
        Action : [
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ],
        Resource : "*"
      }
    ]
  })
}

##
# EFS 
##

resource "aws_efs_file_system" "api" {
  encrypted  = true
  kms_key_id = aws_kms_key.efs.arn
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS" # This reduces storage cost a LOT → good for media files, logs, ES data → things that are not frequently read.
  }
  tags = {
    Name = "${local.prefix}-api"
  }

}

resource "aws_security_group" "efs" {
  name   = "${local.prefix}-efs-security-group"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port = 2049
    to_port   = 2049
    protocol  = "tcp"

    security_groups = [aws_ecs_service.api.id]
  }

}

resource "aws_efs_mount_target" "media" {
  count = length(aws_subnet.private)

  subnet_id       = aws_subnet.private[count.index].id
  security_groups = [aws_security_group.efs.id]
  file_system_id  = aws_efs_file_system.api.id

}

resource "aws_efs_access_point" "media" {
  file_system_id = aws_efs_file_system.api.id
  root_directory {
    path = "/api/media"
    creation_info {
      owner_gid   = 101
      owner_uid   = 101
      permissions = 755
    }
  }

}

