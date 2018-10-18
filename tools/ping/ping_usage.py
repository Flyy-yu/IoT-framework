# the basic command: ping 8.8.8.8

from tools.Utility import *

class Hydra(UtilityTool):
    def __init__(self, config_file):
        if PY3:
            super().__init__(config_file)
        else:
            super(Hydra, self).__init__(config_file)

    def get_basic_command(self,cmd):
        command = []
        command.append("ping")
        command.append("-c 3")
        command.append(cmd['ip'])
        return command

if __name__ == "__main__":
    print("Unit Test")
    test_obj = Hydra("/Users/zli/PycharmProjects/IoT-framework/tools/ping/config.json")
    print("Show Tool Intro:\n",str(test_obj.name),":",str(test_obj.intro))

    print("\nShow Command Intro")
    for key, value in test_obj.get_command_info().items():
        print(str(key)+":"+str(value["intro"]))
    #print(get_basic_command('192.168.1.1', 'telnet', '/usr/share/wordlists/rockyou.txt'))

    print("\nGenerate Command:")
    cmd = {}
    cmd["ip"] = "10.0.0.1"

    run_cmd = test_obj.get_basic_command(cmd)
    print(run_cmd)
    print("\nExecute Test 1 Popen")
    res = test_obj.run_command(1, run_cmd)
    print(res)

    print("\nExecute Test 2 check_output")
    res = test_obj.run_command(2, run_cmd)
    print(res)

