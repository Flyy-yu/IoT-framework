# http://www.willhackforsushi.com/presentations/toorcon11-wright.pdf

# python /home/iot/Desktop/zigbee/killerbee/tools/zbwireshark -c1

from tools.Utility import *


class Killerbee(UtilityTool):
    def __init__(self, config_file):
        super(Killerbee, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = 'sudo python /home/iot/Desktop/zigbee/killerbee/tools/zbwireshark -c {}'.format(cmd['channel'])
        return command

    def get_channel(self):
        command = 'sudo python /home/iot/Desktop/zigbee/killerbee/tools/zbstumbler'
        return command


if __name__ == '__main__':
    print(get_basic_command('1'))
