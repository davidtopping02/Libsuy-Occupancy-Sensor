import threading
from scapy.all import sniff
from collections import Counter
import time

# Global variables
unique_macs = Counter()
mac_counts_array = []
sniffing_flag = threading.Event()

def packet_callback(packet):
    src_mac = None

    if packet.haslayer("Ethernet"):
        src_mac = packet["Ethernet"].src
    elif packet.haslayer("Dot11"):
        src_mac = packet["Dot11"].addr2

    if src_mac:
        unique_macs[src_mac] += 1

def printRuntime(startTime):
    while sniffing_flag.is_set():
        currentTime = time.time()
        elapsedTime = currentTime - startTime
        formattedTime = time.strftime("%H:%M:%S", time.gmtime(elapsedTime))
        print(f"Elapsed time: [{formattedTime}]")
        time.sleep(60)

def sniff_packets(interface, duration_minutes):
    global sniffing_flag
    sniffing_flag.set()

    print(f"Starting sniff on {interface} for {duration_minutes} minutes")
    packets = sniff(iface=interface, prn=packet_callback, timeout=60 * duration_minutes, store=0)
    print("Finished sniffing")

    print("Calculating unique MACs")
    num_unique_macs = len(unique_macs)

    print(f"Number of Unique MAC Addresses: {num_unique_macs}")
    mac_counts_array.append(num_unique_macs)
    unique_macs.clear()

    sniffing_flag.clear()

def capture_packets(interface, duration_minutes):
    while True:
        start_time = time.time()

        # Run sniff asynchronously
        snifferThread = threading.Thread(target=sniff_packets, args=(interface, duration_minutes))
        snifferThread.start()

        # Run printRuntime asynchronously
        timerThread = threading.Thread(target=printRuntime, args=(start_time,))
        timerThread.start()

        # Wait for the sniffing thread to complete
        snifferThread.join()
        timerThread.join()

if __name__ == "__main__":
    network_interface = "wlan1mon"
    capture_duration_minutes = 10

    print("START")
    try:
        capture_packets(network_interface, duration_minutes=capture_duration_minutes)

    except KeyboardInterrupt:
        print("CAPTURE INTERUPTED")

    print("END")
