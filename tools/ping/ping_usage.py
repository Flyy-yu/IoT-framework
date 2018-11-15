# the basic command: ping 8.8.8.8
from tools.Utility import *


class Ping(UtilityTool):
    def __init__(self, config_file):
        super(Ping, self).__init__(config_file)

    def get_basic_command(self, cmd):
        # print(cmd)
        if "count" in cmd:
            count = cmd["count"]
        else:
            count = 3
        command = "ping -c {} {}".format(count, cmd["ip"])
        return command


if __name__ == "__main__":
    print("Unit Test")
    test_obj = Ping("./tools/ping/config.json")
    print("Show Tool Intro:\n", str(test_obj.name), ":", str(test_obj.intro))

    print("\nShow Command Intro")
    for key, value in test_obj.get_command_info().items():
        print(str(key) + ":" + str(value["intro"]))
    # print(get_basic_command('192.168.1.1', 'telnet', '/usr/share/wordlists/rockyou.txt'))

    print("\nGenerate Command:")
    cmd = {}
    cmd["ip"] = "10.0.0.1"
    cmd["count"] = "5"
    run_cmd = test_obj.get_basic_command(cmd)
    print(run_cmd)

    print("\nExecute Test 3 new window")

    _list = []
    _list.append(run_cmd)
    cmd["ip"] = "8.8.8.8"
    cmd["count"] = 3
    run_cmd = test_obj.get_basic_command(cmd)
    _list.append(run_cmd)

    res = test_obj.run_command(3, _list)
    print(res)
