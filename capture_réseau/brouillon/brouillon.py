import threading
import time
import requests as r
from scapy.all import *


def get_url(url):
    i =0
    for i in range (10):
        time.sleep(1.5)
        r.get(url)

def capture(url, interface, filename):
    print("____ Start _____")
    IP_used = socket.gethostbyname(url)
    pkts_sniffed = sniff(filter='host ' + IP_used, iface=interface, timeout=10)
    pkts_sniffed.summary()
    wrpcap(filename, pkts_sniffed)


if __name__ == "__main__":
    start = time.perf_counter()
    threads = []
    t = threading.Thread(target=get_url, args=("https://www.lemonde.fr",))
    m = threading.Thread(target=capture, args=("www.lemonde.fr","en0","Capture.pcapng",))
    t.start()
    m.start()
    threads.append(t)
    threads.append(m)
    for thread in threads:
        thread.join()
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')