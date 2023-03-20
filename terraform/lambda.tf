####### lambda unknown url
resource "aws_lambda_function" "empty_unknown_urls" {
  filename      = "files/empty_package.zip"
  function_name = var.function_name_empty_unknown_urls
  role          = aws_iam_role.unknown_urls_lambda_role.arn
  handler       = var.handler_empty_unknown_urls


  runtime = "python3.8"
}

# aws_cloudwatch_event_rule scheduled action every minute
resource "aws_cloudwatch_event_rule" "schedule_event" {
  name        = "schedule_event"
  schedule_expression = "rate(1 minute)"
}
# aws_cloudwatch_event_target to link the schedule event and the lambda function
resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.schedule_event.name
  target_id = "lambda"
  arn       = aws_lambda_function.empty_unknown_urls.arn
}

# aws_lambda_permission to allow CloudWatch (event) to call the lambda function
resource "aws_lambda_permission" "allow_cloudwatch" {
    statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.empty_unknown_urls.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule_event.arn

}


####### lambda catpure
resource "aws_lambda_function" "capture_stat_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "files/empty_package.zip"
  function_name = var.function_name_capture
  role          = aws_iam_role.lambda_capture_role.arn
  handler       = var.handler_capture

  runtime = "python3.8"

}

resource "aws_lambda_event_source_mapping" "event_sqs_capture" {
  event_source_arn = aws_sqs_queue.sqs_capture.arn
  function_name    = aws_lambda_function.capture_stat_lambda.arn
}

########## lambda ia
resource "aws_lambda_function" "ia_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  #filename      = "files/empty_package.zip"
  function_name = var.function_name_ia
  role          = aws_iam_role.lambda_ia_role.arn
  handler       = var.handler_ia
  package_type  = "Image"
  image_uri = "715437275066.dkr.ecr.eu-west-1.amazonaws.com/test_lambda:tag"

  runtime = "python3.8"

}

resource "aws_lambda_event_source_mapping" "event_sqs_ia" {
  event_source_arn = aws_sqs_queue.sqs_ia.arn
  function_name    = aws_lambda_function.ia_lambda.arn
}

########## lambda refit
/*
resource "aws_lambda_function" "refit_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "files/empty_package.zip"
  function_name = var.function_name_refit
  role          = aws_iam_role.refit_lambda_role.arn
  handler       = var.handler_refit

  runtime = "python3.8"

}

resource "aws_lambda_event_source_mapping" "event_sqs_refit" {
  event_source_arn = aws_sqs_queue.sqs_pred.arn
  function_name    = aws_lambda_function.refit_lambda.arn
}
*/