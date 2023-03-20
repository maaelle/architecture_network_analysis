
###### need to add lambda basic function role for each lambda



########## Iam lambda unknown url
resource "aws_iam_role" "unknown_urls_lambda_role" {
  name               = "unknown_urls_lambda_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


data "aws_iam_policy_document" "sqs_capture_policy_doc" {
  statement {
    sid       = "456456"
    actions   = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:SendMessage"
    ]
    resources = [
      aws_sqs_queue.sqs_capture.arn
    ]
  }
}

resource "aws_iam_policy" "sqs_capture_policy" {
  name   = "sqs_capture_policy"
  policy = data.aws_iam_policy_document.sqs_capture_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "attachment_capture_send" {
  role       = aws_iam_role.unknown_urls_lambda_role.name
  policy_arn = aws_iam_policy.sqs_capture_policy.arn
}



######### iam lambda capture

resource "aws_iam_role" "lambda_capture_role" {
  name = "lambda_capture_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


# autorisation SQS capture for lambda capture

resource "aws_iam_role_policy_attachment" "attachment_capture_receive" {
  role       = aws_iam_role.lambda_capture_role.name
  policy_arn = aws_iam_policy.sqs_capture_policy.arn
}


# autorisation SQS ia for lambda ia

data "aws_iam_policy_document" "sqs_capture_ia_policy_doc" {
  statement {
    sid       = "789789"
    actions   = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:SendMessage"
    ]
    resources = [
      aws_sqs_queue.sqs_ia.arn
    ]
  }
}

resource "aws_iam_policy" "sqs_capture_ia_policy" {
  name   = "sqs_capture_ia_policy"
  policy = data.aws_iam_policy_document.sqs_capture_ia_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "attachment_capture_ia" {
  role       = aws_iam_role.lambda_capture_role.name
  policy_arn = aws_iam_policy.sqs_capture_ia_policy.arn
}




########## Iam lambda ia
resource "aws_iam_role" "lambda_ia_role" {
  name = "lambda_ia_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# autorisation d'accès S3 for lambda ia
resource "aws_iam_role_policy" "iam_policy_for_s3" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_ia_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "s3:PutObject",
                        "s3:GetObject",
                        "s3:DeleteObject"
                      ],
            "Resource": "${aws_s3_bucket.network_bucket.arn}/*"
        }
    ]
}
EOF
}

# autorisation d'accès ECR for lambda ia
resource "aws_iam_role_policy" "iam_policy_for_ecr" {
  name = "lambda_ecr_policy"
  role = aws_iam_role.lambda_ia_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "ecr:BatchGetImage",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:CompleteLayerUpload",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:InitiateLayerUpload",
                        "ecr:PutImage",
                        "ecr:UploadLayerPart"
                      ],
            "Resource": "arn:aws:ecr:eu-west-1:715437275066:repository/ecr_docker_lambda/*"
        }
    ]
}
EOF
}


# autorisation SQS ia for lambda ia
data "aws_iam_policy_document" "sqs_ia_policy_doc" {
  statement {
    sid       = "123123"
    actions   = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:SendMessage"
    ]
    resources = [
      aws_sqs_queue.sqs_ia.arn
    ]
  }
}

resource "aws_iam_policy" "sqs_ia_policy" {
  name   = "sqs_ia_policy"
  policy = data.aws_iam_policy_document.sqs_ia_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "attachment_ia" {
  role       = aws_iam_role.lambda_ia_role.name
  policy_arn = aws_iam_policy.sqs_ia_policy.arn
}

# aut SQS pred pour lamdba ia

data "aws_iam_policy_document" "sqs_pred_policy_doc" {
  statement {
    sid       = "12121212"
    actions   = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:SendMessage"
    ]
    resources = [
      aws_sqs_queue.sqs_pred.arn
    ]
  }
}

resource "aws_iam_policy" "sqs_capture_pred_policy" {
  name   = "sqs_capture_pred_policy"
  policy = data.aws_iam_policy_document.sqs_pred_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "attachment_pred" {
  role       = aws_iam_role.lambda_ia_role.name
  policy_arn = aws_iam_policy.sqs_capture_pred_policy.arn
}


###### Iam refit lambda
/*
resource "aws_iam_role" "refit_lambda_role" {
  name               = "refit_lambda_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "sqs_pred_refit_policy_doc" {
  statement {
    sid       = "3434343434"
    actions   = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:SendMessage"
    ]
    resources = [
      aws_sqs_queue.sqs_pred.arn
    ]
  }
}

resource "aws_iam_policy" "sqs_capture_pred_refit_policy" {
  name   = "sqs_capture_pred_refit_policy"
  policy = data.aws_iam_policy_document.sqs_pred_refit_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "attachment_pred_refit" {
  role       = aws_iam_role.lambda_refit_role.name
  policy_arn = aws_iam_policy.sqs_capture_pred_refit_policy.arn
}

*/