rm lambda_function_payload3.zip
mkdir lambda_package
cp src/empty-unknown-url-db/* lambda_package
cd lambda_package
echo "\e[1;34m installing dependencies... \e[0m"
pip3 install -r requirements.txt --target . > /dev/null
echo "\e[1;34m compressing... \e[0m"
zip -r ../lambda_function_payload3.zip * > /dev/null
cd ..
rm -rf lambda_package