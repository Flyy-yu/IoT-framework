# sudo ifconfig wlx00c0ca59f60e down
# sudo iwconfig wlx00c0ca59f60e mode Monitor
# sudo ifconfig wlx00c0ca59f60e up
# sudo kismet -c wlx00c0ca59f60e
from tools.Utility import *


class Kismet(UtilityTool):
    def __init__(self, config_file):
        super(Kismet, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command1 = 'sudo ifconfig {} down'.format(cmd['interface'])
        command2 = 'sudo iwconfig {} mode Monitor'.format(cmd['interface'])
        command3 = 'sudo kismet --log-prefix /tmp/'
        command = [command1, command2, command3]
        return command


if __name__ == '__main__':
    print(get_basic_command('wlx9cefd5fd8f86'))
