resource "aws_s3_bucket" "network_bucket" {
  bucket        = "network-bucket"
  force_destroy = true
}

#resource "aws_s3_object" "keras_model" {
#  bucket = aws_s3_bucket.network_bucket.bucket
#  acl    = "public-read"
#  key    = "model_lstm"
#  source = "./files/model_lstm.zip"
#  etag   = filemd5("./files/model_lstm.zip")
#}
