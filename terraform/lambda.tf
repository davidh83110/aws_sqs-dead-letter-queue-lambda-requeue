module "lambda-DLQ" {
  source = "git::ssh://git@github.com/davidh83110/terraform-modules-template.git//serverless/lambda"
 
  s3_bucket               = "bucket-name"
  role_arn                = "${data.aws_iam_role.dlq.arn}"
  deployment_package_path = "../function/${var.lambda_deployment_package}"
  function_name           = "Dead-Letter-Queue-requeue"
  stage                   = "${var.lambda_stage}"
  handler                 = "lambda_function.lambda_handler"
  subnet_ids              = []
  runtime                 = "python3.7"
  security_group_id       = ""
}