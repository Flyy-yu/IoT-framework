# tftp -g -r filename.txt 20.20.20.1




from tools.Utility import *


class Tftp(UtilityTool):
    def __init__(self, config_file):
        super(Tftp, self).__init__(config_file)

    def get_basic_command(method, filename, ip):
        if method.lower() == 'get':
            command = 'tftp {} {} {} {}'.format('-g', '-r', filename, ip)

            return command

        if method.lower() == 'put':
            command = 'tftp {} {} {} {}'.format('-p', '-l', filename, ip)
            return command


if __name__ == '__main__':
    print (get_basic_command('Get', '~/file/txt', '8.8.8.8'))

