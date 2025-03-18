variable "tf_state_bucket" {
  description = "Name of S3 bucket in AWS for storing TF state "
  default     = "devops-medium-app-tf-state"

}

variable "tf_state_lock_table" {
  description = "Name of DynamoDB table for state locking"
  default     = "devops-medium-app-state-lock"

}

variable "project" {
  description = "Name of the project for tagging resources"
  default     = "medium-api-prod"

}

variable "contact" {
  description = "Contact name for tagging resources"
  default     = "shandianskypian@gmail.com"

}
