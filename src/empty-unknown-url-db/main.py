import json

import ramda as R

from constants import SQS_ENDPOINT, SQS_UNKNOWN_URL
from manage_mongo import get_all_unknown_urls, delete_all_unknown_urls
from manage_sqs import create_sqs_client, send_message_batch, generate_messages


def send_unknown_to_sqs(sqs):
    return R.pipe(
        get_all_unknown_urls,
        R.uniq_by(R.prop("url")),
        generate_messages,
        send_message_batch(sqs, SQS_UNKNOWN_URL),
    )()


def lambda_handler(event, lambda_context):
    sqs = create_sqs_client(SQS_ENDPOINT)
    sqs_response = send_unknown_to_sqs(sqs)
    delete_all_unknown_urls()
    return {
        "statusCode": 200,
        "sqs_response": json.dumps(sqs_response),
    }


if __name__ == "__main__":
    lambda_handler("", "")
