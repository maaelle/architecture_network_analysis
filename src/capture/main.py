import contextlib
import pickle
import statistics

import pandas as pd
import pyshark
import ramda as R
import requests
from scapy.all import *

from constants import SQS_ENDPOINT, SQS_UNKNOWN_URL
from manage_mongo import insert_kind_data
from manage_sqs import create_sqs_client

PREDICTION_KIND = {
    "0": "malicious",
    "1": "benign",
}

warnings.simplefilter("ignore")


def calculate_metrics(pkts):
    print(len(pkts))

    # Initialize variables to keep track of the packet lengths and times
    global dest_port
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    times = []
    init_win_bytes_forward = 0
    total_length_of_fwd_packets = 0
    bwd_header_length = 0
    subflow_fwd_bytes = 0
    subflows = {}

    # Loop through each packet in the capture
    for pkt in pkts:
        dest_port = pkt.tcp.dstport
        # Check if the packet is a forward or backward packet
        if pkt.ip.src < pkt.ip.dst:
            fwd_packet_lengths.append(int(pkt.length))
            total_length_of_fwd_packets += int(pkt.length)
            init_win_bytes_forward = int(pkt.tcp.window_size_value)
        else:
            bwd_packet_lengths.append(int(pkt.length))
            if len(dir(pkt.tcp)) > 89:
                bwd_header_length += int(pkt.tcp.options.size)

        if "TCP" in pkt and "MPTCP" in pkt:
            subflow_key = (
                f"{pkt['IP'].src}:{pkt['TCP'].sport}-{pkt['IP'].dst}:{pkt['TCP'].dport}"
            )
            if subflow_key not in subflows:
                subflows[subflow_key] = pkt["TCP"].seq
            else:
                subflows[subflow_key] = max(subflows[subflow_key], pkt["TCP"].seq)

        # Add the time of the packet to the list of times
        times.append(pkt.sniff_time.timestamp())

    # Calculate the packet length variance
    if len(fwd_packet_lengths):
        fwd_packet_length_variance = statistics.variance(fwd_packet_lengths)
    else:
        fwd_packet_length_variance = 0

    if len(bwd_packet_lengths):
        bwd_packet_length_variance = statistics.variance(bwd_packet_lengths)
    else:
        bwd_packet_length_variance = 0

    subflow_fwd_bytes = sum(subflows.values())

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
    if "https://" not in url or "http//" not in url:
        url = "https://" + url
    for _ in range(10):
        with contextlib.suppress(Exception):
            time.sleep(1)
            requests.get(url).close()


def write_file_with_sniffed_data(url, interface, filename):
    if "https://" in url:
        url = url.split("https://")[-1]
    elif "http://" in url:
        url = url.split("http://")[-1]
    IP_used = socket.gethostbyname(url)
    pkts_sniffed = sniff(filter=f"host {IP_used}", iface=interface, timeout=10)
    pkts_sniffed.summary()
    wrpcap(filename, pkts_sniffed)
    print("writingdone")


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


def capture(url, interface, filename):
    print("_ Start _")
    threads = [
        threading.Thread(
            target=write_file_with_sniffed_data, args=(url, interface, filename)
        ),
        threading.Thread(target=get_url, args=(url,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def get_x(filename):
    return R.pipe(
        stat,
        R.prop("data"),
        pd.json_normalize,
        lambda x: x.to_numpy(),
    )(filename)


def load_model(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


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
            with contextlib.suppress(Exception):
                url = msg["Body"][1:-1]
                print(url)
                capture(url, "Wi-Fi", filename)
                x = get_x(filename)
                model = load_model("ai.sav")
                prediction = PREDICTION_KIND[str(model.predict(x)[0])]
                print(prediction)
                if prediction == "benign":
                    insert_kind_data("accepted_urls", {"url": url})
                else:
                    insert_kind_data("malicious_urls", {"url": url})
            sqs.delete_message(
                QueueUrl=SQS_UNKNOWN_URL,
                ReceiptHandle=msg["ReceiptHandle"],
            )


if __name__ == "__main__":
    lambda_handler("", "")
