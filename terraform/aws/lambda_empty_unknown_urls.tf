resource "aws_lambda_function" "empty_unknown_urls" {
  filename      = data.archive_file.lambda_empty_unknown_urls.output_path
  function_name = var.function_name_empty_unknown_urls
  role          = ""
  handler       = var.handler_empty_unknown_urls

  source_code_hash = data.archive_file.lambda_empty_unknown_urls.output_base64sha256

  runtime = "python3.9"
}