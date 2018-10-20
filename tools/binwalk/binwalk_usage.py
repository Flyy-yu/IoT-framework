# binwalk -Mre filename
#

from tools.Utility import *


class Binwalk(UtilityTool):
    def __init__(self, config_file):
        super(Binwalk, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'binwalk -Mre --directory=/home/iot/Desktop {}'.format(cmd['imagefile'])
        return command


if __name__ == '__main__':
    print(get_basic_command('/Desktop/a.bin'))
