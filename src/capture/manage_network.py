import contextlib
import socket
import statistics

from scapy.sendrecv import sniff
from scapy.utils import wrpcap


def calculate_metrics(pkts):
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
    fwd_packet_length_variance = statistics.variance(fwd_packet_lengths)
    bwd_packet_length_variance = statistics.variance(bwd_packet_lengths)

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


def write_file_with_sniffed_data(url, interface, filename):
    with contextlib.suppress(Exception):
        if "https://" in url:
            url = url.split("https://")[-1]
        elif "http://" in url:
            url = url.split("http://")[-1]
        IP_used = socket.gethostbyname(url)
        pkts_sniffed = sniff(filter=f"host {IP_used}", iface=interface, timeout=10)
        pkts_sniffed.summary()
        wrpcap(filename, pkts_sniffed)
