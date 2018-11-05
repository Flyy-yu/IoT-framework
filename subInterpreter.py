from cmd import Cmd
import json
import signal
import subprocess
import time
import os
import sys
import platform
import atexit
import shlex
import textwrap
from resources import banner
from colorama import Fore, Back
from resources.prettytable import PrettyTable
import importlib

PROMPT = "IOT-CLI"


class UtilityTool(object):
    def __init__(self, config_file):
        with open(config_file, 'r') as fp:
            self.config = self.load_config(fp)
        self.name = self.config["name"]
        self.version = self.config["version"]
        self.intro = self.config["intro"]
        self.links = self.config["links"]

    def load_config(self, config_file):
        config_file = json.load(config_file)
        return config_file

    # generate system command
    def get_command_info(self):
        command_dict = dict(self.config["command"])
        return command_dict

    def check_cmd(self, cmd):
        for key, value in cmd.items():
            if key in self.config["command"] and value in self.config["command"][key]:
                for req_item, info in self.config["command"][key][value].items():
                    if req_item not in cmd:
                        return 'Error option "{}" needs "{}"'.format(value, req_item)
        return 1

    def get_basic_command(self, cmd_dict):
        self.cmd_string = None
        return self.cmd_string

    # TODO execuate the command
    def run_command(self):
        return 1


class Print_Utils(object):
    def print_info_table(self, dir):
        tool_info = UtilityTool(dir)
        info_table = PrettyTable(header_style='upper', padding_width=0)
        info_table.field_names = ["Name", "Version", "Intro", "Links"]
        info_table.align["Name"] = "c"
        info_table.align["Version"] = "c"
        info_table.align["Intro"] = "c"
        info_table.align["Links"] = "c"
        name = textwrap.fill(str(tool_info.name), 10)
        version = textwrap.fill(str(tool_info.version), 10)
        intro = textwrap.fill(str(tool_info.intro), 60)
        links = textwrap.fill(str(tool_info.links), 60)
        info_table.add_row([name, version, intro, links])
        return info_table

    def print_options(self, dir):
        hydra_option = UtilityTool(dir).get_command_info()
        option_table = PrettyTable(header_style='upper', padding_width=0)
        option_table.field_names = ["Option Name",
                                    "Current Setting", "Required", "Description"]
        option_table.align["Option Name"] = "c"
        option_table.align["Current Setting"] = "c"
        option_table.align["Required"] = "c"
        option_table.align["Description"] = "c"
        # hydra_option['']
        default_cmd = {}
        for item in hydra_option.keys():
            option_name = textwrap.fill(item, 10)
            default_cmd[str(item)] = str(hydra_option[item]['default'])
            current_setting = textwrap.fill(
                str(hydra_option[item]['default']), 20)
            required = textwrap.fill(str(hydra_option[item]['required']), 10)
            description = textwrap.fill(str(hydra_option[item]['intro']), 60)
            option_table.add_row(
                [option_name, current_setting, required, description])
            # padding = '{s:{c}^{n}}'.format(s='-', n=20, c='-')
            next_line = ''
            option_table.add_row([next_line, next_line, next_line, next_line])
        return option_table, default_cmd


# API: Update json config file
class Update_Setting(object):
    # seek() to move the cursor back to the beginning of the file then start writing,
    # followed by a truncate() to deal with the case where the new data is smaller than the previous.
    def set_setting(self, DIR, option_name, new_value):
        with open(DIR, "r+") as jsonFile:
            data = json.load(jsonFile)
            data["command"][option_name]['default'] = str(new_value)
            jsonFile.seek(0)  # rewind
            json.dump(data, jsonFile)
            jsonFile.truncate()

    def refresh(self, DIR):
        refreshing = Print_Utils()
        print("\nSETTING UPDATE!\n")
        print(refreshing.print_options(DIR)[0])


