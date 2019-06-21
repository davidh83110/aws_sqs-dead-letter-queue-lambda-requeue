// mc-preview event mapping
resource "aws_lambda_event_source_mapping" "mc-high-preview" {
  event_source_arn = "${data.aws_sqs_queue.mc-dlq-high-preview.arn}"
  function_name    = "${module.lambda-DLQ.lambda_arn}"
  batch_size       = 1
}

resource "aws_lambda_event_source_mapping" "mc-default-preview" {
  event_source_arn = "${data.aws_sqs_queue.mc-dlq-default-preview.arn}"
  function_name    = "${module.lambda-DLQ.lambda_arn}"
  batch_size       = 1
}

// mc-production event mapping
resource "aws_lambda_event_source_mapping" "mc-high-production" {
  event_source_arn = "${data.aws_sqs_queue.mc-dlq-high-production.arn}"
  function_name    = "${module.lambda-DLQ.lambda_arn}"
  batch_size       = 1
}

resource "aws_lambda_event_source_mapping" "mc-default-production" {
  event_source_arn = "${data.aws_sqs_queue.mc-dlq-default-production.arn}"
  function_name    = "${module.lambda-DLQ.lambda_arn}"
  batch_size       = 1
}