import boto3


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
