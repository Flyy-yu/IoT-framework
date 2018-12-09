# ROPgadget --multibr --binary gets > rettt
# cat rettt | grep "int 0x80 ; ret"

from tools.Utility import *


class Ropgadget(UtilityTool):
    def __init__(self, config_file):
        super(Ropgadget, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'ROPgadget --multibr --binary {} | grep {}'.format(cmd['binary'],cmd['i'])
        return command


if __name__ == '__main__':
    print("Unit Test")
    test_obj = Ropgadget("config.json")

    cmd = {}
    cmd["binary"] = "~/Desktop/rop"
    cmd['i'] = 'add ecx, ecx ; ret'
    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
