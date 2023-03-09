resource "aws_sqs_queue" "sqs_queue" {
  name                      = "queue_ia_mm.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}

resource "aws_sqs_queue" "sqs_queue_capture" {
  name                      = "queue_capture_mm.fifo"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  fifo_queue                  = true

}