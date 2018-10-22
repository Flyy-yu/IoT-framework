# the basic command: ping 8.8.8.8
# tcpdump -i en0 -I -w cap.pcap -c 10
from tools.Utility import *


class Tcpdump(UtilityTool):
    def __init__(self, config_file):
        super(Tcpdump, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'tcpdump -i {} -I -w ~/Desktop/mycap.pcap -c {}'.format(cmd['interface'], cmd['amount'])
        return command

if __name__ == "__main__":
    print 'it work :)'