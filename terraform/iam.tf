
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
                        "s3:DeleteObject"
                      ],
            "Resource": "${aws_s3_bucket.network_bucket.arn}/*"
        }
    ]
}
EOF
}


# autorisation SQS ia for lambda ia
resource "aws_iam_role_policy" "iam_policy_for_sqs_ia" {
  name = "lambda_sqs_policy_ia"
  role = aws_iam_role.lambda_ia_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "sqs:*"
                      ],
            "Resource": "${aws_sqs_queue.sqs_queue_ia.arn}/*"
        }
    ]
}
EOF
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
resource "aws_iam_role_policy" "iam_policy_for_sqs_capture" {
  name = "lambda_sqs_policy_capture"
  role = aws_iam_role.lambda_capture_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "sqs:*"
                      ],
            "Resource": "${aws_sqs_queue.sqs_queue_capture.arn}/*"
        }
    ]
}
EOF
}

# autorisation SQS ia for lambda ia
resource "aws_iam_role_policy" "iam_policy_for_sqs_ia_capt" {
  name = "lambda_sqs_policy_ia_capt"
  role = aws_iam_role.lambda_capture_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "sqs:*"
                      ],
            "Resource": "${aws_sqs_queue.sqs_queue_ia.arn}/*"
        }
    ]
}
EOF
}




