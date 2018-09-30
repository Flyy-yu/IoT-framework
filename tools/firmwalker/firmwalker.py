#firmwalker.sh ../cpio-root/ a.txt


def get_basic_command(path):
    command = 'cd /home/iot/Desktop/firmwalker && ./firmwalker.sh {} ~/Desktop/result.txt'.format(path)
    return command


if __name__ == '__main__':
    print (get_basic_command('/home/iot/Desktop/cpio-root'))
