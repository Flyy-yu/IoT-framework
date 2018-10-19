# apktools d apkname
# apktools b foldername

from tools.Utility import *


class Apktools(UtilityTool):
    def __init__(self, config_file):
        super(Apktools, self).__init__(config_file)

    def get_basic_command(method, apkname):
        path = apkname[:apkname.rfind('/')] + '/'

        if method.lower() == 'build':
            command = 'apktools b {}'.format(apkname)
        if method.lower() == 'decoding':
            command = 'apktools d {}'.format(apkname)
        return command


if __name__ == '__main__':
    print(get_basic_command('build', '/home/iot/Desktop/app-debug.apk'))
