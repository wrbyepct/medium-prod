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
