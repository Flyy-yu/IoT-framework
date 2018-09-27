# tftp -g -r filename.txt 20.20.20.1

def get_basic_command(method, filename, ip_address):
    if method.lower() == 'get':
        command = 'tftp {} {} {} {}'.format('-g', '-r', filename, ip_address)

        return command

    if method.lower() == 'put':
        command = 'tftp {} {} {} {}'.format('-p', '-l', filename, ip_address)
        return command


if __name__ == '__main__':
    print get_basic_command('Get', '~/file/txt', '8.8.8.8')