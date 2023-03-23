# Only works in bash prompt!
# or replace manually the AWS_ACCOUNT_ID by your own ID

# constants to change
REGION=eu-west-1
AWS_ACCOUNT_ID:=$(shell cat aws_account_id.json)
IMAGE_NAME=capture_and_pred
VERSION=latest

# no need to change
ECR_LINK =$(AWS_ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com/$(IMAGE_NAME)

install_libs:
	echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
	apt install -y --force-yes wireshark nmap

install_deps:
	python3 -m pip install -r requirements.txt


install:
	@echo "\e[1;34m Installing Dependencies... $<\e[0m"
	python3.9 -m pip install -r requirements.txt

build:
	@echo "\e[1;34m Building the docker image... $<\e[0m"
	docker build -t $(IMAGE_NAME) .

aws_docker_register: build
	@echo "\e[1;34m Registering the docker.. $<\e[0m"
	aws ecr get-login-password --region $(REGION) | docker login --username AWS \
 		 --password-stdin $(ECR_LINK)

tag_image: aws_docker_register
	@echo "\e[1;34m Tagging the image... $<\e[0m"
	docker tag $(IMAGE_NAME):$(VERSION) $(ECR_LINK):$(VERSION)


deploy: tag_image
	@echo "\e[1;34m deploying... $<\e[0m"
	docker push $(ECR_LINK):$(VERSION)