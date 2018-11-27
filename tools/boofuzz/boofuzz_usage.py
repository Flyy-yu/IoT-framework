from tools.Utility import *
from boofuzz import *


class Boofuzz(UtilityTool):
    def __init__(self, config_file):
        super(Boofuzz, self).__init__(config_file)

    def run_fuzzer(self, cmd):
        session = Session(
            target=Target(
                connection=SocketConnection(cmd['ip'], int(cmd['port']), proto='tcp')
            ),
        )

        s_initialize(name="fuzz")
        with s_block("string"):
            s_string("test")
            s_static("\r\n")

        session.connect(s_get("fuzz"))
        session.fuzz()



if __name__ == '__main__':
    test_obj = Boofuzz("config.json")
    cmd = {}

    cmd['ip'] = '192.168.1.1'
    cmd['port'] = '21'

    cmd = (test_obj.run_fuzzer(cmd))
