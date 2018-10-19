# sudo arpspoof -i 10.10.10.101 -t 10.10.10.100 10.10.10.254
# sudo arpspoof -i 10.10.10.101 -t 10.10.10.254 10.10.10.100
#

import sys
sys.path.append('..')
from Utility import *

class Arpspoof(UtilityTool):
    def __init__(self, config_file):
        super(Arpspoof, self).__init__(config_file)

    def get_basic_command(victimip, myip, routerip):
        command1 = 'arpspoof -i {} -t {} {}'.format(myip, victimip, routerip)
        command2 = 'arpspoof -i {} -t {} {}'.format(myip, routerip, victimip)
        command = [command1, command2]
        return command


if __name__ == '__main__':
    print(get_basic_command('8.8.8.8', '8.8.8.1', '8.8.8.2'))
