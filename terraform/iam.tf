
# Iam lambda ia
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


# iam lambda capture

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

resource "aws_iam_role_policy_attachment" "attachment_capture" {
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





