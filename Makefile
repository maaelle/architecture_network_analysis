package_all:
	./bin/capt/package_lamba.sh
	./bin/ia/package_lamba.sh
	./bin/unknown_url/package_lamba.sh

deploy_all: package_all
	./bin/capt/deploy_lambda.sh
	./bin/ia/deploy_lambda.sh
	./bin/unknown_url/deploy_lambda.sh