package_capt:
	@echo "\e[1;34m packaging capt... $<\e[0m"
	./bin/capt/package_lambda.sh

package_ia:
	@echo "\e[1;34m packaging ai... $<\e[0m"
	./bin/ia/package_lambda.sh

package_unknown:
	@echo "\e[1;34m packaging unknown... $<\e[0m"
	./bin/unknown_url/package_lambda.sh

package_all:  package_unknown package_capt #package_ia
	@echo "\e[1;34m package all done $<\e[0m"

deploy_capt: package_capt
	@echo "\e[1;34m deploying capt... $<\e[0m"
	./bin/capt/deploy_lambda.sh

deploy_ia: package_ia
	@echo "\e[1;34m deploying ai... $<\e[0m"
	./bin/ia/deploy_lambda.sh

deploy_unknown: package_unknown
	@echo "\e[1;34m deploying unknown... $<\e[0m"
	./bin/unknown_url/deploy_lambda.sh


deploy_all: deploy_unknown deploy_capt #deploy_ia
	@echo "\e[1;34m deploy all done $<\e[0m"

clean:
	rm *.zip
	@echo "\e[1;34m all zip files deleted. $<\e[0m"

deploy_clean: deploy_all clean
	@echo "\e[1;34m done $<\e[0m"