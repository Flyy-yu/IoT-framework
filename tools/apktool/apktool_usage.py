# apktools d apkname
# apktools b foldername

from tools.Utility import *


class Apktool(UtilityTool):
    def __init__(self, config_file):
        super(Apktool, self).__init__(config_file)

    def get_basic_command(self, cmd):

        if cmd['method'].lower() == 'build':
            dict_name = cmd['apkname'][cmd['apkname'].rfind('/'):]
            command = 'apktool b {} -o ~/Desktop/{}'.format(cmd['apkname'], dict_name)
        if cmd['method'].lower() == 'decompile':
            filename = cmd['apkname'][cmd['apkname'].rfind('/'), cmd['apkname'].find('.apk')]
            command = 'apktool d {} -o ~/Desktop/{}'.format(cmd['apkname'], filename)
        return command


if __name__ == '__main__':
    test_obj = Apktool("config.json")
    cmd = {}

    cmd['method'] = ''
    cmd['apkname'] = ''

    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
