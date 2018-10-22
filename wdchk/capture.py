from scapy.all import *

def pkt_callback(pkt):
    pkt.show() # debug statement

sniff(iface="en0", prn=pkt_callback, store=0)


# sudo ifconfig wlx9cefd5fd8f86 down

# sudo iwconfig wlx9cefd5fd8f86 mode monitor

# sudo ifconfig wlx9cefd5fd8f86 up