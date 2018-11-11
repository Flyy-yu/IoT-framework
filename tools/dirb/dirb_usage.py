from tools.Utility import *


class Dirb(UtilityTool):
    def __init__(self, config_file):
        super(Dirb, self).__init__(config_file)

    def get_basic_command(self, cmd):
        url = cmd['url'].lower()
        if url.find('http') < 0:
            url = 'http://' + url
        command = 'dirb {} {}'.format(url, cmd['wordlist'])
        return command


if __name__ == '__main__':
    test_obj = Dirb("config.json")
    cmd = {}

    cmd['url'] = '192.168.0.1'
    cmd['wordlist'] = '/home/iot/tools/wordlist/dirb.txt'
    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
