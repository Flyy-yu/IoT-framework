# unzip app-debug.zip
# dex2jar classes.dex
import os

import sys
from tools.Utility import *


class Jdcore(UtilityTool):
    def __init__(self, config_file):
        super(Jdcore, self).__init__(config_file)

    def get_basic_command(self, cmd):

        if cmd['type'].lower() == 'apk':
            command = 'unzip {} -d ~/Desktop/dex  && dex2jar ~/Desktop/dex/classes.dex && java -jar /home/iot/tools/jd-core-java/build/libs/jd-core-java-1.2.jar -z ~/Desktop/classes-dex2jar.jar ~/Desktop/output.zip'.format(
                cmd['file'])
            return command
        if cmd['type'].lower() == 'jar':
            command = 'java -jar /home/iot/tools/jd-core-java/build/libs/jd-core-java-1.2.jar -z {} ~/Desktop/output.zip'.format(
                cmd['file'])
            return command


if __name__ == '__main__':
    print("Unit Test")
    test_obj = Jdcore("config.json")
    cmd = {}
    cmd["type"] = "apk"
    cmd["file"] = "/home/iot/Desktop/a.apk"
    cmd = (test_obj.get_basic_command(cmd))
    print cmd
    test_obj.run_command(3, cmd)
