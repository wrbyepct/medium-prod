######################################################
# ECR repository for Docker images of apps and proxy #
######################################################

resource "aws_ecr_repository" "app" {
  name                 = "medium-api-app"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # Set false for produciton

  image_scanning_configuration {
    scan_on_push = false # Set true for produciton
  }
}

resource "aws_ecr_repository" "proxy" {
  name                 = "medium-api-proxy"
  image_tag_mutability = "MUTABLE"
  force_delete         = true # Set false for produciton

  image_scanning_configuration {
    scan_on_push = false # Set true for produciton
  }

}
