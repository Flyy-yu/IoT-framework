# the basic command: ping 8.8.8.8
from tools.Utility import *


class Wifirecon(UtilityTool):
    def __init__(self, config_file):
        super(Wifirecon, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = ""

        return command


if __name__ == "__main__":
    print("Unit Test")
    test_obj = Wifirecon("config.json")
    cmd = {}
    cmd[""] = ""
    cmd[""] = ""
    cmd = (test_obj.get_basic_command(cmd))
    test_obj.run_command(3, cmd)
