# apktools d apkname
# apktools b foldername

from tools.Utility import *


class Apktool(UtilityTool):
    def __init__(self, config_file):
        super(Apktool, self).__init__(config_file)

    def get_basic_command(self, cmd):

        if cmd['method'].lower() == 'build':
            command = 'apktool b {}'.format(cmd['apkname'])
        if cmd['method'].lower() == 'decompile':
            command = 'apktool d {}'.format(cmd['apkname'])
        return command


if __name__ == '__main__':
    test_obj = Apktool("config.json")
    cmd = {}

    cmd['method'] = ''
    cmd['apkname'] = ''

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
