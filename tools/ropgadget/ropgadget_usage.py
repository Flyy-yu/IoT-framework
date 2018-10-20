# ROPgadget --multibr --binary gets > rettt
# cat rettt | grep "int 0x80 ; ret"

from tools.Utility import *


class Ropgadget(UtilityTool):
    def __init__(self, config_file):
        super(Ropgadget, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'ROPgadget --multibr --binary {} > gadget.txt'.format(cmd['binary'])
        return command


if __name__ == '__main__':
    print(get_basic_command('libc.so.6'))
