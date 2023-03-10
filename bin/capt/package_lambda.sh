rm lambda_function_payload.zip
mkdir lambda_package
pip3 install -r src/capture/requirements.txt --target lambda_package
cp src/capture/captureandstat.py lambda_package/captureandstat.py
cd lambda_package
zip -r ../lambda_function_payload.zip *
cd ..
rm -rf lambda_package