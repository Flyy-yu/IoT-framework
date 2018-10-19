from tools.ping.ping_usage import *

if __name__ == "__main__":
    test_obj = Ping("/Users/zli/PycharmProjects/IoT-framework/tools/ping/config.json")
    # print("Unit Test")
    # test_obj = Hydra("config.json")
    # print("Show Tool Intro:\n",str(test_obj.name),":",str(test_obj.intro))
    #
    # print("\nShow Command Intro")
    # for key, value in test_obj.get_command_info().items():
    #     print(str(key)+":"+str(value["intro"]))
    # #print(get_basic_command('192.168.1.1', 'telnet', '/usr/share/wordlists/rockyou.txt'))

    print("\nGenerate Command:")
    cmd = {}
    cmd["ip"] = "10.0.0.1"

    run_cmd = test_obj.get_basic_command(cmd)
    print(run_cmd)
    print("\nExecute Test 1 Popen")
    res = test_obj.run_command(3, run_cmd)
    print(res)

    print("\nExecute Test 2 check_output")
    res = test_obj.run_command(3, run_cmd)
    print(res)
    
    print("\nExecute Test 3 new window")
    res = test_obj.run_command(3, run_cmd)
    print(res)
