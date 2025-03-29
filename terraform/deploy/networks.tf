##############
# Create VPC #
##############
resource "aws_vpc" "main" {
  cidr_block           = "10.1.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}


#############################################################
# Internet Gateway needed for the inbound access to the ALB #
#############################################################

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${local.prefix}-igw-main"
  }

}

#################################################
# Public subnet for load balancer public access #
#################################################

data "aws_availability_zones" "available" {
  state = "available"
}


resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet("10.1.0.0/23", 1, count.index)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.prefix}-public-${data.aws_availability_zones.available.names[count.index]}"
  }

}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = {
    Name = "${local.prefix}-public-rt"
  }

}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}


##########################################
# Private subnets for application and DB #
##########################################

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet("10.1.10.0/23", 1, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "${local.prefix}-private-${data.aws_availability_zones.available.names[count.index]}"
  }

}

resource "aws_route_table" "private" {
  count  = length(aws_subnet.private)
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${local.prefix}-private-rt-${data.aws_availability_zones.available.names[count.index]}"
  }

}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}


##
# Endpoints for Allowing Private Subnet ECS to Access CloudWatch, ECR, S3 and CloudWatch
##

resource "aws_security_group" "endpoint_access" {

  description = "Security group that allow Access to Endpoints "
  name        = "${local.prefix}-endpoint-access"
  vpc_id      = aws_vpc.main.id

  ingress {
    cidr_blocks = [aws_vpc.main.cidr_block]
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
  }

}


resource "aws_vpc_endpoint" "ecr" {
  vpc_id             = aws_vpc.main.id
  vpc_endpoint_type  = "Interface"
  service_name       = "com.amazonaws.${data.aws_region.current.name}.ecr.api"
  subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
  security_group_ids = [aws_security_group.endpoint_access.id]

  private_dns_enabled = true

  tags = {
    Name = "${local.prefix}-ecr-api-endpoint"
  }
}

resource "aws_vpc_endpoint" "dkr" {
  vpc_id             = aws_vpc.main.id
  vpc_endpoint_type  = "Interface"
  service_name       = "com.amazonaws.${data.aws_region.current.name}.ecr.dkr"
  subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
  security_group_ids = [aws_security_group.endpoint_access.id]

  tags = {
    Name = "${local.prefix}-ecr-dkr-endpoint"
  }
}

resource "aws_vpc_endpoint" "cloudwatch_logs" {
  vpc_id             = aws_vpc.main.id
  vpc_endpoint_type  = "Interface"
  service_name       = "com.amazonaws.${data.aws_region.current.name}.logs"
  subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
  security_group_ids = [aws_security_group.endpoint_access.id]

  tags = {
    Name = "${local.prefix}-cloudwatch-endpoint"
  }
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id = aws_vpc.main.id

  vpc_endpoint_type = "Interface"

  service_name = "com.amazonaws.${data.aws_region.current.name}.ssmmessages"

  subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
  security_group_ids = [aws_security_group.endpoint_access.id]

  tags = {
    Name = "${local.prefix}-ssmmessages-endpoint"
  }
}


resource "aws_vpc_endpoint" "s3" {
  vpc_id = aws_vpc.main.id

  vpc_endpoint_type = "Gateway"

  service_name = "com.amazonaws.${data.aws_region.current.name}.s3"

  route_table_ids = [aws_route_table.private[0].id, aws_route_table.private[1].id]

  tags = {
    Name = "${local.prefix}-s3-endpoint"
  }

}