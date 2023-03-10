resource "aws_lambda_function" "capture_stat_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "files/empty_package.zip"
  function_name = "capture_stat_lambda"
  role          = aws_iam_role.lambda_capture_role.arn
  handler       = "captureandstat.lambda_handler"

  runtime = "python3.7"

}

resource "aws_lambda_event_source_mapping" "event_sqs_capture" {
  event_source_arn = aws_sqs_queue.sqs_capture.arn
  function_name    = aws_lambda_function.capture_stat_lambda.arn
}


resource "aws_lambda_function" "ai_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  function_name = "ai_lambda"
  role          = aws_iam_role.lambda_ia_role.arn
  handler       = "predict.lambda_handler"
  image_uri = "715437275066.dkr.ecr.eu-west-1.amazonaws.com/ecr_docker_lambda"

  runtime = "python3.7"

}

resource "aws_lambda_event_source_mapping" "event_sqs_ia" {
  event_source_arn = aws_sqs_queue.sqs_ia.arn
  function_name    = aws_lambda_function.ai_lambda.arn
}
