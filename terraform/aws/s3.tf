resource "aws_s3_bucket" "network_bucket" {
  bucket = "network-bucket-mmarcelin"
  force_destroy = true
}

resource "aws_s3_object" "keras_model"{
  bucket = aws_s3_bucket.network_bucket.bucket
  acl = "public-read"
  key    = "model_lstm"
  source = "./files/model_lstm.zip"

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  etag = filemd5("./files/model_lstm.zip")
}

