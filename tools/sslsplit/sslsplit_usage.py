# the basic command: ping 8.8.8.8
# sslsplit -D -l connect.log -j . -S . -k ca.key -c ca.crt ssl 0.0.0.0 8443 tcp 0.0.0.0 8080


def get_basic_command():
    command = 'sslsplit -D -l connect.log -j . -S . -k ca.key -c ca.crt ssl 0.0.0.0 8443'
    return command


if __name__ == '__main__':
    print (get_basic_command())
