# capture.py
import pyshark


def capture_live_packets(network_interface):
    capture = pyshark.LiveCapture(interface=network_interface)
    for raw_packet in capture.sniff_continuously():
        print(raw_packet)


def get_packet_details(packet):
    """
    This function is designed to parse specific details from an individual packet.
    :param packet: raw packet from either a pcap file or via live capture using TShark
    :return: specific packet details
    """
    protocol = packet.transport_layer
    source_address = packet.ip.src
    source_port = packet[packet.transport_layer].srcport
    destination_address = packet.ip.dst
    destination_port = packet[packet.transport_layer].dstport
    packet_time = packet.sniff_time
    return f'Packet Timestamp: {packet_time}' \
           f'\nProtocol type: {protocol}' \
           f'\nSource address: {source_address}' \
           f'\nSource port: {source_port}' \
           f'\nDestination address: {destination_address}' \
           f'\nDestination port: {destination_port}\n'


capture_live_packets('WiFi')
