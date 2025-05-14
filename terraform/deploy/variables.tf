variable "prefix" {
  description = "Prefix for AWS resources"
  default     = "raa"
}

variable "project" {
  description = "Name of the project for tagging resources"
  default     = "medium-api-prod"

}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "shandianskypian@gmail.com"

}

variable "db_username" {
  description = "DB name for RDS"
  default     = "mediumapi"

}

variable "db_password" {
  description = "DB password for RDS"

}


variable "ecr_repo_proxy_image" {
  description = "ECR Nginx proxy image"
}

variable "ecr_repo_app_image" {
  description = "ECR Medium app image"
}


variable "dns_zone_name" {
  description = "Domain Name"
  default     = "jamaisvu.click"

}

variable "subdomain" {
  description = "Subdomain based on workspace"
  type        = map(string)

  default = {
    "prod"    = "api"
    "staging" = "api.staging"
    "dev"     = "api.dev"
  }

}

##
# Variable for Django app
##

variable "django_secret_key" {
  description = "Django App Secret Key"
}


variable "jwt_signing_key" {
  description = "JWT signing key"
}

variable "django_admin_url" {
  description = "Django Admin URL"
}

variable "celery_broker_url" {
  description = "Redis Celery Broker URL"
}

variable "domain" {
  description = "Django API Domain name"
}


variable "csrf_trusted_origins" {
  description = "CSRF trusted Origins for Django API"
}

variable "django_allowed_hosts" {
  description = "Allowed Hosts for Django API"
}

variable "smtp_username" {
  description = "SMTP username for SES"
}

variable "smtp_password" {
  description = "SMTP password for SES"
}

variable "email_host" {
  description = "SMTP host for SES"
}