##
# A dedicate dIAM for SES service - Because we use SMTP approach in Django
##

resource "aws_iam_user" "ses_smtp_user" {
  name = "ses-smtp-user"
}

resource "aws_iam_access_key" "ses_smtp_key" {
  user = aws_iam_user.ses_smtp_user.name
}

resource "aws_iam_user_policy" "ses_smtp_policy" {
  name = "AllowSendRawEmail"
  user = aws_iam_user.ses_smtp_user.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect   = "Allow",
      Action   = "ses:SendRawEmail",
      Resource = "*"
    }]
  })
}

