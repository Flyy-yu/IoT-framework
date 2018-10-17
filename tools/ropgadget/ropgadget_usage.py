#ROPgadget --multibr --binary gets > rettt
# cat rettt | grep "int 0x80 ; ret"
def get_basic_command(binary):
    command = 'ROPgadget --multibr --binary {} > gadget.txt'.format(binary)
    return command


if __name__ == '__main__':
    print (get_basic_command('libc.so.6'))
