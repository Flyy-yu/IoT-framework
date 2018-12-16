# the basic command: ping 8.8.8.8
from tools.Utility import *
from .script.capture import *
from .script.analysis import *

class Wifirecon(UtilityTool):
    def __init__(self, config_file):
        super(Wifirecon, self).__init__(config_file)

    def get_basic_command(self, cmd):
        if cmd["method"] == "collect":
            cap = Capture(cmd["interface"])
            cap.file_capture(int(cmd["amount"]),cmd["path"])
            command = "echo Done!"
        elif cmd["method"] == "analysis":
            analys = Analyzer(cmd["path"])
            analys.analyze()
            command = "cat result.json"
        else:
            command = "echo Error"

        return command


if __name__ == "__main__":
    pass

