
# Create IAM user
resource "aws_iam_user" "cd" {
  name = "medium_api_cd"
}

resource "aws_iam_access_key" "cd" {
  user = aws_iam_user.cd.name
}

##################
# Backend Policy #
##################

data "aws_iam_policy_document" "tf_backend" {
  statement {
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${var.tf_state_bucket}"]
  }

  statement {
    effect  = "Allow"
    actions = ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
    resources = [
      "arn:aws:s3:::${var.tf_state_bucket}/tf-state-deploy/*",
      "arn:aws:s3:::${var.tf_state_bucket}/tf-state-deploy-env/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "dynamodb:DescribeTable",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:DeleteItem"
    ]
    resources = [
      "arn:aws:dynamodb:*:*:table/${var.tf_state_lock_table}",
    ]
  }
}

resource "aws_iam_policy" "tf_backend" {
  name        = "${aws_iam_user.cd.name}-tf-s3-dynamodb"
  description = "Allow user to use S3 & DynamoDB for TF backend resources."
  policy      = data.aws_iam_policy_document.tf_backend.json
}

resource "aws_iam_user_policy_attachment" "tf_backend" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.tf_backend.arn
}

#########################
# ECR policy definition #
#########################

data "aws_iam_policy_document" "ecr" {
  statement {
    effect    = "Allow"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "ecr:InitiateLayerUpload",
      "ecr:CompleteLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:BatchCheckLayerAvailability",
      "ecr:PutImage",
    ]
    resources = [
      aws_ecr_repository.app.arn,
      aws_ecr_repository.proxy.arn,
    ]
  }

}


resource "aws_iam_policy" "ecr" {
  name        = "${aws_iam_user.cd.name}-ecr"
  description = "Allow user to update images in ECR"
  policy      = data.aws_iam_policy_document.ecr.json

}

resource "aws_iam_user_policy_attachment" "ecr" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.ecr.arn
}


#########################
# EC2 Policy access #
#########################

data "aws_iam_policy_document" "ec2" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:DescribeVpcs",
      "ec2:CreateVpc",
      "ec2:DeleteVpc",
      "ec2:DescribeVpcEndpoints",
      "ec2:CreateVpcEndpoint",
      "ec2:DeleteVpcEndpoints",
      ########################
      "ec2:DescribeSecurityGroups",
      "ec2:CreateSecurityGroup",
      "ec2:DeleteSecurityGroup",
      ########################
      "ec2:DescribeInternetGateways",
      "ec2:CreateInternetGateway",
      "ec2:DeleteInternetGateway",
      "ec2:AttachInternetGateway",
      "ec2:DetachInternetGateway",
      ########################
      "ec2:DescribeNetworkInterfaces",
      "ec2:DetachNetworkInterface",
      #######################
      "ec2:DescribeRouteTables",
      "ec2:CreateRouteTable",
      "ec2:DeleteRouteTable",
      "ec2:AssociateRouteTable",
      "ec2:DisassociateRouteTable",
      ##########################
      "ec2:CreateRoute",
      "ec2:DeleteRoute",
      ##########################
      "ec2:DescribeVpcAttribute",
      "ec2:ModifyVpcAttribute",
      ###########################
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:AuthorizeSecurityGroupEgress",
      "ec2:RevokeSecurityGroupEgress",
      ###########################
      "ec2:DescribeSubnets",
      "ec2:CreateSubnet",
      "ec2:DeleteSubnet",
      "ec2:ModifySubnetAttribute",
      ###########################
      "ec2:DescribeAvailabilityZones",
      "ec2:DescribeNetworkAcls",
      "ec2:DescribePrefixLists",
      "ec2:CreateTags",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "ec2" {
  name        = "${aws_iam_user.cd.name}-ec2"
  description = "Allow user to manage EC2 resources."
  policy      = data.aws_iam_policy_document.ec2.json
}

resource "aws_iam_user_policy_attachment" "ec2" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.ec2.arn
}