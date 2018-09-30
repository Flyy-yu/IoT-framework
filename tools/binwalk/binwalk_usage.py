# binwalk -Mre filename
#

def get_basic_command(imagefile):
    command = 'binwalk -Mre {}'.format(imagefile)
    return command


if __name__ == '__main__':
    print (get_basic_command('/Desktop/a.bin'))
