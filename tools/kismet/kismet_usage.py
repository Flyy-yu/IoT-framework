# sudo ifconfig wlx9cefd5fd8f86 down
# sudo iwconfig wlx9cefd5fd8f86 mode Monitor
# sudo kismet -c wlx9cefd5fd8f86

def get_basic_command(Interface):
    command1 = 'sudo ifconfig {} down'.format(Interface)
    command2 = 'sudo iwconfig {} mode Monitor'.format(Interface)
    command3 = 'sudo kismet --log-prefix /tmp/'
    command = [command1,command2,command3]
    return command


if __name__ == '__main__':
    print (get_basic_command('wlx9cefd5fd8f86'))
