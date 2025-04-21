
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
# EC2 Policy access for creating VPC #
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


#########################
# Policy for RDS access #
#########################

data "aws_iam_policy_document" "rds" {
  statement {
    effect = "Allow"
    actions = [
      "rds:DescribeDBSubnetGroups",
      "rds:CreateDBSubnetGroup",
      "rds:DeleteDBSubnetGroup",
      "rds:DescribeDBInstances",
      "rds:CreateDBInstance",
      "rds:DeleteDBInstance",
      "rds:ModifyDBInstance",
      "rds:ListTagsForResource",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "rds" {
  name        = "${aws_iam_user.cd.name}-rds"
  description = "Allow user to manage RDS resources."
  policy      = data.aws_iam_policy_document.rds.json
}

resource "aws_iam_user_policy_attachment" "rds" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.rds.arn
}


#########################
# Policy for ECS access #
#########################

data "aws_iam_policy_document" "ecs" {
  statement {
    effect = "Allow"
    actions = [
      "ecs:DescribeClusters",
      "ecs:CreateCluster",
      "ecs:UpdateCluster",
      "ecs:DeleteCluster",
      #####################
      "ecs:DescribeServices",
      "ecs:CreateService",
      "ecs:UpdateService",
      "ecs:DeleteService",
      #####################
      "ecs:DescribeTaskDefinition",
      "ecs:DeregisterTaskDefinition",
      "ecs:RegisterTaskDefinition",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "ecs" {
  name        = "${aws_iam_user.cd.name}-ecs"
  description = "Allow user to manage ECS resources."
  policy      = data.aws_iam_policy_document.ecs.json
}

resource "aws_iam_user_policy_attachment" "ecs" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.ecs.arn
}

#########################
# Policy for IAM access #
#########################

data "aws_iam_policy_document" "iam" {
  statement {
    effect = "Allow"
    actions = [
      "iam:ListInstanceProfilesForRole",
      #######################
      "iam:ListAttachedRolePolicies",
      "iam:AttachRolePolicy",
      "iam:DetachRolePolicy",
      "iam:ListRolePolicies",
      #######################
      "iam:CreateRole",
      "iam:GetRole",
      "iam:TagRole",
      "iam:DeleteRole",
      "iam:PassRole",
      ######################
      "iam:ListPolicyVersions",
      "iam:GetPolicyVersion",
      "iam:GetPolicy",
      "iam:CreatePolicy",
      "iam:DeletePolicy",
      "iam:TagPolicy",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "iam" {
  name        = "${aws_iam_user.cd.name}-iam"
  description = "Allow user to manage IAM resources."
  policy      = data.aws_iam_policy_document.iam.json
}

resource "aws_iam_user_policy_attachment" "iam" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.iam.arn
}

################################
# Policy for CloudWatch access #
################################

data "aws_iam_policy_document" "logs" {
  statement {
    effect = "Allow"
    actions = [
      "logs:DescribeLogGroups",
      "logs:CreateLogGroup",
      "logs:DeleteLogGroup",
      "logs:ListTagsLogGroup",
      "logs:TagResource",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "logs" {
  name        = "${aws_iam_user.cd.name}-logs"
  description = "Allow user to manage CloudWatch resources."
  policy      = data.aws_iam_policy_document.logs.json
}

resource "aws_iam_user_policy_attachment" "logs" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.logs.arn
}


#########################
# Policy for ELB access #
#########################

data "aws_iam_policy_document" "elb" {
  statement {
    effect = "Allow"
    actions = [
      "elasticloadbalancing:DescribeLoadBalancers",
      "elasticloadbalancing:CreateLoadBalancer",
      "elasticloadbalancing:DeleteLoadBalancer",
      "elasticloadbalancing:DescribeListeners",
      ##############################################
      "elasticloadbalancing:CreateListener",
      "elasticloadbalancing:ModifyListener",
      "elasticloadbalancing:DeleteListener",
      ##############################################
      "elasticloadbalancing:DescribeLoadBalancerAttributes",
      "elasticloadbalancing:DescribeTargetGroupAttributes",
      "elasticloadbalancing:ModifyLoadBalancerAttributes",
      "elasticloadbalancing:ModifyTargetGroupAttributes",
      ##############################################
      "elasticloadbalancing:DescribeTargetGroups",
      "elasticloadbalancing:CreateTargetGroup",
      "elasticloadbalancing:DeleteTargetGroup",
      ##############################################
      "elasticloadbalancing:DescribeTags",
      "elasticloadbalancing:AddTags",
      ##############################################
      "elasticloadbalancing:SetSecurityGroups",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "elb" {
  name        = "${aws_iam_user.cd.name}-elb"
  description = "Allow user to manage ELB resources."
  policy      = data.aws_iam_policy_document.elb.json
}

resource "aws_iam_user_policy_attachment" "elb" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.elb.arn
}

#########################
# Policy for EFS access #
#########################

data "aws_iam_policy_document" "efs" {
  statement {
    effect = "Allow"
    actions = [
      "elasticfilesystem:DescribeFileSystems",
      "elasticfilesystem:CreateFileSystem",
      "elasticfilesystem:DeleteFileSystem",
      #######################################
      "elasticfilesystem:DescribeAccessPoints",
      "elasticfilesystem:CreateAccessPoint",
      "elasticfilesystem:DeleteAccessPoint",
      #######################################
      "elasticfilesystem:DescribeMountTargets",
      "elasticfilesystem:CreateMountTarget",
      "elasticfilesystem:DeleteMountTarget",
      #######################################
      "elasticfilesystem:DescribeMountTargetSecurityGroups",
      "elasticfilesystem:DescribeLifecycleConfiguration",
      "elasticfilesystem:TagResource",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "efs" {
  name        = "${aws_iam_user.cd.name}-efs"
  description = "Allow user to manage EFS resources."
  policy      = data.aws_iam_policy_document.efs.json
}

resource "aws_iam_user_policy_attachment" "efs" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.efs.arn
}


#############################
# Policy for Route53 access #
#############################

data "aws_iam_policy_document" "route53" {
  statement {
    effect = "Allow"
    actions = [
      "route53:ListHostedZones",
      "route53:ListHostedZones",
      "route53:GetHostedZone",
      ##########################
      "route53:ChangeTagsForResource",
      "route53:ListTagsForResource",
      ##########################
      "route53:ChangeResourceRecordSets",
      "route53:ListResourceRecordSets",
      "route53:GetChange",
      ##########################
      "acm:DescribeCertificate",
      "acm:CreateCertificate",
      "acm:DeleteCertificate",
      "acm:RequestCertificate",
      "acm:AddTagsToCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "route53" {
  name        = "${aws_iam_user.cd.name}-route53"
  description = "Allow user to manage Route53 resources."
  policy      = data.aws_iam_policy_document.route53.json
}

resource "aws_iam_user_policy_attachment" "route53" {
  user       = aws_iam_user.cd.name
  policy_arn = aws_iam_policy.route53.arn
}