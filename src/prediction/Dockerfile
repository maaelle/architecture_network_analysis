
# https://aws.amazon.com/fr/blogs/machine-learning/using-container-images-to-run-tensorflow-models-in-aws-lambda/


# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.9

RUN yum check-update && yum update -y

RUN yum install make -y

COPY requirements.txt predict.py Makefile ./

# Install the python requirements from requirements.txt
RUN make install

# Set the CMD to your handler
CMD ["predict.lambda_handler"]

