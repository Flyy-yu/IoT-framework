# ping 8.8.8.8

def get_basic_command(ip_address):
    command = 'ping {}'.format(ip_address)
    return command


if __name__ == '__main__':
    print get_basic_command('8.8.8.8')
