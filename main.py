from occupancy_counting.package_scanner import PackageScanner


if __name__ == "__main__":
    network_interface = "wlan1mon"
    capture_duration_minutes = 10

    print("START")
    try:
        packet_sniffer = PackageScanner(network_interface, duration_minutes=capture_duration_minutes)
        packet_sniffer.capture_packets()

    except KeyboardInterrupt:
        print("CAPTURE INTERRUPTED")

    print("END")