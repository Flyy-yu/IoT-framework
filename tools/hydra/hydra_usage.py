# -*- coding: utf-8 -*-

import os
from tools.Utility import *


class Hydra(UtilityTool):
    def __init__(self, config_file):
        super(Hydra, self).__init__(config_file)

    def get_basic_command(self, cmd):

        username_file = os.path.dirname(os.path.abspath(__file__)) + '/username.txt'

        if cmd["protocol"].lower() == 'http':
            # username_file, password_file,ip, url:form_parameters:failed_login_msg
            command = 'hydra -L {} -P {} {} {}:{}:{}'.format(
                username_file, cmd["wordlist"], cmd["ip"], cmd["url"], cmd["form_parameters"], cmd["failed_login_msg"])
        else:
            command = 'hydra -L {} -P {} {} {}'.format(username_file, cmd["wordlist"], cmd["ip"], cmd["protocol"])
        return command


if __name__ == "__main__":
    print("Unit Test")
    test_obj = Hydra("config.json")
    print("Show Tool Intro:\n", str(test_obj.name), ":", str(test_obj.intro))

    print("\nShow Command Intro")
    for key, value in test_obj.get_command_info().items():
        print(str(key) + ":" + str(value["intro"]))
    # print(get_basic_command('192.168.1.1', 'telnet', '/usr/share/wordlists/rockyou.txt'))

    print("\nGenerate Command:")
    cmd = {}
    cmd["ip"] = "192.168.1.1"
    cmd["wordlist"] = "/usr/share/wordlists/rockyou.txt"
    cmd["protocol"] = "telnet"

    print(test_obj.get_basic_command(cmd))

    print("\n Test")
    cmd["protocol"] = "http"
    print(test_obj.check_cmd(cmd))

    cmd["url"] = "http://www.google.com"
    print(test_obj.check_cmd(cmd))

    cmd["form_parameters"] = "username=^USER^&password=^PASS"
    print(test_obj.check_cmd(cmd))

    cmd["failed_login_msg"] = "incorrect"
    print(test_obj.check_cmd(cmd))
    print(test_obj.get_basic_command(cmd))
