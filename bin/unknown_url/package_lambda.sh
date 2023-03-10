rm lambda_function_payload3.zip
mkdir lambda_package
pip3 install -r src/unknown_url/requirements.txt --target lambda_package
cp src/unknown_url/main.py lambda_package/main.py
cp src/unknown_url/constants.py lambda_package/constants.py
cp src/unknown_url/mongo.py lambda_package/mongo.py
cd lambda_package
zip -r ../lambda_function_payload3.zip *
cd ..
rm -rf lambda_package