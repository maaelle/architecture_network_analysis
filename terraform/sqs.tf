# SQS capture
resource "aws_sqs_queue" "sqs_capture" {
  name                      = "sqs_capture.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}


resource "aws_sqs_queue_policy" "sqs_url_capture_policy" {
  queue_url = aws_sqs_queue.sqs_capture.id
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



# SQS IA
resource "aws_sqs_queue" "sqs_ia" {
  name                      = "sqs_ia.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}

# autorisation lambda ia for SQS
resource "aws_sqs_queue_policy" "sqs_capture_ai_policy" {
  queue_url = aws_sqs_queue.sqs_ia.id
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
            "Resource": "${aws_lambda_function.ia_lambda.arn}/*"
        }
    ]
}
EOF
}

# SQS pred
resource "aws_sqs_queue" "sqs_pred" {
  name                      = "sqs_pred.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}

/*
# autorisation lambda ia for SQS
resource "aws_sqs_queue_policy" "sqs_capture_pred_policy" {
  queue_url = aws_sqs_queue.sqs_pred.id
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
            "Resource": "${aws_lambda_function.refit_lambda.arn}/*"
        }
    ]
}
EOF
}
*/