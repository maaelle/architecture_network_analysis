import zipfile

import boto3
import numpy as np
import ramda as R
from pandas import json_normalize
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

from constants import SQS_LINK_RECEIVED


def get_model(s3):
    s3.meta.client.download_file(
        "test-bucket-mmarcelin", "model_lstm.zip", "/tmp/model_lstm.zip"
    )
    return load_model(zipfile.ZipFile("/tmp/model_lstm.zip", "r"))


def scale(x):
    return np.reshape(
        np.array(StandardScaler().fit_transform(x)),
        (x.shape[0], 1, x.shape[1]),
    )


def send_message(sqs, msg, link):
    sqs.send_message(
        QueueUrl=link,
        DelaySeconds=10,
        MessageBody=msg,
    )


def preprocess_x(x):
    return R.pipe(
        R.pluck("Body"),
        R.map(json_normalize),
        R.map(scale),
    )(x)


def get_all_msgs_from_queue(sqs, link):
    return sqs.receive_message(
        QueueUrl=link,
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        VisibilityTimeout=0,
        WaitTimeSeconds=0,
    )["Messages"]


def delete_msg_from_queue(sqs, link):
    return lambda message: sqs.delete_message(
        QueueUrl=link,
        ReceiptHandle=message["ReceiptHandle"],
    )


def delete_all_msgs_from_queue(sqs, link, all_messages):
    destructor = delete_msg_from_queue(sqs, link)
    return map(destructor, all_messages)


def lambda_handler(event):
    s3 = boto3.resource("s3")

    model = get_model(s3)

    sqs = boto3.client("sqs")

    all_msgs = get_all_msgs_from_queue(sqs, SQS_LINK_RECEIVED)

    x = preprocess_x(all_msgs)
    pred = model.predict(x)

    delete_all_msgs_from_queue(sqs, SQS_LINK_RECEIVED, all_msgs)
