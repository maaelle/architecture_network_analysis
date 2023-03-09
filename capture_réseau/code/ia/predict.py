from tensorflow.keras.models import load_model
from pandas import json_normalize
import numpy as np
from sklearn.preprocessing import StandardScaler
import boto3
import zipfile

def recup_model():
    s3 = boto3.resource('s3')
    s3.meta.client.download_file('test-bucket-mmarcelin', 'model_lstm.zip', '/tmp/model_lstm.zip')
    file = zipfile.ZipFile('/tmp/model_lstm.zip', 'r')
    reconstructed_model = load_model(file)
    return reconstructed_model


def pred(x, model):
    scaler = StandardScaler()
    scaler.fit(x)
    x_scaled = scaler.transform(x)
    x_reshape = np.reshape(np.array(x_scaled), (x.shape[0], 1, x.shape[1]))
    pred = model.predict(x_reshape)
    return np.argmax(pred)

def lambda_handler():
    # récuperer le message JSON
    sqs = boto3.client('sqs')
    queue_url = 'SQS_QUEUE_URL'
    response = sqs.receive_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/queue_ia_mm.fifo",
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message = response["Messages"]
    i = 0
    for i in range(len(message)):
        data = message[i]["Body"]
        x = json_normalize(data['data'])
        # récupérer model sur S3
        model = recup_model()
        # lancer la prediction
        prediction = pred(x, model)
        sqs.delete_message(
            QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/queue_ia_mm.fifo",
            ReceiptHandle=message[i]['ReceiptHandle']
        )

