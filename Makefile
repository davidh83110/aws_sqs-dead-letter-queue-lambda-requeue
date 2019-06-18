help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build:
	zip ./dlq-function-`date +%Y-%m-%d:%H:%M:%S`.zip ./*.py -r

init: ## Initial Terraform
	cd ./terraform && terraform init -backend=true -reconfigure

plan: ## Plan Terraform
	cd ./terraform && terraform plan

apply:
	cd ./terraform && terraform apply 

