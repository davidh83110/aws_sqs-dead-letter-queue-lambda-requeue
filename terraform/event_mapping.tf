resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = "${data.aws_sqs_queue.example.arn}"
  function_name    = "${module.lambda-DLQ.lambda_arn}"
  batch_size       = 1
}