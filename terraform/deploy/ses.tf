
resource "aws_ses_domain_identity" "api" {
  domain = var.domain
}



resource "aws_route53_record" "ses_verification" {
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "_amazonses.${aws_ses_domain_identity.api.domain}"
  type    = "TXT"
  ttl     = 600
  records = [aws_ses_domain_identity.api.verification_token]
}


resource "aws_ses_domain_dkim" "api" {
  domain = aws_ses_domain_identity.api.domain
}


resource "aws_route53_record" "dkim" {
  count   = 3
  zone_id = data.aws_route53_zone.primary.zone_id
  name    = "${aws_ses_domain_dkim.api.dkim_tokens[count.index]}._domainkey.${aws_ses_domain_dkim.api.domain}"
  type    = "CNAME"
  ttl     = 600
  records = ["${aws_ses_domain_dkim.api.dkim_tokens[count.index]}.dkim.amazonses.com"]
}