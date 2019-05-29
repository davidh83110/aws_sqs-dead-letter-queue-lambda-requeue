module "sqs" {
  source = "git::https://github.com/davidh83110/terraform_ecs_template//sqs"

  sqs_name    = "${var.sqs_name}"
  AWS_ACCOUNT = "${var.AWS_ACCOUNT}"

  //equal to 256KB
  sqs_max_msg_size               = "262144"
  sqs_VISIBILITY_TIMEOUT_SECONDS = "300"
  sqs_DELAY_SECONDS              = "0"
  sqs_MESSAGE_RETENTION_SECONDS  = "1209600"
  sqs_RECEIVE_WAIT_TIME_SECONDS  = "0"
  sqs_redrive_policy             = "{\"deadLetterTargetArn\":\"${module.lambda-DLQ.lambda_arn}\",\"maxReceiveCount\":1}"
}


resource "aws_sqs_queue" "dlq-default" {
  name                       = "DLQ-${var.sqs_name}"
  max_message_size           = "262144"
  visibility_timeout_seconds = "300"
  delay_seconds              = "0"
  receive_wait_time_seconds  = "0"
}

resource "aws_sqs_queue_policy" "dlq-policy-default" {
  queue_url = "${aws_sqs_queue.dlq-default.id}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "sqspolicy",
  "Statement": [
    {
      "Sid": "allowSameAccountSendMessage",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "sqs:SendMessage",
      "Resource": "${aws_sqs_queue.dlq-default.arn}",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:${var.AWS_REGION}:${var.AWS_ACCOUNT}:*"
        }
      }
    }
  ]
}
POLICY
}
