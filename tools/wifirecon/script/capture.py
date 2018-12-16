from scapy.all import *


class Capture:
    def __init__(self, interface):
        self.interface = interface

    def file_capture(self, number, path):
        packets = sniff(iface=self.interface, prn=lambda x: x.summary(), count=number)
        wrpcap(path, packets)

    def live_capture(self, number):
        packets = sniff(iface=self.interface, prn=lambda x: x.summary(), count=number)
        return packets


if __name__ == "__main__":
    path = "/home/iot/Desktop/temp.pcap"
    test = Capture('wlan0', path)
    test.file_capture(100)
