rm lambda_function_payload_ai.zip
mkdir /tmp/lambda_package
pip3 install -r code/ia/requirements.txt --target /tmp/lambda_package
cp code/ia/predict.py /tmp/lambda_package/predict.py
cd /tmp/lambda_package
zip -r ../lambda_function_payload_ai.zip *
cd ..
rm -rf /tmp/lambda_package