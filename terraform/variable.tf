variable "region" {
  default = "eu-west-1"
}

variable "source_dir_lambda" {
  description = "source dir where we can find the source code of the lambda"
  default     = "./files/empty_package.zip"
  type        = string
}

variable "handler_empty_unknown_urls" {
  description = "handler function to take in which file"
  default     = "main.lambda_handler"
  type        = string
}

variable "handler_capture" {
  description = "handler function to take in which file"
  default     = "captureandstat.lambda_handler"
  type        = string
}

variable "handler_ia" {
  description = "handler function to take in which file"
  default     = "predict.lambda_handler"
  type        = string
}

variable "handler_refit" {
  description = "handler function to take in which file"
  default     = "refit.lambda_handler"
  type        = string
}


variable "function_name_empty_unknown_urls" {
  description = "function name of the lambda"
  default     = "empty_unknown_urls"
  type        = string
}

variable "function_name_capture" {
  description = "function name of the lambda"
  default     = "capture_stat_lambda"
  type        = string
}

variable "function_name_ia" {
  description = "function name of the lambda"
  default     = "ia_lambda"
  type        = string
}

variable "function_name_refit" {
  description = "function name of the lambda"
  default     = "ia_lambda"
  type        = string
}


