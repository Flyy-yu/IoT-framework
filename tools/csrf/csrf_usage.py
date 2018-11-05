# binwalk -Mre filename
#

from tools.Utility import *


class Csrf(UtilityTool):
    def __init__(self, config_file):
        super(Csrf, self).__init__(config_file)

    def get_basic_command(self, cmd):
        poc = open('poc.html','w')
        poc.close()
        return 'echo There is the HTML file'


if __name__ == '__main__':
    print(get_basic_command('/Desktop/a.bin'))
