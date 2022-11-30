# ------------------  utils  ---------------------------

variable "region" {
  default = "eu-west-1"
}

# ------------------  S3  ---------------------------

variable "s3_user_bucket_name" {
  description = "Nom du bucket"
  type        = string
}

variable "s3_full_access_policy" {
  description = "Arn of the s3 full access policy"
  default = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# ------------------ Lambda ---------------------------

variable "data_processing_lambda_lambda_name" {
  description = "Nom de la lambda"
  type        = string
}

# ------------------ Athena -----------------------------

variable "athena_db_name" {
  description = "Nom de la db Athena"
  type        = string
}

variable "athena_results_key_bucket_name" {
  description = "Chemin vers le bucket pour stocker les résultats des requêtes Athena"
  type        = string
}

variable "processed_job_offers_key_name" {
  description = "Chemin menant aux offres d'emploies traitées par la lambda"
  type        = string
}

# ------------------ EC2 -----------------------------

variable "ami_id" {
  description = "id of an ami by default it's ubuntu 20.04"
  type        = string
  default     = "ami-06fd8a495a537da8b"
}

variable "instance_type" {
  description = "aws ec2 instance type"
  type        = string
  default     = "t2.micro"
}

variable "tag_name" {
  description = "Aws tag name permit to search an instance by tag"
  type        = string
  default     = "esme"
}

variable "aws_public_key_ssh_path" {
  description = "The key name of the Key Pair to use for the instance"
  type        = string
}

variable "aws_private_key_ssh_path" {
  description = "The key name of the Key Pair to use for the instance"
  type        = string
}

variable "aws_keypair_name" {
  type    = string
  default = "admin"
}
