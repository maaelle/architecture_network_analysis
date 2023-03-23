import json

import boto3
import ramda as R


def send_message_batch(sqs, queue_url):
    def send(messages):
        if len(messages):
            return sqs.send_message_batch(
                QueueUrl=queue_url,
                Entries=messages,
            )
        else:
            return {"update": "there was no data available in mongo"}

    return send


def create_sqs_client(endpoint: str):
    return boto3.client(
        "sqs",
        endpoint_url=endpoint,
        aws_access_key_id=None,
        aws_secret_access_key=None,
    )


def generate_key(list_or_str):
    return R.pipe(len, id, str)(list_or_str)


def generate_messages(list_of_values):
    message_group_id = generate_key(list_of_values)
    return R.map(
        R.apply_spec(
            {
                "Id": generate_key,
                "MessageBody": json.dumps,
                "MessageGroupId": lambda x: message_group_id,
                "MessageDeduplicationId": generate_key,
            }
        )
    )(list_of_values)


def receive_all_messages(queue_url):
    sqs = boto3.client("sqs")
    messages = []
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=["All"],
            MaxNumberOfMessages=10,
            VisibilityTimeout=0,
            WaitTimeSeconds=0,
        )
        if "Messages" not in response:
            break
        for message in response["Messages"]:
            messages.append(message)
            sqs.delete_message(
                QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
            )
    return messages
