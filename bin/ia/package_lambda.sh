rm lambda_function_payload_ai.zip
mkdir /tmp/lambda_package
pip3 install -r src/prediction-scikit/requirements.txt --target /tmp/lambda_package
cp src/prediction-sckit/* /tmp/lambda_package/
cd /tmp/lambda_package
zip -r ../lambda_function_payload_ai.zip *
cd ..
rm -rf /tmp/lambda_package