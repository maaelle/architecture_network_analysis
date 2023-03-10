import zipfile

import boto3
import numpy as np
from pandas import json_normalize
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model


def recup_model():
    s3 = boto3.resource("s3")
    s3.meta.client.download_file(
        "test-bucket-mmarcelin", "model_lstm.zip", "/tmp/model_lstm.zip"
    )
    return load_model(zipfile.ZipFile("/tmp/model_lstm.zip", "r"))

def pred(x, model):
    scaler = StandardScaler()
    scaler.fit(x)
    x_scaled = scaler.transform(x)
    x_reshape = np.reshape(np.array(x_scaled), (x.shape[0], 1, x.shape[1]))
    pred = model.predict(x_reshape)
    return np.argmax(pred)

def send_message(prediction):
    sqs = boto3.client('sqs')
    sqs.send_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_pred.fifo",
        DelaySeconds=10,
        MessageBody=prediction
    )


def lambda_handler():
    # récuperer le message JSON
    sqs = boto3.client("sqs")
    response = sqs.receive_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_pred.fifo",
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        VisibilityTimeout=0,
        WaitTimeSeconds=0,
    )
    message = response["Messages"]
    for i in range(len(message)):
        data = message[i]["Body"]
        x = json_normalize(data["data"])
        # récupérer model sur S3
        model = recup_model()
        # lancer la prediction
        prediction = pred(x, model)
        send_message(prediction)
        sqs.delete_message(
            QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_ia.fifo",
            ReceiptHandle=message[i]["ReceiptHandle"],
        )
