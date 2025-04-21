##
# EFS 
##

resource "aws_efs_file_system" "media" {
  encrypted = true
  tags = {
    Name = "${local.prefix}-media"
  }
  
}

resource "aws_security_group" "efs" {
  name = "${local.prefix}-efs-security-group"
  vpc_id = aws_vpc.main.id 
  
  ingress {
    from_port = 2049
    to_port = 2049
    protocol = "tcp"

    security_groups = [aws_ecs_service.api.id]
  }
  
}

resource "aws_efs_mount_target" "media" {
  count = length(aws_subnet.private)
  
  file_system_id = aws_efs_file_system.media.id
  subnet_id = aws_subnet.private[count.index].id
  security_groups = [aws_security_group.efs.id]

}

resource "aws_efs_access_point" "media" {
  file_system_id = aws_efs_file_system.media.id 
  root_directory {
    path = "/api/media"
    creation_info {
      owner_gid = 101
      owner_uid = 101
      permissions = 755
    }
  }

}