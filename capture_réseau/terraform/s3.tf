resource "aws_s3_bucket" "network_bucket" {
  bucket = "network-bucket-mmarcelin"
  force_destroy = true
}

resource "aws_s3_object" "keras_model"{
  bucket = aws_s3_bucket.network_bucket.bucket
  acl = "public-read"
  for_each = fileset("./documents/", "**")
  key = each.value
  source = "./files/model_lstm/${each.value}"
  etag = filemd5("./files/model_lstm/${each.value}")
}

