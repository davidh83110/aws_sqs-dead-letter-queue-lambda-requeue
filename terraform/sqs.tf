// mc-preview dlq
data "aws_sqs_queue" "example" {
  name = "DLQ-example-queue"
}
