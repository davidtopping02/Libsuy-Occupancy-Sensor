import asyncio
import logging
from scapy.all import sniff
from collections import Counter


class PackageScanner:

    def __init__(self, interface):
        self.interface = interface
        self.unique_macs = Counter()

    def packet_callback(self, packet):
        src_mac = None

        if packet.haslayer("Ethernet"):
            src_mac = packet["Ethernet"].src
        elif packet.haslayer("Dot11"):
            src_mac = packet["Dot11"].addr2
        if src_mac:
            self.unique_macs[src_mac] += 1

    async def sniff_packets(self, duration_minutes):

        self.unique_macs.clear()

        logging.info(
            f"Starting scan on {self.interface} for {duration_minutes} minutes")

        packets = sniff(iface=self.interface, prn=self.packet_callback,
                        timeout=60*duration_minutes, store=0)

        mac_count = len(self.unique_macs)

        logging.info(f"{mac_count} unique macs found")

        return mac_count

    async def scan(self, scan_duration):

        mac_count = await self.sniff_packets(scan_duration)

        return mac_count
