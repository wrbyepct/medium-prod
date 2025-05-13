#######################
# Load Balancer Setup #
#######################
resource "aws_security_group" "lb" {
  description = "Security Group for Application Load Balancer"
  name        = "${local.prefix}-elb-security-group"
  vpc_id      = aws_vpc.main.id

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "tcp"
    from_port   = 8080
    to_port     = 8080
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "api" {
  name               = "${local.prefix}-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.public[0].id, aws_subnet.public[1].id]
  security_groups    = [aws_security_group.lb.id]
}


resource "aws_lb_target_group" "api" {
  name        = "${local.prefix}-lb-target-group"
  vpc_id      = aws_vpc.main.id
  protocol    = "HTTP"
  port        = 8080
  target_type = "ip"

  health_check {
    path                = "/api/v1/health/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 10 # 👈 allow more failures before declaring unhealthy
  }

}


resource "aws_lb_listener" "api_http" {
  load_balancer_arn = aws_lb.api.arn
  protocol          = "HTTP"
  port              = 80

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }

  }

}


resource "aws_lb_listener" "api_https" {
  load_balancer_arn = aws_lb.api.arn
  protocol          = "HTTPS"
  port              = 443

  certificate_arn = aws_acm_certificate_validation.cert.certificate_arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }

}