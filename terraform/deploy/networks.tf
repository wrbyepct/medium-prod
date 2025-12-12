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
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "${local.prefix}-private-rt"
  }

}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}


##
# Endpoints for Allowing Private Subnet ECS to Access CloudWatch, ECR, S3, SES and CloudWatch
##

resource "aws_security_group" "endpoint_access" {

  description = "Security group that allow Access to Endpoints "
  name        = "${local.prefix}-endpoint-access"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }
  # For SMTP email to SES
  ingress {
    from_port   = 587
    to_port     = 587
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

}


module "vpc_endpoints" {
  source = "./modules/vpc_endpoints"

  vpc_id             = aws_vpc.main.id
  subnet_ids         = [aws_subnet.private[0].id, aws_subnet.private[1].id]
  security_group_ids = [aws_security_group.endpoint_access.id]
  route_table_ids    = [aws_route_table.private.id]

  ecs_service_dependency = aws_ecs_service.api.id

  interface_services = [
    "ecr.api",
    "ecr.dkr",
    "logs",
    "ssmmessages",
    "email-smtp"
  ]

  gateway_services = ["s3"]

}
