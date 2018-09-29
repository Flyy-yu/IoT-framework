# the basic command: ping 8.8.8.8

def get_basic_command(ip):
    command = 'ping {}'.format(ip)
    return command


if __name__ == '__main__':
    print get_basic_command('8.8.8.8')
