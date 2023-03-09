resource "aws_lambda_function" "capture_stat_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "files/empty_package.zip"
  function_name = "capture_stat_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "captureandstat.lambda_handler"

  runtime = "python3.7"

}

resource "aws_lambda_event_source_mapping" "event_sqs_capture" {
  event_source_arn = aws_sqs_queue.sqs_queue_capture.arn
  enabled          = true
  function_name    = "${aws_lambda_function.capture_stat_lambda.arn}"
  batch_size       = 1
}


resource "aws_lambda_function" "ai_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "files/empty_package.zip"
  function_name = "ai_lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "predict.lambda_handler"

  runtime = "python3.7"

}

resource "aws_lambda_event_source_mapping" "event_sqs_ia" {
  event_source_arn = aws_sqs_queue.sqs_queue.arn
  enabled          = true
  function_name    = "${aws_lambda_function.ai_lambda.arn}"
  batch_size       = 1
}
