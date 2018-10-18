# http://www.willhackforsushi.com/presentations/toorcon11-wright.pdf

# python /home/iot/Desktop/zigbee/killerbee/tools/zbwireshark -c1


def get_basic_command(channel):
    command = 'sudo python /home/iot/Desktop/zigbee/killerbee/tools/zbwireshark -c {}'.format(channel)
    return command


def get_channel():
    command: 'sudo python /home/iot/Desktop/zigbee/killerbee/tools/zbstumbler'
    return command


if __name__ == '__main__':
    print(get_basic_command('1'))
