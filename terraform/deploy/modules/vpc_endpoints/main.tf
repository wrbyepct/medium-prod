variable "vpc_id" {}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_ids" {
  type = list(string)
}

variable "route_table_ids" {
  type = list(string)
}


variable "interface_services" {
  type = list(string)
  default = []
}


variable "gateway_services" {
  type = list(string)
  default = []
}


data "aws_region" "current" {}


resource "aws_vpc_endpoint" "interface_endpoints" {
  count = length(var.interface_services)

  vpc_id = var.vpc_id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.${data.aws_region.current.name}.${var.interface_services[count.index]}"

  subnet_ids = var.subnet_ids
  security_group_ids = var.security_group_ids
  private_dns_enabled = true

  tags = {
    Name = "${interface_services[count.index]}-endpoint"
  }
}


resource "aws_vpc_endpoint" "gateway_endpoints" {
  count = length(var.gateway_services)
  
  vpc_id = var.vpc_id
  vpc_endpoint_type = "Gateway"
  service_name = "com.amazonaws.${data.aws_region.current.name}.${var.gateway_services[count.index]}"

  route_table_ids = var.route_table_ids

  tags = {
    Name = "${var.gateway_services[count.index]}-endpoint"
  }
}


