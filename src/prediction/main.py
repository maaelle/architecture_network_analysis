import zipfile

import boto3
import numpy as np
import ramda as R
from pandas import json_normalize
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

from constants import *
from mongo import push_data_to_mongo_collections


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


def preprocess_x(messages):
    return R.pipe(
        R.pluck("Body"),
        R.map(R.dissoc("url")),
        R.map(json_normalize),
        R.map(scale),
    )(messages)


def get_all_links(messages):
    return R.pipe(R.pluck("Body"), R.pluck("url"))(messages)


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


def push_all_kind_pred(links_pred, kind, collection):
    kind_url = list(filter(lambda p: p == kind, links_pred))
    return push_data_to_mongo_collections(collection, kind_url)


def push_all_malicious_pred(links_pred):
    return push_all_kind_pred(links_pred, PRED_MALICIOUS, MALICIOUS_COLLECTION)


def push_all_accepted_pred(links_pred):
    return push_all_kind_pred(links_pred, PRED_ACCEPTED, ACCEPTED_COLLECTION)


def lambda_handler(event):
    s3 = boto3.resource("s3")
    model = get_model(s3)

    sqs = boto3.client("sqs")
    all_msgs = get_all_msgs_from_queue(sqs, SQS_LINK_RECEIVED)

    x = preprocess_x(all_msgs)
    links = get_all_links(all_msgs)
    pred = model.predict(x)

    links_pred = list(zip(links, pred))
    push_all_malicious_pred(links_pred)
    push_all_accepted_pred(links_pred)

    delete_all_msgs_from_queue(sqs, SQS_LINK_RECEIVED, all_msgs)