class SubInterpreter(Cmd):
    # static object: json file directory

    def __init__(self, json_file):
        self.json_file = json_file
        Cmd.__init__(self)
        Cmd.doc_header = "\n\nSupported Commands\n=============================="
        Cmd.undoc_header = Fore.LIGHTYELLOW_EX + \
                           'Execute Module \n===========================' + Fore.RESET
        Cmd.ruler = ''

    intro = Fore.MAGENTA + "Tool Interface: \n\
        ==============================================\n \
        info\t\t show all descriptions in CLI\n \
        options\t\t show all options and current setting\n \
        set\t\t update config value\n \
        back\t\t back to the previous CLI level\n\n " + Fore.RESET + \
            Fore.RED + "\t run\t\t generate the command based on user's setting and run the command in a new terminal\n\n" + Fore.RESET + \
            Fore.MAGENTA + "\n \Type ? to list full commands\n And you can type help <command> to get help\n\
        ==============================================" + Fore.RESET

    def do_run(self, args):
        # dynamic import module and class base on selected tool
        tool_name = self.__class__.__name__
        tool_name = tool_name[:tool_name.find('SubInterpreter')]
        tool_module_name = 'tools.{}.{}'.format(tool_name.lower(), tool_name.lower() + '_usage')
        current_module = importlib.import_module(tool_module_name)
        current_class = getattr(current_module, tool_name)
        current_object = current_class(self.json_file)
        raw_cmd = Print_Utils().print_options(self.json_file)[1]
        print(raw_cmd)
        run_cmd = current_object.get_basic_command(raw_cmd)
        res = current_object.run_command(3, run_cmd)
        print(res)

    def do_options(self, args):
        options = Print_Utils()
        table = options.print_options(self.json_file)[0]
        print(table)
        print("\nFor example, You can type:\n   set ip 192.168.1.1 \n\n to update current setting.")

    def help_options(self):
        print("show all options and arguments...")

    def do_info(self, args):
        # "tools/hydra/config.json"
        info = Print_Utils()
        table = info.print_info_table(self.json_file)
        print(table)

    def help_info(self):
        print("show all brief info ...")

    def do_back(self, args):
        print("Back to Pre CLI...")
        return True

    def help_back(self):
        print("Back to Pre CLI...")


class PingSubInterpreter(SubInterpreter):
    # update setting value from user's input
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'ip':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


# third level
class HydraSubInterpreter(SubInterpreter):
    # update setting value from user's input


    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'ip':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'protocol':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'wordlist':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")

    def help_set(self, args):
        print("customize your settings...")


# third level
class ArpspoofSubInterpreter(SubInterpreter):
    def do_run(self, args):
        tool_module_name = 'tools.{}.{}'.format('arpspoof', 'arpspoof' + '_usage')
        current_module = importlib.import_module(tool_module_name)
        current_object = current_module.Arpspoof(self.json_file)
        raw_cmd = Print_Utils().print_options(self.json_file)[1]
        print(raw_cmd)
        run_cmd = current_object.get_basic_command(raw_cmd)
        res = current_object.run_command(3, run_cmd)
        print(res)

    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'victimIp':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'RouterIP':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'myIP':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


# third level
class TftpSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'method':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'filename':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class BinwalkSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'imagefile':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class KismetSubInterpreter(SubInterpreter):
    def do_run(self, args):
        tool_module_name = 'tools.{}.{}'.format('kismet', 'kismet' + '_usage')
        current_module = importlib.import_module(tool_module_name)
        current_object = current_module.Kismet(self.json_file)
        raw_cmd = Print_Utils().print_options(self.json_file)[1]
        print(raw_cmd)
        run_cmd = current_object.get_basic_command(raw_cmd)
        res = current_object.run_command(3, run_cmd)
        print(res)

    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'interface':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class RopgadgetSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'binary':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class ApktoolsSubInterpreter(SubInterpreter):
    def do_run(self, args):
        tool_module_name = 'tools.{}.{}'.format('apktools', 'apktools' + '_usage')
        current_module = importlib.import_module(tool_module_name)
        current_object = current_module.Apktools(self.json_file)
        raw_cmd = Print_Utils().print_options(self.json_file)[1]
        print(raw_cmd)
        run_cmd = current_object.get_basic_command(raw_cmd)
        res = current_object.run_command(3, run_cmd)
        print(res)

    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'method':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'apkname':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class KillerbeeSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'channel':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class BaudrateSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'ip':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'protocol':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'wordlist':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class FirmwalkerSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'dir':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class JdcoreSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'type':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            if option_name == 'file':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")


class TcpdumpSubInterpreter(SubInterpreter):
    def do_set(self, args):
        update = Update_Setting()
        setting_args = shlex.split(args)
        if len(setting_args) != 2:
            print("check your args! Type 'options' to get help...")
        else:
            option_name = setting_args[0].lower()
            setting_value = setting_args[1]
            if option_name == 'interface':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            elif option_name == 'amount':
                update.set_setting(self.json_file, option_name, setting_value)
                update.refresh(self.json_file)
            else:
                print("Please check the option name. Type 'options' to get help... ")
