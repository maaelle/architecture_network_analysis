data "archive_file" "lambda_empty_unknown_urls" {
  source_dir  = var.source_dir_empty_unknown_urls
  output_path = "${path.module}/lambdas/${var.function_name_empty_unknown_urls}.zip"
  type        = "zip"
}