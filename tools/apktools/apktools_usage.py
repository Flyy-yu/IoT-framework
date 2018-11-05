# apktools d apkname
# apktools b foldername

from tools.Utility import *


class Apktools(UtilityTool):
    def __init__(self, config_file):
        super(Apktools, self).__init__(config_file)

    def get_basic_command(self, cmd):
        path = cmd['apkname'][:cmd['apkname'].rfind('/')] + '/'

        if cmd['method'].lower() == 'build':
            command = 'apktools b {}'.format(cmd['apkname'])
        if cmd['method'].lower() == 'decoding':
            command = 'apktools d {}'.format(cmd['apkname'])
        return command


if __name__ == '__main__':
    test_obj = Apktools("config.json")
    cmd = {}

    cmd['method'] = ''
    cmd['apkname'] = ''

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
