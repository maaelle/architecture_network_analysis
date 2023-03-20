# empty-unknown-urls

## Overview

1. [Constants](#constants)
2. [Configuration](#configuration)
    1. [MongoDB](#mongodb)

## Constants

you can change some variables in the `constants.py` file as:
- LOGIN_MONGO_PATH : the path where the mongo login is, by default it's `mongo_login.json`, see [MongoDB Configuration](#mongodb)
- MALICIOUS : the name of the collection of malicious urls
- UNKNOWN : the name of the collection of unknown urls
- SQS : the link of the SQS in which this lambda sends
- SQS_DELAY : The delay seconds of the SQS timeout

## Configuration

### MongoDB

you need to add to the root of the project a file named `mongo_login.json` with this information inside :
```json
{
  "username": "",
  "password": "",
  "db": ""
}
```