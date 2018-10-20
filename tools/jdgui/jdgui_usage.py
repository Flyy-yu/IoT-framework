# unzip app-debug.zip
# dex2jar classes.dex
import os

import sys
from tools.Utility import *


class Jdgui(UtilityTool):
    def __init__(self, config_file):
        super(Jdgui, self).__init__(config_file)

    def get_basic_command(self, cmd):
        path = cmd['apkname'][:cmd['apkname'].rfind('/')]
        command = 'unzip {}'.format(cmd['apkname'])
        return command + ' && dex2jar {}/classes.dex'.format(path)


if __name__ == '__main__':
    print(get_basic_command('/home/iot/Desktop/app-debug.apk'))
