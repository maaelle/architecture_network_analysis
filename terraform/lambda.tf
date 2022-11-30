resource "aws_lambda_function" "is_url_ok" {
  function_name = "is_url_ok"
  role          = ""
}

resource "aws_lambda_function" "url_listening" {
  function_name = "url_listening"
  role          = ""
}

resource "aws_lambda_function" "url_prediction" {
  function_name = "url_prediction"
  role          = ""
}

resource "aws_lambda_function" "malicious_analysis" {
  function_name = "malicious_analysis"
  role          = ""
}

resource "aws_lambda_function" "malicious_fuzzy_logic" {
  function_name = ""
  role          = ""
}