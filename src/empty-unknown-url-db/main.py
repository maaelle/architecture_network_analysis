from collections import Counter

import boto3
import ramda as R

from constants import SQS, SQS_DELAY
from mongo import get_all_unknown_urls, delete_all_unknown_urls


def unique_urls(list_of_urls):
    return list(Counter(list_of_urls).keys())


def send_sqs(sqs):
    return lambda url: sqs.send_message(
        QueueUrl=SQS,
        DelaySeconds=SQS_DELAY,
        MessageBody=url,
    )


def send_all_urls_to_sqs(sqs):
    return lambda list_of_urls: map(send_sqs(sqs), list_of_urls)


def lambda_handler(event):
    sqs = boto3.client("sqs")
    R.pipe(
        get_all_unknown_urls,
        unique_urls,
        send_all_urls_to_sqs(sqs),
        delete_all_unknown_urls,
    )
    return {"statusCode": 200}