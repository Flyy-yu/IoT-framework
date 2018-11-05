# the basic command: ping 8.8.8.8
from tools.Utility import *


class Sqlmap(UtilityTool):
    def __init__(self, config_file):
        super(Sqlmap, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = ''
        if cmd['type'].lower() == 'get':
            command = 'sqlmap {} --dump --level=5 --risk=3 --threads=3'.format(cmd['url'])

        if cmd['type'].lower() == 'post':
            command = 'sqlmap -r {} -p {} --dump --level=5 --risk=3 --threads=3'.format(cmd['post_body'], cmd['param'])
        return command


if __name__ == "__main__":
    pass
