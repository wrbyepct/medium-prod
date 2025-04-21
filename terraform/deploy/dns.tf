# Name our dns zone

data "aws_route53_zone" "primary" {
  name = var.dns_zone_name
}

resource "aws_route53_record" "app" {
  zone_id = data.aws_route53_zone.primary.zone_id
  
  name = "${lookup(var.subdomain, terraform.workspace)}.${data.aws_route53_zone.zone.name}"
  records = [aws_lb.api.dns_name]
  type = "CNAME"

  ttl = "300"

}


##
# ACM TSL certify 
##

resource "aws_acm_certificate" "cert" {
  domain_name = aws_route53_record.app.name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
  
}

resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name = dvo.resource_record_name
      record = dvo.resource_record_value
      type = dvo.resource_resorc_type
    }
  }

  name = each.value.name
  records = [each.value.record]
  type = each.value.type 

  allow_overwrite = true
  ttl = 60

  zone_id = data.aws_route53_zone.zone.zone_id

}


resource "aws_acm_certificate_validation" "cert" {
  certificate_arn = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
  
}