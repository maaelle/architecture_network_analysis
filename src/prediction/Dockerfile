
# https://aws.amazon.com/fr/blogs/machine-learning/using-container-images-to-run-tensorflow-models-in-aws-lambda/


# Pull the base image with python 3.8 as a runtime for your Lambda
FROM python:3.9

RUN apt update && apt upgrade -y

RUN apt install make

COPY ./ ./

# Install the python requirements from requirements.txt
RUN make install

# Set the CMD to your handler
CMD ["predict.lambda_handler"]

