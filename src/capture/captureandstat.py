import statistics

import boto3
import pyshark
import requests as r
from scapy.all import *


def calculate_metrics(pkts):
    # Initialize variables to keep track of the packet lengths and times
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    times = []
    init_win_bytes_forward = 0
    total_length_of_fwd_packets = 0
    bwd_header_length = 0
    subflow_fwd_bytes = 0

    # Loop through each packet in the capture
    for pkt in pkts:
        dest_port = pkt.tcp.dstport
        # Check if the packet is a forward or backward packet
        if pkt.ip.src < pkt.ip.dst:
            fwd_packet_lengths.append(int(pkt.length))
            total_length_of_fwd_packets += int(pkt.length)
            init_win_bytes_forward = int(pkt.tcp.window_size_value)
            subflow_fwd_bytes += int(pkt.length)
        else:
            bwd_packet_lengths.append(int(pkt.length))
            bwd_header_length += int(pkt.tcp.options.size)

        # Add the time of the packet to the list of times
        times.append(pkt.sniff_time.timestamp())

    # Calculate the packet length variance
    fwd_packet_length_variance = statistics.variance(fwd_packet_lengths)
    bwd_packet_length_variance = statistics.variance(bwd_packet_lengths)

    # Calculate the backward packets per second
    bwd_packets_per_second = len(bwd_packet_lengths) / (times[-1] - times[0])

    # Calculate the average packet size
    total_packet_lengths = fwd_packet_lengths + bwd_packet_lengths
    average_packet_size = sum(total_packet_lengths) / len(total_packet_lengths)

    # Calculate the backward packet length standard deviation
    bwd_packet_length_std = statistics.stdev(bwd_packet_lengths)

    return (
        init_win_bytes_forward,
        dest_port,
        total_length_of_fwd_packets,
        bwd_header_length,
        subflow_fwd_bytes,
        fwd_packet_length_variance,
        bwd_packet_length_variance,
        bwd_packets_per_second,
        average_packet_size,
        bwd_packet_length_std,
    )


def get_url(url):
    i = 0
    for i in range(10):  ## temps limité ici aussi: 10* 1.5s environ
        time.sleep(1.5)
        r.get(url)


def snif(url, interface, filename):
    IP_used = socket.gethostbyname(url)
    pkts_sniffed = sniff(
        filter="host " + IP_used, iface=interface, timeout=10
    )  ## timeout 10 donc peut pas tourner plus
    wrpcap(filename, pkts_sniffed)


def capture(url, interface, filename):
    print("____ Start _____")
    threads = []
    t = threading.Thread(target=get_url, args=(url,))
    m = threading.Thread(
        target=capture,
        args=(
            url,
            interface,
            filename,
        ),
    )
    t.start()
    m.start()
    threads.append(t)
    threads.append(m)
    for thread in threads:
        thread.join()


def stat(filename, url):
    cap = pyshark.FileCapture(filename)
    (
        init_win_bytes_forward,
        dest_port,
        total_length_of_fwd_packets,
        bwd_header_length,
        subflow_fwd_bytes,
        fwd_packet_length_variance,
        bwd_packet_length_variance,
        bwd_packets_per_second,
        average_packet_size,
        bwd_packet_length_std,
    ) = calculate_metrics(cap)
    return {
        "data": [
            {
                "Init_Win_bytes_forward": str(init_win_bytes_forward),
                "Total Length of Fwd Packets": str(total_length_of_fwd_packets),
                "Bwd Header Length": str(bwd_header_length),
                "Destination Port": str(dest_port),
                "Subflow Fwd Bytes": str(subflow_fwd_bytes),
                "Packet Length Std": str(fwd_packet_length_variance),
                "Packet Length Variance": str(bwd_packet_length_variance),
                "Bwd Packets/s": str(bwd_packets_per_second),
                "Average Packet Size": str(average_packet_size),
                "Bwd Packet Length Std": str(bwd_packet_length_std),
                "url": url,
            }
        ]
    }


def send_JSON(Json):
    sqs = boto3.client("sqs")
    sqs.send_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_ia.fifo",
        DelaySeconds=10,
        MessageBody=(Json),
    )


def lambda_handler(event):
    sqs = boto3.client("sqs")
    response = sqs.receive_message(
        QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_capture.fifo",
        AttributeNames=["SentTimestamp"],
        MaxNumberOfMessages=1,
        MessageAttributeNames=["All"],
        VisibilityTimeout=0,
        WaitTimeSeconds=0,
    )
    message = response["Messages"]
    filename = "Capture.pcapng"
    for i in range(len(message)):
        url = message[i]["Body"]
        capture(url, "en0", filename)
        Json = stat(filename, url)
        send_JSON(Json)
        sqs.delete_message(
            QueueUrl="https://sqs.eu-west-1.amazonaws.com/715437275066/sqs_capture.fifo",
            ReceiptHandle=message[i]["ReceiptHandle"],
        )
