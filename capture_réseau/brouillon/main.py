# Recap des colonnes nécessaires :
## Init_Win_bytes_forward
## Total Length of Fwd Packets
## Bwd Header Length
## Destination Port
## Subflow Fwd Bytes
## Packet Length Std
## Packet Length Variance
## Bwd Packets/s
## Average Packet Size
## Bwd Packet Length Std



from scapy.all import *
from scapy.layers.inet import TCP

# Create the sniffer
sniffer = sniff(timeout=10)

for pkt in sniffer:
    if TCP in pkt:
        print("* TRAME *")
        # comment les récupérer un par un
        # print(pkt[TCP].sport)
        # print(pkt[TCP].dport)
        # afficher toute la trame
        print(pkt.display())