import threading
from scapy.all import sniff
from collections import Counter
import time

class PackageScanner:
    
    def __init__(self, interface, duration_minutes):
        self.interface = interface
        self.duration_minutes = duration_minutes
        self.unique_macs = Counter()
        self.mac_counts_array = []
        self.sniffing_flag = threading.Event()

    def packet_callback(self, packet):
        src_mac = None

        if packet.haslayer("Ethernet"):
            src_mac = packet["Ethernet"].src
        elif packet.haslayer("Dot11"):
            src_mac = packet["Dot11"].addr2

        if src_mac:
            self.unique_macs[src_mac] += 1

    def print_runtime(self, start_time):
        while self.sniffing_flag.is_set():
            current_time = time.time()
            elapsed_time = current_time - start_time
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print(f"Elapsed time: [{formatted_time}]")
            time.sleep(60)

    def sniff_packets(self):
        self.sniffing_flag.set()

        print(f"Starting sniff on {self.interface} for {self.duration_minutes} minutes")
        packets = sniff(iface=self.interface, prn=self.packet_callback, timeout=60 * self.duration_minutes, store=0)
        print("Finished sniffing")

        print("Calculating unique MACs")
        num_unique_macs = len(self.unique_macs)

        print(f"Number of Unique MAC Addresses: {num_unique_macs}")
        self.mac_counts_array.append(num_unique_macs)
        self.unique_macs.clear()

        self.sniffing_flag.clear()

    def capture_packets(self):
        while True:
            start_time = time.time()

            # Run sniff asynchronously
            sniffer_thread = threading.Thread(target=self.sniff_packets)
            sniffer_thread.start()

            # Run print_runtime asynchronously
            timer_thread = threading.Thread(target=self.print_runtime, args=(start_time,))
            timer_thread.start()

            # Wait for the sniffing thread to complete
            sniffer_thread.join()
            timer_thread.join()