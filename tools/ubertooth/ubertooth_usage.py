from tools.Utility import *


class Ubertooth(UtilityTool):
    def __init__(self, config_file):
        super(Ubertooth, self).__init__(config_file)

    def get_basic_command(self, cmd):
        command = "sudo ubertooth-btle -f -c ~/Desktop/cap.pcap"
        return command


if __name__ == "__main__":
    test_obj = Ubertooth("./tools/ping/config.json")

    cmd = {}
    run_cmd = test_obj.get_basic_command(cmd)
    print(run_cmd)

    res = test_obj.run_command(3, run_cmd)
