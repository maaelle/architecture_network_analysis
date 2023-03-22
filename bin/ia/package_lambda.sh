rm lambda_function_payload_ai.zip
mkdir lambda_package
cp src/prediction-scikit/* lambda_package/
cd lambda_package
pip3 install -r requirements.txt --target .
zip -r ../lambda_function_payload_ai.zip *
cd ..
rm -rf lambda_package