##
# CD user credentials
##

output "cd_user_access_key_id" {
  description = "AWS access key ID for CD user."
  value       = aws_iam_access_key.cd.id
}


output "cd_user_access_key_secret" {
  description = "AWS access key secret for CD user."
  value       = aws_iam_access_key.cd.secret
  sensitive   = true
}

##
# SES SMTP user fo
##

output "ses_user_access_key_id" {
  description = "AWS access key ID for SES SMTP user."
  value       = aws_iam_access_key.ses_smtp_key.id
}


output "ses_user_access_key_secret" {
  description = "AWS access key secret for SES SMTP user."
  value       = aws_iam_access_key.ses_smtp_key.secret
  sensitive   = true
}

##
# ECR repo
##

output "ecr_repo_app" {
  description = "ECR respository URL for app image."
  value       = aws_ecr_repository.app.repository_url

}

output "ecr_repo_proxy" {
  description = "ECR respository URL for proxy image."
  value       = aws_ecr_repository.proxy.repository_url

}
