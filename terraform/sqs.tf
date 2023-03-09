# SQS 1
resource "aws_sqs_queue" "sqs_queue_ia" {
  name                      = "queue_ia.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}

# autorisation lambda ia for SQS1
resource "aws_sqs_queue_policy" "sqs_capture_ai_policy" {
  queue_url = aws_sqs_queue.sqs_queue_ia.id
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
            "Resource": "${aws_lambda_function.ai_lambda.arn}/*"
        }
    ]
}
EOF
}

resource "aws_sqs_queue_policy" "my_sqs_policy_ai" {
  queue_url = aws_sqs_queue.sqs_queue_ia.id

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
      "Resource": "${aws_sqs_queue.sqs_queue_ia.arn}"
    }
  ]
}
POLICY
}

resource "aws_sqs_queue" "sqs_queue_capture" {
  name                      = "queue_capture.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

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