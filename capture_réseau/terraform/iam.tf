resource "aws_iam_role" "lambda_role" {
  name = "lambda_role"

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


resource "aws_iam_role_policy" "iam_policy_for_s3" {
  name = "lambda_s3_policy"
  role = aws_iam_role.lambda_role.id

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

resource "aws_iam_role_policy" "iam_policy_for_sqs" {
  name = "lambda_sqs_policy"
  role = aws_iam_role.lambda_role.id

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "sqs:*"
                      ],
            "Resource": "${aws_sqs_queue.sqs_queue.arn}/*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "iam_policy_for_sqs_capture" {
  name = "lambda_sqs_policy_capture"
  role = aws_iam_role.lambda_role.id

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

resource "aws_sqs_queue_policy" "sqs_capture_ai_policy" {
  queue_url = aws_sqs_queue.sqs_queue.id
  policy    = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "lambda:CreateEventSourceMapping",
                        "lambda:ListEventSourceMappings",
                        "lambda:ListFunctions"
                      ],
            "Resource": "${aws_lambda_function.capture_stat_lambda.arn}/*"
        }
    ]
}
EOF
}

resource "aws_sqs_queue_policy" "my_sqs_policy_ai" {
  queue_url = aws_sqs_queue.sqs_queue.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*",
      "Resource": "${aws_sqs_queue.sqs_queue.arn}"
    }
  ]
}
POLICY
}

resource "aws_sqs_queue_policy" "sqs_url_capture_policy" {
  queue_url = aws_sqs_queue.sqs_queue_capture.id
  policy    = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                        "lambda:CreateEventSourceMapping",
                        "lambda:ListEventSourceMappings",
                        "lambda:ListFunctions"
                      ],
            "Resource": "${aws_lambda_function.capture_stat_lambda.arn}/*"
        }
    ]
}
EOF
}

resource "aws_sqs_queue_policy" "my_sqs_policy_capture" {
  queue_url = aws_sqs_queue.sqs_queue_capture.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:*",
      "Resource": "${aws_sqs_queue.sqs_queue_capture.arn}"
    }
  ]
}
POLICY
}