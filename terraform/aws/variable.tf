variable "region" {
  default = "eu-west-1"
}

variable "source_dir_empty_unknown_urls" {
  description = "source dir where we can find the source code of the lambda"
  default     = "../../src/empty_unknown_urls"
  type        = string
}

variable "handler_empty_unknown_urls" {
  description = "handler function to take in which file"
  default     = "main.lambda_handler"
  type        = string
}

variable "function_name_empty_unknown_urls" {
  description = "function name of the lambda"
  default     = "empty_unknown_urls"
  type        = string
}

