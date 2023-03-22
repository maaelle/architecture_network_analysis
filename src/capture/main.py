import contextlib

import boto3
import pyshark
import ramda as R
import requests as r
from scapy.all import *

from constants import SQS_AI, SQS_UNKNOWN_URL, SQS_ENDPOINT
from manage_network import calculate_metrics
from src.capture.manage_sqs import create_sqs_client


def get_url(url):
    for _ in range(10):
        time.sleep(1.5)
        with contextlib.suppress(Exception):
            r.get(url)


def capture(url, interface, filename):
    threads = [
        Thread(target=get_url, args=(url)),
        Thread(target=capture, args=(url, interface, filename)),
    ]
    map(lambda t: t.start(), threads)
    map(lambda t: t.join(), threads)


def stat(filename):
    return R.pipe(
        pyshark.FileCapture,
        calculate_metrics,
        R.apply_spec(
            {
                "Init_Win_bytes_forward": R.pipe(R.nth(0), str),
                "Total Length of Fwd Packets": R.pipe(R.nth(2), str),
                "Bwd Header Length": R.pipe(R.nth(3), str),
                "Destination Port": R.pipe(R.nth(1), str),
                "Subflow Fwd Bytes": R.pipe(R.nth(4), str),
                "Packet Length Std": R.pipe(R.nth(5), str),
                "Packet Length Variance": R.pipe(R.nth(6), str),
                "Bwd Packets/s": R.pipe(R.nth(7), str),
                "Average Packet Size": R.pipe(R.nth(8), str),
                "Bwd Packet Length Std": R.pipe(R.nth(9), str),
            }
        ),
        R.apply_spec({"data": R.identity}),
    )(filename)


def send_JSON(url, Json):
    sqs = boto3.client("sqs")
    sqs.send_message(
        QueueUrl=SQS_AI,
        DelaySeconds=10,
        MessageBody={{"url": url}, {"json": Json}},
    )


def lambda_handler(event, lambda_context):
    filename = "Capture.pcapng"
    sqs = create_sqs_client(SQS_ENDPOINT)
    while True:
        # voir s'il n'y a pas un autre moyen pour récupéreer tous les msgs du sqs
        # pour se débarrassr de la boucle
        response = sqs.receive_message(
            QueueUrl=SQS_UNKNOWN_URL,
            MessageAttributeNames=["url"],
            AttributeNames=["url"],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=1,
        )
        if "Messages" not in response:
            continue

        for msg in response["Messages"]:
            url = msg["Body"]
            print(url)
            # capture(url, "en0", filename)
            # data = stat(filename)
            # todo: send data & url to sqs ai

            # todo: uncomment this line below once you've finished the capture
            # sqs.delete_message(
            #     QueueUrl=SQS_UNKNOWN_URL,
            #     ReceiptHandle=msg["ReceiptHandle"],
            # )


if __name__ == "__main__":
    lambda_handler("", "")
