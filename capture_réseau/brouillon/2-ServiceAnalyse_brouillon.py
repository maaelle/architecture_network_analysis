# Recap des colonnes nécessaires :
## 1) Init_Win_bytes_forward
## 2) Total Length of Fwd Packets
## 3) Bwd Header Length
## 4) Destination Port
## 5) Subflow Fwd Bytes
## 6) Packet Length Std
## 7) Packet Length Variance
## 8) Bwd Packets/s
## 9) Average Packet Size
## 10) Bwd Packet Length Std


import pyshark
import statistics
# IP esme.fr  =  104.21.79.224

import socket
IP_used = socket.gethostbyname('www.lemonde.fr')


#dataCaptured = pyshark.FileCapture('MaCaptureMonde2.pcapng',
#                                   display_filter="ip.addr == 104.21.79.224")

dataCaptured = pyshark.FileCapture('MaCaptureMonde3.pcapng',
                                   display_filter="ip.addr =="+ IP_used)

def calculate_total_length_of_forward_packets(pkts):
    # Initialize a variable to keep track of the total length
    total_length = 0

    # Loop through each packet in the capture
    for pkt in pkts:
        # Extract the IP layer from the packet
        ip_layer = pkt['IP']

        # Check if the packet is a forward packet
        if ip_layer.src < ip_layer.dst:
            # Add the length of the packet to the total length
            total_length += len(pkt)

    return total_length

# to check
def calculate_bwd_header_length(pkts):
    # Initialize a variable to keep track of the total backward header length
    total_bwd_header_length = 0

    # Loop through each packet in the capture
    for pkt in pkts:
        # Check if the packet is a backward packet
        if pkt.ip.src > pkt.ip.dst:
            # Add the length of the IP and transport layer headers to the total backward header length
            total_bwd_header_length += float(pkt['IP'].hdr_len) + float(pkt['TCP'].hdr_len)

    return total_bwd_header_length

#to check
def calculate_subflow_fwd_bytes(pkts):
    # Initialize a variable to keep track of the total forward bytes
    total_fwd_bytes = 0

    # Loop through each packet in the capture
    for pkt in pkts:
        # Check if the packet is a forward packet
        if pkt.ip.src < pkt.ip.dst:
            # Add the length of the packet payload to the total forward bytes
            total_fwd_bytes += int(pkt.length)

    return total_fwd_bytes


def calculate_packet_length_std(pkts):
    # Initialize a list to keep track of the packet lengths
    packet_lengths = []

    # Loop through each packet in the capture
    for pkt in pkts:
        # Add the length of the packet to the list of packet lengths
        packet_lengths.append(int(pkt.length))

    # Calculate the standard deviation of the packet lengths
    packet_length_std = statistics.stdev(packet_lengths)

    return packet_length_std

def calculate_metrics(pkts):
    # Initialize variables to keep track of the packet lengths and times
    fwd_packet_lengths = []
    bwd_packet_lengths = []
    times = []

    # Loop through each packet in the capture
    for pkt in pkts:
        # Check if the packet is a forward or backward packet
        if pkt.ip.src < pkt.ip.dst:
            fwd_packet_lengths.append(int(pkt.length))
        else:
            bwd_packet_lengths.append(int(pkt.length))

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

    return fwd_packet_length_variance, bwd_packet_length_variance, bwd_packets_per_second, average_packet_size, bwd_packet_length_std


packet  = dataCaptured[0]
tcp_layer = packet['TCP']
win_size = tcp_layer.window_size
Init_Win_bytes_forward = float(win_size) / 8
print("IP dst ===", packet['IP'].dst)
print("IP src ===", packet['IP'].src)
print("1) Init_Win_bytes_forward ==", Init_Win_bytes_forward)
print("2) Total Length of Fwd Packets == ",calculate_total_length_of_forward_packets(dataCaptured))
print("3) Bwd Header Length == ", calculate_bwd_header_length(dataCaptured))
print("4) Destination Port == ", tcp_layer.dstport)
print("5) Subflow Fwd Bytes == ", calculate_subflow_fwd_bytes(dataCaptured))
print("6) Packet Length Std == ", calculate_packet_length_std(dataCaptured))
metrics = calculate_metrics(dataCaptured)
print("7) Packet Length Variance == ", metrics[0])
print("8) Bwd Packets/s == ", metrics[2])
print("9) Average Packet Size == ", metrics[3])
print("10) Bwd Packet Length Std == ", metrics[1])




"""

all atribute for tcp
'ack', 'ack_raw', 'analysis', 'analysis_bytes_in_flight', 'analysis_push_bytes_sent', 'checksum', 'checksum_status', 'completeness', 'dstport', 'field_names', 'flags', 'flags_ack', 'flags_ae', 'flags_cwr', 'flags_ece', 'flags_fin', 'flags_push', 'flags_res', 'flags_reset', 'flags_str', 'flags_syn', 'flags_urg', 'get', 'get_field', 'get_field_by_showname', 'get_field_value', 'has_field', 'hdr_len', 'layer_name', 'len', 'nxtseq', 'option_kind', 'option_len', 'options', 'options_nop', 'options_timestamp', 'options_timestamp_tsecr', 'options_timestamp_tsval', 'payload', 'port', 'pretty_print', 'raw_mode', 'seq', 'seq_raw', 'srcport', 'stream', 'time_delta', 'time_relative', 'urgent_pointer', 'window_size', 'window_size_scalefactor', 'window_size_value'

"""
"""
for pkt in dataCaptured:
    #print (pkt)
    protocol = pkt.transport_layer   # ip |  transport_layer
    print ("Protocol is : ", protocol)
    source_address = pkt.ip.src
    print("Source IP adress is : ", source_address)
    source_port = pkt[pkt.transport_layer].srcport
    print("Source port is : ", source_port)
    destination_address = pkt.ip.dst
    print("Destination IP adress is : ", destination_address)
    destination_port = pkt[pkt.transport_layer].dstport
    print("Destination port is : ", destination_port)
    print("---------------------------------------")


paquet = cap[0]
print(paquet['ip'].dst)


i = 1
for paquet in cap:
    print("N° paquet  = ", i)
    print(paquet['ip'].dst)
    i = i+1
"""