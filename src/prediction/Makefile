# Only works in bash prompt!
# or replace manually the AWS_ACCOUNT_ID by your own ID
REGION=eu-west-1
AWS_ACCOUNT_ID:=$(shell cat aws_account_id.json)
IMAGE_NAME=predict_refit_malicious_tcp_ai
VERSION =1.0.0
ECR_LINK =$(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE_NAME)

test:
	echo $(ECR_LINK)

install:
	@echo "\e[1;34m Installing Dependencies... $<\e[0m"
	python3.9 -m pip install -r requirements.txt

build:
	@echo "\e[1;34m Building the docker image... $<\e[0m"
	docker build -t $(IMAGE_NAME) .

reg_docker: #build
	@echo "\e[1;34m Registering the docker.. $<\e[0m"
	aws ecr get-login-password --region $(REGION) | docker login --username AWS \
 		 --password-stdin $(ECR_LINK)

tag_image: reg_docker
	@echo "\e[1;34m Tagging the image... $<\e[0m"
	docker tag $(IMAGE_NAME):latest $(ECR_LINK):latest


deploy: tag_image
	@echo "\e[1;34m deploying... $<\e[0m"
	docker push $(ECR_LINK):latest