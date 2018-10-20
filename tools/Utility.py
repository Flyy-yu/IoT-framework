# -*- coding: utf-8 -*-

import json,os,sys
from subprocess import Popen,PIPE,STDOUT,check_output, CalledProcessError
if sys.version > '3':
    PY3 = True
else:
    PY3 = False

class UtilityTool(object):
    def __init__(self,config_file):
        with open(config_file,'r') as fp:
            self.config = self.load_config(fp)
        self.name = self.config["name"]
        self.intro = self.config["intro"]

    def load_config(self,config_file):
        config_file = json.load(config_file)
        return config_file

    # generate system command
    def get_command_info(self):
        command_dict = dict(self.config["command"])
        return command_dict

    def check_cmd(self,cmd):
        for key,value in cmd.items():
            if key in self.config["command"] and value in self.config["command"][key]:
                for req_item, info in self.config["command"][key][value].items():
                    if req_item not in cmd:
                        return 'Error option "{}" needs "{}"'.format(value,req_item)
        return 1

    def get_basic_command(self,cmd_dict):
        self.cmd_string = None
        return self.cmd_string

    # TODO execuate the command
    def run_command(self, exec_function, cmd):
        if exec_function == 1:
            # out = Popen(cmd, stderr=STDOUT, stdout=PIPE)
            out = Popen(cmd)
            exec_res = out.communicate()[0], out.returncode
            return exec_res
        elif exec_function == 2:
            try:
                out = check_output(cmd)
                exec_res = 0, out
            except CalledProcessError as e:
                exec_res = e.returncode, e.message
            return exec_res
        elif exec_function == 3:
            if isinstance(cmd,list):
                pre_cmd = ' '
            else:
                pre_cmd = ''
            pre_cmd = pre_cmd.join(cmd)
            pre_cmd = pre_cmd + ';exec bash'
            exe_cmd = ['gnome-terminal', '-x', 'bash', '-c', pre_cmd]
            # exe_cmd.append(cmd)
            # print(exe_cmd)
            # print 'above'
            out = Popen(exe_cmd)
            exec_res = out.communicate()[0], out.returncode
            return exec_res
        return 1

