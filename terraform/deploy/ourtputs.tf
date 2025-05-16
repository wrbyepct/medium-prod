output "api_endpoint" {
  value = aws_route53_record.app.fqdn
}


output "es_endpoint" {
  value = aws_opensearch_domain.es.endpoint
}
