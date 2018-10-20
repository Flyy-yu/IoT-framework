# firmwalker.sh ../cpio-root/ a.txt
from tools.Utility import *


class Firmwalker(UtilityTool):
    def __init__(self, config_file):
        super(Firmwalker, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'cd /home/iot/Desktop/firmwalker && ./firmwalker.sh {} ~/Desktop/result.txt'.format(cmd['cmd'])
        return command


if __name__ == '__main__':
    print(get_basic_command('/home/iot/Desktop/cpio-root'))
