# the basic command: ping 8.8.8.8

from tools.Utility import *


class Baudrate(UtilityTool):
    def __init__(self, config_file):
        super(Baudrate, self).__init__(config_file)

    def get_basic_command(self):
        command = 'python /home/iot/tools/baudrate/baudrate.py'
        return command


if __name__ == '__main__':
    print('1')
