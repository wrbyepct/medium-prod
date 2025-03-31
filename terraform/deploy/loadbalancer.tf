#######################
# Load Balancer Setup #
#######################
resource "aws_security_group" "lb" {
  description = "Security Group for Application Load Balancer" 
  name = "${local.prefix}-elb-security-group"
  vpc_id = aws_vpc.main.id 

  ingress {
    protocol = "tcp"
    from_port = 80
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol = "tcp"
    from_port = 443
    to_port = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol = "tcp"
    from_port = 8000
    to_port = 8000
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "api" {
  name = "${local.prefix}-lb"
  load_balancer_type = "application"
  subnets = [aws_subnet.public[0].id, aws_subnet.public[1].id]
  security_groups = [aws_security_group.lb.id]
}