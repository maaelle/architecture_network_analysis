# predict tcp packet

> **Warning**
> only works on Linux Prompt!

> **Note**
> You need to install **docker** to continue

## Overview

1. [How to deploy](#how-to-deploy)
2. [AWS configuration](#aws-configuration)
   1. [IAM](#iam)
   2. [ECR](#ecr)
3. [MongoDB Configuration](#mongodb-configuration)
4. [Makefile](#makefile)
    1. [Initialization of Makefile variables](#initialization-of-makefile-variables)
    2. [All commands available](#all-commands-available-in-the-makefile)


## How to deploy

you need to respect the following conditions to deploy the app:
- you have created an IAM user and an ECR following this [AWS Configuration](#aws-configuration)
- you have created a `mongo_login.json` file following this [MongoDB Configuration](#mongodb-configuration)

if you respect this conditions, you can then execute [make deploy](#make-deploy)



## AWS Configuration

### IAM
you need to create an IAM user with this policy : `AmazonEC2ContainerRegistryFullAccess`

Then you can type in the terminal `aws configure` and register to this user to continue.

### ECR

you need to create manually an ECR with the same [image name](#imagename) as the docker you have created.

## MongoDB configuration

you need to create a `login.json` file at the root of the directory reproducing this configuration:
```json
{
  "username": "",
  "password": "",
  "db": ""
}
```

then fill the necessary information to permit access to the database.


## Makefile

### Initialization of Makefile variables

#### Overview of All Makefile variables
- [REGION](#region)
- [AWS_ACCOUNT_ID](#aws-account-id)
- [IMAGE_NAME](#image-name)
- [VERSION](#version)

#### REGION

keep `eu-west-1` if you want your ECR in Ireland.

#### AWS_ACCOUNT_ID 

you can create a new file near to this script called `aws_account_id.json` and 
put it your AWS account ID.
No need to put brackets, just write your ID, and it will work.

#### IMAGE_NAME

it will change the image name on your PC. 
> **Note**
> Be careful to put the same image nam as created on aws

#### VERSION

if you want to change the version of the image, by default it's set to `latest`.

### All commands available in the Makefile

#### Overview of all make commands
1. [install](#make-install)
2. [build](#make-build)
3. [aws_docker_register](#make-awsdockerregister)
4. [tag_image](#make-tagimage)
5. [deploy](#make-deploy)

#### `make install`

This command install all dependencies needed listed in the `requirements.txt` file.
It's mostly used by the [make build](#make-build) command

#### `make build`

This command create a new docker image and put all this directory inside.
Then it calls [make install](#make-install)

#### `make aws_docker_register`

This command get login from aws and connect docker to this.
It depends on [make build](#make-build).

#### `make tag_image`

This command give a new tag to the build recently created.
It changes the docker image name by the link of the ECR.
It depends on [make aws_docker_register](#make-awsdockerregister).

#### `make deploy`

This command deploys the build directly to the ECR.
it depends on [make tag_image](#make-tagimage).
