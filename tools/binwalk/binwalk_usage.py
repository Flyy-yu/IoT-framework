from tools.Utility import *


class Binwalk(UtilityTool):
    def __init__(self, config_file):
        super(Binwalk, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'binwalk -Mre --directory=/home/iot/Desktop {}'.format(cmd['imagefile'])
        return command


if __name__ == '__main__':
    test_obj = Binwalk("config.json")
    cmd = {}

    cmd['imagefile'] = '~/Desktop/test.bin'

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
