# firmwalker.sh ../cpio-root/ a.txt
from tools.Utility import *


class Firmwalker(UtilityTool):
    def __init__(self, config_file):
        super(Firmwalker, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'cd /home/iot/tools/firmwalker && ./firmwalker.sh {} ~/Desktop/result.txt'.format(cmd['dir'])
        return command


if __name__ == '__main__':
    test_obj = Firmwalker("config.json")
    cmd = {}

    cmd['dir'] = ''

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
