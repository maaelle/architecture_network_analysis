import json

import ramda as R

from constants import SQS_ENDPOINT, SQS
from manage_mongo import get_all_unknown_urls, delete_all_unknown_urls
from manage_sqs import create_sqs_client, send_message_batch


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


def send_unknown_to_sqs(sqs):
    return R.pipe(
        get_all_unknown_urls,
        R.uniq_by(R.prop("url")),
        generate_messages,
        send_message_batch(sqs, SQS),
    )()


def lambda_handler(event, lambda_context):
    sqs = create_sqs_client(SQS_ENDPOINT)
    sqs_response = send_unknown_to_sqs(sqs)
    delete_all_unknown_urls()
    return {
        "statusCode": 200,
        "sqs_response": json.dumps(sqs_response),
    }
