install:
	python3.9 -m pip install -r requirements.txt

build:
	docker build -t lambda_tensorflow_predict .

create_ecr:
	aws ecr create-repository \
		--repository-name lambda-tensorflow-example \
		--image-scanning-configuration scanOnPush=true \
		--region eu-west-1