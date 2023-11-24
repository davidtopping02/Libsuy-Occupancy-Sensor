from scapy.all import sniff
from collections import Counter
import time

# Global variables
unique_macs = Counter()
mac_counts_array = []

def packet_callback(packet):
    if packet.haslayer("Ethernet"):
        src_mac = packet["Ethernet"].src
        unique_macs[src_mac] += 1

    elif packet.haslayer("Dot11"):
        src_mac = packet["Dot11"].addr2
        unique_macs[src_mac] += 1

def capture_packets(interface, duration_minutes):
    start_time = time.time()
    end_time = start_time + duration_minutes * 60

    print(f"Capturing packets on interface {interface} for {duration_minutes} minutes...")

    # Capture packets for the specified duration
    packets = sniff(iface=interface, prn=packet_callback, timeout=100, store=0)

    # Process the captured packets
    for packet in packets:
        packet_callback(packet)

    # Capture is finished, calculate the number of unique MAC addresses
    num_unique_macs = len(unique_macs)

    # Print and store the result
    print(f"Number of Unique MAC Addresses: {num_unique_macs}")
    mac_counts_array.append(num_unique_macs)

    # Reset the counters for the next iteration
    unique_macs.clear()

    # Sleep until the next capture interval
    sleep_duration = end_time - time.time()
    if sleep_duration > 0:
        time.sleep(sleep_duration)


if __name__ == "__main__":

    network_interface = "wlan1mon"
    capture_duration_minutes = 2

    try:
        # Continuously capture packets every two minutes
        while True:
            capture_packets(network_interface, duration_minutes=capture_duration_minutes)
            
    except KeyboardInterrupt:
        print("Capture stopped.")
