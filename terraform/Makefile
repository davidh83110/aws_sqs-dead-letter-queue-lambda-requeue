help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

build:
	cd ../function && zip ./dlq-function-`date +%Y-%m-%d:%H:%M:%S`.zip ./ -r

update: ## Update all modules 
	terraform get -update

init: ## Initial Terraform
	terraform init -backend=true -reconfigure

plan: ## Plan Terraform
	terraform plan

apply:
	terraform apply 

