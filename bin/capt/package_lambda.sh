rm lambda_function_payload.zip
mkdir lambda_package
cp ./src/capture/* lambda_package/
cd lambda_package
pip3 install -r requirements.txt --target .
zip -r ../lambda_function_payload.zip *
cd ..
rm -rf lambda_package