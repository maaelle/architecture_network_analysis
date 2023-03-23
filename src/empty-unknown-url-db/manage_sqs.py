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
                "MessageAttributes": lambda x: {
                    "from": {"StringValue": "url", "DataType": "String"}
                },
            }
        )
    )(list_of_values)
