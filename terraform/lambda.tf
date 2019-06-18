module "lambda-DLQ" {
  source = "git::https://github.com/davidh83110/terraform_ecs_template//lambda"
 
  s3_bucket               = "${var.lambda_s3_bucket_name}"
  role_arn                = "${data.aws_iam_role.dlq.id}"
  deployment_package_path = "${var.lambda_deployment_package}"
  function_name           = "DLQ-${var.sqs_name}"
  stage                   = "${var.lambda_stage}"
  handler                 = "lambda_function.lambda_handler"
  subnet_ids              = []
  runtime                 = "python3.7"
  security_group_id       = ""
}
